import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
from io import BytesIO
from fastapi import HTTPException

# Initialize MediaPipe face detection module
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Function to perform facial detection and cropping
def process_image(image_data: bytes) -> dict:
    # Convert bytes to OpenCV image
    image_np = np.array(Image.open(BytesIO(image_data)))
    
    # Convert image to RGB (MediaPipe requires RGB input)
    image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

    # Detect faces in the image
    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(image_rgb)
        if not results.detections:
            raise HTTPException(status_code=400, detail="No faces detected")
        
        # Get bounding box of the first detected face
        detection = results.detections[0]
        bboxC = detection.location_data.relative_bounding_box
        ih, iw, _ = image_np.shape

        # Convert bounding box coordinates from relative to absolute
        xmin, ymin, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

        # Crop detected face from the original image
        cropped_image = image_np[ymin:ymin+h, xmin:xmin+w]

        # Draw bounding box and landmarks on the image
        image_rgb.flags.writeable = True
        image_rgb = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_detection(image_rgb, detection)

    # Convert OpenCV image back to bytes
    retval, buffer = cv2.imencode('.jpg', cv2.cvtColor(image_rgb, cv2.COLOR_BGR2RGB))
    image_bytes = buffer.tobytes()

    return {"cropped_image": image_bytes, "facial_landmarks": detection}
