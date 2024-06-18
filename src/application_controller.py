from ui.ui_control import UiControl
from stats.heartmap import HeartmapGenerator
from detection.eye_controlled_mouse import EyeControlledMouse
from database.database_service import DatabaseService
import cv2


class ApplicationController:
    def __init__(self):
        self.ui_control = UiControl(self)
        self.eye_control = EyeControlledMouse(self)
        self.vid = cv2.VideoCapture(0) 
        self.database_service = DatabaseService()
        self.framne = None

    def start(self):
        self.ui_control.start()
        

    def update_mouse_control(self, data):
        self.eye_control.process_new_data(data)

    def update_ui(self, status):
        self.ui_control.display_status(status)


    def open_camera(self):
        _, self.frame = self.vid.read() 
        self.eye_control.run(frame=self.frame)

        

    #################### Methods execution ####################

    def calculate_correction(self):
        self.eye_control.calculate_correction()

    def add_test(self):
        if self.ui_control.is_full_calibrated():
            self.ui_control.add_test()
            self.eye_control.add_test()
        else:
            self.ui_control.show_alert('Aún es pronto', "Necesitas realizar la calibración antes de hacer pruebas, debes realizar dos vueltas a la calibración")

    def reset_test(self):
        self.ui_control.reset_test()
        self.eye_control.reset_test()

    def save_test_results(self):
        self.eye_control.save_test_results()

    def log_next_coordenates(self):
        self.eye_control.log_next_coordenate()

    def execute_check_nineth_coordinate(self):
        self.ui_control.check_nineth_coordinate()


    ##################### GETTERS AND SETTERS #####################


    def get_correction(self, side: str):
        if side == "left":
            return self.ui_control.left_correction
        elif side == "right":
            return self.ui_control.right_correction
        else:
            return None
        
    def set_correction(self, side: str, correction):
        if side == "left":
            self.ui_control.left_correction = correction
        elif side == "right":
            self.ui_control.right_correction = correction
        else:
            return None
        
    def get_right_eye_frame(self):
        return self.ui_control.right_eye_frame
    
    def get_left_eye_frame(self):
        return self.ui_control.left_eye_frame
    
    def get_face_frame(self):
        return self.ui_control.face_frame
    
    def get_test_point(self):
        return self.ui_control.test_point
    
    def get_test_point_box(self):
        return self.ui_control.test_point_box
    
    def get_test_index(self):
        return self.ui_control.test_index
    
    def get_test_points(self):
        return self.ui_control.test_points
    
    def get_coordenates(self):
        return self.ui_control.coordenates
    
    def get_labels(self):
        return self.ui_control.labels
    
    def set_right_eye_frame(self, frame):
        self.ui_control.right_eye_frame = frame

    def set_left_eye_frame(self, frame):
        self.ui_control.left_eye_frame = frame

    def set_face_frame(self, frame):
        self.ui_control.face_frame = frame

    def set_test_point(self, point):
        self.ui_control.test_point = point

    def set_test_point_box(self, box):
        self.ui_control.test_point_box = box

    def set_test_index(self, index):
        self.ui_control.test_index = index

    def set_test_points(self, points):
        self.ui_control.test_points = points

    def set_coordenates(self, coordenates):
        self.ui_control.coordenates = coordenates

    def get_default_coordenates(self):
        return self.ui_control.default_coordenates

    def set_labels(self, labels):
        self.ui_control.labels = labels

    def get_box_size(self):
        return self.ui_control.box_size
    
    def get_threshold(self):
        return self.ui_control.threshold
    
    def get_text_box_increment(self):
        return self.ui_control.text_box_increment
    
    def get_app(self):
        return self.ui_control.app
    
    def get_test_point_box(self):
        return self.ui_control.test_point_box

    def update_current_test_point(self):
        self.ui_control.update_current_test_point()

    def format_text_in_label(self, i: int, text):
      self.ui_control.format_text_in_label(i, text)

    def get_use_both_eyes(self):
        return self.ui_control.use_both_eyes
    
    def show_heartmap(self):
      if self.database_service.get_inferred_points_count() < 1:
          self.ui_control.show_alert("No hay datos", "No hay datos suficientes para calcular el mapa de calor. Aún no se ha usado la aplicación por lo que no hay datos.")
      else:
            heartmap = HeartmapGenerator()
            heartmap.generate_heatmap()