#!/usr/bin/python
#dropmonitor.py

threshold = 0.2
wait = 60
url = "https://mtgox.com/code/data/ticker.php"
alertBorder = 20
WinH = 960
WinW = 1280

import pygame
import time
from random import randint
from pygame.locals import *
import urllib

alert = False
drop = -1
pct = "-1%"
exceptionmsg = ""

while alert == False:
  time.sleep(wait)
  
  try:
    page = urllib.urlopen(url)
    line = page.readline()
  except IOError:
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
    alert = True
  
  if drop > threshold:
    alert = True

r = 0
g = 0
b = 255

pygame.init()

screen = pygame.display.set_mode((640,480))
if drop > threshold:
  pct = str(int(drop * 100)) + "%"
  message = pct + " DROP: " + str(high) + " TO " + str(last)
  pygame.display.set_caption(message)
  r = 255
  g = 0
  b = 0
else:
  pygame.display.set_caption("EXCEPTION")
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

background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))
bord = alertBorder

while True:
  pygame.draw.rect(screen, (r,g,b), (bord,bord,WinW-(bord*2),WinH-(bord*2)))
  pygame.display.flip()
  time.sleep(1)
  print 'EXCEPTION/PRICE DROP: ', pct, drop
  pygame.draw.rect(screen, (0,0,0), (bord,bord,WinW-(bord*2),WinH-(bord*2)))
  pygame.display.flip()
  time.sleep(1)
