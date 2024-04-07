import turtle
import tkinter as tk
from PIL import Image, ImageTk
import random

w = 500
h = 500
food_size = 10
delay = 100

offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}


def reset():
    global caterpillar, caterpillar_dir, food_position, pen
    caterpillar = [[0, 0], [0, 20], [0, 40], [0, 60], [0, 80]]
    caterpillar_dir = "up"
    food_position = get_random_food_position()
    food.goto(food_position)
    move_caterpillar()


def move_caterpillar():
    global caterpillar_dir

    new_head = caterpillar[-1].copy()
    new_head[0] = caterpillar[-1][0] + offsets[caterpillar_dir][0]
    new_head[1] = caterpillar[-1][1] + offsets[caterpillar_dir][1]

    if new_head in caterpillar[:-1]:
        reset()
    else:
        caterpillar.append(new_head)

        if not food_collision():
            caterpillar.pop(0)

        if caterpillar[-1][0] > w / 2:
            caterpillar[-1][0] -= w
        elif caterpillar[-1][0] < - w / 2:
            caterpillar[-1][0] += w
        elif caterpillar[-1][1] > h / 2:
            caterpillar[-1][1] -= h
        elif caterpillar[-1][1] < -h / 2:
            caterpillar[-1][1] += h

        pen.clearstamps()

        for segment in caterpillar:
            pen.goto(segment[0], segment[1])
            pen.stamp()

        screen.update()

        turtle.ontimer(move_caterpillar, delay)


def food_collision():
    global food_position
    if get_distance(caterpillar[-1], food_position) < 20:
        food_position = get_random_food_position()
        food.goto(food_position)
        return True
    return False


def get_random_food_position():
    x = random.randint(- w / 2 + food_size, w / 2 - food_size)
    y = random.randint(- h / 2 + food_size, h / 2 - food_size)
    return (x, y)


def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return distance


def go_up():
    global caterpillar_dir
    if caterpillar_dir != "down":
        caterpillar_dir = "up"


def go_right():
    global caterpillar_dir
    if caterpillar_dir != "left":
        caterpillar_dir = "right"


def go_down():
    global caterpillar_dir
    if caterpillar_dir != "up":
        caterpillar_dir = "down"


def go_left():
    global caterpillar_dir
    if caterpillar_dir != "right":
        caterpillar_dir = "left"


screen = turtle.Screen()
screen.setup(w, h)
screen.title("Caterpillar")

image = Image.open("/Users/drishtijain/Downloads/space.jpg")
photo = ImageTk.PhotoImage(image)

canvas = tk.Canvas(screen.cv, width=w, height=h)
canvas.create_image(0, 0, anchor=tk.NW, image=photo)
canvas.grid(row=0, column=0, sticky="nsew")

screen.cv.grid_rowconfigure(0, weight=1)
screen.cv.grid_columnconfigure(0, weight=1)

screen.setup(500, 500)
screen.tracer(0)

pen = turtle.Turtle("circle")
pen.penup()

food = turtle.Turtle()
food.shape("square")
food.color("green")
food.shapesize(food_size / 20)
food.penup()

screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")

reset()
turtle.done()