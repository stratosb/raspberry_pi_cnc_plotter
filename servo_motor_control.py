import RPi.GPIO as GPIO
from time import sleep

class servo_motor:
  servoPIN = 0

  def __init__(self, pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    self.servoPIN = pin
    
  def move_up(self):
    self.pwm = GPIO.PWM(self.servoPIN, 50)
    self.pwm.start(2.5)
    self.pwm.ChangeDutyCycle(2.5)
    sleep(1)
    self.pwm.stop()

  def move_down(self):
    self.pwm = GPIO.PWM(self.servoPIN, 50)
    self.pwm.start(2.5)
    self.pwm.ChangeDutyCycle(7.5)
    sleep(1)
    self.pwm.stop()
