import cv2
import mediapipe as mp
import os
import json

# Initialize MediaPipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Define classes
classes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 
           'Yes', 'No', 'I Love You']
images_per_session = 117
max_images_per_class = 3510

# Directory setup
dataset_path = 'ASL_Dataset'
os.makedirs(dataset_path, exist_ok=True)
for class_name in classes:
    os.makedirs(os.path.join(dataset_path, class_name), exist_ok=True)

# Tracking file setup
tracking_file = os.path.join(dataset_path, "image_tracking.json")
if not os.path.exists(tracking_file):
    with open(tracking_file, 'w') as f:
        json.dump({}, f)

# Load tracking data
with open(tracking_file, 'r') as f:
    tracking_data = json.load(f)

# Input participant ID
participant_id = input("Enter participant ID: ").strip()
if participant_id not in tracking_data:
    tracking_data[participant_id] = {class_name: 0 for class_name in classes}

# Initialize variables
current_class_index = 0  # Start with the first class (Class A)
current_class = classes[current_class_index]
session_image_count = tracking_data[participant_id].get(current_class, 0)

print(f"Starting with Class: {current_class}. Press 'c' to capture, 'n' for next class, and 'q' to quit.")

# Start video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Flip frame for a mirror effect
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame with MediaPipe
    results = hands.process(rgb_frame)
    
    # Draw hand landmarks and bounding box
    hand_detected = False
    if results.multi_hand_landmarks:
        hand_detected = True
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get bounding box
            h, w, _ = frame.shape
            bbox_x = [int(lm.x * w) for lm in hand_landmarks.landmark]
            bbox_y = [int(lm.y * h) for lm in hand_landmarks.landmark]
            x_min, x_max = min(bbox_x), max(bbox_x)
            y_min, y_max = min(bbox_y), max(bbox_y)

            # Add a margin to the bounding box
            margin = 20
            x_min = max(0, x_min - margin)
            x_max = min(w, x_max + margin)
            y_min = max(0, y_min - margin)
            y_max = min(h, y_max + margin)

            # Draw the enlarged bounding box
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    # Display current class and session image count
    cv2.putText(frame, f"Class: {current_class}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Session Images: {session_image_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Capture", frame)

    key = cv2.waitKey(1)

    # Key controls
    if key == ord('q'):  # Quit
        break
    elif key == ord('n'):  # Next class
        if current_class_index + 1 < len(classes):  # Check if more classes exist
            current_class_index += 1
            current_class = classes[current_class_index]
            session_image_count = tracking_data[participant_id].get(current_class, 0)
            print(f"Switched to Class: {current_class}.")
        else:
            print("No more classes to capture.")
    elif key == ord('c'):  # Capture image
        if hand_detected:
            current_folder = os.path.join(dataset_path, current_class)
            total_images = len([img for img in os.listdir(current_folder) if img.endswith('.jpg')])

            if total_images < max_images_per_class and session_image_count < images_per_session:
                # Save cropped image
                save_path = os.path.join(current_folder, f"{current_class}_{participant_id}_{total_images + 1}.jpg")
                cropped_image = frame[y_min:y_max, x_min:x_max]
                cv2.imwrite(save_path, cropped_image)
                session_image_count += 1
                tracking_data[participant_id][current_class] = session_image_count
                print(f"Captured image {session_image_count} for Class: {current_class}, Participant: {participant_id}.")
            elif session_image_count >= images_per_session:
                print(f"Session limit of {images_per_session} images reached for Class: {current_class}.")
            else:
                print(f"Class '{current_class}' already has {max_images_per_class} images.")
        else:
            print("No hand detected. Please try again.")

# Save tracking data
with open(tracking_file, 'w') as f:
    json.dump(tracking_data, f)

cap.release()
cv2.destroyAllWindows()