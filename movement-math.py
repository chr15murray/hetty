#!/usr/bin/env python
# coding: Latin-1

import math

leftstick = {'button': False, 'x': 511, 'y': 511, 'xmin': 0, 'xmid': 511, 'xmax': 1023, 'ymin': 0, 'ymid': 511, 'ymax': 1023}
rightstick = {'button': False, 'x': 511, 'y': 511, 'xmin': 0, 'xmid': 511, 'xmax': 1023, 'ymin': 0, 'ymid': 511, 'ymax': 1023}
controllermovement = {'degree':0, 'speed':0, 'rotation':0}


def calc_controller_movement(stick):
    movement = {}

    # Stick X range and position
    if stick['x'] >= stick['xmid']:
        stickxrange = float(stick['xmax'] - stick['xmid'])
        stickxpos = float(stick['x'] - stick['xmid'])
    else:
        stickxrange = float(stick['xmid'] - stick['xmin'])
        stickxpos = float(stick['xmid'] - stick['x'])

    # Stick Y range and position
    if stick['y'] >= stick['ymid']:
        stickyrange = float(stick['ymax'] - stick['ymid'])
        stickypos = float(stick['y'] - stick['ymid'])
    else:
        stickyrange = float(stick['ymid'] - stick['ymin'])
        stickypos = float(stick['ymid'] - stick['y'])

    # Convert position to relative position
    relx = 100 * stickxpos / stickxrange
    rely = 100 * stickypos / stickyrange

    movement['speed'] = -1

    if stick['x'] >= stick['xmid'] and stick['y'] >= stick['ymid']:
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
            movement['degree'] = round(math.degrees(math.atan2(relx, rely)))


    elif stick['x'] >= stick['xmid'] and stick['y'] < stick['ymid']:
        # 90 to 180 degree
        movement['degree'] = 90 + round(math.degrees(math.atan2(rely, relx)))

    elif stick['x'] < stick['xmid'] and stick['y'] < stick['ymid']:
        # 180 to 270 degree
        movement['degree'] = 180 + round(math.degrees(math.atan2(relx, rely)))

    else:
        # 270 to 360 degree
        movement['degree'] = 270 + round(math.degrees(math.atan2(rely, relx)))

    # Calculate speed for most cases
    if movement['speed'] == -1:
        spos = round(math.hypot(rely, relx))
        movement['speed'] = round(spos / 1.41421356237)  # 100 * math.hypot(100, 100))
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
leftstick['x'] = 511 + math.sqrt(3) * 100
leftstick['y'] = 511 + 1 * 100
print calc_controller_movement(leftstick)

# 90* test
print '90* test'
leftstick['x'] = 1023
leftstick['y'] = 511
print calc_controller_movement(leftstick)

# 120* test
print '120* test'
leftstick['x'] = 511 + math.sqrt(3) * 100
leftstick['y'] = 511 - 1 * 100
print calc_controller_movement(leftstick)

# 135
print '135* test'
leftstick['x'] = 511 + 100
leftstick['y'] = 511 - 100
print calc_controller_movement(leftstick)

# 150* test
print '150* test'
leftstick['x'] = 511 + 1 * 100
leftstick['y'] = 511 - math.sqrt(3) * 100
print calc_controller_movement(leftstick)

# 180* test
print '180* test'
leftstick['x'] = 511
leftstick['y'] = 511 - 100
print calc_controller_movement(leftstick)

# 210* test
print '210* test'
leftstick['x'] = 511 - 1 * 100
leftstick['y'] = 511 - math.sqrt(3) * 100
print calc_controller_movement(leftstick)

# 225* test
print '225* test'
leftstick['x'] = 511 - 100
leftstick['y'] = 511 - 100
print calc_controller_movement(leftstick)

# 240* test
print '240* test'
leftstick['x'] = 511 - math.sqrt(3) * 100
leftstick['y'] = 511 - 1 * 100
print calc_controller_movement(leftstick)

# 270* test
print '270* test'
leftstick['x'] = 511 - 1 * 100
leftstick['y'] = 511
print calc_controller_movement(leftstick)

# 300* test
print '300* test'
leftstick['x'] = 511 - math.sqrt(3) * 100
leftstick['y'] = 511 + 1 * 100
print calc_controller_movement(leftstick)

# 315* test
print '315* test'
leftstick['x'] = 511 - 1 * 100
leftstick['y'] = 511 + 1 * 100
print calc_controller_movement(leftstick)

# 330* test
print '330* test'
leftstick['x'] = 511 - 1 * 100
leftstick['y'] = 511 + math.sqrt(3) * 100
print calc_controller_movement(leftstick)