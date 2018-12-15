import turtle
import random

SCREEN_X = 1200
SCREEN_Y = 800

window = turtle.Screen()
window.bgpic('images/background.png')
window.setup(1200 + 3, 800 + 3)
window.screensize(SCREEN_X, SCREEN_Y)
window.tracer(n=2)

BASE_X, BASE_Y = 0, -300
ENEMY_COUNT = 5


def create_missile(color, x1, y1, x2, y2):
    missile = turtle.Turtle(visible=False)
    missile.speed(0)
    missile.color(color)
    missile.penup()
    missile.setpos(x=x1, y=y1)
    missile.pendown()
    heading = missile.towards(x2, y2)
    missile.setheading(heading)
    missile.showturtle()
    missile.forward(10)

    flare = turtle.Turtle(visible=True)
    flare.color('#d000ff')
    flare.shape('circle')
    flare.shapesize(0.2)
    flare.speed(0)
    flare.penup()
    flare.setpos(x=x1, y=y1)
    flare.setheading(heading)

    info = {'missile': missile, 'target': [x2, y2], 'state': 'launched', 'radius': 0, 'flare': flare}
    return info


def fire_missile(x, y):
    info = create_missile('white', BASE_X, BASE_Y, x, y)
    our_missiles.append(info)


def fire_enemy_missile():
    enemy_x = random.randint(-SCREEN_X / 2, SCREEN_X / 2)
    enemy_y = SCREEN_Y / 2
    info = create_missile('red', enemy_x, enemy_y, BASE_X, BASE_Y)
    enemy_missiles.append(info)


def move_missiles(missiles):
    for missile_info in missiles:
        state = missile_info['state']
        missile = missile_info['missile']
        flare = missile_info['flare']
        if state == 'launched':
            missile.forward(4)
            flare.forward(4)
            flare.shapesize(random.randint(1, 4) / 10)
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
        elif state == 'dead':
            missile.clear()
            missile.hideturtle()

    dead_missiles = [info for info in missiles if info['state'] == 'dead']
    for dead in dead_missiles:
        missiles.remove(dead)


def check_enemy_count():
    if len(enemy_missiles) < ENEMY_COUNT:
        fire_enemy_missile()


def check_interception():
    for our_info in our_missiles:
        if our_info['state'] != 'explode':
            continue
        our_missile = our_info['missile']
        for enemy_info in enemy_missiles:
            enemy_missile = enemy_info['missile']
            if enemy_missile.distance(our_missile.xcor(), our_missile.ycor()) < 20:
                enemy_info['state'] = 'dead'


window.onclick(fire_missile)

our_missiles = []
enemy_missiles = []

while True:
    window.update()

    # if len(enemy_missiles) < 5:
    #     fire_enemy_missile(BASE_X, BASE_Y)

    if random.randint(1, 60) == 1:
        fire_enemy_missile()

    check_interception()
    move_missiles(our_missiles)
    move_missiles(enemy_missiles)

    check_enemy_count()
