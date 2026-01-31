[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Kf5HLjuv)

## Pong (Ping-Pong) in Python

This repo includes a simple **Ping-Pong (Pong)** game that matches the assignment’s minimum requirements:

- **Game environment setup**: playing field + 2 paddles + ball
- **Player input**: move paddles up/down
- **Ball movement + collisions**: ball bounces off walls and paddles
- **Score keeping**: score is tracked and shown on screen

### Run

No dependencies needed (uses Python’s built-in `turtle`).

```bash
python3 pong.py
```

### Controls

- **Left paddle**: `W` (up), `S` (down)
- **Right paddle**: `↑` (up), `↓` (down)
- **Pause/Resume**: `Space`
- **Reset score**: `R`
- **Quit**: `Q`

## Pong in the Browser (Web App)

There’s also a browser-playable version in `web/` (HTML/CSS/JS + Canvas).

When the page loads, choose **Single Player** (right paddle = computer) or **Two Players**.

### Run (recommended)

Start a tiny local server so the browser loads assets reliably:

```bash
python3 -m http.server 8000 --directory web
```

Then open `http://localhost:8000` in your browser.

### Controls

- **Left paddle**: `W` (up), `S` (down)
- **Right paddle**:
  - **Two Players**: `↑` (up), `↓` (down)
  - **Single Player**: computer-controlled (no player-two controls)
- **Pause/Resume**: `Space`
- **Reset score**: `R`
