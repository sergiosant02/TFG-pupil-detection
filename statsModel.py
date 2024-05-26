import pandas as pd
import datetime
import os
import pyautogui
import math


class RecordModel:

    def __init__(self, point, recorded: list) -> None:
        self.point = point
        self.recorded = recorded if recorded is not None else []
        self.view_distance = 60
        self.width, self.height = pyautogui.size()
        self.screen_width_cm = 52.7
        self.screen_height_cm = 29.6

    def calculate_average_point(self):
        if len(self.recorded) > 0:
            self.average_point = (sum([i[0] for i in self.recorded]) / len(self.recorded), sum([i[1] for i in self.recorded]) / len(self.recorded))
    
    def calculate_error(self):
        if len(self.recorded) > 0:
            self.calculate_average_point()
            self.error = (abs(self.average_point[0] - self.point[0]), abs(self.average_point[1] - self.point[1]))

    def get_point_str(self, point):
        return f"({point[0]:.3f}, {point[1]:.3f})"

    def generate_line(self):
        if len(self.recorded) > 0:
            self.calculate_error()
            points_str = ", ".join([self.get_point_str(i) for i in self.recorded])
            pixel_size_x = self.screen_width_cm / self.width
            pixel_size_y = self.screen_height_cm / self.height
            difference_x_cm = self.error[0] * pixel_size_x 
            difference_y_cm = self.error[1] * pixel_size_y
            angle_x_rad = math.atan(difference_x_cm / self.view_distance)
            angle_y_rad = math.atan(difference_y_cm / self.view_distance)
            angle_x_deg = math.degrees(angle_x_rad)
            angle_y_deg = math.degrees(angle_y_rad)
            return [f"({self.point[0]}, {self.point[1]})", f"[{points_str}]", f"{len(self.recorded)}", f"{self.get_point_str(self.error)}", f"{angle_x_deg:.3f}", f"{angle_y_deg:.3f}"]
        

class Stats: 

    def __init__(self, records: list[RecordModel]) -> None:
        self.records = records
        self.directory = 'evidences'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def generate_frame(self):
        date = datetime.datetime.now()
        data = {
            'point': [ i.generate_line()[0] for i in self.records],
            'recorded points': [ i.generate_line()[1] for i in self.records],
            'len': [ i.generate_line()[2] for i in self.records],
            'error': [ i.generate_line()[3] for i in self.records],
            'error angle X': [ i.generate_line()[4] for i in self.records],
            'error angle Y': [ i.generate_line()[4] for i in self.records]
        }
        df = pd.DataFrame(data)

        filename = f'errorRegister__{date.timestamp()}.csv'
        save_download = os.path.join(self.directory, filename)
        df.to_csv(save_download, index=False)
        print(f"Evidence recorded: {filename}")