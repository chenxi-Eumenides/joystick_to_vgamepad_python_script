import pyautogui as pg
import pygetwindow
from time import sleep


a = 'a'
b = 'b'
x = 'x'
y = 'y'
l = 'l'
r = 'r'
zl = ','
zr = 't'
bp = '='
mp = '-'
lp = 'c'
lu = 'e'
ld = 'd'
ll = 's'
lr = 'f'
rp = 'm'
ru = 'u'
rd = 'j'
rl = 'h'
rr = 'k'
up = 'up'
dw = 'down'
le = 'left'
ri = 'right'

run = a
jump = y
paragliders = y
attack = x
power = l
defense = zl
throw_weapon = r
bow = zr
move_front = lu
move_back = ld
move_left = ll
move_right = lr
gui_power = up
gui_weapon = ri
gui_second_hand = le
gui_horse = dw

confirm = b
cancel = a
open_backpack = bp
open_map = mp
backpack_switch_left = ll
backpack_switch_right = lr
backpack_switch_up = lu
backpack_switch_down = ld
backpack_switch_type_left = rl
backpack_switch_type_right = rr
backpack_switch_page_left = l
backpack_switch_page_right = r
gui_switch_left = rl
gui_switch_right = rr

keys = []


def Press(key: str, time: float = 0.05, space: float = 0.05):
    if key in keys:
        return 1
    pg.keyDown(key)
    sleep(time)
    pg.keyUp(key)
    sleep(space)
    return 0


def Down(key: str, space: float = 0.05):
    if key in keys:
        return 1
    keys.append(key)
    pg.keyDown(key)
    sleep(space)
    return 0


def Up(key: str, space: float = 0.05):
    if key in keys:
        keys.remove(key)
    else:
        return 1
    pg.keyUp(key)
    sleep(space)
    return 9


def reset(keep_keys: list):
    for key in keys:
        if key in keep_keys:
            continue
        pg.keyUp(key)


def start_game():
    Press(confirm)
    sleep(1)
    Press(confirm)
    sleep(1)
    Press(confirm)


def switch_to_circle_boob():
    Down(gui_power)
    Down(gui_switch_left)
    sleep(1)
    Up(gui_switch_left)
    Up(gui_power)


def fly_by_boom_1():
    sleep(1)
    switch_to_circle_boob()
    # 持盾往前跑后取消盾
    Down(defense, 0.5)
    Down(move_front)
    Up(defense)
    # 起跳并放圆形炸弹后拉弓
    Down(jump)
    Down(power)
    Down(bow)
    Up(jump)
    Up(power)
    Up(bow)
    # 切方形炸弹并放方形炸弹
    Down(gui_power)
    Press(gui_switch_right)
    Up(gui_power)
    Press(power)
    # 切圆形炸弹
    Down(gui_power)
    Press(gui_switch_left)
    Up(gui_power)
    # 引爆
    Press(power)
    sleep(1)
    for _ in range(10):
        Press(paragliders, space=0)
        sleep(0.1)


def exit_game():
    Press(open_backpack)
    Press(backpack_switch_page_left)
    Press(backpack_switch_up, 0.5)
    Press(confirm)
    Press(backpack_switch_up)
    Press(confirm)
    Press(backpack_switch_down, 0.5)
    Press(confirm)
    Press(backpack_switch_up)
    Press(confirm)


while pygetwindow.getActiveWindowTitle()[:4] != 'Cemu':
    sleep(0.5)


fly_by_boom_1()

reset([move_front])
