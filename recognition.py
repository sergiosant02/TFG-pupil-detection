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

def face_recognition_process(name: str):
    image = face_recognition.load_image_file(name)
    face_locations = face_recognition.face_locations(image)
    frame = cv2.imread(name)
    print(face_locations)
    for (top,right,bottom,left) in face_locations:
        cv2.rectangle(frame, (left, top), (right , bottom), (0, 0, 255), 2)
        frame = frame[top:bottom, left:right]
        detect_eyes(name, frame)
    #cv2.imshow(name, frame)
    return frame

def detect_eyes(name, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dimension = gray.shape
    gray_right = gray.copy()
    gray_left = gray.copy()
    gray_left = gray_left[:dimension[0]//2, dimension[1]//2:]
    gray_right = gray_right[:dimension[0]//2, :dimension[1]//2]
    
    left_eye_loc = eye_left_cascade.detectMultiScale(gray_left)
    right_eye_loc = eye_right_cascade.detectMultiScale(gray_right)
    for (x, y, w, h) in left_eye_loc:
        cv2.rectangle(frame, (x + dimension[1]//2, y), (x + w + dimension[1]//2, y + h), (0, 255, 0), 2)
        left_eye_image = frame[y:y+h, x+dimension[1]//2:x+w+dimension[1]//2]
        left_edge = apply_canny_filter(left_eye_image)
    for (x, y, w, h) in right_eye_loc:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        right_eye_image = frame[y:y+h, x:x+w]
        right_edge = apply_canny_filter(right_eye_image)
    
    pictures = [gray_right, gray_left, right_eye_image, left_eye_image, right_edge, left_edge, frame]


    detect_pupil(pictures=pictures, name="prueba")
    
    return pictures

def detect_pupil_on_eye(gray):

    _, img = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    img = cv2.erode(img, None, iterations=2) 
    img = cv2.dilate(img, None, iterations=4) 
    img = cv2.medianBlur(img, 5) 
    keypoints = detector.detect(img)
    return keypoints

def detect_pupil(pictures:list, name):
    gray_right, gray_left, right_eye_image, left_eye_image, right_edge, left_edge, frame = pictures
    keypoints: set = detect_pupil_on_eye(gray_right)
    keypoints_left = []
    for keypoint in detect_pupil_on_eye(gray_left):
        keypoint.pt = (keypoint.pt[0] + gray_right.shape[1], keypoint.pt[1])
        keypoints_left.append(keypoint)

    keypoints = keypoints + tuple(keypoints_left)
    print('keypoints: ',keypoints)
    if len(keypoints) > 0:
        print("encontrado")
        for i in keypoints:
            print(i.pt, i.size)
        cv2.drawKeypoints(frame, keypoints, frame, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imshow('my image', gray_right)
        cv2.imshow('my image color', frame)
    else:
        cv2.imshow('gray right', frame)
    

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
    circle_detection(gray, frame, edges)
    return edges

def circle_detection(gray, color, canny): 
    circles = cv2.HoughCircles(
    gray, cv2.HOUGH_GRADIENT, dp=1, minDist=60, param1=200, param2=20, minRadius=0, maxRadius=0
    )
    print('circle:', circles)
    # Dibujar los círculos detectados
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            cv2.circle(color, center, 3, (0, 255, 255), -1)
            cv2.circle(color, center, radius, (0, 0, 255), 1)

        # Calcular la transformada de distancia
        dt = cv2.distanceTransform(255 - (canny > 0).astype(np.uint8), cv2.DIST_L2, 3)

        # Probar para semi-círculos
        minInlierDist = 2.0
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]

            inlier = 0
            maxInlierDist = max(radius / 25.0, minInlierDist)

            for t in np.arange(0, 2 * np.pi, 0.1):
                counter += 1
                cX = int(radius * np.cos(t) + i[0])
                cY = int(radius * np.sin(t) + i[1])

                if dt[cY, cX] < maxInlierDist:
                    inlier += 1
                    cv2.circle(color, (cX, cY), 3, (0, 255, 0))
                else:
                    cv2.circle(color, (cX, cY), 3, (255, 0, 0))

            print(f"{100.0 * inlier / counter}% of a circle with radius {radius} detected")

        # Mostrar la imagen resultante
        cv2.namedWindow("output")
        cv2.imshow("output", color)
    
def main():
    
    #face_recognition_process("positions/picture1.jpg")
    #face_recognition_process("positions/picture2.jpg")
    #face_recognition_process("positions/picture3.jpg")
    face_recognition_process("positions/picture4.jpg")
    #face_recognition_process("positions/picture5.jpg")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()