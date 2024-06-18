import sqlite3
import datetime

class DatabaseService:

    def __init__(self):
        print("Database started")
        self.conn = sqlite3.connect('pupil_database.db')
        self.cursor = self.conn.cursor()
        self.init_tables()

    def init_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS AccuracyTest (id INTEGER PRIMARY KEY, timestamp DATETIME, tarjet_point_x INTEGER, tarjet_point_y INTEGER, points_calculated_len INTEGER, average_point_x INTEGER, average_point_y INTEGER, average_error_angle REAL)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS InferredPoints (id INTEGER PRIMARY KEY, timestamp DATETIME, point_x INTEGER, point_y INTEGER)""")
        self.conn.commit()

    def insert_inferred_point(self, point):
        timestamp = datetime.datetime.now()
        self.cursor.execute("""INSERT INTO InferredPoints (timestamp, point_x, point_y) VALUES (?,?,?)""", (timestamp, point[0], point[1]))
        self.conn.commit()

    def insert_accuracy_test(self, tarjet_point, points_calculated, average_point, average_error_angle):
        timestamp = datetime.datetime.now()
        self.cursor.execute("""INSERT INTO AccuracyTest (timestamp, tarjet_point_x, tarjet_point_y, points_calculated_len, average_point_x, average_point_y, average_error_angle) VALUES (?,?,?,?,?,?,?)""", (timestamp, tarjet_point[0], tarjet_point[1], len(points_calculated), average_point[0], average_point[1], average_error_angle))
        self.conn.commit()

    def get_inferred_points(self):
        self.cursor.execute("""SELECT point_x, point_y FROM InferredPoints""")
        return self.cursor.fetchall()
    
    def get_inferred_points_count(self):
        self.cursor.execute("""SELECT count(*) FROM InferredPoints""")
        return self.cursor.fetchone()[0]