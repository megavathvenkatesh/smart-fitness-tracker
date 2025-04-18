💪 Smart Fitness Tracker using Pose Estimation
This project is a computer vision-based fitness tracker built using Python, OpenCV, and MediaPipe. It helps users perform and track push-ups, sit-ups, and dumbbell curls in real-time by detecting body posture and counting reps through webcam video.

📹 How It Works
Pose Detection: Uses MediaPipe Pose to detect and track human body landmarks.

Repetition Counting: Tracks body angles using landmark coordinates and counts reps based on movement stages (up ↔ down).

Side View & Front View Detection: Identifies correct camera orientation for each exercise.

Live Feedback: Displays on-screen feedback if the posture is incorrect or incomplete.

Timers: Countdown before each workout and rest sessions between exercises.

🏋️‍♀️ Exercises Supported

Exercise	View Required	Description
Push-ups	Side View	Tracks elbow angle to count reps
Sit-ups	Side View	(To be implemented fully)
Dumbbell Curls	Front View	(To be implemented fully)
🚀 How to Run
Prerequisites
Python 3.7+

OpenCV

MediaPipe

NumPy

Install Dependencies
bash
Copy
Edit
pip install opencv-python mediapipe numpy
Run the App
bash
Copy
Edit
python fitness_tracker.py
The app uses your webcam. Press Q anytime to quit.

📈 Future Improvements
✅ Calorie Estimation: Estimate calories burned based on reps and body weight.

✅ Posture Feedback Enhancements: Add better feedback when form is incorrect.

✅ More Exercises: Add support for squats, jumping jacks, etc.

✅ UI Improvements: Add graphical UI or dashboard.

✅ Performance Metrics: Track sessions over time.


🧠 Built With
OpenCV
MediaPipe
NumPy
