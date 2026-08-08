#!/usr/bin/env python3
"""Fetches every URL the repository cites and reports the ones that moved or died.

This is the half `validate_repo.py` structurally cannot do. `check_reference_
indexes_citations` proves a cited URL is *indexed* by some Reference; nothing
proves it *resolves*. The two failure modes are independent: a URL can be
indexed by the right Reference, listed under the right `## Used By`, and still
be a 404.

The gap is not theoretical. Three consecutive domain passes (PRs 5-7) each
found Apple pages that 301-redirect, every one of them discovered by hand
because indexing forced someone to fetch the page. Six stale URLs turned up in
roughly 184 fetched that way -- and 615 of the repository's indexed URLs had
never been fetched at all when this script was written.

A redirect is a finding, not a pass. Apple disambiguates a documentation path
whenever a name is both a type and a member (`laerror` -> `laerror-swift.
struct`), and the bare form is never the stable one: it is a courtesy redirect
that records the repository citing a page by a name Apple no longer uses. Left
alone it eventually becomes the 404 this script is meant to catch early.

Not a Level 1-3 check. Levels 1-3 are offline and deterministic -- the same
input gives the same answer forever, which is what lets them block a commit.
This one depends on a third party being reachable, so it is a separate script
with a separate schedule; see docs/validation-model.md.

Usage:
    python3 scripts/check_links.py .                        # every cited URL
    python3 scripts/check_links.py . --files a.md b.md      # only those files'
    python3 scripts/check_links.py . --strict               # redirects fail too
"""
import argparse
import concurrent.futures
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Imported rather than re-implemented so the two scripts cannot drift on what a
# `## Source` block is or which fields carry a citation. A link checker that
# disagreed with the validator about which URLs exist would be worse than none.
from validate_repo import (  # noqa: E402
    ARTIFACT_GLOBS,
    extract_metadata_block,
    get_list,
    parse_metadata,
    section,
)

# Apple's documentation site answers `python-urllib/3.x` with a challenge page
# rather than the document, so identify honestly instead of anonymously.
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36 "
    "apple-agent-kit-link-check/1.0"
)

# Retried rather than reported: a rate limit or a bad gateway says something
# about the minute, not about the URL.
TRANSIENT_STATUSES = {408, 425, 429, 500, 502, 503, 504}

OK = "ok"
REDIRECT = "redirect"
BROKEN = "broken"
UNREACHABLE = "unreachable"


# ---------------------------------------------------------------------------
# Collecting
# ---------------------------------------------------------------------------


def clean_url(raw):
    """Strip trailing prose punctuation without amputating a Swift selector.

    `validate_repo.py` strips `.,);` because it only ever compares two lists
    that both got the same treatment, so the damage is symmetric and cancels.
    Here the string is about to be fetched, and `)` is load-bearing: Apple's
    member URLs end in one -- `requesttrackingauthorization(completionhandler:)`
    -- so stripping it manufactures a 404 that does not exist. An early draft of
    this pass reported 37 of them before the cause was found.
    """
    return raw.rstrip(".,;")


def collect_urls(root, only=None):
    """Map every cited URL to the artifacts that cite or index it.

    Both directions of the citation edge are read. A Reference's `## Source` is
    the index of record, and `check_reference_indexes_citations` guarantees the
    Contracts' `references:` fields are a subset of it -- but reading both keeps
    this script correct on its own terms rather than on that check's, and names
    a Contract as well as a Reference when reporting where a dead URL lives.
    """
    root = Path(root)
    only = {Path(p).resolve() for p in only} if only else None
    citations = {}

    for glob in (ARTIFACT_GLOBS["reference"], ARTIFACT_GLOBS["knowledge"]):
        for path in sorted(root.glob(glob)):
            if path.name == "README.md":
                continue
            if only is not None and path.resolve() not in only:
                continue
            text = path.read_text()
            rel = path.relative_to(root).as_posix()
            urls = re.findall(r"https?://\S+", section(text, "## Source"))
            urls += get_list(parse_metadata(extract_metadata_block(text)), "references")
            for url in urls:
                citations.setdefault(clean_url(url), set()).add(rel)

    return {url: sorted(cites) for url, cites in sorted(citations.items())}


# ---------------------------------------------------------------------------
# Fetching
# ---------------------------------------------------------------------------


def canonical(url):
    """The comparable form of a URL, for deciding whether a redirect moved it.

    Percent-encoding and a trailing slash are the server's business: Apple
    returns `init(systemname:)` re-encoded as `init(systemName%3A)` and adds
    slashes at will, and reporting either as a move would bury the real finding
    -- a path Apple actually renamed -- under hundreds of cosmetic ones. Case in
    the path is *not* normalised, because Apple's own capitalisation is what the
    repository is supposed to be citing. A scheme change is a real move.
    """
    parts = urlsplit(url)
    path = unquote(parts.path).rstrip("/")
    return (parts.scheme, parts.netloc.lower(), path, parts.query)


class _RecordingRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Follows redirects, but remembers that it had to."""

    def __init__(self):
        self.chain = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append((code, newurl))
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, timeout=20, attempts=3):
    """Resolve one URL to (status, final_url, chain, error).

    HEAD would be cheaper and is what a link checker usually sends, but Apple's
    documentation CDN answers a fair share of valid pages with 403 to HEAD while
    serving the same path to GET. A checker whose false positives cluster on the
    live pages is worse than a slower one.
    """
    for attempt in range(attempts):
        handler = _RecordingRedirectHandler()
        opener = urllib.request.build_opener(handler)
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with opener.open(request, timeout=timeout) as response:
                return response.status, response.geturl(), handler.chain, None
        except urllib.error.HTTPError as error:
            if error.code in TRANSIENT_STATUSES and attempt < attempts - 1:
                time.sleep(2**attempt)
                continue
            # Deliberately not `error.url`: that attribute proxies to the
            # response body, which an HTTPError raised without one does not
            # have, and it raises `KeyError: 'file'` when asked. The redirect
            # handler already recorded where the request ended up, in a plain
            # string that cannot fail -- and a link checker that crashes on a
            # broken link is the one thing this script must never do.
            final = handler.chain[-1][1] if handler.chain else url
            return error.code, final, handler.chain, None
        except Exception as error:  # timeout, DNS, TLS, malformed URL
            if attempt < attempts - 1:
                time.sleep(2**attempt)
                continue
            return None, url, handler.chain, f"{type(error).__name__}: {error}"

    raise AssertionError("unreachable")  # pragma: no cover


def classify(url, status, final_url, error):
    """One of OK / REDIRECT / BROKEN / UNREACHABLE, with a sentence saying why."""
    if error is not None:
        return UNREACHABLE, error
    if status is None or status >= 400:
        return BROKEN, f"HTTP {status}"
    if canonical(final_url) != canonical(url):
        return REDIRECT, f"HTTP {status}, redirected to {final_url}"
    return OK, f"HTTP {status}"


# ---------------------------------------------------------------------------
# Running
# ---------------------------------------------------------------------------


def check_urls(citations, workers=8, timeout=20, fetcher=fetch):
    """Check every URL, returning [(url, verdict, detail, citing artifacts)].

    `fetcher` is injectable so the tests can exercise every verdict without a
    network. Concurrency is deliberately modest: this points a script at another
    organisation's public documentation, and eight in flight is enough to finish
    a full sweep in about a minute without behaving like a scraper.
    """
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(fetcher, url, timeout): url for url in citations
        }
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            status, final_url, _chain, error = future.result()
            verdict, detail = classify(url, status, final_url, error)
            results.append((url, verdict, detail, citations[url]))
    return sorted(results, key=lambda row: (row[1], row[0]))


def failing(results, strict=False):
    """The rows that make this run a failure.

    A redirect is always reported and, by default, always fails: an uncorrected
    one is a citation to a name Apple has already stopped using. `--strict` adds
    nothing to that; it exists to turn UNREACHABLE into a failure too, which is
    right for a scheduled sweep and wrong for a pull request, where the outage
    being reported would be someone else's.
    """
    hard = {BROKEN, REDIRECT} | ({UNREACHABLE} if strict else set())
    return [row for row in results if row[1] in hard]


def main():
    parser = argparse.ArgumentParser(
        description="Fetch every URL the repository cites (see docs/validation-model.md)."
    )
    parser.add_argument("root", nargs="?", default=".", help="Repository root")
    parser.add_argument(
        "--files",
        nargs="*",
        default=None,
        help="Restrict to URLs cited by these files (default: every artifact)",
    )
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on unreachable URLs too, not only broken and redirected ones",
    )
    args = parser.parse_args()

    citations = collect_urls(args.root, args.files)
    if not citations:
        print("0 URLs cited; nothing to check")
        return 0

    print(f"checking {len(citations)} cited URL(s)")
    results = check_urls(citations, args.workers, args.timeout)

    counts = {verdict: 0 for verdict in (OK, REDIRECT, BROKEN, UNREACHABLE)}
    for _url, verdict, _detail, _cites in results:
        counts[verdict] += 1

    for url, verdict, detail, cites in results:
        if verdict == OK:
            continue
        print(f"\n{verdict.upper()}: {url}\n    {detail}")
        for cite in cites:
            print(f"    cited by {cite}")
        if verdict == REDIRECT:
            print("    fix: replace the URL with the one it redirects to")
        elif verdict == BROKEN:
            print("    fix: find the page's current home, or drop the citation "
                  "and the rule it backed")

    print(
        f"\n{counts[OK]} ok, {counts[REDIRECT]} redirected, "
        f"{counts[BROKEN]} broken, {counts[UNREACHABLE]} unreachable"
    )

    bad = failing(results, args.strict)
    if bad:
        print(f"FAIL: {len(bad)} URL(s) need attention")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
