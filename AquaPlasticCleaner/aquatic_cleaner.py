import cv2
import os
import random

video_path = "water_video.mp4"

# ------------------ CHECK VIDEO ------------------
if not os.path.exists(video_path):
    print("❌ water_video.mp4 not found")
    exit()

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("❌ Cannot open video")
    exit()

print("✅ System Started")

plastic_count = 0
frame_number = 0
PLASTIC_WEIGHT_PER_ITEM = 0.5

FRAME_WIDTH = 800
FRAME_HEIGHT = 500

# ------------------ WATER SURFACE ------------------
water_surface_y = int(FRAME_HEIGHT * 0.75)  # 75% height

# ------------------ BOAT ------------------
boat_x = 50
boat_speed = 5
boat_width = 90
boat_height = 28

# ------------------ PLASTIC ------------------
plastics = [[random.randint(100, 700), random.randint(water_surface_y-30, water_surface_y-5)]
            for _ in range(5)]

# ------------------ FISH ------------------
fish = [[random.randint(800, 1200), random.randint(200, water_surface_y-60)]
        for _ in range(3)]

# ------------------ OTHER AQUATIC ANIMALS ------------------
turtle = [900, water_surface_y - 80]
jellyfish = [600, water_surface_y - 120]

while True:
    ret, frame = cap.read()
    if not ret:
        break


    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    frame_number += 1

    # ------------------ BOAT MOVEMENT ------------------
    boat_x += boat_speed
    if boat_x > FRAME_WIDTH:
        boat_x = -boat_width

    # ------------------ DETECTION LOGIC ------------------
    if frame_number % 120 == 0:
        status = "FISH / ANIMAL DETECTED - BOAT STOPPED"
        color = (0, 0, 255)
        boat_speed = 0
    elif frame_number % 60 == 0:
        plastic_count += 1
        status = "PLASTIC DETECTED - COLLECTING"
        color = (0, 255, 0)
        boat_speed = 5
    else:
        status = "SCANNING WATER..."
        color = (255, 255, 255)
        boat_speed = 5

    # ------------------ DRAW PLASTIC ------------------
    for p in plastics:
        cv2.rectangle(frame, (p[0], p[1]), (p[0]+30, p[1]+15),
                      (0, 255, 0), -1)  # GREEN = plastic
            
        cv2.putText(frame, "PLASTIC",
                (p[0], p[1]-5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4, (0, 255, 0), 1)

        p[0] -= 1
            # -------- PLASTIC COLLECTION LOGIC (COLLISION) --------
    if (boat_x < p[0] + 30 and
        boat_x + boat_width > p[0] and
        water_surface_y - boat_height <= p[1] <= water_surface_y):

        plastic_count += 1
        p[0] = FRAME_WIDTH + random.randint(100, 300)

        if p[0] < -30:
            p[0] = FRAME_WIDTH

    # ------------------ DRAW FISH ------------------
    for f in fish:
        cv2.ellipse(frame, (f[0], f[1]), (25, 12), 0, 0, 360,
                    (255, 0, 0), -1)  # BLUE = fish
        cv2.putText(frame, "FISH",
                (f[0]-15, f[1]-18),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4, (255, 0, 0), 1)

        f[0] -= 3
        if f[0] < -50:
            f[0] = FRAME_WIDTH + random.randint(50, 200)

    # ------------------ DRAW TURTLE ------------------
    cv2.ellipse(frame, (turtle[0], turtle[1]), (20, 15), 0, 0, 360,
                (0, 100, 0), -1)  # DARK GREEN = turtle
    cv2.putText(frame, "TURTLE",
            (turtle[0]-20, turtle[1]-20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4, (0, 150, 0), 1)

    turtle[0] -= 2
    if turtle[0] < -50:
        turtle[0] = FRAME_WIDTH + 150

    # ------------------ DRAW JELLYFISH ------------------
    
    cv2.circle(frame, (jellyfish[0], jellyfish[1]), 10,
               (255, 0, 255), -1)  # PINK = jellyfish
    cv2.putText(frame, "JELLYFISH",
            (jellyfish[0]-30, jellyfish[1]-15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4, (255, 0, 255), 1)

    jellyfish[1] += random.choice([-1, 1])
    

    # ------------------ DRAW BOAT (ON WATER SURFACE) ------------------
    cv2.rectangle(frame,
                  (boat_x, water_surface_y - boat_height),
                  (boat_x + boat_width, water_surface_y),
                  (139, 69, 19), -1)

    cv2.putText(frame, "CLEANING BOAT",
                (boat_x - 10, water_surface_y - boat_height - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 1)

    # ------------------ TEXT INFO ------------------
    cv2.putText(frame, status, (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    cv2.putText(frame, f"Plastic Collected: {plastic_count}",
                (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (255, 255, 0), 2)

    cv2.imshow("AI Aquatic Plastic Cleaning System", frame)

    if cv2.waitKey(30) & 0xFF == 27:
        break
    # -------- VIDEO LOOP --------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # boat movement
    # detection logic
    # drawing boat, plastic, fish
    # status text

    cv2.imshow("AI Aquatic Plastic Cleaning System", frame)

    if cv2.waitKey(30) & 0xFF == 27:
        break

# -------- RELEASE VIDEO --------
cap.release()
cv2.destroyAllWindows()

# ================== PASTE HERE ==================
# ------------------ FINAL RESULT CALCULATION ------------------
PLASTIC_WEIGHT_PER_ITEM = 0.5  # kg per plastic item
total_weight = plastic_count * PLASTIC_WEIGHT_PER_ITEM

import numpy as np

result_screen = 30 * np.ones((500, 800, 3), dtype=np.uint8)

cv2.putText(result_screen, "CLEANING SUMMARY",
            (220, 80),
            cv2.FONT_HERSHEY_SIMPLEX, 1.2,
            (0, 255, 255), 3)

cv2.putText(result_screen,
            f"Plastic Collected : {plastic_count} items",
            (200, 160),
            cv2.FONT_HERSHEY_SIMPLEX, 0.9,
            (255, 255, 255), 2)

cv2.putText(result_screen,
            f"Total Plastic Weight : {total_weight} kg",
            (200, 210),
            cv2.FONT_HERSHEY_SIMPLEX, 0.9,
            (255, 255, 255), 2)

cv2.putText(result_screen,
            "Status : Cleaning Completed Successfully",
            (170, 270),
            cv2.FONT_HERSHEY_SIMPLEX, 0.9,
            (0, 255, 0), 2)

cv2.putText(result_screen,
            "Press any key to exit",
            (260, 340),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
            (200, 200, 200), 2)

cv2.imshow("Final Result", result_screen)
cv2.waitKey(0)
cv2.destroyAllWindows()
