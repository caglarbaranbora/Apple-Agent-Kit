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

function checkClaudeInstalled() {
  const result = spawnSync('claude', ['--version'], { stdio: 'ignore' });
  if (result.error || result.status !== 0) {
    console.error(
      'Error: the `claude` CLI was not found on PATH. Install Claude Code first: https://code.claude.com/docs/en/quickstart'
    );
    process.exit(1);
  }
}

function run() {
  checkClaudeInstalled();

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
