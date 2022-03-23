from multiprocessing import Process
import RPi.GPIO as GPIO
import time
import subprocess
import psutil

GPIO.setmode(GPIO.BCM)
ledPin = 17
buttonPin = 18
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, GPIO.LOW)

def buttonCheck():
  while True:
    input_state = GPIO.input(18)
    if input_state == False:
      print('button pressed')
      # get the list of pids for SSH sessions on loopback
      users = psutil.users()
      for user in users:
        if '127.0.0.1' in str(user.host):
          subprocess.run(['kill', '-9', str(user.pid)])

    time.sleep(0.25)

def sshCheck():
  while True:
    detected = False
    users = psutil.users()
    for user in users:
      if '127.0.0.1' in str(user.host):
        detected = True

    if detected:
        GPIO.output(ledPin, GPIO.HIGH)
    else:
        GPIO.output(ledPin, GPIO.LOW)

    time.sleep(0.25)

if __name__ == '__main__':
    Process(target=buttonCheck).start()
    Process(target=sshCheck).start()
