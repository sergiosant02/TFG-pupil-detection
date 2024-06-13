
import cv2

class PupileDetector:

    def __init__(self, right_eye, left_eye, frame, ui_control):
        self.right_eye = right_eye
        self.left_eye = left_eye
        self.frame = frame
        self.ui_control = ui_control

        self.detector_params = cv2.SimpleBlobDetector_Params()
        self.detector_params.filterByArea = True
        self.detector_params.maxArea = 1500
        self.detector = cv2.SimpleBlobDetector_create(self.detector_params)

    def detect_pupil_on_eye(self, img_original):
        gray_frame = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(gray_frame, self.ui_control.threshold, 255, cv2.THRESH_BINARY)
        img = cv2.erode(img, None, iterations=3) 
        img = cv2.dilate(img, None, iterations=5) 
        img = cv2.medianBlur(img, 5) 
        keypoints = self.detector.detect(img) 
        if len(keypoints) > 1: # To avoid false positives
            t = max(keypoints, key=lambda x: x.size)
            keypoints = [t]
        if len(keypoints) > 0:
            center = (int(keypoints[0].pt[0]), int(keypoints[0].pt[1]))
            cv2.circle(img_original, center, 1, (255,0,0), cv2.FILLED)
        return keypoints

    def detect(self):
        keypoints = self.detect_pupil_on_eye(self.right_eye) 
        keypoints_left = self.detect_pupil_on_eye(self.left_eye)
        if len(keypoints) > 0: 
            self.right_eye = cv2.drawKeypoints(self.right_eye, keypoints, self.right_eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        if len(keypoints_left) > 0:
            self.left_eye = cv2.drawKeypoints(self.left_eye, keypoints_left, self.left_eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)