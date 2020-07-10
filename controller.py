#!/usr/bin/env python3

import board
import busio
import digitalio

from adafruit_si7021 import SI7021
#local
from display import I2C_OLED, OLED_Menu
from bank import DataBank
from panel import SwitchBoard


def check(task):

    alert = data.alerts[task]
    flag = data.flags[task]
    value = data.sensors[alert['sensor']]

    boo = not flag['on']

    if boo:                             # If furnace is [off]
        arg = value < alert['on']       # TRUE if colder than [on] alert
    else:                               # If furnace is [on]
        arg = value > alert['off']      # TRUE if warmer than [off] alert

    if alert['on'] > alert['off']:      # Correction for air conditioning
        arg = not arg

    if arg:
        if flag['check'] == boo:
            flag['on'] = boo
            sb.turn(task, boo) #sb.io[task].value = boo
            
        else:
            flag['check'] = boo
    else:
        flag['check'] = not boo


def respond(frequency=0.2, test=False):
    status = sb.get_input()
    if any(status.values()):
        button = list(status.keys())[list(status.values()).index(True)]
        menu.goto(button)
        #frequency = 0.5
    return frequency


def monitor(frequency=1, test=False):

    data.sensors['temperature'] = round(sensor.temperature, 1)
    data.sensors['humidity'] = round(sensor.relative_humidity, 1)

    menu.interface()

    if test:
        menu.test()
        print(f"\nTemperature: {round(sensor.temperature, 2)} C")
        print(f"Humidity: {round(sensor.relative_humidity, 2)} %")
        print(data)

    return frequency


def operate(frequency=30, test=False):

    check('furnace')
    data.log()

    return frequency

folder = (__file__)[0:-13]

i2c = busio.I2C(board.SCL, board.SDA)   # Adafruit Bus I2C port library
sensor = SI7021(i2c)                    # Adafruit library for SI7021 sensor
data = DataBank(folder)
#oled = I2C_OLED(128, 64, i2c, folder, data)   # Object that handles display
menu = OLED_Menu(128, 64, i2c, folder, data)   # Object that handles display

sb = SwitchBoard()
sb.digital_output('furnace', board.D18)
sb.digital_input('up', board.D17)
sb.digital_input('down', board.D27)
#sb.digital_input('up', 11)
#up = Button(11)
#up.when_pressed = sb.hi
#up.when_released = sb.bye
#sb.digital_input('down', 13)
#sb.digital_input('left', board.D17)
#sb.digital_input('right', board.D17)

