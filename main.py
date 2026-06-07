"""
OrbitaVerde - Deteccao de Fumaca e Fogo
Global Solution 2026 | Physical Computing: IoT & IoB | FIAP

Integrantes:
  Davi Vieira      RM556798
  Luca Monteiro    RM556906
  Arthur Silva     RM553320
  Eduardo Escudero RM556527

Uso:
  python main.py --video caminho/para/video.mp4
  python main.py --webcam
"""

import argparse
import time
import cv2

from detector import FireSmokeDetector
from utils import draw_detections, draw_hud

MAX_DISPLAY_HEIGHT = 600   # altura maxima da janela de exibicao
WARMUP_FRAMES = 15         # frames iniciais p/ o modelo de fundo estabilizar


def run(source, delay=1):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"[ERRO] Nao foi possivel abrir: {source}")
        return

    detector = FireSmokeDetector()
    print("[INFO] OrbitaVerde iniciado. Pressione Q para sair.\n")

    prev_time = time.time()
    frame_count = 0
    alert_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[INFO] Fim do video.")
            break

        frame_count += 1
        frame = _resize_to_fit(frame)

        now = time.time()
        fps = 1.0 / (now - prev_time + 1e-9)
        prev_time = now

        detections = detector.detect(frame)

        # Ignora deteccoes durante o aquecimento do modelo de fundo
        if frame_count <= WARMUP_FRAMES:
            detections = []

        if detections:
            alert_count += 1
            _log(frame_count, detections)

        frame = draw_detections(frame, detections)
        frame = draw_hud(frame, detections, fps)

        cv2.imshow("OrbitaVerde - Deteccao de Fumaca e Fogo", frame)
        if cv2.waitKey(delay) & 0xFF == ord("q"):
            print("[INFO] Encerrado pelo usuario.")
            break

    cap.release()
    cv2.destroyAllWindows()
    _summary(frame_count, alert_count)


def _resize_to_fit(frame):
    h, w = frame.shape[:2]
    if h > MAX_DISPLAY_HEIGHT:
        scale = MAX_DISPLAY_HEIGHT / h
        frame = cv2.resize(frame, (int(w * scale), MAX_DISPLAY_HEIGHT))
    return frame


def _log(frame_n, detections):
    labels = ", ".join(d["label"] for d in detections)
    conf = max(d["confidence"] for d in detections)
    print(f"[FRAME {frame_n:04d}] {labels} | confianca max: {conf}%")


def _summary(frames, alerts):
    print(f"\n[RESUMO] Frames analisados : {frames}")
    print(f"[RESUMO] Frames com alerta : {alerts}")
    if frames:
        print(f"[RESUMO] Taxa de deteccao  : {alerts / frames * 100:.1f}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="OrbitaVerde - Deteccao de Fumaca e Fogo via Visao Computacional")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--video",  type=str, help="Caminho para arquivo de video")
    group.add_argument("--webcam", action="store_true", help="Usar webcam (indice 0)")
    parser.add_argument("--delay", type=int, default=1,
                        help="Atraso por frame em ms (use ~120 para camera lenta)")
    parser.add_argument("--slow", action="store_true",
                        help="Atalho para camera lenta (delay de 120ms)")
    args = parser.parse_args()

    delay = 120 if args.slow else args.delay
    run(0 if args.webcam else args.video, delay)
