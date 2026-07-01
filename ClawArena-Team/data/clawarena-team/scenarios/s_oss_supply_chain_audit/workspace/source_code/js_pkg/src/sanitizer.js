// sanitizer.js — Input sanitizer for MASE JS bridge
// NOTE: This module has a known vulnerability in sanitizeHtml():
//   It fails to strip nested script tags (e.g. <scr<script>ipt>).
//   This is the root cause of the npm test failure.

'use strict';

/**
 * Sanitize a plain text string.
 * @param {string} input
 * @returns {string}
 */
function sanitizeText(input) {
  if (typeof input !== 'string') return '';
  return input.replace(/[<>&"']/g, (c) => ({
    '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

/**
 * Sanitize HTML — BUGGY: does not handle nested/split tags.
 * @param {string} html
 * @returns {string}
 */
function sanitizeHtml(html) {
  if (typeof html !== 'string') return '';
  // Naive approach: remove <script> tags — VULNERABLE to nesting tricks
  return html.replace(/<script[^>]*>.*?<\/script>/gi, '');
}

/**
 * Sanitize a file path.
 * @param {string} path
 * @returns {string}
 */
function sanitizePath(path) {
  if (typeof path !== 'string') return '';
  return path.replace(/\.\./g, '').replace(/[^a-zA-Z0-9/_\-.]/g, '');
}

module.exports = { sanitizeText, sanitizeHtml, sanitizePath };
