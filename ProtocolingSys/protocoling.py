import cv2
import mediapipe as mp
import os
import dlib
from scipy.spatial import distance as dist
import time

# Initialize Mediapipe for face detection
mp_face_detection = mp.solutions.face_detection

# Dlib for gaze tracking
detector = dlib.get_frontal_face_detector()

# path = os.path.abspath("C:/Users/avive/Desktop/ProtocolingSys/shape_predictor_68_face_landmarks.dat")
predictor = dlib.shape_predictor("C:/Users/avive/Desktop/ProtocolingSys/shape_predictor_68_face_landmarks.dat")

# Thresholds
EAR_THRESHOLD = 0.2
HEAD_VISIBILITY_THRESHOLD = 0.35  # 35% of frame width
MULTI_PERSON_TIMEOUT = 10  # Added missing constant
LOG_COOLDOWN = 1.0

# State tracking variables
last_head_log_time = 0
last_eyes_closed_time = 0
multi_person_start_time = None
multi_person_logged = False

def eye_aspect_ratio(eye):
    eye = [(point.x, point.y) for point in eye]
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def is_head_insufficient(bbox, frame_width):
    if bbox is None: return True
    _, _, w, _ = bbox   # Unpacking a sequence mainly a bounding box where first _ is x, second _ is y and last _ is height
    return (w / frame_width) < HEAD_VISIBILITY_THRESHOLD

cap = cv2.VideoCapture(0)

with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        current_time = time.time()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_height, frame_width, _ = frame.shape
        
        # Face detection
        face_results = face_detection.process(rgb_frame)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray_frame)

        # Head visibility check
        head_visible = len(faces) > 0
        head_state = "visible"
        
        if not head_visible:
            if current_time - last_head_log_time > LOG_COOLDOWN:
                print("[LOG] Head not visible in frame!")
                last_head_log_time = current_time
        else:
            for face in faces:
                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                
                if is_head_insufficient((x, y, w, h), frame_width):
                    head_state = "too_small"
                    if current_time - last_head_log_time > LOG_COOLDOWN:
                        print(f"[LOG] Head visible but too small ({w/frame_width*100:.1f}% of frame)")
                        last_head_log_time = current_time

                # Eye tracking
                landmarks = predictor(gray_frame, face)
                left_eye = [landmarks.part(i) for i in range(36, 42)]
                right_eye = [landmarks.part(i) for i in range(42, 48)]
                ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2
                
                if ear < EAR_THRESHOLD and current_time - last_eyes_closed_time > LOG_COOLDOWN:
                    print("[LOG] Eyes closed!")
                    last_eyes_closed_time = current_time

        # Multiple person detection
        if face_results.detections:
            if len(face_results.detections) > 1:
                if multi_person_start_time is None:
                    multi_person_start_time = current_time
                elif current_time - multi_person_start_time > MULTI_PERSON_TIMEOUT and not multi_person_logged:
                    print("[LOG] Multiple people detected for 15+ seconds!")
                    multi_person_logged = True
            else:
                multi_person_start_time = None
                multi_person_logged = False

        cv2.imshow("Proctoring System", frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()