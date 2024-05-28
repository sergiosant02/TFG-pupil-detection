from tkinter import *
from tkinter.ttk import Combobox
import cv2 
from PIL import Image, ImageTk 

class UiControl:
   def __init__(self, controller):
      self.app = Tk() 
      self.controller = controller
      self.app.title("Pupil detection")
      self.face_placeholder = Image.open('placeholders/face_placeholder.jpg')
      self.eye_placeholder = Image.open('placeholders/eye_placeholder.png')
      self.face_frame: cv2.Mat = None
      self.left_eye_frame: cv2.Mat = None
      self.right_eye_frame: cv2.Mat = None
      self.width, self.height = self.app.winfo_screenwidth(), self.app.winfo_screenheight() 
      self.pictures_space_height = self.height // 2
      self.main_width = self.width
      self.main_height = self.height // 2
      self.secundary_width = self.width // 2
      self.secundary_height = self.height // 4
      self.bottom_height = self.height // 2
      self.threshold = 25
      self.box_size = 5
      self.text_box_increment = 3
      self.test_points: list = []
      self.test_point = None
      self.test_point_box: Canvas = None
      self.test_index = None
      self.left_correction = None
      self.right_correction = None
      self.labels: list[Label] = []
      self.coordenates = []
      self.canvas: list[Canvas] = []
      self.default_coordenates = []

   def check_nineth_coordinate(self):
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
      self.check_nineth_coordinate()

   def focus_in_handler(self, event):
      self.app.focus_set()

   def setup_ui(self):
      self.controller.vid.set(cv2.CAP_PROP_FRAME_WIDTH, self.main_width) 
      self.controller.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, self.main_height) 
      self.generate_default_coordenates()
      self.app.bind('<Escape>', lambda e: self.app.quit()) 
      dimensions = '{}x{}+{}+{}'.format(self.width, self.height, 0, 0)
      self.app.geometry(dimensions)

      main_frame = Frame(self.app)
      main_frame.pack(fill=BOTH, expand=True)

      # Label for pictures
      photos_frame = Frame(main_frame)
      photos_frame.pack(fill=BOTH, expand=True)

      # Label for face
      self.face_label = Label(photos_frame, height=self.main_height, width=self.secundary_width) 
      self.face_label.pack(side=LEFT) 

      # Label for eyes
      eyes_frame = Frame(photos_frame)
      eyes_frame.pack(side=LEFT)

      # Label for left eye picture
      self.left_eye_label = Label(eyes_frame, height=self.secundary_height, width=self.secundary_width)
      self.left_eye_label.pack()

      # Label for right eye picture
      self.right_eye_label = Label(eyes_frame, height=self.secundary_height, width=self.secundary_width)
      self.right_eye_label.pack()

      # Frame for horizontal stacks
      horizontal_stack_frame = Frame(main_frame)
      horizontal_stack_frame.pack(fill=BOTH, expand=True)

      # Frame for slider and entry
      slider_frame = Frame(horizontal_stack_frame)
      slider_frame.pack(side=LEFT, fill=BOTH, expand=True)

     # Frame for the button and label
      button_frame = Frame(horizontal_stack_frame)
      button_frame.pack(side=LEFT, fill=BOTH, expand=True)

      # Frame for 9 labels
      labels_frame = Frame(horizontal_stack_frame)
      labels_frame.pack(side=LEFT, fill=BOTH, expand=True)

      # Slider and Entry
      threshold_label_info = Label(slider_frame, text="Threshold:")
      #threshold_label_info.pack(anchor=W, padx=10)

      self.threshold_box = Entry(slider_frame, width=5)
      self.threshold_box.bind("<KeyRelease>", self.update_threshold_entry)
      #self.threshold_box.pack(anchor=W, padx=10)

      self.slider = Scale(slider_frame, from_=0, to=255, orient=HORIZONTAL, command=self.update_threshold_slider)
      self.slider.set(self.threshold)
      #self.slider.pack(fill=BOTH, expand=True, padx=10, pady=5)

      # Botón and Label
      self.right_correction_label = Label(button_frame, wraplength=300, justify="left", text='Para iniciar los test debes pullsar el botón inferior, en caso de querer calibrar el sistema deberá de pulsar sobre sobre "Registrar siguiente coordenada"')
      self.right_correction_label.pack(fill=BOTH, expand=True, padx=10, pady=5)

      self.correction_button = Button(button_frame, text="Aplicar corrección", command=self.controller.calculate_correction)
      #correction_button.pack(fill=BOTH, expand=True, padx=10, pady=5)
      self.test_button = Button(button_frame, text="Comenzar las pruebas", command=self.controller.add_test)
      #self.reset_test_button = Button(button_frame, text="Comenzar las pruebas", command=self.controller.reset_test)
      self.test_button.pack(fill=BOTH, expand=True, padx=10, pady=2)
      #self.save_test_button = Button(button_frame, text="Guardar las pruebas", command=self.controller.save_test_results)

      # Aditionals labels
      for i in range(3):
         for j in range(3):
            label_text = f"Coordenada {i*3+j+1}"
            label = Label(labels_frame, text=label_text, width=15)
            label.grid(row=i, column=j, padx=5, pady=5, sticky=W)
            self.labels.append(label)

      # Register the next coordenate
      self.register_button = Button(labels_frame, text="Registrar siguiente coordenada", command=self.controller.log_next_coordenates)
      self.register_button.grid(row=3, columnspan=3, pady=5)
      self.reset_button = Button(labels_frame, text="Reiniciar", command=self.reset_coordenates)

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

   def open_camera(self): 
      
      self.controller.open_camera()
      
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

      #self.right_correction_label.config(text=f"Right correction: {self.right_correction}")
        
      self.left_eye_label.photo_image = left_eye_tk_image
      self.left_eye_label.configure(image=left_eye_tk_image)

      self.right_eye_label.photo_image = right_eye_tk_image
      self.right_eye_label.configure(image=right_eye_tk_image)
      self.face_label.after(1, self.open_camera)

   def generate_default_coordenates(self):
      txy1_up = (self.width//3 - self.box_size + self.text_box_increment, self.height//8 - self.box_size - 1.5*self.text_box_increment)
      txy2_up = (2*self.width//3 - self.box_size + self.text_box_increment, self.height//8 - self.box_size - 1.5*self.text_box_increment)
      self.test_points = [txy1_up, txy2_up]
      for h in [1,2,3]:
         txy1 = (self.width//12 - self.box_size - 1.5*self.text_box_increment, h * self.height//4 - self.box_size - 1.5*self.text_box_increment)
         xy1 = (self.width//6 + self.box_size, h * self.height//4 - self.box_size)
         txy2 = (self.width//3 - self.box_size - 1.5*self.text_box_increment, h * self.height//4 - self.box_size - 1.5*self.text_box_increment)
         xy2 = (self.width//2 + self.box_size, h * self.height//4 - self.box_size)
         txy3 = (2*self.width//3 - self.box_size - 1.5*self.text_box_increment, h * self.height//4 - self.box_size - 1.5*self.text_box_increment)
         xy3 = (5*self.width//6 + self.box_size, h * self.height//4 - self.box_size)
         txy4 = (11*self.width//12 - self.box_size - 1.5*self.text_box_increment, h * self.height//4 - self.box_size - 1.5*self.text_box_increment)
         self.default_coordenates.append(xy1)
         self.default_coordenates.append(xy2)
         self.default_coordenates.append(xy3)

         self.test_points.append(txy1)
         self.test_points.append(txy2)
         self.test_points.append(txy3)
         self.test_points.append(txy4)
      txy1_down = (self.width//3 - self.box_size + self.text_box_increment, 7*self.height//8 - self.box_size - 1.5*self.text_box_increment)
      txy2_down = (2*self.width//3 - self.box_size + self.text_box_increment, 7*self.height//8 - self.box_size - 1.5*self.text_box_increment)

      self.test_points.append(txy1_down)
      self.test_points.append(txy2_down)

   def generate_default_canvas(self):
      for i in range(9):
         canvas = Canvas(self.app, width=self.box_size, height=self.box_size, background="green", highlightbackground="orange", highlightthickness=2 )
         canvas.place(x=self.default_coordenates[i][0], y=self.default_coordenates[i][1])
         self.canvas.append(canvas)

   def reset_test(self):
      self.test_index = None
      self.test_button.pack(fill=BOTH, expand=True, padx=10, pady=2)
      #self.save_test_button.pack(fill=BOTH, expand=True, padx=10, pady=2)
      #self.reset_test_button.pack_forget()

   def bring_to_front(self):
      # Put the window on the front side
      self.app.attributes('-topmost', True) 
      self.app.attributes('-topmost', False) 

   def update_current_test_point(self):
      self.test_point = self.test_points[self.test_index]

   def add_test(self):
        if self.test_index == None:
            self.test_index = 0
            self.test_point = self.test_points[self.test_index]
            self.test_point_box = Canvas(self.app, width=self.box_size, height=self.box_size, background="red", highlightbackground="red", highlightthickness=self.box_size + self.text_box_increment )
            self.test_point_box.place(x=self.test_points[0][0], y=self.test_points[0][1])
            self.test_button.pack_forget()
            #self.save_test_button.pack(fill=BOTH, expand=True, padx=10, pady=2)
            #self.reset_test_button.pack(fill=BOTH, expand=True, padx=10, pady=2)
        elif self.test_index != None and self.test_index < len(self.test_points)-1:
            self.test_index += 1 
            self.test_point = self.test_points[self.test_index]
            self.test_point_box.place(x=self.test_points[self.test_index][0], y=self.test_points[self.test_index][1])
        else:
            self.test_index = None
            self.test_point = None
            self.reset_test()

   def reset_test(self):
      self.test_index = None
      self.test_point = None
      self.test_point_box.place_forget()
      self.test_button.pack(fill=BOTH, expand=True, padx=10, pady=2)

   def format_text_in_label(self, i: int, text):
      self.labels[i].configure(text=text)



   def start(self):
      self.setup_ui()
      self.open_camera()
      self.bring_to_front()
      self.app.mainloop()
