# 🎨 Universal Color Distance Tracker

A Computer Vision application built with **Pure OpenCV** that detects specific colored objects and calculates the real-time distance between them in centimeters (cm). Features a built-in interactive GUI to dynamically toggle target colors without restarting the program.

## ✨ Features
- **Pure OpenCV Approach:** Zero dependencies on heavy Machine Learning models (like MediaPipe), ensuring 100% compatibility and stability across newer Python versions (including Python 3.13).
- **Interactive GUI (Trackbars):** Dynamically toggle up to 10 distinct colors (Blue, Orange, Red, Green, Yellow, Purple, Pink, Brown, White, Black) on the fly.
- **Smart Tracking:** Automatically isolates and tracks the two largest objects among the selected colors to reduce background noise.
- **Real-Time Measurement:** Calculates Euclidean distance and accurately converts pixels to centimeters.
- **Low Latency:** Highly optimized to run smoothly on standard local hardware.

## 🛠️ Tech Stack
- **Python** - **OpenCV** (`opencv-python`) - For image processing, masking, and GUI.
- **NumPy** - For matrix operations and color range array definitions.
- **Math** - For Euclidean distance calculations.

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/username-kamu/color-distance-tracker.git](https://github.com/username-kamu/color-distance-tracker.git)
   cd color-distance-tracker
