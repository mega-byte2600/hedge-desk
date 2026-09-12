// Shared Playwright loader for the console checks.
//
// Playwright is deliberately not a project dependency, and an `npx` cache can hold
// several versions at once — each expecting its own browser revision. Picking the
// first directory found is how the browser tooling broke once already. This loader
// tries each candidate and returns the first one that can actually launch the
// requested engine, so the scripts need no environment setup.
//
// Override with PLAYWRIGHT_PATH=/path/to/node_modules/playwright if you want a
// specific copy.

import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);

export const DEFAULT_ARGS = ['--disable-dev-shm-usage', '--no-sandbox'];

function candidates() {
  const out = [];
  if (process.env.PLAYWRIGHT_PATH) out.push(process.env.PLAYWRIGHT_PATH);
  out.push('playwright');
  try {
    const npxDir = path.join(process.env.HOME || '', '.npm', '_npx');
    for (const hash of fs.readdirSync(npxDir)) {
      out.push(path.join(npxDir, hash, 'node_modules', 'playwright'));
    }
  } catch (e) { /* no npx cache */ }
  return out;
}

/** The module only, or null. For scripts that just need to detect availability. */
export function loadPlaywright() {
  for (const candidate of candidates()) {
    try { return require(candidate); } catch (e) { /* try next */ }
  }
  return null;
}

/**
 * Return { playwright, browser } using the first candidate that can launch
 * `engine`, or { error } listing why each candidate failed.
 */
export async function launchEngine(engine = 'chromium', args = DEFAULT_ARGS) {
  const failures = [];
  for (const candidate of candidates()) {
    let playwright;
    try {
      playwright = require(candidate);
    } catch (e) {
      continue;
    }
    const type = playwright[engine];
    if (!type) continue;
    try {
      const browser = await type.launch({ args });
      return { playwright, browser, source: candidate };
    } catch (e) {
      failures.push(`${candidate} [${engine}]: ${String(e.message).split('\n')[0].slice(0, 90)}`);
    }
  }
  return { error: failures.join(' | ') || `no candidate provides ${engine}` };
}
