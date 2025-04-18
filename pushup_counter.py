import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Calculate angle between three points
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180 else angle

def show_message(image, msg, y=50, color=(0, 0, 255)):
    cv2.putText(image, msg, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

# Timer helper
def wait_screen(message, seconds=10):
    start = time.time()
    while time.time() - start < seconds:
        screen = np.zeros((400, 600, 3), dtype=np.uint8)
        show_message(screen, f'{message} - Starting in {int(seconds - (time.time() - start))} sec', 200, (255, 255, 255))
        cv2.imshow('Smart Fitness Tracker', screen)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
    return True

# Workout session logic
def run_session(cap, pose, duration, exercise):
    counter = 0
    stage = None
    start_time = time.time()

    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            lm = results.pose_landmarks.landmark
            get = lambda x: [lm[x.value].x, lm[x.value].y]

            l_sh = get(mp_pose.PoseLandmark.LEFT_SHOULDER)
            l_el = get(mp_pose.PoseLandmark.LEFT_ELBOW)
            l_wr = get(mp_pose.PoseLandmark.LEFT_WRIST)
            l_hip = get(mp_pose.PoseLandmark.LEFT_HIP)
            l_knee = get(mp_pose.PoseLandmark.LEFT_KNEE)
            l_ank = get(mp_pose.PoseLandmark.LEFT_ANKLE)
            r_sh = get(mp_pose.PoseLandmark.RIGHT_SHOULDER)

            if exercise == 'pushup':
                shoulder_diff = np.abs(l_sh[0] - r_sh[0])
                if shoulder_diff < 0.1:
                    angle = calculate_angle(l_sh, l_el, l_wr)
                    if angle > 160:
                        stage = 'up'
                    elif angle < 90 and stage == 'up':
                        stage = 'down'
                        counter += 1
                    elif angle >= 90:
                        show_message(image, "Lower your body more for a full push-up", 100)
                else:
                    show_message(image, "Turn 90 degrees for side view (Push-ups)", 100)

            elif exercise == 'situp':
                angle = calculate_angle(l_sh, l_hip, l_knee)
                if angle > 160:
                    stage = 'down'
                elif angle < 100 and stage == 'down':
                    stage = 'up'
                    counter += 1

            elif exercise == 'curl':
                shoulder_diff = np.abs(l_sh[0] - r_sh[0])
                if shoulder_diff > 0.1:
                    angle = calculate_angle(l_sh, l_el, l_wr)
                    if angle > 160:
                        stage = 'down'
                    elif angle < 50 and stage == 'down':
                        stage = 'up'
                        counter += 1
                else:
                    show_message(image, "Face the camera for curls (Front View)", 100)

            # Show counter
            cv2.putText(image, f'{exercise.capitalize()} Count: {counter}', (10, 420),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        except Exception as e:
            pass

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        elapsed = int(duration - (time.time() - start_time))
        cv2.putText(image, f'Time Left: {elapsed}s', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.imshow('Smart Fitness Tracker', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    return counter

# MAIN
cap = cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:

    if not wait_screen("Push-ups (Side View)", 10): exit()
    pushups = run_session(cap, pose, 60, 'pushup')

    if not wait_screen("Rest", 10): exit()

    if not wait_screen("Sit-ups (Side View)", 10): exit()
    situps = run_session(cap, pose, 60, 'situp')

    if not wait_screen("Rest", 10): exit()

    if not wait_screen("Dumbbell Curls (Front View)", 10): exit()
    curls = run_session(cap, pose, 60, 'curl')

    # Final results screen
    while True:
        result_screen = np.zeros((400, 600, 3), dtype=np.uint8)
        show_message(result_screen, f'Push-ups: {pushups}', 150, (255, 0, 0))
        show_message(result_screen, f'Sit-ups: {situps}', 200, (0, 255, 0))
        show_message(result_screen, f'Curls: {curls}', 250, (0, 0, 255))
        show_message(result_screen, 'Workout Complete! Press Q to exit', 320, (255, 255, 0))
        cv2.imshow('Smart Fitness Tracker', result_screen)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
