from tkinter import *
from tkinter.ttk import Combobox
import cv2 
from PIL import Image, ImageTk 
from mediapipe_detection import EyeControlledMouse

class UiControl:
   def __init__(self):
      self.app = Tk() 
      self.app.title("Pupil detection")
      self.face_placeholder = Image.open('placeholders/face_placeholder.jpg')
      self.eye_placeholder = Image.open('placeholders/eye_placeholder.png')
      self.face_frame: cv2.Mat = None
      self.left_eye_frame: cv2.Mat = None
      self.right_eye_frame: cv2.Mat = None
      self.width, self.height = self.app.winfo_screenwidth(), self.app.winfo_screenheight() 
      print(self.app.winfo_screenwidth(), self.app.winfo_screenheight())
      self.pictures_space_height = self.height // 2
      self.main_width = self.width
      self.main_height = self.height // 2
      self.secundary_width = self.width // 2
      self.secundary_height = self.height // 4
      self.bottom_height = self.height // 2
      self.threshold = 25
      self.box_size = 5
      self.vid = cv2.VideoCapture(0) 
      self.left_correction = None
      self.right_correction = None
      self.labels = []
      self.coordenates = []
      self.method = "Relativo"
      self.canvas = []
      self.default_coordenates = []

   def check_ninth_coordinate(self):
      if len(self.coordenates) >= 8:
        self.register_button.grid_forget()
        self.reset_button.grid(row=3, columnspan=3, pady=5)
      else:
        self.reset_button.grid_forget()
        self.register_button.grid(row=3, columnspan=3, pady=5)

   def reset_coordenates(self):
      self.coordenates = []
      index = 0
      for i in range(3):
         for j in range(3):
            label_text = f"Coordenada {i*3+j+1}"
            self.labels[index].configure(text=label_text)
            index += 1
      self.check_ninth_coordinate()

   def focus_in_handler(self, event):
      self.app.focus_set()

   def change_method(self, event):
      self.method = event.widget.get()
      print(self.method)

   def setup_ui(self, mediapipe_det: EyeControlledMouse):
      self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, self.main_width) 
      self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, self.main_height) 
      self.generate_default_coordenates()
      self.app.bind('<Escape>', lambda e: self.app.quit()) 
      dimensions = '{}x{}+{}+{}'.format(self.width, self.height, 0, 0)
      self.app.geometry(dimensions)

      # Marco principal para los elementos de la interfaz
      main_frame = Frame(self.app)
      main_frame.pack(fill=BOTH, expand=True)

      # Marco para las fotos
      photos_frame = Frame(main_frame)
      photos_frame.pack(fill=BOTH, expand=True)

      # Etiqueta para la imagen facial
      self.face_label = Label(photos_frame, height=self.main_height, width=self.secundary_width) 
      self.face_label.pack(side=LEFT) 

      # Marco para los ojos
      eyes_frame = Frame(photos_frame)
      eyes_frame.pack(side=LEFT)

      # Etiqueta para el ojo izquierdo
      self.left_eye_label = Label(eyes_frame, height=self.secundary_height, width=self.secundary_width)
      self.left_eye_label.pack()

      # Etiqueta para el ojo derecho
      self.right_eye_label = Label(eyes_frame, height=self.secundary_height, width=self.secundary_width)
      self.right_eye_label.pack()

      # Marco para las pilas horizontales
      horizontal_stack_frame = Frame(main_frame)
      horizontal_stack_frame.pack(fill=BOTH, expand=True)

      # Marco para el slider y el entry
      slider_frame = Frame(horizontal_stack_frame)
      slider_frame.pack(side=LEFT, fill=BOTH, expand=True)

      # Marco para el botón y el label
      button_frame = Frame(horizontal_stack_frame)
      button_frame.pack(side=LEFT, fill=BOTH, expand=True)

      # Marco para los 9 labels
      labels_frame = Frame(horizontal_stack_frame)
      labels_frame.pack(side=LEFT, fill=BOTH, expand=True)

      # Slider y Entry
      threshold_label_info = Label(slider_frame, text="Threshold:")
      threshold_label_info.pack(anchor=W, padx=10)

      self.threshold_box = Entry(slider_frame, width=5)
      self.threshold_box.bind("<KeyRelease>", self.update_threshold_entry)
      self.threshold_box.pack(anchor=W, padx=10)

      self.slider = Scale(slider_frame, from_=0, to=255, orient=HORIZONTAL, command=self.update_threshold_slider)
      self.slider.set(self.threshold)
      self.slider.pack(fill=BOTH, expand=True, padx=10, pady=5)

      # Botón y Label
      self.right_correction_label = Label(button_frame, wraplength=300, justify="left", text="Si desea aplicar una corrección del centro del ojo, para aquellos casos en los que hay una leve diferencia entre el punto azul y el rojo central cuando mira al centro de la pantalla, mire hacia el punto verde y mientras lo hace pulse el botón para corregir")
      self.right_correction_label.pack(fill=BOTH, expand=True, padx=10, pady=5)

      correction_button = Button(button_frame, text="Aplicar corrección", command=mediapipe_det.calculate_correction)
      correction_button.pack(fill=BOTH, expand=True, padx=10, pady=5)

      # Labels adicionales
      for i in range(3):
         for j in range(3):
            label_text = f"Coordenada {i*3+j+1}"
            label = Label(labels_frame, text=label_text, width=15)
            label.grid(row=i, column=j, padx=5, pady=5, sticky=W)
            self.labels.append(label)

      # Botón para registrar la siguiente coordenada
      self.register_button = Button(labels_frame, text="Registrar siguiente coordenada", command=mediapipe_det.log_next_coordenate)
      self.register_button.grid(row=3, columnspan=3, pady=5)
      self.reset_button = Button(labels_frame, text="Reiniciar", command=self.reset_coordenates)
      #self.select_mode = Combobox(labels_frame, values=["Relativo", "Absoluto"], postcommand=self.change_method)
      self.select_mode = Combobox(labels_frame, values=["Relativo", "Absoluto"])
      self.select_mode.set("Relativo")  # Establecer el valor predeterminado
      self.select_mode.bind("<<ComboboxSelected>>", self.change_method)
      self.select_mode.grid(row=4, columnspan=3, pady=5)

      self.generate_default_canvas()


   def update_threshold_slider(self, value):
      self.threshold_box.delete(0, END)
      self.threshold_box.insert(0, value)
      self.threshold = int(value)

   def update_threshold_entry(self, event=None):
      value = self.threshold_box.get()
      if not value.replace(' ', '').isnumeric():
         value = '0'
      value_int = int(value)
      if value_int < 0:
         value_int = 0
      elif value_int > 255:
         value_int = 255
      self.slider.set(value_int)
      self.threshold = value_int
      self.threshold_box.delete(0, END)
      self.threshold_box.insert(0, str(value_int))

   def open_camera(self, face_mesh_detector: EyeControlledMouse): 
      _, frame = self.vid.read() 

      face_mesh_detector.run(frame)

      if self.face_frame is not None and self.face_frame.all() != None and self.face_frame.size > 0:
         self.face_image = cv2.cvtColor(self.face_frame, cv2.COLOR_BGR2RGBA) 
         face_array = Image.fromarray(self.face_image) 
         face_tk_image = ImageTk.PhotoImage(image=face_array) 
      else:
         face_tk_image = ImageTk.PhotoImage(image=self.face_placeholder) 

      if self.left_eye_frame is not None and self.left_eye_frame.all() != None and self.left_eye_frame.size > 0 :
         self.left_image = cv2.cvtColor(self.left_eye_frame, cv2.COLOR_BGR2RGBA) 
         left_eye_array = Image.fromarray(cv2.resize(self.left_image, (self.secundary_width, self.secundary_height))) 
         left_eye_tk_image = ImageTk.PhotoImage(image=left_eye_array) 
      else:
         left_eye_tk_image = ImageTk.PhotoImage(image=self.eye_placeholder) 

      if self.right_eye_frame is not None and self.right_eye_frame.all() != None and self.right_eye_frame.size > 0:
         self.right_image = cv2.cvtColor(self.right_eye_frame, cv2.COLOR_BGR2RGBA) 
         right_eye_array = Image.fromarray(cv2.resize(self.right_image, (self.secundary_width, self.secundary_height))) 
         right_eye_tk_image = ImageTk.PhotoImage(image=right_eye_array) 
      else:
         right_eye_tk_image = ImageTk.PhotoImage(image=self.eye_placeholder) 

      self.face_label.photo_image = face_tk_image 
      self.face_label.configure(image=face_tk_image) 

      self.right_correction_label.config(text=f"Right correction: {self.right_correction}")
        
      self.left_eye_label.photo_image = left_eye_tk_image
      self.left_eye_label.configure(image=left_eye_tk_image)

      self.right_eye_label.photo_image = right_eye_tk_image
      self.right_eye_label.configure(image=right_eye_tk_image)
      self.face_label.after(1, self.open_camera, face_mesh_detector)
      
   def start(self, face_mesh_detector: EyeControlledMouse):
      self.open_camera(face_mesh_detector)
      self.app.mainloop()

   def generate_default_coordenates(self):
      for h in [1,2,3]:
         xy1 = (self.width//6 - self.box_size, h * self.height//4 - self.box_size)
         xy2 = (self.width//2 - self.box_size, h * self.height//4 - self.box_size)
         xy3 = (5*self.width//6 - self.box_size, h * self.height//4 - self.box_size)
         self.default_coordenates.append(xy1)
         self.default_coordenates.append(xy2)
         self.default_coordenates.append(xy3)

   def generate_default_canvas(self):
      for i in range(9):
         canvas = Canvas(self.app, width=self.box_size, height=self.box_size, background="green", highlightbackground="orange", highlightthickness=2 )
         canvas.place(x=self.default_coordenates[i][0], y=self.default_coordenates[i][1])
         self.canvas.append(canvas)

if __name__ == "__main__":
   ui = UiControl()
   mediapipe_det = EyeControlledMouse(ui)
   ui.setup_ui(mediapipe_det)
   ui.start(mediapipe_det)
