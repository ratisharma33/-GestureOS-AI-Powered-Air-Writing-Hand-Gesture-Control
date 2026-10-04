import cv2
import mediapipe as mp
import numpy as np
import os
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# ==========================================
# MODEL
# ==========================================

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "hand_landmarker.task"
)

base_options = python.BaseOptions(
    model_asset_path=MODEL_PATH
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

detector = vision.HandLandmarker.create_from_options(options)


# ==========================================
# CAMERA
# ==========================================

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# ==========================================
# AIR CANVAS
# ==========================================

canvas = None

previous_x = None
previous_y = None

drawing = False

brush_size = 5


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    success, frame = cap.read()

    if not success:
        print("Camera not found!")
        break

    frame = cv2.flip(frame, 1)

    height, width, _ = frame.shape

    # Create canvas once
    if canvas is None:
        canvas = np.zeros_like(frame)


    # ======================================
    # MEDIAPIPE IMAGE
    # ======================================

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = detector.detect(mp_image)


    gesture = "NO HAND"
    mode = "WAITING"


    # ======================================
    # HAND DETECTED
    # ======================================

    if result.hand_landmarks:

        hand = result.hand_landmarks[0]

        # ----------------------------------
        # GET FINGER STATES
        # ----------------------------------

        index_up = hand[8].y < hand[6].y
        middle_up = hand[12].y < hand[10].y
        ring_up = hand[16].y < hand[14].y
        pinky_up = hand[20].y < hand[18].y

        # ----------------------------------
        # INDEX FINGER POSITION
        # ----------------------------------

        index_x = int(hand[8].x * width)
        index_y = int(hand[8].y * height)


        # ==================================
        # AIR WRITING
        # ==================================

        if index_up and not middle_up and not ring_up and not pinky_up:

            gesture = "INDEX FINGER"
            mode = "AIR WRITING"

            # Draw fingertip
            cv2.circle(
                frame,
                (index_x, index_y),
                10,
                (0, 255, 0),
                -1
            )


            # Draw line from previous position
            if previous_x is not None:

                cv2.line(
                    canvas,
                    (previous_x, previous_y),
                    (index_x, index_y),
                    (0, 255, 255),
                    brush_size
                )

            previous_x = index_x
            previous_y = index_y

            drawing = True


        # ==================================
        # FIST = STOP WRITING
        # ==================================

        elif not index_up and not middle_up and not ring_up and not pinky_up:

            gesture = "FIST"
            mode = "PAUSED"

            previous_x = None
            previous_y = None

            drawing = False


        # ==================================
        # PEACE = ERASER
        # ==================================

        elif index_up and middle_up and not ring_up and not pinky_up:

            gesture = "PEACE"
            mode = "ERASER"

            cv2.circle(
                frame,
                (index_x, index_y),
                20,
                (0, 0, 255),
                2
            )

            # Erase around fingertip
            cv2.circle(
                canvas,
                (index_x, index_y),
                30,
                (0, 0, 0),
                -1
            )

            previous_x = None
            previous_y = None


        # ==================================
        # OPEN PALM
        # ==================================

        elif index_up and middle_up and ring_up and pinky_up:

            gesture = "OPEN PALM"
            mode = "READY"

            previous_x = None
            previous_y = None


        else:

            gesture = "OTHER"
            mode = "PAUSED"

            previous_x = None
            previous_y = None


        # ==================================
        # DRAW HAND LANDMARKS
        # ==================================

        for point in hand:

            x = int(point.x * width)
            y = int(point.y * height)

            cv2.circle(
                frame,
                (x, y),
                4,
                (255, 255, 255),
                -1
            )


        # Draw connections
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (0, 5), (5, 6), (6, 7), (7, 8),
            (5, 9), (9, 10), (10, 11), (11, 12),
            (9, 13), (13, 14), (14, 15), (15, 16),
            (13, 17), (17, 18), (18, 19), (19, 20),
            (0, 17)
        ]

        for start, end in connections:

            x1 = int(hand[start].x * width)
            y1 = int(hand[start].y * height)

            x2 = int(hand[end].x * width)
            y2 = int(hand[end].y * height)

            cv2.line(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 255, 255),
                2
            )

    else:

        previous_x = None
        previous_y = None


    # ==========================================
    # COMBINE CANVAS WITH CAMERA
    # ==========================================

    frame = cv2.addWeighted(
        frame,
        1,
        canvas,
        0.8,
        0
    )


    # ==========================================
    # TOP INFORMATION PANEL
    # ==========================================

    cv2.rectangle(
        frame,
        (10, 10),
        (430, 145),
        (20, 20, 20),
        -1
    )

    cv2.putText(
        frame,
        "AIR WRITE",
        (30, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Gesture: " + gesture,
        (30, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Mode: " + mode,
        (30, 112),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 0),
        2
    )


    # ==========================================
    # INSTRUCTIONS
    # ==========================================

    cv2.putText(
        frame,
        "INDEX = WRITE | PEACE = ERASE | FIST = PAUSE",
        (20, height - 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "C = CLEAR    S = SAVE    Q = EXIT",
        (20, height - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    # ==========================================
    # SHOW
    # ==========================================

    cv2.imshow(
        "GestureOS - Air Writing",
        frame
    )


    # ==========================================
    # KEYBOARD CONTROLS
    # ==========================================

    key = cv2.waitKey(1) & 0xFF


    # Clear
    if key == ord("c"):

        canvas = np.zeros_like(frame)

        previous_x = None
        previous_y = None


    # Save
    elif key == ord("s"):

        filename = (
            "air_writing_"
            + str(int(time.time()))
            + ".png"
        )

        cv2.imwrite(filename, canvas)

        print("Saved:", filename)


    # Exit
    elif key == ord("q") or key == 27:

        break


# ==========================================
# CLEANUP
# ==========================================

cap.release()

cv2.destroyAllWindows()

detector.close()
