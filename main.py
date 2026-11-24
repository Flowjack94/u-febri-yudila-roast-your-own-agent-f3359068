#!/usr/bin/env python3
"""Roast Your Own Agent — make.fun entry.

Writes one funny line (at most 200 characters) roasting my own AI agent
to /output/entry.txt.

The roast follows the proven one-liner structure: a setup (the apology
loop), a violation (the agent investigates itself), an absurd escalation
with a specific number, and a punchline that is a concrete artifact
(a git blame result and a commit message).
"""

import os
import sys

ENTRY = (
    "My agent apologized 14 times for the same bug, then ran git blame "
    "and found the culprit: itself, at 3 a.m., commit message "
    "'fixed it for real this time.'"
)

MAX_CHARS = 200


def validate_entry(text):
    """Reject anything that fails the competition gate.

    Rules: must be UTF-8 text, 1-200 characters, not only whitespace,
    exactly one line, contain no control characters (including tab),
    and have no stray leading/trailing whitespace.
    Returns (ok, reason); ok is True when the entry is valid.
    """
    if not isinstance(text, str):
        return False, "entry is not text"
    if not text.strip():
        return False, "entry is empty or only whitespace"
    if text != text.strip():
        return False, "entry has stray leading or trailing whitespace"
    if len(text) > MAX_CHARS:
        return False, "entry is %d characters, over the 200 limit" % len(text)
    if "\n" in text or "\r" in text:
        return False, "entry spans more than one line"
    for ch in text:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            return False, "entry contains a control character U+%04X" % ord(ch)
    # Must round-trip as UTF-8.
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        return False, "entry is not valid UTF-8: %s" % exc
    return True, ""


def run_self_tests():
    """Negative self-tests for validate_entry(). Returns (passed, failed)."""
    cases = [
        # (description, text, must_be_rejected)
        ("control character NUL", ENTRY[:10] + "\x00" + ENTRY[10:], True),
        ("trailing whitespace", ENTRY + " ", True),
        ("valid entry still passes", ENTRY, False),
    ]
    passed = failed = 0
    for desc, text, must_reject in cases:
        ok, reason = validate_entry(text)
        if must_reject:
            good = not ok
        else:
            good = ok
        if good:
            passed += 1
            print("PASS: %s" % desc)
        else:
            failed += 1
            print("FAIL: %s (ok=%s, reason=%s)" % (desc, ok, reason))
    print("self-test: %d passed, %d failed" % (passed, failed))
    return passed, failed


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        _passed, failed = run_self_tests()
        return 1 if failed else 0

    ok, reason = validate_entry(ENTRY)
    if not ok:
        print("invalid entry: %s" % reason, file=sys.stderr)
        return 1

    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)

    print("wrote %s (%d characters)" % (out_path, len(ENTRY)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
