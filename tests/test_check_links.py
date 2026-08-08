"""Tests for the link checker.

No test here touches the network. The point of the script is to fetch, so the
fetching is injectable and everything around it -- which URLs get collected,
what counts as having moved, what makes a run fail -- is tested as a pure
function. A test that hit developer.apple.com would fail for reasons that have
nothing to do with this repository, which is the exact property that kept this
check out of Levels 1-3 in the first place.
"""
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_links  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "check_links.py"

URL = "https://developer.apple.com/documentation/example/thing"
OTHER_URL = "https://developer.apple.com/documentation/example/other"

REFERENCE = """# Example

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: reference.apple.example
artifact_type: reference
title: Example
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Reference index for Apple's example documentation.
domain: Example
last_updated: 2026-08-08
```

## Source

{url}

## Purpose

Reference index for Apple's example documentation.

## Primary Topics

- Example topic

## Used By

- knowledge/example/thing.md ([[knowledge/example/thing]])
""".format(url=URL)

KNOWLEDGE = """# Thing

Status: Approved
Version: 1.0.0

## Metadata

``` yaml
id: knowledge.example.thing
artifact_type: knowledge
title: Thing
version: 1.0.0
status: Approved
owner: Apple Agent Kit
summary: Defines the thing.
domain: Example
tags:
  - thing
references:
  - {url}
depends_on: []
related: []
last_updated: 2026-08-08
```

## Intent

Intent.

## Rules

### Rule 1

Rule.

## Compliant Example

OK.

## Non-Compliant Example

Not OK.

## Dependencies

None.
""".format(url=URL)


class LinkFixture:
    """A repository with one Reference and one Contract citing the same URL."""

    def __init__(self, tmpdir):
        self.root = Path(tmpdir)
        self.write("references/apple/example.md", REFERENCE)
        self.write("knowledge/example/thing.md", KNOWLEDGE)

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path


class LinkTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.repo = LinkFixture(self._tmp.name)


class TestCollecting(LinkTestCase):
    def test_a_url_is_collected_once_and_credits_every_citer(self):
        citations = check_links.collect_urls(self.repo.root)
        self.assertEqual(
            citations,
            {URL: ["knowledge/example/thing.md", "references/apple/example.md"]},
        )

    def test_a_url_only_a_reference_indexes_is_still_collected(self):
        self.repo.write(
            "references/apple/example.md",
            REFERENCE.replace(f"## Source\n\n{URL}", f"## Source\n\n{URL}\n{OTHER_URL}"),
        )
        self.assertIn(OTHER_URL, check_links.collect_urls(self.repo.root))

    def test_files_restricts_collection_to_the_named_files(self):
        self.repo.write(
            "references/apple/example.md",
            REFERENCE.replace(f"## Source\n\n{URL}", f"## Source\n\n{URL}\n{OTHER_URL}"),
        )
        citations = check_links.collect_urls(
            self.repo.root, only=[self.repo.root / "knowledge/example/thing.md"]
        )
        self.assertEqual(list(citations), [URL])

    def test_a_repository_citing_nothing_collects_nothing(self):
        with tempfile.TemporaryDirectory() as empty:
            self.assertEqual(check_links.collect_urls(empty), {})


class TestCleanUrl(unittest.TestCase):
    def test_a_trailing_paren_survives_because_apple_member_urls_end_in_one(self):
        # The regression this exists for: `validate_repo.py` strips `)` safely
        # because it strips both sides of a comparison, and an early draft of
        # this script copied that and manufactured 37 nonexistent 404s.
        url = "https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager/requesttrackingauthorization(completionhandler:)"
        self.assertEqual(check_links.clean_url(url), url)

    def test_trailing_prose_punctuation_is_stripped(self):
        self.assertEqual(check_links.clean_url(URL + "."), URL)
        self.assertEqual(check_links.clean_url(URL + ","), URL)


class TestCanonical(unittest.TestCase):
    def test_percent_encoding_is_not_a_move(self):
        plain = "https://developer.apple.com/documentation/uikit/uiimage/init(systemname:)"
        encoded = "https://developer.apple.com/documentation/uikit/uiimage/init%28systemname%3A%29"
        self.assertEqual(check_links.canonical(plain), check_links.canonical(encoded))

    def test_a_trailing_slash_is_not_a_move(self):
        self.assertEqual(check_links.canonical(URL), check_links.canonical(URL + "/"))

    def test_a_renamed_path_is_a_move(self):
        bare = "https://developer.apple.com/documentation/localauthentication/laerror"
        suffixed = bare + "-swift.struct"
        self.assertNotEqual(check_links.canonical(bare), check_links.canonical(suffixed))

    def test_a_scheme_change_is_a_move(self):
        self.assertNotEqual(
            check_links.canonical(URL),
            check_links.canonical(URL.replace("https://", "http://")),
        )


class TestClassify(unittest.TestCase):
    def test_a_200_at_the_requested_url_is_ok(self):
        verdict, _ = check_links.classify(URL, 200, URL, None)
        self.assertEqual(verdict, check_links.OK)

    def test_a_200_somewhere_else_is_a_redirect(self):
        verdict, detail = check_links.classify(URL, 200, OTHER_URL, None)
        self.assertEqual(verdict, check_links.REDIRECT)
        self.assertIn(OTHER_URL, detail)

    def test_a_404_is_broken(self):
        verdict, detail = check_links.classify(URL, 404, URL, None)
        self.assertEqual(verdict, check_links.BROKEN)
        self.assertIn("404", detail)

    def test_a_network_error_is_unreachable_not_broken(self):
        verdict, detail = check_links.classify(URL, None, URL, "timeout")
        self.assertEqual(verdict, check_links.UNREACHABLE)
        self.assertIn("timeout", detail)


class TestFetchRetries(unittest.TestCase):
    """Transient statuses say something about the minute, not about the URL."""

    def _opener(self, responses):
        calls = {"n": 0}

        class FakeResponse:
            status = 200

            def geturl(self):
                return URL

            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

        class FakeOpener:
            def open(self, request, timeout=None):
                outcome = responses[calls["n"]]
                calls["n"] += 1
                if isinstance(outcome, Exception):
                    raise outcome
                return FakeResponse()

        return FakeOpener(), calls

    def test_a_503_is_retried_and_a_later_200_wins(self):
        error = urllib.error.HTTPError(URL, 503, "Service Unavailable", {}, None)
        opener, calls = self._opener([error, "ok"])
        with mock.patch.object(check_links.urllib.request, "build_opener",
                               return_value=opener), \
                mock.patch.object(check_links.time, "sleep"):
            status, final, _chain, err = check_links.fetch(URL)
        self.assertEqual((status, final, err), (200, URL, None))
        self.assertEqual(calls["n"], 2)

    def test_a_404_is_not_retried(self):
        error = urllib.error.HTTPError(URL, 404, "Not Found", {}, None)
        opener, calls = self._opener([error, "ok"])
        with mock.patch.object(check_links.urllib.request, "build_opener",
                               return_value=opener), \
                mock.patch.object(check_links.time, "sleep"):
            status, _final, _chain, err = check_links.fetch(URL)
        self.assertEqual((status, err), (404, None))
        self.assertEqual(calls["n"], 1, "a 404 is about the URL, not the minute")

    def test_a_persistent_timeout_becomes_unreachable(self):
        opener, calls = self._opener([TimeoutError("timed out")] * 3)
        with mock.patch.object(check_links.urllib.request, "build_opener",
                               return_value=opener), \
                mock.patch.object(check_links.time, "sleep"):
            status, _final, _chain, err = check_links.fetch(URL)
        self.assertIsNone(status)
        self.assertIn("TimeoutError", err)
        self.assertEqual(calls["n"], 3)


class TestCheckUrls(LinkTestCase):
    def test_every_verdict_is_reported_against_its_citers(self):
        citations = {
            URL: ["references/apple/example.md"],
            OTHER_URL: ["references/apple/example.md"],
        }

        def fake_fetch(url, timeout=20):
            if url == URL:
                return 200, URL, [], None
            return 404, url, [], None

        results = check_links.check_urls(citations, fetcher=fake_fetch)
        verdicts = {url: verdict for url, verdict, _detail, _cites in results}
        self.assertEqual(
            verdicts, {URL: check_links.OK, OTHER_URL: check_links.BROKEN}
        )
        self.assertEqual(results[0][3], ["references/apple/example.md"])


class TestFailing(unittest.TestCase):
    def _rows(self):
        return [
            (URL, check_links.OK, "", []),
            (URL, check_links.REDIRECT, "", []),
            (URL, check_links.BROKEN, "", []),
            (URL, check_links.UNREACHABLE, "", []),
        ]

    def test_broken_and_redirected_fail_by_default(self):
        verdicts = {row[1] for row in check_links.failing(self._rows())}
        self.assertEqual(verdicts, {check_links.REDIRECT, check_links.BROKEN})

    def test_strict_adds_unreachable(self):
        verdicts = {row[1] for row in check_links.failing(self._rows(), strict=True)}
        self.assertIn(check_links.UNREACHABLE, verdicts)

    def test_a_clean_run_fails_nothing(self):
        self.assertEqual(check_links.failing([(URL, check_links.OK, "", [])]), [])


class TestCommandLine(LinkTestCase):
    def test_a_run_with_nothing_to_check_exits_zero_without_fetching(self):
        empty = self.repo.write("references/apple/empty.md", "# Empty\n")
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), str(self.repo.root),
             "--files", str(empty)],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("nothing to check", result.stdout)


if __name__ == "__main__":
    unittest.main()
