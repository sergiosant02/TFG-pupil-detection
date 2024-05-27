import cv2
import numpy as np
from face_mesh_detector import FaceEyeMeshDetector
from pupile_detector import PupileDetector

class Detection:
    """
    This class detects the face and the eyes, then processes that information to pass it to face_mesh_detector,
    with the purpose of finding the key points of the eye, to be used in conjunction with detectionClass.
    """
    def __init__(self, ui_control):
        self.ui_control = ui_control
        self.detector_params = cv2.SimpleBlobDetector_Params()
        self.detector_params.filterByArea = True
        self.detector_params.maxArea = 1500
        self.detector = cv2.SimpleBlobDetector_create(self.detector_params)

        self.eye_left_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_lefteye_2splits.xml")
        self.eye_right_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_righteye_2splits.xml")
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def detect_faces(self, img):
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        min_size = (round(gray_frame.shape[0] * 0.1), round(gray_frame.shape[1] * 0.1)) 
        coords = self.face_cascade.detectMultiScale(gray_frame, 1.3, 5, minSize=min_size)
        biggest = None
        max_area = 0
        for (x, y, w, h) in coords:
            if w * h > max_area:
                biggest = (x, y, w, h)
                max_area = w * h
        if biggest is not None:
            x, y, w, h = biggest
            gray_frame = gray_frame[y:y + h, x:x + w]
            frame = img[y:y + h, x:x + w]
            frame = self.detect_eyes(frame, gray_frame)
            cv2.rectangle(img, (x, y + h), (x + w, y), (0, 0, 0), 2)
            self.ui_control.face_frame = img
        return img

    def detect_eyes(self, frame, gray):
        dimension = gray.shape
        gray_left = gray[:dimension[0] // 2, dimension[1] // 2:]
        gray_right = gray[:dimension[0] // 2, :dimension[1] // 2]
        left_eye_loc = self.eye_left_cascade.detectMultiScale(gray_left)
        right_eye_loc = self.eye_right_cascade.detectMultiScale(gray_right)
        # FacemeshDetector se crea fuera del bucle
        facemesh_detector = FaceEyeMeshDetector(frame)
        facemesh_detector.visualize()
        for (x, y, w, h) in left_eye_loc:
            cv2.rectangle(frame, (x + dimension[1] // 2, y + h * 1 // 3), (x + w + dimension[1] // 2, y + h),
                          (0, 255, 0), 2)
            left_eye_image = frame[y + h * 1 // 3:y + h, x + dimension[1] // 2:x + w + dimension[1] // 2]
        for (x, y, w, h) in right_eye_loc:
            cv2.rectangle(frame, (x, y + h * 1 // 3), (x + w, y + h), (255, 0, 0), 2)
            right_eye_image = frame[y + h * 1 // 3:y + h, x:x + w]
        if right_eye_image is not None and left_eye_image is not None:
            pictures = [right_eye_image, left_eye_image, frame]
            self.ui_control.right_eye_frame = cv2.resize(pictures[0], (self.ui_control.secundary_width,
                                                                        self.ui_control.secundary_height))
            self.ui_control.left_eye_frame = cv2.resize(pictures[1], (self.ui_control.secundary_width,
                                                                       self.ui_control.secundary_height))
            pupile_detector = PupileDetector(right_eye_image, left_eye_image, frame, self.ui_control)
            pupile_detector.detect()
        else:
            self.ui_control.left_eye_frame = None
            self.ui_control.right_eye_frame = None
        return frame

    def main(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if frame is not None and frame.any():
                frame = self.detect_faces(img=frame)
                if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        cap.release()
        cv2.destroyAllWindows()

    def start(self, frame):
        if frame is not None and frame.any():
            frame = self.detect_faces(img=frame)
