import cv2
import mediapipe as mp

# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize hands detector
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Initialize the webcam
cap = cv2.VideoCapture(0)

def count_raised_fingers(hand_landmarks):
    """Counts the number of raised fingers based on hand landmarks."""
    if not hand_landmarks:
        return 0

    # Access the landmarks for the thumb and fingers
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_dip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_dip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_dip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP]

    def is_finger_raised(tip, dip):
        """Determines if a finger is raised based on the tip and dip landmarks."""
        return tip.y < dip.y

    # Counting raised fingers
    fingers = 0

    # Thumb: Typically check x-coordinate as thumb extends away from palm
    if thumb_tip.x < thumb_ip.x:
        fingers += 1

    # Index Finger
    if is_finger_raised(index_tip, index_dip):
        fingers += 1

    # Middle Finger
    if is_finger_raised(middle_tip, middle_dip):
        fingers += 1

    # Ring Finger
    if is_finger_raised(ring_tip, ring_dip):
        fingers += 1

    # Pinky Finger
    if is_finger_raised(pinky_tip, pinky_dip):
        fingers += 1

    return fingers

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the image
    results = hands.process(rgb_frame)

    # Draw hand landmarks and count raised fingers
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            num_raised_fingers = count_raised_fingers(hand_landmarks)
            cv2.putText(frame, f'Raised Fingers: {num_raised_fingers}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Show the image
    cv2.imshow('Hand Gesture Recognition', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'ESC' to exit
        break

cap.release()
cv2.destroyAllWindows()
