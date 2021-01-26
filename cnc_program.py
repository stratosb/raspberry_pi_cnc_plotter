import RPi.GPIO as GPIO
from stepper_motor_control import stepper_motor
from servo_motor_control import servo_motor

#filename = './files/circle.gcode'
#filename = './files/gear.gcode'
#filename = './files/dolphin.gcode'
#filename = './files/mickey.gcode'
#filename = './files/hoover.gcode'
#filename = './files/robot.gcode'
filename = './files/raspi.gcode'

x_stepper = stepper_motor(8 ,7, 10, 9)
y_stepper = stepper_motor(23, 24, 17, 27)
servo = servo_motor(11)

x_mm_per_step = 0.4150
y_mm_per_step = 0.0104

x_delay = 0.05
y_delay = 0.003

x_distance = y_distance = -1
old_x_pos = old_y_pos = 0
x3 = y3 = -1  # keep the position of the pen up-to-date, the distance traveled


def sign(n): #return the sign of a number
  if n > 0:
    return 1
  elif n < 0:
    return -1
  else:
    return 0
	
def move(x_distance, y_distance, x, y):
  # the direction (+, -)
  x_direction = sign(x_distance)
  y_direction = sign(y_distance)
  # absolute distance
  x_distance = abs(x_distance)
  y_distance = abs(y_distance)

  x_no_steps = int(round(x_distance / x_mm_per_step))
  y_no_steps = int(round(y_distance / y_mm_per_step))
  print "X no steps: " + str(x_no_steps)
  print "Y no steps: " + str(y_no_steps)
	
  over = 0
  if (x_no_steps > y_no_steps):
    for i in range(0, x_no_steps):
      if (x_direction > 0):
        x += 1
      elif (x_direction < 0):
        x -= 1
      x_stepper.motor_move(x, x_delay)
      over += y_no_steps
      if (over >= x_no_steps):
        if (y_direction > 0):
          y += 1
        elif (y_direction < 0):
          y -= 1
        y_stepper.motor_move(y, y_delay)
        over -= x_no_steps
  else:
    for i in range(0, y_no_steps):
      if (y_direction > 0):
        y += 1
      elif (y_direction < 0):
        y -= 1
      y_stepper.motor_move(y, y_delay)
      over += x_no_steps
      if (over >= y_no_steps):
        if (x_direction > 0):
          x += 1
        elif (x_direction < 0):
          x -= 1
        x_stepper.motor_move(x, x_delay)
        over -= y_no_steps
  # return the values for the global values
  return x, y;


try:
  for line in open(filename, 'r'):
    if line[0:3]=='G21':
      print 'G21: working in milimmiters'

    elif line[0:4]=='M300':
      if 'S50' in line:
        print 'M300 S50 -> pen up'
        servo.move_up()
      elif 'S30' in line:
        print 'M300 S30-> pen down'
        servo.move_down()

    elif (line[0:3]=='G0 ') or (line[0:3]=='G1 ') or (line[0:3]=='G01'):
      print "old_x_pos: " + str(old_x_pos)
      print "old_y_pos: " + str(old_y_pos)
      if 'X' in line:
        x_pos = float(line[line.index('X')+1:line.index('Y')-1])
        y_pos = float(line[line.index('Y')+1:line.index('F')-1])

	x_distance = x_pos - old_x_pos
	y_distance = y_pos - old_y_pos
        print "x_distance: " + str(x_distance)
        print "y_distance: " + str(y_distance)

        [x3, y3] = move(x_distance, y_distance, x3, y3)

	print "x3: " + str(x3)
	print "y3: " + str(y3)

      old_x_pos = x_pos
      old_y_pos = y_pos
    
except KeyboardInterrupt:
  exit()

finally:
  GPIO.cleanup();
