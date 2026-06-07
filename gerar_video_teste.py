"""
Gera um video de teste com simulacao de fogo e fumaca.
Resultado: teste_fogo.mp4 na mesma pasta.
"""

import cv2
import numpy as np

WIDTH, HEIGHT, FPS, DURACAO = 640, 480, 30, 8
OUT = cv2.VideoWriter("teste_fogo.mp4",
                      cv2.VideoWriter_fourcc(*"mp4v"),
                      FPS, (WIDTH, HEIGHT))

for frame_n in range(FPS * DURACAO):
    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    t = frame_n / FPS

    # Fundo escuro com leve variacao
    frame[:] = (20, 20, 20)

    # --- FOGO (laranja/vermelho) ---
    cx = int(200 + 30 * np.sin(t * 2))
    cy = int(350 + 10 * np.cos(t * 3))
    for i in range(80):
        r = np.random.randint(5, 40)
        ox = np.random.randint(-50, 50)
        oy = np.random.randint(-80, 10)
        # BGR: vermelho-laranja
        b = np.random.randint(0, 40)
        g = np.random.randint(60, 160)
        rv = np.random.randint(200, 255)
        cv2.circle(frame, (cx + ox, cy + oy), r, (b, g, rv), -1)

    # --- FUMACA (cinza claro) ---
    sx = int(420 + 20 * np.sin(t * 1.5))
    sy = int(200 - int(t * 8) % 200)
    for i in range(60):
        r = np.random.randint(10, 50)
        ox = np.random.randint(-60, 60)
        oy = np.random.randint(-40, 40)
        v = np.random.randint(160, 220)
        alpha_frame = frame.copy()
        cv2.circle(alpha_frame, (sx + ox, sy + oy), r, (v, v, v), -1)
        cv2.addWeighted(alpha_frame, 0.3, frame, 0.7, 0, frame)

    # Suaviza para parecer mais natural
    frame = cv2.GaussianBlur(frame, (7, 7), 0)
    OUT.write(frame)

OUT.release()
print("Video gerado: teste_fogo.mp4")
