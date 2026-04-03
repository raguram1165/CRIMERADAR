"""
RedShield AI — CCTV Intelligent Detection System
Features:
  - Live webcam feed
  - Motion detection using background subtraction
  - Crowd density estimation
  - Alert on suspicious activity
  - Save snapshots on detection

Run: python cctv_detection.py
Press 'q' to quit | 's' to save snapshot | 'r' to reset background
"""

import cv2
import numpy as np
import datetime
import os

print("🎥 RedShield CCTV Detection System Starting...")
print("Controls: [Q] Quit | [S] Save Snapshot | [R] Reset Background Model")

os.makedirs("cctv_snapshots", exist_ok=True)

# Initialize video capture (0 = webcam, or use video file path)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not found. Using demo mode with test video pattern.")
    # Create a demo window showing the system is ready
    demo_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(demo_frame, "RedShield CCTV System", (120, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 100), 2)
    cv2.putText(demo_frame, "No camera detected", (160, 260),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
    cv2.putText(demo_frame, "Connect a webcam and restart", (100, 320),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 255), 1)
    cv2.imshow("RedShield CCTV", demo_frame)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()
    exit()

# Background subtractor for motion detection
bg_subtractor = cv2.createBackgroundSubtractorMOG2(
    history=500, varThreshold=50, detectShadows=True
)

alert_count = 0
frame_count = 0
snapshot_count = 0

print("✅ Camera feed started. Monitoring for suspicious activity...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Apply background subtraction
    fg_mask = bg_subtractor.apply(frame)

    # Remove shadows (gray pixels → black)
    _, fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)

    # Morphological cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    fg_mask = cv2.dilate(fg_mask, kernel, iterations=2)

    # Find contours (moving objects)
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_count = 0
    alert = False

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1500:  # Filter small noise
            x, y, w, h = cv2.boundingRect(contour)
            motion_count += 1

            # Color based on size (large object = suspicious)
            if area > 8000:
                color = (0, 0, 255)   # Red = high alert
                alert = True
            elif area > 4000:
                color = (0, 165, 255) # Orange = medium
            else:
                color = (0, 255, 0)   # Green = low

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"Motion ({int(area)})", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    # Alert triggered
    if alert:
        alert_count += 1
        cv2.putText(frame, "⚠ ALERT: SUSPICIOUS ACTIVITY", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        # Red border flash every other frame
        if alert_count % 2 == 0:
            cv2.rectangle(frame, (0, 0), (frame.shape[1]-1, frame.shape[0]-1), (0, 0, 255), 5)

        # Auto-save snapshot on new alert
        if alert_count % 30 == 1:
            snap_path = f"cctv_snapshots/alert_{snapshot_count:04d}_{datetime.datetime.now().strftime('%H%M%S')}.jpg"
            cv2.imwrite(snap_path, frame)
            print(f"📸 Alert snapshot saved: {snap_path}")
            snapshot_count += 1

    # Crowd density
    density = "CLEAR" if motion_count == 0 else "LOW" if motion_count < 3 else "MEDIUM" if motion_count < 6 else "HIGH"
    density_color = (0, 255, 0) if density == "CLEAR" else (0, 165, 255) if density in ["LOW", "MEDIUM"] else (0, 0, 255)

    # HUD overlay
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (400, 100), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    cv2.putText(frame, f"RedShield CCTV | {timestamp}", (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    cv2.putText(frame, f"Objects: {motion_count} | Density: {density}", (10, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, density_color, 1)
    cv2.putText(frame, f"Alerts: {alert_count} | Frames: {frame_count}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)
    cv2.putText(frame, "[Q] Quit  [S] Snapshot  [R] Reset", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)

    cv2.imshow("RedShield CCTV — AI Detection", frame)

    # Keyboard controls
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("👋 Shutting down CCTV system...")
        break
    elif key == ord('s'):
        snap_path = f"cctv_snapshots/manual_{snapshot_count:04d}.jpg"
        cv2.imwrite(snap_path, frame)
        print(f"📸 Manual snapshot saved: {snap_path}")
        snapshot_count += 1
    elif key == ord('r'):
        bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)
        print("🔄 Background model reset.")

cap.release()
cv2.destroyAllWindows()
print(f"\n📊 Session Summary: {frame_count} frames | {alert_count} alerts | {snapshot_count} snapshots")
