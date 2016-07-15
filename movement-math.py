#!/usr/bin/env python
# coding: Latin-1

import math

leftstick = {'button': False, 'x': 511, 'y': 511, 'xmin': 0, 'xmid': 511, 'xmax': 1023, 'ymin': 0, 'ymid': 511, 'ymax': 1023}
rightstick = {'button': False, 'x': 511, 'y': 511, 'xmin': 0, 'xmid': 511, 'xmax': 1023, 'ymin': 0, 'ymid': 511, 'ymax': 1023}
controllermovement = {'degree':0, 'speed':0, 'rotation':0}


def calc_controller_movement(stick):
    movement = {}
    if stick['x'] >= stick['xmid'] and stick['y'] >= stick['ymid']:

        movement['sector'] = '360-90'
        stickxrange = float(stick['xmax'] - stick['xmid'])
        stickxpos = float(stick['x']-stick['xmid'])
        stickyrange = float(stick['ymax'] - stick['ymid'])
        stickypos = float(stick['y'] - stick['ymid'])

        # Handle 0 co-ordinates
        if stickxpos == stickypos == 0:
            movement['degree'] = 360
            movement['speed'] = 0
        elif stickxpos == 0:
            movement['degree'] = 360
            movement['speed'] = 100 * stickypos / stickyrange
        elif stickypos == 0:
            movement['degree'] = 90
            movement['speed'] = 100 * stickxpos / stickxrange
        else:
            relx = 100 * stickxpos / stickxrange
            rely = 100 * stickypos / stickyrange
            movement['degree'] = round(math.degrees(math.atan2(relx, rely)))
            movement['speed'] = round(math.hypot(relx, rely))

            # TODO: test and comment out the one not needed
            # If max at 45* is xmax and ymax (square grid of x,y co-ordinates)
            # movement['speed'] = round(math.hypot(relx, rely))
            # if max at 45* is less than xmax and ymax (circular grid of x,y co-ordinates)
            # movement['speed'] = round(math.hypot(relx, rely))


    elif stick['x'] >= stick['xmid'] and stick['y'] < stick['ymid']:
        # 90 to 180 degree
        movement['sector'] = '90-180'


    elif stick['x'] < stick['xmid'] and stick['y'] < stick['ymid']:
        # 180 to 270 degree
        movement['sector'] = '180-270'

    else:
        # 270 to 360 degree
        movement['sector'] = '270-360'



    return movement



# 360* test
print '360* test'
leftstick['x'] = 511
leftstick['y'] = 1023
print calc_controller_movement(leftstick)

# 30* test
print '30* test'
leftstick['x'] = 511 + 1 * 100
leftstick['y'] = 511 + math.sqrt(3) * 100
print calc_controller_movement(leftstick)

# 45* test
print '45* test'
leftstick['x'] = 1023
leftstick['y'] = 1023
print calc_controller_movement(leftstick)

# 60* test
print '30* test'
leftstick['x'] = 511 + math.sqrt(3)
leftstick['y'] = 511 + 1
print calc_controller_movement(leftstick)

# 90* test
print '90* test'
leftstick['x'] = 1023
leftstick['y'] = 511
print calc_controller_movement(leftstick)

# 120* test
print '120* test'
leftstick['x'] = 511 + math.sqrt(3)
leftstick['y'] = 511 - 1
print calc_controller_movement(leftstick)