import cv2
import numpy as np
import math

# --- 1. KAMUS WARNA LENGKAP (HSV & BGR) ---
all_colors_dict = {
    "BIRU": [(90, 80, 50), (130, 255, 255), (255, 0, 0)],
    "OREN": [(5, 100, 100), (20, 255, 255), (0, 165, 255)],
    "KUNING": [(20, 100, 100), (35, 255, 255), (0, 255, 255)],
    "HIJAU": [(35, 100, 100), (85, 255, 255), (0, 255, 0)],
    "MERAH": [(0, 120, 70), (10, 255, 255), (0, 0, 255)],
    "UNGU": [(130, 50, 50), (160, 255, 255), (255, 0, 255)],
    "PINK": [(160, 50, 50), (180, 255, 255), (203, 192, 255)], 
    "COKLAT": [(10, 50, 20), (20, 255, 200), (42, 42, 165)], 
    "PUTIH": [(0, 0, 200), (180, 50, 255), (255, 255, 255)], 
    "HITAM": [(0, 0, 0), (180, 255, 50), (0, 0, 0)] 
}

PIXEL_TO_CM_RATIO = 12.5 

# Fungsi kosong yang dibutuhkan oleh Trackbar OpenCV
def empty(a):
    pass

# --- 2. SETUP KAMERA & GUI ---
cap = cv2.VideoCapture(0)
cap.set(3, 1280) 
cap.set(4, 720)  

# Membuat Window utama dan Window untuk Kontrol (GUI)
cv2.namedWindow("Scanner App")
cv2.namedWindow("Pilih Warna", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Pilih Warna", 400, 500)

# Menambahkan tombol on/off (Trackbar) untuk setiap warna di GUI
for color_name in all_colors_dict.keys():
    # Set default ke 1 (ON) untuk BIRU dan OREN, sisanya 0 (OFF)
    default_state = 1 if color_name in ["BIRU", "OREN"] else 0
    cv2.createTrackbar(color_name, "Pilih Warna", default_state, 1, empty)

print("🚀 Program Berjalan! Silakan pilih warna di window 'Pilih Warna'...")

while True:
    success, img = cap.read()
    if not success: break
    
    img = cv2.flip(img, 1) 
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    detected_objects = []
    
    # --- 3. BACA PILIHAN DARI GUI ---
    selected_colors = {}
    for color_name in all_colors_dict.keys():
        # Baca status dari Trackbar (0 atau 1)
        state = cv2.getTrackbarPos(color_name, "Pilih Warna")
        if state == 1:
            selected_colors[color_name] = all_colors_dict[color_name]
    
    # Jika tidak ada warna yang dipilih sama sekali, jangan proses apa-apa
    if not selected_colors:
        cv2.putText(img, "TIDAK ADA WARNA DIPILIH", (400, 350), 
                    cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 0, 255), 2)
    else:
        # --- 4. DETEKSI WARNA SESUAI PILIHAN GUI ---
        for color_name, (lower, upper, bgr_color) in selected_colors.items():
            lower_np = np.array(lower)
            upper_np = np.array(upper)
            
            mask = cv2.inRange(hsv, lower_np, upper_np)
            
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.erode(mask, kernel, iterations=1)
            mask = cv2.dilate(mask, kernel, iterations=2)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                c = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(c)
                
                if area > 500:
                    M = cv2.moments(c)
                    if M['m00'] != 0:
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        detected_objects.append((area, cx, cy, color_name, bgr_color, c))

        # --- 5. CARI 2 BENDA TERBESAR ---
        detected_objects.sort(key=lambda x: x[0], reverse=True)
        
        if len(detected_objects) >= 2:
            obj1 = detected_objects[0] 
            obj2 = detected_objects[1] 
            
            _, cx1, cy1, name1, color1, c1 = obj1
            _, cx2, cy2, name2, color2, c2 = obj2
            
            # Gambar Benda 1
            cv2.drawContours(img, [c1], -1, color1, 3) 
            cv2.circle(img, (cx1, cy1), 8, color1, cv2.FILLED)
            cv2.putText(img, name1, (cx1 - 20, cy1 - 25), cv2.FONT_HERSHEY_DUPLEX, 0.8, color1, 2)
            
            # Gambar Benda 2
            cv2.drawContours(img, [c2], -1, color2, 3) 
            cv2.circle(img, (cx2, cy2), 8, color2, cv2.FILLED)
            cv2.putText(img, name2, (cx2 - 20, cy2 - 25), cv2.FONT_HERSHEY_DUPLEX, 0.8, color2, 2)
            
            # Kalkulasi Jarak
            cv2.line(img, (cx1, cy1), (cx2, cy2), (255, 255, 255), 2)
            cx_mid, cy_mid = (cx1 + cx2) // 2, (cy1 + cy2) // 2
            
            length_px = math.hypot(cx2 - cx1, cy2 - cy1)
            distance_cm = length_px / PIXEL_TO_CM_RATIO
            
            cv2.putText(img, f'{distance_cm:.1f} cm', (cx_mid - 40, cy_mid - 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    # --- 6. TAMPILAN GUI DASAR ---
    cv2.putText(img, "GUI COLOR TRACKER", (40, 50), 
                cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
    
    cv2.imshow("Scanner App", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Scanner App", cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()