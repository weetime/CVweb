import cv2
import mediapipe as mp
import asyncio
import websockets
import json

SERVER_URI = "ws://localhost:8080"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

async def send_gesture(action):
    async with websockets.connect(SERVER_URI) as ws:
        await ws.send(json.dumps({"type": "gesture", "action": action}))

async def main():
    cap = cv2.VideoCapture(0)
    last_action = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        action = None
        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

                wrist_y = handLms.landmark[0].y
                if wrist_y < 0.4:
                    action = "scroll_up"
                elif wrist_y > 0.6:
                    action = "scroll_down"

        cv2.imshow("Gesture Camera", frame)

        if action and action != last_action:
            print("Detected:", action)
            await send_gesture(action)
            last_action = action

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())
