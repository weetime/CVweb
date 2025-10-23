import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Tuple


class GestureRecognizer:
    def __init__(self, max_num_hands: int = 1):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Optional[str]]:
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)
        
        gesture = None
        
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                gesture = self._detect_gesture(hand_landmarks)
        
        return frame, gesture
    
    def _detect_gesture(self, hand_landmarks) -> Optional[str]:
        wrist = hand_landmarks.landmark[0]
        wrist_y = wrist.y
        
        if wrist_y < 0.4:
            return "scroll_up"
        elif wrist_y > 0.6:
            return "scroll_down"
        
        return None
    
    def release(self):
        pass
