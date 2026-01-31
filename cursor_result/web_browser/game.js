/* Pong (Ping-Pong) in the browser using Canvas.
   - 2 paddles (W/S and ArrowUp/ArrowDown)
   - Ball movement + wall/paddle collisions
   - Score keeping
   - Space pauses/starts, R resets score
*/

(() => {
  /** @type {HTMLCanvasElement} */
  const canvas = document.getElementById("game");
  /** @type {CanvasRenderingContext2D} */
  const ctx = canvas.getContext("2d");

  const overlay = document.getElementById("overlay");
  const overlayTitle = document.getElementById("overlayTitle");
  const overlayBody = document.getElementById("overlayBody");
  const btnSingle = document.getElementById("btnSingle");
  const btnTwo = document.getElementById("btnTwo");
  const modeText = document.getElementById("modeText");

  // Match the Python version’s feel
  const W = canvas.width;
  const H = canvas.height;

  const PADDLE_W = 20;
  const PADDLE_H = 120;
  const PADDLE_SPEED = 720; // px/sec (roughly similar to step-per-frame feel)

  const BALL_SIZE = 18;
  const BALL_START_SPEED = 420; // px/sec
  const BALL_SPEEDUP_ON_PADDLE = 1.05;
  const BALL_MAX_SPEED = 980;

  const FG = "#ffffff";
  const MUTED = "#b5b7c8";

  const bounds = {
    top: 10,
    bottom: H - 10,
    left: 10,
    right: W - 10,
  };

  const keys = new Set();

  const state = {
    mode: null, // "single" | "two"
    paused: true,
    scoreL: 0,
    scoreR: 0,
    // paddles centered
    paddleL: { x: 60, y: H / 2 - PADDLE_H / 2 },
    paddleR: { x: W - 60 - PADDLE_W, y: H / 2 - PADDLE_H / 2 },
    ball: { x: W / 2 - BALL_SIZE / 2, y: H / 2 - BALL_SIZE / 2, vx: 0, vy: 0 },
  };

  function clamp(v, lo, hi) {
    return Math.max(lo, Math.min(hi, v));
  }

  function randChoice(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  function resetRound(direction) {
    state.ball.x = W / 2 - BALL_SIZE / 2;
    state.ball.y = H / 2 - BALL_SIZE / 2;

    const base = BALL_START_SPEED;
    state.ball.vx = base * direction;
    state.ball.vy = base * randChoice([-0.75, -0.55, 0.55, 0.75]);
  }

  function resetAll() {
    state.scoreL = 0;
    state.scoreR = 0;
    state.paddleL.y = H / 2 - PADDLE_H / 2;
    state.paddleR.y = H / 2 - PADDLE_H / 2;
    resetRound(randChoice([-1, 1]));
  }

  function aabbOverlap(ax, ay, aw, ah, bx, by, bw, bh) {
    return ax < bx + bw && ax + aw > bx && ay < by + bh && ay + ah > by;
  }

  function applyPaddleBounce(paddle, direction) {
    // position ball just outside paddle (avoid sticking)
    if (direction > 0) {
      state.ball.x = paddle.x + PADDLE_W + 2;
    } else {
      state.ball.x = paddle.x - BALL_SIZE - 2;
    }

    // impact in [-1, 1] based on hit location
    const paddleCenterY = paddle.y + PADDLE_H / 2;
    const ballCenterY = state.ball.y + BALL_SIZE / 2;
    let impact = (ballCenterY - paddleCenterY) / (PADDLE_H / 2);
    impact = clamp(impact, -1, 1);

    state.ball.vx = Math.abs(state.ball.vx) * direction * BALL_SPEEDUP_ON_PADDLE;
    state.ball.vy = (state.ball.vy + impact * 160) * 0.98;

    state.ball.vx = clamp(state.ball.vx, -BALL_MAX_SPEED, BALL_MAX_SPEED);
    state.ball.vy = clamp(state.ball.vy, -BALL_MAX_SPEED, BALL_MAX_SPEED);
  }

  function togglePause() {
    if (!state.mode) {
      // If user hits Space before choosing, default to 2-player.
      setMode("two");
      return;
    }
    state.paused = !state.paused;
    overlay.hidden = !state.paused;
    syncOverlay();
  }

  function setMode(mode) {
    state.mode = mode;
    state.paused = false;
    overlay.hidden = true;
    modeText.textContent = mode === "single" ? "Single Player" : "Two Players";
    syncOverlay();
    resetAll();
  }

  function syncOverlay() {
    if (!overlayTitle || !overlayBody) return;

    if (!state.mode) {
      overlayTitle.textContent = "Choose a mode";
      overlayBody.innerHTML =
        "Single player uses an AI paddle on the right.<br />" +
        "Two players uses <kbd>↑</kbd>/<kbd>↓</kbd> for the right paddle.";
      return;
    }

    if (state.paused) {
      overlayTitle.textContent = "Paused";
      overlayBody.innerHTML =
        `Mode: <b>${state.mode === "single" ? "Single Player" : "Two Players"}</b><br />` +
        "Press <kbd>Space</kbd> to resume. Press <kbd>R</kbd> to reset score.<br />" +
        "You can also switch modes:";
    } else {
      overlayTitle.textContent = "Pong";
      overlayBody.innerHTML =
        `Mode: <b>${state.mode === "single" ? "Single Player" : "Two Players"}</b><br />` +
        "Press <kbd>Space</kbd> to pause. Press <kbd>R</kbd> to reset score.";
    }
  }

  function drawCenterLine() {
    ctx.save();
    ctx.strokeStyle = "rgba(255,255,255,0.65)";
    ctx.lineWidth = 3;
    ctx.setLineDash([18, 14]);
    ctx.beginPath();
    ctx.moveTo(W / 2, bounds.top);
    ctx.lineTo(W / 2, bounds.bottom);
    ctx.stroke();
    ctx.restore();
  }

  function drawScore() {
    ctx.save();
    ctx.fillStyle = FG;
    ctx.font = "bold 34px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace";
    ctx.textAlign = "center";
    ctx.textBaseline = "top";
    ctx.fillText(`${state.scoreL}   :   ${state.scoreR}`, W / 2, 18);
    ctx.restore();
  }

  function drawHint() {
    ctx.save();
    ctx.fillStyle = MUTED;
    ctx.font = "14px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace";
    ctx.textAlign = "center";
    ctx.textBaseline = "bottom";
    const rightHint = state.mode === "single" ? "Right: AI" : "Right: ↑/↓";
    ctx.fillText(
      `Left: W/S   ${rightHint}   Space: Pause/Resume   R: Reset`,
      W / 2,
      H - 14
    );
    ctx.restore();
  }

  function render() {
    // Clear
    ctx.fillStyle = "#000000";
    ctx.fillRect(0, 0, W, H);

    // Mid line + score
    drawCenterLine();
    drawScore();

    // Paddles
    ctx.fillStyle = FG;
    ctx.fillRect(state.paddleL.x, state.paddleL.y, PADDLE_W, PADDLE_H);
    ctx.fillRect(state.paddleR.x, state.paddleR.y, PADDLE_W, PADDLE_H);

    // Ball
    ctx.fillRect(state.ball.x, state.ball.y, BALL_SIZE, BALL_SIZE);

    drawHint();
  }

  function update(dt) {
    // Paddle movement (hold keys)
    const dy = PADDLE_SPEED * dt;

    if (keys.has("KeyW")) state.paddleL.y -= dy;
    if (keys.has("KeyS")) state.paddleL.y += dy;
    if (state.mode === "two") {
      if (keys.has("ArrowUp")) state.paddleR.y -= dy;
      if (keys.has("ArrowDown")) state.paddleR.y += dy;
    } else if (state.mode === "single") {
      // Simple AI: track ball when it's coming toward the right paddle,
      // otherwise drift toward center.
      const aiSpeed = PADDLE_SPEED * 0.92;
      const centerY = H / 2 - PADDLE_H / 2;
      const targetY =
        state.ball.vx > 0
          ? state.ball.y + BALL_SIZE / 2 - PADDLE_H / 2
          : centerY;
      const diff = targetY - state.paddleR.y;
      const step = clamp(diff, -aiSpeed * dt, aiSpeed * dt);
      state.paddleR.y += step;
    }

    const paddleTop = bounds.top;
    const paddleBottom = bounds.bottom - PADDLE_H;
    state.paddleL.y = clamp(state.paddleL.y, paddleTop, paddleBottom);
    state.paddleR.y = clamp(state.paddleR.y, paddleTop, paddleBottom);

    if (state.paused) return;

    // Move ball
    state.ball.x += state.ball.vx * dt;
    state.ball.y += state.ball.vy * dt;

    // Wall collisions (top/bottom)
    const ballTop = bounds.top;
    const ballBottom = bounds.bottom - BALL_SIZE;
    if (state.ball.y <= ballTop) {
      state.ball.y = ballTop;
      state.ball.vy *= -1;
    } else if (state.ball.y >= ballBottom) {
      state.ball.y = ballBottom;
      state.ball.vy *= -1;
    }

    // Paddle collisions
    const b = state.ball;
    const pL = state.paddleL;
    const pR = state.paddleR;

    if (
      b.vx < 0 &&
      aabbOverlap(b.x, b.y, BALL_SIZE, BALL_SIZE, pL.x, pL.y, PADDLE_W, PADDLE_H)
    ) {
      applyPaddleBounce(pL, +1);
    } else if (
      b.vx > 0 &&
      aabbOverlap(b.x, b.y, BALL_SIZE, BALL_SIZE, pR.x, pR.y, PADDLE_W, PADDLE_H)
    ) {
      applyPaddleBounce(pR, -1);
    }

    // Scoring (ball exits left/right)
    const rightOut = W + 40;
    const leftOut = -40 - BALL_SIZE;
    if (state.ball.x > rightOut) {
      state.scoreL += 1;
      resetRound(-1);
    } else if (state.ball.x < leftOut) {
      state.scoreR += 1;
      resetRound(+1);
    }
  }

  // Input
  window.addEventListener("keydown", (e) => {
    if (e.code === "Space") {
      e.preventDefault();
      togglePause();
      return;
    }
    if (e.code === "ArrowUp" || e.code === "ArrowDown") {
      // prevent page scroll while playing
      e.preventDefault();
    }
    if (e.code === "KeyR") {
      resetAll();
      return;
    }
    keys.add(e.code);
  });

  window.addEventListener("keyup", (e) => {
    keys.delete(e.code);
  });

  // Ensure canvas can take focus for key hints (not strictly required)
  canvas.addEventListener("pointerdown", () => {
    // On some browsers, focusing the page helps key events.
    window.focus();
  });

  // Start
  resetAll();
  overlay.hidden = false;
  modeText.textContent = "Choose…";
  syncOverlay();

  btnSingle?.addEventListener("click", () => setMode("single"));
  btnTwo?.addEventListener("click", () => setMode("two"));

  let last = performance.now();
  function loop(now) {
    const dt = clamp((now - last) / 1000, 0, 1 / 20);
    last = now;
    update(dt);
    render();
    requestAnimationFrame(loop);
  }

  requestAnimationFrame(loop);
})();

