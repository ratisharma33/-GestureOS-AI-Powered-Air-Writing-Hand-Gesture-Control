
 # 🖐️ GestureOS – AI-Powered Air Writing & Hand Gesture Control

GestureOS is a real-time computer vision application that allows users to interact with a computer using hand gestures.

The project uses a webcam to detect hand landmarks and track the user's index finger. The tracked finger can then be used as a virtual pen for writing or drawing in the air.

---

## ✨ Features

- 🖐️ Real-time hand detection
- ☝️ Index finger air writing
- ✌️ Gesture-based erasing
- ✊ Fist gesture for pause
- 🖐️ Open palm detection
- 🎨 Virtual drawing canvas
- 💾 Save air drawings as PNG images
- 🧹 Clear canvas using keyboard
- 📷 Live webcam processing
- 🤖 AI-based hand landmark tracking
- ⚡ Real-time interaction

---

## 🧠 How It Works

The application follows this pipeline:

Webcam
↓
OpenCV
↓
MediaPipe Hand Landmarker
↓
21 Hand Landmarks
↓
Gesture Recognition
↓
Virtual Canvas
↓
Air Writing / Erasing

The index fingertip is tracked in real time and its coordinates are used to draw a virtual line on the camera feed.

---

## 🎮 Gesture Controls

| Gesture | Action |
|--------|--------|
| ☝️ Index Finger | Air Writing |
| ✌️ Peace Gesture | Eraser |
| ✊ Fist | Pause Writing |
| 🖐️ Open Palm | Ready Mode |
| `C` | Clear Canvas |
| `S` | Save Drawing |
| `Q` / `ESC` | Exit |

---

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- Computer Vision

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/GestureOS-Air-Writing.git
