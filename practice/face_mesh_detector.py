from cvzone.FaceMeshModule import FaceMeshDetector
import cv2

class FaceEyeMeshDetector:
    """
    This class is intended to recognize the eyes, to be used in conjunction with detectionClass
    """
    def __init__(self, image):
        self.detector = FaceMeshDetector(maxFaces=1)
        self.radius = 1
        self.color = (0, 0, 255)
        self.image = image

    def visualize(self):
        img, faces = self.detector.findFaceMesh(self.image, draw=False)
        for face in faces:
            izq1 = face[382]
            cv2.circle(img, (izq1[0], izq1[1]), self.radius, self.color, cv2.FILLED)
            izq2 = face[263]
            cv2.circle(img, (izq2[0], izq2[1]), self.radius, self.color, cv2.FILLED)

            left_center = ((izq2[0] + izq1[0])//2, (izq2[1] + izq1[1])//2)

            cv2.circle(img, left_center, self.radius, self.color, cv2.FILLED)

            der1 = face[33]
            cv2.circle(img, (der1[0], der1[1]), self.radius, self.color, cv2.FILLED)

            der2 = face[155]
            cv2.circle(img, (der2[0], der2[1]), self.radius, self.color, cv2.FILLED)

            right_center = ((der2[0] + der1[0])//2, (der2[1] + der1[1])//2)

            cv2.circle(img, right_center, self.radius, self.color, cv2.FILLED)            

        