import cv2
import os


def extract_frames(video_path, output_folder="data/video_frames", every_n=60):

    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path) 
    count = 0
    saved = []

    while True:
        success, frame = cap.read()
        if not success:
            break

        if count % every_n == 0:
            frame_path = os.path.join(output_folder, f"frame_{count}.jpg")
            cv2.imwrite(frame_path, frame)
            saved.append(frame_path)

        count += 1

    cap.release()
    return saved
