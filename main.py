import cv2
import mediapipe as mp
import math
import pygame
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import time
from socketio import Client
import smtplib
from email.mime.text import MIMEText


receiver_email = input("Enter email to receive fall alerts: ")

fall_count = 0
last_email_time = 0
email_sent_count = 0

EMAIL_COOLDOWN = 120
MAX_EMAILS = 2

SENDER_EMAIL = "your email id"
SENDER_PASSWORD = "your password"


# ---------------- EMAIL FUNCTION ----------------

def send_email_alert(time_of_fall, risk):

    subject = "Fall Alert Detected"

    body = f"""
A fall has been detected.

Time: {time_of_fall}
Risk Score: {risk}/3

Please check the monitoring dashboard.

http://localhost:5000/
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(SENDER_EMAIL,SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL,receiver_email,msg.as_string())
        server.quit()

        print("Email alert sent!")

    except Exception as e:
        print("Email failed:",e)


# ---------------- Alarm Setup ----------------

pygame.mixer.init()
pygame.mixer.music.load("alarm.mp3")


# ---------------- MediaPipe Pose ----------------

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils


# ---------------- Tkinter Window ----------------

root = tk.Tk()
root.title("Real-Time Fall Detection")
root.geometry("950x600")
root.configure(bg="#f0f0f0")

video_label = Label(root, bd=5, relief="sunken")
video_label.pack(side="left", padx=15, pady=15)

sidebar = tk.Frame(root, width=250, bg="#d0d0d0")
sidebar.pack(side="right", fill="y", padx=10, pady=10)

status_label = Label(sidebar, text="Status: NORMAL", font=("Helvetica", 16), bg="#d0d0d0", fg="green")
status_label.pack(pady=10)

torso_label = Label(sidebar, text="Torso Angle: 0", font=("Helvetica", 12), bg="#d0d0d0")
torso_label.pack(pady=5)

shoulder_label = Label(sidebar, text="Shoulder Tilt: 0", font=("Helvetica", 12), bg="#d0d0d0")
shoulder_label.pack(pady=5)

head_label = Label(sidebar, text="Head-Hip Diff: 0", font=("Helvetica", 12), bg="#d0d0d0")
head_label.pack(pady=5)

risk_label = Label(sidebar, text="Risk Score: 0/3", font=("Helvetica", 12), bg="#d0d0d0")
risk_label.pack(pady=5)

last_fall_label = Label(sidebar, text="Last Fall: None", font=("Helvetica", 12), bg="#d0d0d0", fg="red")
last_fall_label.pack(pady=20)


# ---------------- Buttons ----------------

def start_detection():
    global running
    running = True

def stop_detection():
    global running
    running = False
    pygame.mixer.music.stop()

def reset_alarm():
    pygame.mixer.music.stop()
    status_label.config(text="Status: NORMAL", fg="green")
    video_label.config(bd=5, relief="sunken", highlightbackground="#000", highlightcolor="#000")

Button(sidebar, text="Start Detection", command=start_detection, width=20).pack(pady=5)
Button(sidebar, text="Stop Detection", command=stop_detection, width=20).pack(pady=5)
Button(sidebar, text="Reset Alarm", command=reset_alarm, width=20).pack(pady=5)


# ---------------- SocketIO Dashboard ----------------

sio = Client()
try:
    sio.connect('http://localhost:5000')
except:
    print("Could not connect to dashboard.")


# ---------------- Video Capture ----------------

cap = cv2.VideoCapture(0)
running = True
fall_detected = False
no_pose_frames = 0
NO_POSE_THRESHOLD = 5
last_risk_count = 0


# ---------------- Thresholds ----------------

TORSO_ANGLE_THRESHOLD = 45
VERTICAL_DIFF_THRESHOLD = 0.15
SHOULDER_TILT_THRESHOLD = 0.1
TORSO_SPEED_THRESHOLD = 0.02
torso_y_history = []


# ---------------- Frame Processing ----------------

def update_frame():

    global fall_detected, no_pose_frames, last_risk_count, torso_y_history
    global fall_count, last_email_time, email_sent_count

    if running:

        ret, frame = cap.read()

        if ret:

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)

            if results.pose_landmarks:

                no_pose_frames = 0

                mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                landmarks = results.pose_landmarks.landmark

                left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                head = landmarks[mp_pose.PoseLandmark.NOSE]

                shoulder_x = (left_shoulder.x + right_shoulder.x) / 2
                shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
                hip_x = (left_hip.x + right_hip.x) / 2
                hip_y = (left_hip.y + right_hip.y) / 2
                head_y = head.y

                dx = hip_x - shoulder_x
                dy = hip_y - shoulder_y
                torso_angle = abs(math.degrees(math.atan2(dy, dx)))

                vertical_diff = abs(shoulder_y - hip_y)
                shoulder_tilt = abs(left_shoulder.y - right_shoulder.y)
                head_below_hip = head_y > hip_y

                torso_y = (shoulder_y + hip_y) / 2
                torso_y_history.append(torso_y)

                if len(torso_y_history) > 5:
                    torso_y_history.pop(0)

                torso_speed = abs(torso_y_history[-1] - torso_y_history[-2]) if len(torso_y_history) >= 2 else 0

                risk_count = 0

                if torso_angle > TORSO_ANGLE_THRESHOLD:
                    risk_count += 1

                if head_below_hip and vertical_diff < VERTICAL_DIFF_THRESHOLD:
                    risk_count += 1

                if shoulder_tilt > SHOULDER_TILT_THRESHOLD:
                    risk_count += 1

                last_risk_count = risk_count

                if risk_count >= 2 or torso_speed > TORSO_SPEED_THRESHOLD:

                    formatted_time = time.strftime("%I:%M %p")

                    status_label.config(text="Status: FALL DETECTED!", fg="red")
                    last_fall_label.config(text=f"Last Fall: {formatted_time}")

                    video_label.config(bd=8, relief="solid", highlightbackground="red", highlightcolor="red")

                    if not fall_detected:

                        fall_detected = True
                        pygame.mixer.music.play(-1)

                        try:
                          fall_type = "UNSTABLE POSTURE"

                          if torso_angle > 70 and torso_speed > 0.02:
                              fall_type = "BACKWARD FALL"
                          elif shoulder_tilt > 0.05:
                              fall_type = "SIDE FALL"

# -------- SEND DATA --------
                          sio.emit('new_fall', {
                              'time': formatted_time,
                              'risk': risk_count,
                              'torso_angle': int(torso_angle),
                              'shoulder_tilt': round(shoulder_tilt, 2),
                              'head_hip_diff': round(vertical_diff, 2),
                              'torso_speed': round(torso_speed, 3),
                              'type': fall_type   # ✅ NEW FIELD
                           })
                           

                        except:
                            print("Could not send to dashboard.")

                        fall_count += 1
                        current_time = time.time()

                        if fall_count >= 5 and email_sent_count < MAX_EMAILS:
                            if current_time - last_email_time > EMAIL_COOLDOWN:
                                send_email_alert(formatted_time, risk_count)
                                last_email_time = current_time
                                email_sent_count += 1
                                fall_count = 0

                    alert_popup = tk.Label(root,text="FALL ALERT!",font=("Helvetica",20,"bold"),bg="red",fg="white")
                    alert_popup.place(x=300,y=50)
                    root.after(1500,alert_popup.destroy)

                else:

                    status_label.config(text="Status: NORMAL", fg="green")
                    video_label.config(bd=5, relief="sunken", highlightbackground="#000", highlightcolor="#000")

                    if fall_detected:
                        fall_detected = False
                        pygame.mixer.music.stop()

                torso_label.config(text=f"Torso Angle: {int(torso_angle)}")
                shoulder_label.config(text=f"Shoulder Tilt: {round(shoulder_tilt,2)}")
                head_label.config(text=f"Head-Hip Diff: {round(vertical_diff,2)}")
                risk_label.config(text=f"Risk Score: {risk_count}/3")

            else:

                no_pose_frames += 1

                if no_pose_frames >= NO_POSE_THRESHOLD and last_risk_count >= 2:

                    status_label.config(text="Status: FALL DETECTED (OFF-FRAME)!", fg="red")
                    video_label.config(bd=8, relief="solid", highlightbackground="red", highlightcolor="red")

                    if not fall_detected:
                        fall_detected = True
                        pygame.mixer.music.play(-1)

            img = Image.fromarray(rgb)
            imgtk = ImageTk.PhotoImage(image=img)

            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)

    video_label.after(30, update_frame)


update_frame()
root.mainloop()

cap.release()
pygame.mixer.quit()