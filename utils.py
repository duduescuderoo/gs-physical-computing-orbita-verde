import cv2
import numpy as np

COLORS = {
    "FOGO":   (0, 60, 255),
    "FUMACA": (180, 180, 180),
}

RISK_CONFIG = [
    (0.10, "PERIGO",  (0, 0, 200),   (0, 0, 255)),
    (0.03, "ALERTA",  (0, 100, 200), (0, 165, 255)),
    (0.00, "NORMAL",  (0, 120, 0),   (0, 200, 0)),
]


def draw_detections(frame, detections):
    for d in detections:
        color = COLORS.get(d["label"], (255, 255, 255))
        x, y, w, h = d["bbox"]

        # Bounding box com cantos estilizados
        _draw_corner_box(frame, x, y, w, h, color)

        # Label + confiança
        label_text = f"{d['label']}  {d['confidence']}%"
        (tw, th), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
        cv2.rectangle(frame, (x, y - th - 10), (x + tw + 8, y), color, -1)
        cv2.putText(frame, label_text, (x + 4, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
    return frame


def draw_hud(frame, detections, fps):
    h, w = frame.shape[:2]
    total_area = h * w

    detected_area = sum(d["bbox"][2] * d["bbox"][3] for d in detections)
    ratio = detected_area / total_area

    _, risk_label, bg_color, text_color = RISK_CONFIG[-1]
    for threshold, lbl, bgc, txc in RISK_CONFIG:
        if ratio >= threshold:
            risk_label, bg_color, text_color = lbl, bgc, txc
            break

    n_fogo   = sum(1 for d in detections if d["label"] == "FOGO")
    n_fumaca = sum(1 for d in detections if d["label"] == "FUMACA")

    # Painel superior esquerdo
    overlay = frame.copy()
    cv2.rectangle(overlay, (8, 8), (260, 120), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

    cv2.putText(frame, f"RISCO: {risk_label}", (16, 38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.85, text_color, 2)
    cv2.putText(frame, f"FOGO detectado:   {n_fogo}", (16, 62),
                cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 100, 255), 1)
    cv2.putText(frame, f"FUMACA detectada: {n_fumaca}", (16, 82),
                cv2.FONT_HERSHEY_SIMPLEX, 0.52, (180, 180, 180), 1)
    cv2.putText(frame, f"Cobertura: {ratio*100:.1f}%", (16, 102),
                cv2.FONT_HERSHEY_SIMPLEX, 0.52, (200, 200, 200), 1)

    # FPS — canto superior direito
    cv2.putText(frame, f"FPS: {fps:.0f}", (w - 100, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)

    # Barra de risco na parte inferior
    bar_w = int(w * min(ratio * 5, 1.0))
    cv2.rectangle(frame, (0, h - 8), (w, h), (40, 40, 40), -1)
    cv2.rectangle(frame, (0, h - 8), (bar_w, h), text_color, -1)

    # Marca d'agua OrbitaVerde
    cv2.putText(frame, "OrbitaVerde | FIAP GS 2026", (w - 280, h - 14),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (80, 80, 80), 1)

    return frame


def _draw_corner_box(frame, x, y, w, h, color, length=20, thickness=2):
    # Retangulo leve
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1)
    # Cantos destacados
    for px, py, dx, dy in [
        (x,     y,     1,  1),
        (x+w,   y,    -1,  1),
        (x,     y+h,   1, -1),
        (x+w,   y+h,  -1, -1),
    ]:
        cv2.line(frame, (px, py), (px + dx * length, py), color, thickness)
        cv2.line(frame, (px, py), (px, py + dy * length), color, thickness)
