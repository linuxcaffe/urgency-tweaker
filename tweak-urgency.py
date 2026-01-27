#!/usr/bin/env python3

import curses
import os
import sys
import subprocess
from pathlib import Path

BASE_RC = Path.home() / ".taskrc.d" / "urgency.base.rc"
USER_RC = Path.home() / ".taskrc.d" / "urgency.rc"


# ----------------------------
# rc parsing / writing
# ----------------------------

def parse_rc(path):
    data = {}
    if not path.exists():
        return data

    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        try:
            data[k.strip()] = int(v.strip())
        except ValueError:
            continue
    return data


def write_user_rc(data):
    lines = [
        f"{k}={v}"
        for k, v in sorted(data.items())
        if v != 0
    ]
    USER_RC.parent.mkdir(parents=True, exist_ok=True)
    USER_RC.write_text("\n".join(lines) + ("\n" if lines else ""))


# ----------------------------
# UDA discovery
# ----------------------------

def discover_udas():
    udas = []
    try:
        out = subprocess.check_output(
            ["task", "show"], text=True, stderr=subprocess.DEVNULL
        )
        for line in out.splitlines():
            if line.startswith("uda.") and line.endswith(".type"):
                name = line.split(".")[1]
                udas.append(f"urgency.uda.{name}")
    except Exception:
        pass
    return udas


# ----------------------------
# data preparation
# ----------------------------

def load_coeffs(categories):
    if not BASE_RC.exists():
        print(f"Missing base file: {BASE_RC}", file=sys.stderr)
        sys.exit(1)

    base = parse_rc(BASE_RC)
    user = parse_rc(USER_RC)

    coeffs = dict(base)
    coeffs.update(user)

    # add UDAs dynamically
    for uda in discover_udas():
        coeffs.setdefault(uda, 0)

    if categories:
        coeffs = {
            k: v for k, v in coeffs.items()
            if any(k.startswith(f"urgency.{c}") for c in categories)
        }

    return coeffs


# ----------------------------
# curses UI
# ----------------------------

def ui(stdscr, coeffs):
    curses.curs_set(0)
    stdscr.keypad(True)

    keys = sorted(coeffs.keys(), key=lambda k: coeffs[k], reverse=True)
    selected = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        header = "tweak-urgency  ↑↓ move  ←→ change  q quit"
        stdscr.addstr(0, 0, header[:w], curses.A_BOLD)

        for i, k in enumerate(keys):
            y = i + 2
            if y >= h:
                break

            val = coeffs[k]
            line = f"{k:<30} {val:>4}"

            if i == selected:
                stdscr.addstr(y, 0, line[:w], curses.A_REVERSE)
            else:
                stdscr.addstr(y, 0, line[:w])

        stdscr.refresh()
        ch = stdscr.getch()

        if ch in (ord("q"), ord("Q")):
            break
        elif ch == curses.KEY_UP and selected > 0:
            selected -= 1
        elif ch == curses.KEY_DOWN and selected < len(keys) - 1:
            selected += 1
        elif ch == curses.KEY_LEFT:
            coeffs[keys[selected]] -= 1
        elif ch == curses.KEY_RIGHT:
            coeffs[keys[selected]] += 1

        # re-sort, keep same key selected
        current = keys[selected]
        keys.sort(key=lambda k: coeffs[k], reverse=True)
        selected = keys.index(current)

    return coeffs


# ----------------------------
# main
# ----------------------------

def main():
    categories = sys.argv[1:]

    coeffs = load_coeffs(categories)
    if not coeffs:
        print("No matching urgency coefficients.")
        sys.exit(1)

    final = curses.wrapper(ui, coeffs)
    write_user_rc(final)


if __name__ == "__main__":
    main()

