# Smart Fall Risk Prediction System using AI-Based Human Pose Analysis

## 📌 Project Overview

The Smart Fall Risk Prediction System is a real-time computer vision application designed to improve the safety of elderly individuals and patients by detecting potential fall events without requiring wearable sensors. The system captures live video from a webcam, extracts human body landmarks using MediaPipe Pose, analyzes posture-based parameters, and determines whether a person is at risk of falling.

When a fall is detected, the system immediately triggers an alarm, updates a web-based monitoring dashboard, records the event history, and sends an email notification to caregivers for timely assistance.

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

*(Screenshots will be added here.)*

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

B.Tech Computer Science Engineering

Andhra Loyola Institute of Engineering and Technology
