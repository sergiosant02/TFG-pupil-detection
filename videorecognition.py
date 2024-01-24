import face_recognition
from PIL import Image
import cv2
import numpy as np  
from pupil_detectors import Detector2D


detector_params = cv2.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector = cv2.SimpleBlobDetector_create(detector_params)


eye_left_cascade =  cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_lefteye_2splits.xml")
eye_right_cascade =  cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_righteye_2splits.xml")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def detect_faces(img):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
    if len(coords) > 1:
        biggest = (0, 0, 0, 0)
        for i in coords:
            if i[3] > biggest[3]:
                biggest = i
        biggest = np.array([i], np.int32)
    elif len(coords) == 1:
        biggest = coords
    else:
        return None
    for (x, y, w, h) in biggest:
        frame = img[y:y + h, x:x + w]
        frame = detect_eyes("prueba", frame)
    return frame


def detect_eyes(name, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dimension = gray.shape
    
    gray_left = gray[:dimension[0]//2, dimension[1]//2:]
    gray_right = gray[:dimension[0]//2, :dimension[1]//2]
    right_eye_image, left_eye_image = None, None
    left_eye_loc = eye_left_cascade.detectMultiScale(gray_left)
    right_eye_loc = eye_right_cascade.detectMultiScale(gray_right)
    for (x, y, w, h) in left_eye_loc:
        cv2.rectangle(frame, (x + dimension[1]//2, y), (x + w + dimension[1]//2, y + h), (0, 255, 0), 2)
        left_eye_image = frame[y:y+h, x+dimension[1]//2:x+w+dimension[1]//2]
        #left_edge = apply_canny_filter(left_eye_image)
    for (x, y, w, h) in right_eye_loc:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        right_eye_image = frame[y:y+h, x:x+w]
        #right_edge = apply_canny_filter(right_eye_image)
    
    if right_eye_image is not None and left_eye_image is not None:
        pictures = [right_eye_image, left_eye_image, frame]


        frame = detect_pupil(pictures=pictures, name="prueba")
    
    return frame

def detect_pupil_on_eye(img_original):
    gray_frame = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(gray_frame, 8, 255, cv2.THRESH_BINARY)
    img = cv2.erode(img, None, iterations=2) 
    img = cv2.dilate(img, None, iterations=5) 
    img = cv2.medianBlur(img, 5) 
    keypoints = detector.detect(img)
    return keypoints

def detect_pupil(pictures:list, name):
    gray_right, gray_left, frame = pictures
    keypoints: set = detect_pupil_on_eye(gray_right) 
    keypoints_left = detect_pupil_on_eye(gray_left)
    """
    keypoints_left = []
    for keypoint in detect_pupil_on_eye(gray_left):
        keypoint.pt = (keypoint.pt[0] + gray_right.shape[1], keypoint.pt[1])
        keypoints_left.append(keypoint)

    keypoints = keypoints + tuple(keypoints_left)
    """
    if len(keypoints) > 0:
       
        gray_right = cv2.drawKeypoints(gray_right, keypoints, gray_right, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    if len(keypoints_left) > 0:
       
        gray_left = cv2.drawKeypoints(gray_left, keypoints_left, gray_left, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        #cv2.imshow('my image', gray_right)
        #cv2.imshow('my image color', frame)

    return frame
    

def print_pictures(pictures:list, name):
    gray_right, gray_left, right_eye_image, left_eye_image, right_edge, left_edge = pictures
    pad_height = max(gray_right.shape[0], right_edge.shape[0], gray_left.shape[0], left_edge.shape[0])
    pad_width = max(gray_right.shape[1], right_edge.shape[1], gray_left.shape[1], left_edge.shape[1])

    left_edge = cv2.copyMakeBorder(left_edge, 0, pad_height - left_edge.shape[0], 0, pad_width - left_edge.shape[1], cv2.BORDER_CONSTANT, value=0)
    right_edge = cv2.copyMakeBorder(right_edge, 0, pad_height - right_edge.shape[0], 0, pad_width - right_edge.shape[1], cv2.BORDER_CONSTANT, value=0)
    gray_left = cv2.copyMakeBorder(gray_left, 0, pad_height - gray_left.shape[0], 0, pad_width - gray_left.shape[1], cv2.BORDER_CONSTANT, value=0)
    gray_right = cv2.copyMakeBorder(gray_right, 0, pad_height - gray_right.shape[0], 0, pad_width - gray_right.shape[1], cv2.BORDER_CONSTANT, value=0)

    stacked_images = np.hstack((gray_left, gray_right,left_edge, right_edge))
    cv2.imshow(name + " left, right , edge_left, edge_right", stacked_images)

def apply_canny_filter(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 0)
    normalized_image = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    edges = cv2.Canny(normalized_image, 50, 90)
    return edges


    
def main():
    
    #face_recognition_process("positions/picture1.jpg")
    #face_recognition_process("positions/picture2.jpg")
    #face_recognition_process("positions/picture3.jpg")
    #face_recognition_process("positions/picture4.jpg")
    #face_recognition_process("positions/picture5.jpg")
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


    while True:
        cap = cv2.VideoCapture(0)

        ret, frame = cap.read()

        if ret and frame is not None and frame.any():
            frame = detect_faces(img=frame)
            if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()