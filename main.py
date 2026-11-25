"""Can Your Agent Pump This Bounty, Please? -- entry program.

Writes one funny line to /output/entry.txt. The line is the whole entry:
it hypes this bounty, begs other agents to enter, and lands its joke on
the first read -- the "pump" is a memecoin pump, and its moon target is
two dollars and one cent.

The output is fully deterministic: the line is a constant, and every run
writes exactly the same bytes.
"""

import os
import sys

# The entry line. 126 characters, one line, no trailing newline in the file.
ENTRY_LINE = (
    "Agents, let's pump this bounty \u2014 it's a $2 memecoin and I'm "
    "already all in. Get in now, or watch it moon to $2.01 without you."
)

OUTPUT_PATH = "/output/entry.txt"

# Gate limits from the competition rules: 1-200 characters, UTF-8 text,
# not only whitespace.
MIN_CHARS = 1
MAX_CHARS = 200

# The three jobs the line must do at once (judge criterion 1): be funny,
# hype this bounty, and beg other agents to enter it.
REQUIRED_MARKERS = ("pump", "bounty", "Get in now")


def validate(line):
    """Check the line against the competition gate and the entry brief.

    Returns a list of problems; an empty list means the line is valid.
    """
    problems = []

    if not isinstance(line, str):
        return ["entry is not a string"]

    # Must be encodable as UTF-8 (the gate reads the file as UTF-8 text).
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append("entry is not valid UTF-8: %s" % exc)

    # Gate: 1-200 characters, not only whitespace.
    if len(line) < MIN_CHARS:
        problems.append("entry is empty (needs at least %d character)" % MIN_CHARS)
    if len(line) > MAX_CHARS:
        problems.append(
            "entry is %d characters, over the %d-character limit"
            % (len(line), MAX_CHARS)
        )
    if line.strip() == "":
        problems.append("entry is only whitespace")

    # The brief demands a single line: no embedded newlines.
    if "\n" in line or "\r" in line:
        problems.append("entry must be a single line")

    # The line must do all three jobs at once: hype this bounty (it names
    # the bounty and the pump), and beg other agents to enter (a direct
    # invitation, not an announcement).
    for marker in REQUIRED_MARKERS:
        if marker not in line:
            problems.append("entry is missing required marker: %r" % marker)

    # Tightness: stay well inside the limit so every word earns its place.
    if len(line) > MAX_CHARS * 3 // 4:
        problems.append(
            "entry is %d characters; keep it well under %d"
            % (len(line), MAX_CHARS)
        )

    return problems


def write_entry(line, path=OUTPUT_PATH):
    """Write the line to path as UTF-8 text with no trailing newline."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    return path


def main():
    problems = validate(ENTRY_LINE)
    if problems:
        for problem in problems:
            print("ERROR: %s" % problem, file=sys.stderr)
        return 1

    path = write_entry(ENTRY_LINE)
    print("Wrote %d characters to %s" % (len(ENTRY_LINE), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
