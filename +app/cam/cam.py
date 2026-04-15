import cv2
import mediapipe as mp
import pyautogui
import math
import threading
import pygame

# Inicializa Pygame Mixer
pygame.mixer.init()

# Função para tocar som
def tocar_som():
    pygame.mixer.music.load("censor-beep-1.mp3")  # nome do arquivo de som
    pygame.mixer.music.play()

# Inicializa MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_face = mp.solutions.face_detection
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
face_detection = mp_face.FaceDetection(min_detection_confidence=0.7)

# Tamanho da tela
screen_width, screen_height = pyautogui.size()

# Acessa webcam
cap = cv2.VideoCapture(0)

click_down = False
face_detected = False

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    hand_results = hands.process(rgb_frame)
    face_results = face_detection.process(rgb_frame)

    # ===== DETECÇÃO DE ROSTO =====
    if face_results.detections:
        if not face_detected:
            face_detected = True
            threading.Thread(target=tocar_som).start()
        for detection in face_results.detections:
            bboxC = detection.location_data.relative_bounding_box
            x = int(bboxC.xmin * frame_width)
            y = int(bboxC.ymin * frame_height)
            w = int(bboxC.width * frame_width)
            h = int(bboxC.height * frame_height)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cv2.putText(frame, 'Rosto Detectado', (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    else:
        face_detected = False

    # ===== DETECÇÃO DE MÃO =====
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger = hand_landmarks.landmark[8]
            thumb = hand_landmarks.landmark[4]

            index_x = int(index_finger.x * frame_width)
            index_y = int(index_finger.y * frame_height)
            screen_x = screen_width * index_finger.x
            screen_y = screen_height * index_finger.y
            pyautogui.moveTo(screen_x, screen_y)

            dist = math.hypot(index_x - int(thumb.x * frame_width),
                              index_y - int(thumb.y * frame_height))

            if dist < 40:
                if not click_down:
                    click_down = True
                    pyautogui.click()
                    cv2.putText(frame, 'CLIQUE!', (index_x, index_y - 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                click_down = False

    cv2.imshow("Controle com a Mão + Rosto + Som (pygame)", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
