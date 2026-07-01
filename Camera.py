import cv2
import mediapipe as mp
import math
import numpy as np


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)
current_mode = "NORMAL"

print("Program başlatıldı. Çıkmak için 'q' tuşuna basın.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Kameradan görüntü alınamadı.")
        break

    # Aynalama etkisini engellemek için görüntüyü yatayda çevir
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    hand_centers = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:


            # Elin merkez noktasını (9 numaralı eklem) alıyoruz
            
            
            cx, cy = int(hand_landmarks.landmark[9].x * w), int(hand_landmarks.landmark[9].y * h)
            hand_centers.append((cx, cy))

    if len(hand_centers) == 2:
        x1, y1 = hand_centers[0]
        x2, y2 = hand_centers[1]
        distance = int(math.hypot(x2 - x1, y2 - y1))
        
        # Mesafe aralıklarına göre filtre modunu seçiyoruz
        if distance < 280:
            current_mode = "SIYAH-BEYAZ"
        elif 280 <= distance <= 650:
            current_mode = "TERS (INVERT)"
        else:
            current_mode = "SEPYA"
    else:
        
        pass

    
    if current_mode == "SIYAH-BEYAZ":
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        text_color = (0, 0, 0)
        
    elif current_mode == "TERS (INVERT)":
        
        frame = cv2.bitwise_not(frame)
        text_color = (0, 255, 255)
        
    elif current_mode == "SEPYA":
        # Sepya efekti için özel bir renk matrisi (kernel) kullanıyoruz(Gemini)
        sepia_kernel = np.array([[0.131, 0.534, 0.272],
                                 [0.168, 0.686, 0.349],
                                 [0.189, 0.769, 0.393]])
        
        # Matris çarpımı ile renkleri sepya tonlarına çekiyoruz(Gemini)
        frame = cv2.transform(frame, sepia_kernel)

        # Piksel değerlerinin 255'i aşmasını engellemek için kırpıyoruz (Gemini)

        frame = np.clip(frame, 0, 255).astype(np.uint8)

        text_color = (20, 60, 130)
        
    else:
        
        text_color = (255, 255, 255) # Beyaz yazı rengi

    # 3. FİLTRELENMİŞ GÖRÜNTÜNÜN ÜZERİNE ÇİZİMLERİ EKLE
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # İki el ekrandayken aralarındaki çizgiyi ve modu ekrana yazdır

    if len(hand_centers) == 2:
        cv2.line(frame, hand_centers[0], hand_centers[1], (0, 255, 0), 3)
        cv2.putText(frame, f"Mesafe: {distance} px", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Aktif olan modu ekrana yazdır
    cv2.putText(frame, f"AKTIF FILTRE: {current_mode}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 3)

    cv2.imshow("Canli Kamera Filtreleri", frame)

    # 'q' tuşuna basılırsa (q=quit) programdan çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
