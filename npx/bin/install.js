#!/usr/bin/env node
'use strict';

const { spawnSync } = require('child_process');

const REPO = 'caglarbaranbora/Apple-Agent-Kit';
const MARKETPLACE_NAME = 'apple-agent-kit-marketplace';
const PLUGIN_NAME = 'apple-agent-kit';

const dryRun = process.argv.includes('--dry-run');

const commands = [
  ['claude', ['plugin', 'marketplace', 'add', REPO]],
  ['claude', ['plugin', 'install', `${PLUGIN_NAME}@${MARKETPLACE_NAME}`]],
];

function commandExists(cmd) {
  const result = spawnSync(cmd, ['--version'], { stdio: 'ignore' });
  return !result.error && result.status === 0;
}

function printCodexInstructions() {
  console.log('The `claude` CLI was not found on PATH, but `codex` was.');
  console.log('Apple Agent Kit installs into Codex from inside a Codex session, not from this script.');
  console.log('');
  console.log('Run inside Codex:');
  console.log(`  /plugin marketplace add ${REPO}`);
  console.log('');
  console.log('Then install the `apple-agent-kit` plugin from that marketplace and restart Codex.');
  console.log('For a manual install instead, see .codex/INSTALL.md in this repository.');
}

function printNeitherFoundError() {
  console.error('Error: neither the `claude` nor the `codex` CLI was found on PATH.');
  console.error('Install Claude Code: https://code.claude.com/docs/en/quickstart');
  console.error('...or install Codex CLI, then re-run this command.');
}

function run() {
  if (!commandExists('claude')) {
    if (commandExists('codex')) {
      printCodexInstructions();
      process.exit(0);
    }
    printNeitherFoundError();
    process.exit(1);
  }

  for (const [cmd, args] of commands) {
    const printable = [cmd, ...args].join(' ');
    if (dryRun) {
      console.log(`[dry-run] ${printable}`);
      continue;
    }
    console.log(`Running: ${printable}`);
    const result = spawnSync(cmd, args, { stdio: 'inherit' });
    if (result.status !== 0) {
      console.error(`Failed: ${printable}`);
      process.exit(result.status || 1);
    }
  }

  if (!dryRun) {
    console.log('Apple Agent Kit plugin installed.');
  }
}

run();
