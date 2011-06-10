#!/usr/bin/python
#mtgoxdropmon2.py
#This started as a very-beginner, simple program to monitor the Bitcoin
#exchange Mt. Gox for precipitous drops in value.
#Currently when run it will print a quote every minute (or however long is
#specified in "wait") including the 48-hour high, the last price, and the
#percentage drop between the two.
#BUT if the drop exceeds 20% (or whatever is specified in "threshold"), it will
#use the pygame library to open a window with a huge, blinking red box as an
#alert. The alert goes away if it detects the price has risen back above the
#threshold.
#If it encounters an error (in the program or in connecting to mtgox.com), it
#will raise a blinking yellow alert.

threshold = 0.2
wait = 60
url = "https://mtgox.com/code/data/ticker.php"
alertBorder = 20
WinH = 480
WinW = 640

import pygame
import time
from random import randint
from pygame.locals import *
import urllib

alert = False
drop = -1
pct = "-1%"
exceptionmsg = ""

def alarm(drop):
  
  r = 0
  g = 0
  b = 255
  
  if drop > threshold:
    pct = str(int(drop * 100)) + "%"
    message = pct + " DROP: " + str(high) + " TO " + str(last)
    r = 255
    g = 0
    b = 0
  else:
    message = "EXCEPTION"
    r = 255
    g = 255
    b = 0
    print "line: ", line
    print "drop: ", drop
    print "threshold: ", threshold
    print "high: ", high
    print "last: ", last
    print "h1: ", h1, "h2: ", h2, "l1: ", l1, "l2: ", l2
    print "Error Message: ", exceptionmsg
  
  pygame.init()
  screen = pygame.display.set_mode((WinW,WinH))
  pygame.display.set_caption(message)
  
  background = pygame.Surface(screen.get_size())
  background.fill((0, 0, 0))
  bord = alertBorder
  
  for i in range(0,wait,2):
    pygame.draw.rect(screen, (r,g,b), (bord,bord,WinW-(bord*2),WinH-(bord*2)))
    pygame.display.flip()
    time.sleep(1)
    pygame.draw.rect(screen, (0,0,0), (bord,bord,WinW-(bord*2),WinH-(bord*2)))
    pygame.display.flip()
    time.sleep(1)
  
  pygame.display.quit()
  

while True:
  
  try:
    page = urllib.urlopen(url)
    line = page.readline()
  except IOError:
    print "url open error"
    alert = True
    exceptionmsg = "url open error"
  #line = '{"ticker":{"high":18.998,"low":15.5,"vol":35381,"buy":17.8002,"sell":18,"last":17.8002}}'
  #line = '{"ticker":{"high":18.998,"low":15.5,"vol":35381,"buy":17.8002,"sell":18,"last":14.8002}}'
  
  h1 = -1
  h2 = -1
  l1 = -1
  l2 = -1
  
  for i in range(len(line)):
    if i+7 < len(line):
      sub = line[i:i+7]
    if sub == '"high":':
      h1 = i+7
    if sub == '"last":':
      l1 = i+7
    if line[i:i+2] == ',"' or line[i] == '}':
      if h1 != -1 and h2 == -1:
        h2 = i
      if h2 != -1 and l1 != -1 and l2 == -1:
        l2 = i
  
  if h1 > -1 and h2 > -1 and l1 > -1 and l2 > -1:
    high = float(line[h1:h2])
    last = float(line[l1:l2])
    drop = (high - last)/high
    print high, last, str(int(drop * 100)) + "%"
  else:
    print "h1, h2, l1, or l2 problem"
    alert = True
  
  if drop > threshold:
    print "drop > threshold"
    alert = True
  
  if alert:
    alarm(drop)
    alert = False
  else:
    time.sleep(wait)
