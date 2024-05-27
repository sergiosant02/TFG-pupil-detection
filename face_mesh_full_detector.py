from cvzone.FaceMeshModule import FaceMeshDetector
import cv2
from pupile_detector import PupileDetector

class FaceFullMeshDetector:
    """
    This class has the objective of recognizing eyes and faces, it is an alternative to detection using openCV and its models, 
    since it gives a much better result.
    """
    def __init__(self, ui_control):
        self.cap = cv2.VideoCapture(0)
        self.detector = FaceMeshDetector(maxFaces=1)
        self.radius = 2
        self.color = (0, 0, 255)
        self.image = None
        self.ui_control = ui_control
        self.pupile_detector = None

    def generate_rectangle_coordenates(self, center_up, external_point, center_down):
        left_corner = (center_up[0] - (center_up[0] - external_point[0] + 5), center_up[1] - 5)
        right_corner = (center_up[0] + (center_up[0] - external_point[0] + 5), center_down[1] + 5)
        return left_corner, right_corner

    def visualize(self, image):
        if image is not None:
            self.image = image
            img, faces = self.detector.findFaceMesh(self.image, draw=False)
            for face in faces:
                left_eye1 = face[382]
                cv2.circle(img, (left_eye1[0], left_eye1[1]), self.radius, self.color, cv2.FILLED)
                left_eye2 = face[263]
                cv2.circle(img, (left_eye2[0], left_eye2[1]), self.radius, self.color, cv2.FILLED)

                right_eye1 = face[33]
                cv2.circle(img, (right_eye1[0], right_eye1[1]), self.radius, self.color, cv2.FILLED)

                right_eye2 = face[155]
                cv2.circle(img, (right_eye2[0], right_eye2[1]), self.radius, self.color, cv2.FILLED)     

                eye_up_right = face[158]
                cv2.circle(img, (eye_up_right[0], eye_up_right[1]), self.radius, self.color, cv2.FILLED)

                eye_down_right = face[144]
                cv2.circle(img, (eye_down_right[0], eye_down_right[1]), self.radius, self.color, cv2.FILLED)

                eye_up_left = face[385]
                cv2.circle(img, (eye_up_left[0], eye_up_left[1]), self.radius, self.color, cv2.FILLED)

                eye_down_left = face[373]
                cv2.circle(img, (eye_down_left[0], eye_down_left[1]), self.radius, self.color, cv2.FILLED)

                right_center = (((right_eye2[0] + right_eye1[0])//2 + (eye_up_right[0] + eye_down_right[0])//2)//2, ((right_eye2[1] + right_eye1[1])//2 + (eye_up_right[1] + eye_down_right[1])//2)//2)
                cv2.circle(img, right_center, self.radius, self.color, cv2.FILLED) 

                left_center = (((left_eye2[0] + left_eye1[0]) // 2 + (eye_up_left[0] + eye_down_left[0]) // 2) // 2, ((left_eye2[1] + left_eye1[1]) // 2 + (eye_up_left[1] + eye_down_left[1]) // 2) // 2)
                cv2.circle(img, left_center, self.radius, self.color, cv2.FILLED)

                right_eye_left_corner, right_eye_right_corner  = self.generate_rectangle_coordenates(eye_up_right, right_eye1, eye_down_right)
                right_eye_crop = img[right_eye_left_corner[1]:right_eye_right_corner[1],  right_eye_left_corner[0]:right_eye_right_corner[0]]
                self.ui_control.right_eye_frame = right_eye_crop
                left_eye_left_corner, left_eye_right_corner  = self.generate_rectangle_coordenates(eye_up_left, left_eye1, eye_down_left)
                left_eye_crop = img[left_eye_left_corner[1]:left_eye_right_corner[1],  left_eye_left_corner[0]:left_eye_right_corner[0]]
                self.ui_control.left_eye_frame = left_eye_crop
                self.pupile_detector = PupileDetector(right_eye=right_eye_crop, left_eye=left_eye_crop, frame=self.image, ui_control=self.ui_control)
                self.pupile_detector.detect()

            self.ui_control.face_frame = image

