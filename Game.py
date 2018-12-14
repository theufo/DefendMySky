import turtle
import math
import random

SCREEN_X = 1200
SCREEN_Y = 800

window = turtle.Screen()
window.bgpic('images/background.png')
window.setup(1200 + 3, 800 + 3)
window.screensize(SCREEN_X,SCREEN_Y)
# window.tracer(n=2)

BASE_X, BASE_Y = 0, -300


def calc_heading(x1,x2,y1,y2):
    dx = x2 - x1
    dy = y2 - y1
    length = (dx ** 2 + (dy) ** 2) ** 0.5
    cos_alpha = dx/length
    alpha = math.acos(cos_alpha)
    alpha = math.degrees(alpha)
    if dy < 0:
        alpha = - alpha
    return alpha


def fire_missile(x, y):
    missile = turtle.Turtle(visible=False)
    missile.speed(0)
    missile.color('white')
    missile.penup()
    missile.setpos(x=BASE_X, y=BASE_Y)
    missile.pendown()
    heading = calc_heading(x1=BASE_X, x2=x, y1=BASE_Y, y2=y)
    missile.setheading(heading)
    missile.showturtle()
    info = {'missile': missile, 'target': [x,y], 'state': 'launched', 'radius': 0}
    our_missiles.append(info)

def fire_enemy_missile(x, y):
    enemy_x = random.randint(-SCREEN_X/2, SCREEN_X/2)
    enemy_y = SCREEN_Y/2
    missile = turtle.Turtle(visible=False)
    missile.speed(0)
    missile.color('red')
    missile.penup()
    missile.setpos(x=enemy_x, y=enemy_y)
    missile.pendown()
    heading = calc_heading(x1=enemy_x, x2=x, y1=enemy_y, y2=y)
    missile.setheading(heading)
    missile.showturtle()
    missile.forward(10)

    flare = turtle.Turtle(visible=True)
    flare.color('#d000ff')
    flare.shape('circle')
    flare.shapesize(0.2)
    flare.speed(0)
    flare.penup()
    flare.setpos(x=enemy_x, y=enemy_y)
    flare.setheading(heading)

    info = {'missile': missile, 'target': [x,y], 'state': 'launched', 'radius': 0, 'flare': flare}
    enemy_missiles.append(info)


window.onclick(fire_missile)

our_missiles = []
enemy_missiles = []

while True:
    window.update()

    if len(enemy_missiles) < 5:
        fire_enemy_missile(BASE_X, BASE_Y)

    for missile_info in our_missiles:
        state = missile_info['state']
        missile = missile_info['missile']
        if state == 'launched':
            missile.forward(4)
            target = missile_info['target']
            if missile.distance(x=target[0], y=target[1]) < 20:
                missile_info['state'] = 'explode'
                missile.shape('circle')
        elif state == 'explode':
            missile_info['radius'] += 1
            missile.shapesize(missile_info['radius'])
            if missile_info['radius'] > 5:
                missile_info['state'] = 'dead'
                missile.clear()
                missile.hideturtle()

    for missile_info in enemy_missiles:
        state = missile_info['state']
        missile = missile_info['missile']
        flare = missile_info['flare']
        if state == 'launched':
            missile.forward(4)
            flare.forward(4)
            flare.shapesize(random.randint(1, 4)/10)
            target = missile_info['target']
            if missile.distance(x=target[0], y = target[1]) < 20:
               missile_info['state'] = 'explode'
               missile.shape('circle')
        elif state == 'explode':
            missile_info['radius'] += 1
            missile.shapesize(missile_info['radius'])
            if missile_info['radius'] > 5:
                missile_info['state'] = 'dead'
                missile.clear()
                missile.hideturtle()

    dead_our_missiles = [info for info in our_missiles if info['state'] == 'dead']
    for dead in dead_our_missiles:
        our_missiles.remove(dead)

    dead_enemy_missiles = [info for info in enemy_missiles if info['state'] == 'dead']
    for dead in dead_enemy_missiles:
        enemy_missiles.remove(dead)
