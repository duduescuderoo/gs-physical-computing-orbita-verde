"""
Detector de fogo e fumaca por visao computacional.

Estrategia: combinar analise de COR (HSV) com analise de MOVIMENTO
(subtracao de fundo). Fogo e fumaca se movem; o cenario estatico nao.
Isso elimina falsos positivos de objetos parados com cor parecida
(troncos avermelhados, fundo acinzentado, pontos de luz).
"""

import cv2
import numpy as np


class FireSmokeDetector:
    # --- Cor do FOGO (HSV) ---
    # Saturacao alta separa chama (laranja/vermelho vivo) da fumaca (desaturada).
    FIRE_RANGES = [
        (np.array([0,   90, 150]), np.array([25,  255, 255])),  # laranja-vermelho
        (np.array([155, 90, 150]), np.array([180, 255, 255])),  # vermelho escuro
    ]

    # --- Cor da FUMACA (HSV) ---
    # Baixa saturacao (acinzentada) e brilho medio/alto, evitando pretos e brancos puros.
    SMOKE_SAT_MAX = 60
    SMOKE_VAL_MIN = 90
    SMOKE_VAL_MAX = 240

    MIN_FIRE_AREA  = 250
    MIN_SMOKE_AREA = 900
    SMOKE_MAX_EXTENT = 0.88  # fumaca e difusa; descarta blobs muito solidos

    def __init__(self):
        # Modelo de fundo: aprende o cenario estatico e isola o que se move.
        self._bg = cv2.createBackgroundSubtractorMOG2(
            history=150, varThreshold=35, detectShadows=False)
        self._kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    def detect(self, frame):
        """Retorna lista de deteccoes: {label, bbox, area, confidence}."""
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        motion = self._motion_mask(blurred)

        # FOGO = cor de chama saturada (cor ja e distintiva o bastante;
        # a alta saturacao exigida evita confundir com fumaca desaturada)
        fire_mask = self._clean(self._fire_color(hsv))

        # FUMACA = cor acinzentada E em movimento, sem o que ja e fogo
        smoke_mask = cv2.bitwise_and(self._smoke_color(hsv), motion)
        smoke_mask = cv2.subtract(smoke_mask, fire_mask)
        smoke_mask = self._clean(smoke_mask, close_iter=3)

        detections  = self._extract(fire_mask,  "FOGO",   self.MIN_FIRE_AREA)
        detections += self._extract(smoke_mask, "FUMACA", self.MIN_SMOKE_AREA,
                                    max_extent=self.SMOKE_MAX_EXTENT)
        return detections

    # ------------------------------------------------------------------ #
    def _motion_mask(self, frame):
        mask = self._bg.apply(frame)
        _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
        return cv2.dilate(mask, self._kernel, iterations=3)

    def _fire_color(self, hsv):
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for lower, upper in self.FIRE_RANGES:
            mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lower, upper))
        return mask

    def _smoke_color(self, hsv):
        lower = np.array([0,   0,                  self.SMOKE_VAL_MIN])
        upper = np.array([180, self.SMOKE_SAT_MAX, self.SMOKE_VAL_MAX])
        return cv2.inRange(hsv, lower, upper)

    def _clean(self, mask, close_iter=1):
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  self._kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self._kernel, iterations=close_iter)
        return mask

    def _extract(self, mask, label, min_area, max_extent=None):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        result = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < min_area:
                continue

            x, y, w, h = cv2.boundingRect(cnt)

            if max_extent is not None:
                extent = area / (w * h) if w * h else 1.0
                if extent > max_extent:
                    continue

            result.append({
                "label": label,
                "bbox": (x, y, w, h),
                "area": area,
                "confidence": min(int((area / 4000) * 100), 99),
            })
        return result
