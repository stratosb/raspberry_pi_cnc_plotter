import RPi.GPIO as GPIO
import time

steps_list = [[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1],[1,0,0,0]]
num_phase=len(steps_list);

class stepper_motor:
  motorA1 = 0
  motorA2 = 0
  motorB1 = 0
  motorB2 = 0

  def __init__(self,a1,a2,b1,b2):
    # Use physical pin numbers
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    self.motorA1 = a1;
    self.motorA2 = a2;
    self.motorB1 = b1;
    self.motorB2 = b2;

    GPIO.setup(self.motorA1, GPIO.OUT)
    GPIO.setup(self.motorA2, GPIO.OUT)
    GPIO.setup(self.motorB1, GPIO.OUT)
    GPIO.setup(self.motorB2, GPIO.OUT)

  # Function for step sequence
  def setStep(self, w1, w2, w3, w4):
    GPIO.output(self.motorA1, w1)
    GPIO.output(self.motorB1, w2)
    GPIO.output(self.motorA2, w3)
    GPIO.output(self.motorB2, w4)

  def motor_move(self, stepNo, delay):
    index = stepNo % 8
    sl = steps_list[index]
    self.setStep(sl[0], sl[1], sl[2], sl[3])
    time.sleep(delay)
