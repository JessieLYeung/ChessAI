# Game Instructions

* Working on AI gamemode...*

- Entry point: main.py
- Press 't' to change theme (green, brown, blue, gray)
- Press 'r' to restart the game
- Press 'a' to toggle AI mode (AI plays as black)

## How to start

1. Run `python src/main.py`
2. Choose mode:
   - Click "PvP" button for Player vs Player
   - Click "AI Mode" button for Player vs AI (you play white, AI plays black)
   - Or press P for PvP, A for AI

## Tech stack

- Language: Python 3.13
- Game library: Pygame
- Project layout: simple single-player local game with assets (images and sounds) in the `assets/` folder

## How to load & play

1. Install Python 3.11+ (this project was developed & tested on Python 3.13). Ensure `python` or the full executable path is available.

2. Install dependencies (recommended inside a virtual environment):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If you don't use a virtual environment, you can simply run:

```powershell
python -m pip install -r requirements.txt
```

3. Run the game from the project root:

```powershell
python src\main.py
```

4. Controls while playing:
- Click and drag pieces to move them.
- Press `t` to cycle the board theme (green, brown, blue, gray).
- Press `r` to restart the game.

Notes:
- The `assets/images/` folder contains piece images used by the UI and `assets/sounds/` contains move/capture sounds.
- If the game fails to start with an import error for `pygame`, install it with `python -m pip install pygame` (or re-run step 2).

