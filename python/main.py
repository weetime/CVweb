import cv2
import asyncio
import websockets
import json
from gesture_recognizer import GestureRecognizer

SERVER_URI = "ws://localhost:8080"

async def send_gesture(action):
    async with websockets.connect(SERVER_URI) as ws:
        await ws.send(json.dumps({"type": "gesture", "action": action}))

async def main():
    # Initialize camera and gesture recognizer.
    cap = cv2.VideoCapture(0)
    gesture_recognizer = GestureRecognizer()
    last_action = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process frame with gesture recognizer.
        annotated_frame, action = gesture_recognizer.process_frame(frame)

        # Display the annotated frame.
        cv2.imshow("Gesture Camera", annotated_frame)

        # Send gesture action if detected and different from last action.
        if action and action != last_action:
            print("Detected:", action)
            await send_gesture(action)
            last_action = action

        # Exit on 'q' key press.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup resources.
    cap.release()
    gesture_recognizer.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())
