# GTPB! — Terminal Puzzle Game

A terminal game written in Python with the `curses` library. The player moves a character around a text-based map, collects items and tries to finish before a countdown timer runs out. The in-game messages are themed around getting your phone back before your mom comes home.

This was a group project for ENGG1330 (Computer Programming) at HKU, completed in the first semester of Year 1.

## Authorship

The course project was a group assignment. All of the code in this repository was written by me.

## What the game does (from reading the code)

- Start screen with three difficulty levels (`easy`, `medium`, `hard`) and an exit option, navigated with the arrow keys and Enter
- Four text maps (`mapstores.py`). The `hard` level continues into a second map and carries over the remaining time
- Movement on the map with collision checks
- Items with their own interactions: keys, bat, timer and time trap (`items.py`, `itemstores.py`)
- A countdown timer that runs in a background thread pool
- Periodic in-game messages (`sysmsg.py`)
- Windows and panels built with `curses` and `curses.panel`, with handling for terminal resize
- End screen with a win/lose result and an option to start a new game

## Tech stack

- Python 3 (standard library only: `curses`, `asyncio`, `concurrent.futures`, `collections`, `random`, `time`)
- Object-oriented structure: classes `Startscr`, `ui_times`, `Body`, `Items`, `Map` and `Endscr`

## Project structure

| File | Role |
| --- | --- |
| `main.py` | Entry point and game loop, level flow, restart |
| `startscr.py` | Level selection screen |
| `UItimes.py` | Main UI: windows, panels, timer, item interactions |
| `body.py` | Player character movement and map interaction |
| `maptest.py`, `mapstores.py` | Map class and the map data |
| `items.py`, `itemstores.py` | Item class and item artwork |
| `endscr.py` | Ending screen |
| `sysmsg.py` | In-game message text |

## Run

Requires a terminal that supports `curses`, so macOS or Linux. On Windows, `curses` is not included in the standard Python install and this has not been tried. The terminal window also needs to be large enough for the map and panels.

```
python3 main.py
```

There are no third-party dependencies, so there is no `requirements.txt`.

## Verification status

- All ten Python files parse without syntax errors (static check only).
- An automated launch test did not give a conclusive result. Gameplay, timing behaviour and each level have not been checked as part of this portfolio preparation.

## Limitations and known issues

- No automated tests.
- `maptest.py` holds the `Map` class despite its name.
- The UI depends on the terminal size. Small windows may cause curses errors.
- Restarting a game calls `main()` recursively, so very long sessions grow the call stack.
- Some code paths catch broad exceptions and ignore them.

## Credits

Course project for ENGG1330, HKU.
