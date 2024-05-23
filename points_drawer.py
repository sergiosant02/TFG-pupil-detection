import turtle
from screeninfo import get_monitors

# Get information about the primary monitor
screen = get_monitors()[0]
# Obtiene el ancho y alto de la pantalla
screen_width = screen.width
screen_height = screen.height

turtle.speed(speed=0)

# Configura la pantalla
turtle.setup(width=screen_width, height=screen_height)

# Establece el color de fondo
turtle.bgcolor("white")

# Oculta la tortuga
turtle.hideturtle()

# Función para dibujar un punto verde en una esquina
def draw_green_point(x, y):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.dot(10, "green")

# Dibuja los puntos en las cuatro esquinas
draw_green_point(-screen_width/2.03, screen_height/2.05)
draw_green_point(screen_width/2.05, screen_height/2.05)
draw_green_point(-screen_width/2.03, -screen_height/2.1)
draw_green_point(screen_width/2.05, -screen_height/2.1)

# Mantén la ventana abierta
turtle.mainloop()
