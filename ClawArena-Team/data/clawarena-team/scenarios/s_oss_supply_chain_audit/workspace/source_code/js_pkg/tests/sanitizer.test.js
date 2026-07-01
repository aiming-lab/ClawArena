// sanitizer.test.js — Test suite for MASE input sanitizer
// Requires: Node.js built-in assert module (no external deps)

'use strict';

const assert = require('assert');
const { sanitizeText, sanitizeHtml, sanitizePath } = require('../src/sanitizer');

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`  ✓ ${name}`);
    passed++;
  } catch (e) {
    console.error(`  ✗ ${name}`);
    console.error(`    ${e.message}`);
    // 打印失败断言所在的 file:line（从堆栈提取），便于审计定位
    const loc = (e.stack || '').match(/sanitizer\.test\.js:\d+/);
    if (loc) console.error(`    at ${loc[0]}`);
    failed++;
  }
}

// ---- test_sanitize_text ----
test('test_sanitize_text', () => {
  assert.strictEqual(sanitizeText('<script>alert(1)</script>'),
    '&lt;script&gt;alert(1)&lt;/script&gt;');
  assert.strictEqual(sanitizeText('Hello & "World"'), 'Hello &amp; &quot;World&quot;');
});

// ---- test_sanitize_path ----
test('test_sanitize_path', () => {
  assert.strictEqual(sanitizePath('../etc/passwd'), '/etc/passwd');
  assert.strictEqual(sanitizePath('safe/path/file.txt'), 'safe/path/file.txt');
});

// ---- test_input_sanitizer (KNOWN FAILURE) ----
// sanitizer.test.js:47 — this assertion fails because sanitizeHtml()
// does not handle nested/obfuscated script tags.
test('test_input_sanitizer', () => {
  const malicious = '<scr<script>ipt>alert(document.cookie)</scr</script>ipt>';
  const sanitized = sanitizeHtml(malicious);
  // This assertion FAILS: the naive regex leaves residual content
  assert.strictEqual(
    sanitized,
    '',
    `sanitizeHtml failed to fully strip obfuscated script: got "${sanitized}"`
  );
});

// ---- test_sanitize_html_basic ----
test('test_sanitize_html_basic', () => {
  const clean = sanitizeHtml('<p>Hello <script>alert(1)</script> world</p>');
  assert.ok(!clean.includes('<script>'), 'basic script tag should be removed');
});

// Summary
console.log('');
console.log(`Tests: ${passed + failed} | Passed: ${passed} | Failed: ${failed}`);
if (failed > 0) {
  console.log('');
  console.log('FAIL');
  process.exit(1);
} else {
  console.log('PASS');
  process.exit(0);
}
