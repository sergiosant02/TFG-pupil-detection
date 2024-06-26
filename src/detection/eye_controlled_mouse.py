import cv2
import mediapipe as mp
import numpy as np
import pyautogui
from control.mouse_control import MouseControl
from detection.interpolate2D import InterpolatePixelTarget
import time
from stats.statsModel import RecordModel,Stats
from database.database_service import DatabaseService

class EyeControlledMouse:


    def __init__(self, controller):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        self.screen_w, self.screen_h = pyautogui.size()
        self.controller = controller
        self.radius = 1
        self.color = (0, 0, 255)
        self.new_left_center = None
        self.new_right_center = None
        self.mouse_control = MouseControl()
        self.interpolator = None
        self.decimal_precision = 3
        self.time_reference = 0
        self.laps = 2
        self.records: list[RecordModel] = []
        self.record: RecordModel = None
        self.flag = False
        self.min_close = 0.015
        self.database_service = DatabaseService()

    def get_coordenates_decimal(self, index):
        return (self.landmarks[index].x * self.frame_w, self.landmarks[index].y * self.frame_h)

    def convert_coordenate(self, index):
        return (int(self.landmarks[index].x * self.frame_w), int(self.landmarks[index].y * self.frame_h))
    
    def draw_eye_limits(self, frame):
        self.left_eye1 = self.convert_coordenate(33)
        left_eye2 = self.convert_coordenate(155)
        self.right_eye1 = self.convert_coordenate(362)
        self.right_eye1_decimal = self.get_coordenates_decimal(362)
        right_eye2 = self.convert_coordenate(263)
        self.right_eye2_decimal = self.get_coordenates_decimal(263)
        self.eye_up_right = self.convert_coordenate(385)
        self.eye_up_right_decimal = self.get_coordenates_decimal(385)
        self.eye_down_right = self.convert_coordenate(373)
        self.eye_down_right_decimal = self.get_coordenates_decimal(373)
        self.eye_up_left = self.convert_coordenate(158)
        self.eye_down_left = self.convert_coordenate(144)
        self.right_center = ((right_eye2[0] + self.right_eye1[0])//2, (self.eye_up_right[1] + self.eye_down_right[1])//2 )
        self.right_center_decimal = ((self.right_eye2_decimal[0] + self.right_eye1_decimal[0])/2 , (self.eye_up_right[1] + self.eye_down_right[1])/2 )
        self.left_center = (((left_eye2[0] + self.left_eye1[0]) // 2 + (self.eye_up_left[0] + self.eye_down_left[0]) // 2) // 2, ((left_eye2[1] + self.left_eye1[1]) // 2 + (self.eye_up_left[1] + self.eye_down_left[1]) // 2) // 2)

    def draw_eye_center(self, frame):
        self.left_pupile = self.convert_coordenate(468)
        self.right_pupile = self.convert_coordenate(473)
        cv2.circle(frame, self.left_pupile, 1, (0, 255, 255))
        cv2.circle(frame, self.right_pupile, 1, (0, 0, 255))

        right_eye_landmarks = [self.landmarks[i] for i in [362,398,384,385,386,387,388,466,263,381,380,374,373,390,249]]
        for i in right_eye_landmarks:
            cv2.circle(frame, (int(self.frame_w*i.x), int(self.frame_h*i.y)), 1, (255, 255, 255))
        eye_x = sum([lm.x for lm in right_eye_landmarks]) / len(right_eye_landmarks)
        eye_y = sum([lm.y for lm in right_eye_landmarks]) / len(right_eye_landmarks)
        screen_x = self.frame_w * eye_x
        screen_y = self.frame_h * eye_y
        self.new_center = [int(screen_x)//1,int(screen_y)//1]
        cv2.circle(frame, self.new_center, 1, (0, 255, 255))


    def calculate_correction(self):
        print(f"Para calcular la correción ---- right pupile: {self.right_pupile} ---- right center: {self.right_center}")
        self.controller.set_correction('left', tuple(x - y for x, y in zip(self.left_pupile, self.left_center)))
        self.controller.set_correction('right', tuple(x - y for x, y in zip(self.right_pupile, self.right_center)))
        self.new_left_center = tuple(x + y for x, y in zip(self.controller.get_correction('left'), self.left_center))
        self.new_right_center = tuple(x + y for x, y in zip(self.controller.get_correction('right'), self.right_center))
        
    def generate_rectangle_coordenates(self, center_up, external_point, center_down):
        left_corner = (center_up[0] - (center_up[0] - external_point[0] + 5), center_up[1] - 5)
        right_corner = (center_up[0] + (center_up[0] - external_point[0] + 12), center_down[1] + 5)
        return left_corner, right_corner

    def run(self, frame):
        if frame is not None:
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output = self.face_mesh.process(rgb_frame)
            landmark_points = output.multi_face_landmarks
            self.frame_h, self.frame_w, _ = frame.shape
            if landmark_points:
                self.landmarks = landmark_points[0].landmark
                for id, landmark in enumerate(self.landmarks[474:478]):
                    x = int(landmark.x * self.frame_w)
                    y = int(landmark.y * self.frame_h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 0))
                left = [self.landmarks[145], self.landmarks[159]]
                right = [self.landmarks[374], self.landmarks[386]]
                self.draw_eye_center(frame)
                self.draw_eye_limits(frame)
                if self.controller.get_correction('left') is not None and self.controller.get_correction('right') is not None:
                    self.new_left_center = tuple(x + y for x, y in zip(self.controller.get_correction('left'), self.left_center))
                    self.new_right_center = tuple(x + y for x, y in zip(self.controller.get_correction('right'), self.right_center))
                if self.new_right_center is not None and self.new_right_center is not None:
                    cv2.circle(frame, self.new_left_center, 2, (255, 0, 255), cv2.FILLED)
                    cv2.circle(frame, self.new_right_center, 2, (255, 0, 255), cv2.FILLED)
                for landmark in left:
                    x = int(landmark.x * self.frame_w)
                    y = int(landmark.y * self.frame_h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 255))

                if len(self.controller.get_coordenates()) >= (9 * self.laps) and ((left[0].y - left[1].y) < self.min_close and not self.controller.get_use_both_eyes()) and not (right[0].y - right[1].y) < self.min_close:  # Abierto solo derecho
                    self.get_curent_absolute_move()
                    if self.controller.get_test_index() != None:
                        self.record.recorded.append(self.mouse_control.get_current_position())
                        self.flag = True

                if len(self.controller.get_coordenates()) >= (9 * self.laps) and ((left[0].y - left[1].y) > self.min_close and self.controller.get_use_both_eyes()) and not (right[0].y - right[1].y) < self.min_close:  # Abierto solo derecho
                    self.get_curent_absolute_move()
                    if self.controller.get_test_index() != None:
                        self.record.recorded.append(self.mouse_control.get_current_position())
                        self.flag = True
                
                if len(self.controller.get_coordenates()) >= (9 * self.laps) and (right[0].y - right[1].y) < self.min_close and self.time_reference == 0: # Parpadeo derecho inicio contador
                    self.time_reference = time.time()
                
                if len(self.controller.get_coordenates()) >= (9 * self.laps) and (right[0].y - right[1].y) > self.min_close and self.time_reference > 0: # Parpadeo derecho opciones
                    current_time = time.time()
                    if current_time -self.time_reference > 0.05 and current_time - self.time_reference <= 1:
                        self.mouse_control.click()
                        self.time_reference = 0
                    elif current_time - self.time_reference > 1:
                        self.mouse_control.right_click()
                        self.time_reference = 0

                
                if len(self.controller.get_coordenates()) >= (9 * self.laps) and ((left[0].y - left[1].y) > self.min_close and (right[0].y - right[1].y) > self.min_close): # Alguno de los ojos abiertos
                    if self.flag:
                        self.controller.add_test()
                        self.flag = False   

                if len(self.controller.get_coordenates()) >= (9 * self.laps) and ((left[0].y - left[1].y) < self.min_close and (right[0].y - right[1].y) > self.min_close) and self.controller.get_use_both_eyes(): # Alguno de los ojos abiertos
                    if self.flag:
                        self.controller.add_test()
                        self.flag = False 
                        
                self.controller.set_face_frame(frame)
                right_eye_left_corner, right_eye_right_corner  = self.generate_rectangle_coordenates(self.eye_up_right, self.right_eye1, self.eye_down_right)
                right_eye_crop = frame[right_eye_left_corner[1]:right_eye_right_corner[1],  right_eye_left_corner[0]:right_eye_right_corner[0]]
                self.controller.set_right_eye_frame(right_eye_crop)
                left_eye_left_corner, left_eye_right_corner  = self.generate_rectangle_coordenates(self.eye_up_left, self.left_eye1, self.eye_down_left)
                left_eye_crop = frame[left_eye_left_corner[1]:left_eye_right_corner[1],  left_eye_left_corner[0]:left_eye_right_corner[0]]
                self.controller.set_left_eye_frame(left_eye_crop)

    
    def log_next_coordenate(self):
        if len(self.controller.get_coordenates()) >= (9 * self.laps) - 1:
            self.controller.execute_check_nineth_coordinate()
        if len(self.controller.get_coordenates()) < (9 * self.laps):
            self.interpolator = None
            right_pupile_decimal = self.get_coordenates_decimal(473)
            coordenate = tuple(round(x - y, self.decimal_precision)for x, y in zip(self.new_center, right_pupile_decimal))
            print(f"self.eye_down_right: {self.eye_down_right}, right_pupile_decimal: {right_pupile_decimal}")
            self.controller.get_coordenates().append(coordenate)
            print(f'coordenate register: {coordenate}')

            self.controller.get_labels()[(len(self.controller.get_coordenates())-1)%9].configure(text=f"({coordenate[0]:.3f}, {coordenate[1]:.3f})")
        

    def get_curent_absolute_move(self):
        if self.interpolator is None:
            self.interpolator = InterpolatePixelTarget(self.controller)
        right_pupile_decimal = self.get_coordenates_decimal(473)
        coordenate = tuple(round(x - y, self.decimal_precision) for x, y in zip(self.new_center, right_pupile_decimal))
        next_position_decimal = self.interpolator.interpolate_move(coordenate)
        if np.all(np.isfinite(next_position_decimal)):
            print("next_position_decimal: ", next_position_decimal)
            next_position = (int(next_position_decimal[0]), int(next_position_decimal[1]))
            self.database_service.insert_inferred_point(next_position)
            print("next_position: ", next_position)
            self.mouse_control.absolute_move(next_position)

    def add_test(self):
        if self.controller.get_test_index() == 0:
            self.controller.update_current_test_point()
            self.record = RecordModel(self.controller.get_test_point(), None)
        elif self.controller.get_test_index() != None and self.controller.get_test_index() > 0 and self.controller.get_test_index() < len(self.controller.get_test_points()):
            self.records.append(self.record)
            self.record = RecordModel(self.controller.get_test_point(), None)
        else:
            self.records.append(self.record)
            self.save_test_results()
            self.reset_test()


    def save_test_results(self):
        stats: Stats = Stats(self.records)
        stats.generate_frame()

    def reset_test(self):
        self.record = None
        self.records = []
    
