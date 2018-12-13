import turtle
import math

window = turtle.Screen()
window.bgpic('images/background.png')
window.setup(1200 + 3, 800 + 3)
window.screensize(1200,800)
window.tracer(n=2)

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


window.onclick(fire_missile)

our_missiles = []

while True:
    window.update()

    for missile_info in our_missiles:
        state = missile_info['state']
        missile = missile_info['missile']
        if state == 'launched':
            missile.forward(4)
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

    dead_missiles = [info for info in our_missiles if info['state'] == 'dead']
    for dead in dead_missiles:
        our_missiles.remove(dead)
