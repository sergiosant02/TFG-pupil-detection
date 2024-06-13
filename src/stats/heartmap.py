import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from database.database_service import DatabaseService
from tkinter import *
import pyautogui

class HeartmapGenerator:
    def __init__(self):
        self.database_service = DatabaseService()
        self.load_coordenates()
        self.data = pd.DataFrame({'x': self.x_coords, 'y': self.y_coords})
        self.width, self.height = pyautogui.size()

    def generate_heatmap(self, bw_adjust=0.5, cmap='hot', title='Mapa de Calor Suavizado de Coordenadas'):
        plt.figure(figsize=(10, 8))
        kdeplot = sns.kdeplot(x=self.data['x'], y=self.data['y'], cmap=cmap, fill=True, bw_adjust=bw_adjust)
        plt.xlim(0, self.data['x'].max())
        plt.ylim(0, self.data['y'].max())

        plt.xlim(0, self.width)
        plt.ylim(self.height, 0)
        plt.gca().set_aspect('equal', adjustable='box')

        colorbar = plt.colorbar(kdeplot.collections[0], ax=kdeplot.axes, orientation='horizontal', pad=0.1)
        colorbar.set_label('Densidad')

        plt.title(title)
        plt.xlabel('X')
        plt.ylabel('Y')

        plt.show()

    def load_coordenates(self):
        coordenates = self.database_service.get_inferred_points()
        self.x_coords = [i[0] for i in coordenates]
        self.y_coords = [i[1] for i in coordenates]


