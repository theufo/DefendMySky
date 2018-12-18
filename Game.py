import os
import turtle
import random

SCREEN_X = 1200
SCREEN_Y = 800
BASE_PATH = os.path.dirname(__file__)
BASE_X, BASE_Y = 0, -300
ENEMY_COUNT = 5


class Building:
    def __init__(self, x1, y1, health, name):
        self.x = x1
        self.y = y1
        self.health = health
        self.name = name

        pen = turtle.Turtle(visible=False)
        pen.speed(0)
        pen.penup()
        pen.setpos(x=x1, y=y1)
        pic_path = os.path.join(BASE_PATH, "images", self.get_pic_name())
        window.register_shape(pic_path)
        pen.shape(pic_path)
        pen.showturtle()

        self.pen = pen

    def get_pic_name(self):
        return f"{self.name}_1.gif"


class MissileBase(Building):
    def get_pic_name(self):
        return f"{self.name}.gif"


class Missile:
    def __init__(self, x1, y1, color, x2, y2):
        self.x = x1
        self.y = y1
        self.color = color

        pen = turtle.Turtle(visible=False)
        pen.speed(0)
        pen.color(color)
        pen.penup()
        pen.setpos(x=x1, y=y1)
        pen.pendown()
        heading = pen.towards(x2, y2)
        pen.setheading(heading)
        pen.showturtle()
        pen.forward(10)
        self.pen = pen

        self.state = 'launched'
        self.target = x2, y2
        self.radius = 0

    def step(self):
        if self.state == 'launched':
            self.pen.forward(4)
            # flare.forward(4)
            # flare.shapesize(random.randint(1, 4) / 10)
            # target = missile_info['target']
            if self.pen.distance(x=self.target[0], y=self.target[1]) < 20:
                self.state = 'explode'
                # missile_info['flare'].clear
                # missile_info['flare'].hideturtle()
                self.pen.shape('circle')
        elif self.state == 'explode':
            self.radius += 1
            if self.radius > 5:
                self.state = 'dead'
                self.pen.clear()
                self.pen.hideturtle()
            else:
                self.pen.shapesize(self.radius)
        elif self.state == 'dead':
            self.pen.clear()
            self.pen.hideturtle()

    def distance(self, x, y):
        return self.pen.distance(x, y)

    def get_x(self):
        return self.pen.xcor()

    def get_y(self):
        return self.pen.ycor()


def fire_missile(x, y):
    info = Missile(x1=BASE_X, y1=BASE_Y, x2=x, y2=y, color='blue')
    our_missiles.append(info)


def fire_enemy_missile():
    enemy_x = random.randint(-SCREEN_X / 2, SCREEN_X / 2)
    enemy_y = SCREEN_Y / 2
    info = Missile(x1=enemy_x, y1=enemy_y, x2=BASE_X, y2=BASE_Y, color='red')
    enemy_missiles.append(info)


def move_missiles(missiles):
    for missile in missiles:
        missile.step()

    dead_missiles = [missile for missile in missiles if missile.state == 'dead']
    for dead in dead_missiles:
        missiles.remove(dead)


def check_enemy_count():
    if len(enemy_missiles) < ENEMY_COUNT:
        fire_enemy_missile()


def check_interception():
    for our_missile in our_missiles:
        if our_missile.state != 'explode':
            continue
        for enemy_missile in enemy_missiles:
            if enemy_missile.distance(our_missile.get_x, our_missile.get_y) < our_missile.radius * 10:
                enemy_missile.state = 'dead'


def check_impact():
    global base_health
    for enemy_missile in enemy_missiles:
        if enemy_missile.state != 'explode':
            continue
        if enemy_missile.distance(BASE_X, BASE_Y) < enemy_missile.radius * 10:
            base.health -= 100


def game_over():
    return base.health < 0

window = turtle.Screen()
window.bgpic('images/background.png')
window.setup(1200 + 3, 800 + 3)
window.screensize(SCREEN_X, SCREEN_Y)
window.tracer(n=2)
window.onclick(fire_missile)

buildings = []
base = MissileBase(x1=BASE_X, y1=BASE_Y, health=1000, name='base')
our_missiles = []
enemy_missiles = []

building_infos = {
    'house': [BASE_X-400, BASE_Y],
    'kremlin': [BASE_X-200, BASE_Y],
    'nuclear': [BASE_X+200, BASE_Y],
    'skyscraper': [BASE_X+400, BASE_Y]
    }

for name, position in building_infos.items():
    base = Building(x1=position[0], y1=position[1], health=1000, name=name)

buildings.append(base)

while True:
    window.update()

    check_impact()
    if game_over():
        continue

    if random.randint(1, 60) == 1:
        fire_enemy_missile()

    check_interception()
    move_missiles(our_missiles)
    move_missiles(enemy_missiles)

    check_enemy_count()
