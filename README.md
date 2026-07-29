# Smart Fall Risk Prediction System using AI-Based Human Pose Analysis

## 📌 Project Overview

The **Smart Fall Risk Prediction System** is a real-time computer vision application that enhances the safety of elderly individuals and patients through continuous, contact-free monitoring. Unlike traditional wearable sensor-based systems, this solution uses a webcam to analyse human posture and movement, eliminating the need for any physical monitoring device.

The system leverages **OpenCV** for live video capture and **MediaPipe Pose** for extracting human body landmarks. By analysing posture-based parameters such as torso angle, shoulder alignment, head position, body tilt, and movement patterns, it identifies potential fall events in real time. Whenever a fall is detected, the system immediately activates an audible alarm, updates a web-based monitoring dashboard, records the event history, and sends an email notification to caregivers for timely assistance.

Designed with a focus on simplicity, accessibility, and real-time performance, this project demonstrates how computer vision can be applied to create practical healthcare monitoring solutions for homes, hospitals, and elderly care environments.

---

## 🎯 Motivation

Falls are one of the leading causes of injuries among elderly individuals and patients. Traditional fall detection systems depend on wearable sensors, which may be uncomfortable, require regular charging, or fail if they are not worn correctly.

This project provides a non-contact, camera-based solution that continuously monitors a person's posture using computer vision and generates real-time alerts whenever a fall is detected.

---

## ✨ Features

- Real-time human pose detection using MediaPipe Pose
- Live video processing using OpenCV
- Webcam-based monitoring without wearable devices
- Posture analysis using body landmarks
- Automatic fall risk detection
- Audible alarm on fall detection
- Email notifications to caregivers using SMTP
- Interactive web dashboard
- Fall history tracking
- Analytics dashboard for monitoring fall events

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Programming Language |
| OpenCV | Live video processing |
| MediaPipe Pose | Human pose estimation |
| HTML | Web pages |
| CSS | User Interface |
| JavaScript | Front-end interactions |
| Flask | Web dashboard |
| Flask-SocketIO | Real-time communication |
| SMTP | Email notifications |

---

## ⚙️ System Workflow

1. Capture live video from the webcam.
2. Detect human body landmarks using MediaPipe Pose.
3. Calculate posture-related parameters such as torso angle, shoulder alignment, body tilt, and head position.
4. Determine whether the posture indicates a potential fall.
5. Trigger an alarm if a fall is detected.
6. Send an email notification to the caregiver.
7. Update the web dashboard with the latest fall event.
8. Store the event for future analysis and history.

---

## 📂 Project Structure

```text
Fall_Detection_Project
│
├── screenshots/
├── web_dashboard/
│   ├── static/
│   ├── templates/
│   └── app.py
│
├── main.py
├── alarm.mp3
├── .gitignore
└── README.md
```

---

## 📷 Application Screenshots

### 🏠 Welcome Page
The landing page of the Smart Fall Risk Prediction System.

![Welcome Page](screenshots/01_welcome_page.png)

---

### 📝 Registration Page
Allows new users to create an account.

![Registration Page](screenshots/02_registration_page.png)

---

### 🔐 Login Page
Secure login page for accessing the monitoring dashboard.

![Login Page](screenshots/03_login_page.png)

---

### 📊 Smart Dashboard
Displays the live monitoring interface and overall system status.

![Dashboard](screenshots/04_smart_dashboard.png)

---

### ✅ Normal Detection
Shows the system continuously monitoring a person under normal conditions.

![Normal Detection](screenshots/05_normal_detection.png)

---

### 🚨 Fall Detection
Displays the system identifying an abnormal posture and triggering a fall alert.

![Fall Detection](screenshots/06_fall_detection.png)

---

### 📧 Email Alert
Automatic email notification sent to caregivers after a fall is detected.

![Email Alert](screenshots/07_email_alert.png)

---

### 📈 Analytics Dashboard
Provides visual insights and statistics related to recorded fall events.

![Analytics](screenshots/08_analytics_dashboard.png)

---

### 📋 Fall History
Displays previously detected fall events with timestamps for monitoring and record keeping.

![History](screenshots/09_fall_history.png)

---

## 🚀 Future Improvements

- Improve fall detection accuracy using deep learning models.
- Support multiple-person monitoring.
- Mobile application for caregivers.
- Cloud database integration.
- Real-time SMS notifications.
- Integration with IoT healthcare devices.

---

## 👩‍💻 Author

**Sethu Phani Madhavi**

