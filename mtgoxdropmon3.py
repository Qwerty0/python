#!/usr/bin/python
#mtgoxdropmon3.py
#This started as a very-beginner, simple program to monitor the Bitcoin
#exchange Mt. Gox for precipitous drops in value.
#Currently when run it will print a quote every minute (or however long is
#specified in "WAIT") including the 48-hour high, the last price, and the
#percentage drop between the two.
#BUT if the drop exceeds 20% (or whatever is specified in "THRESHOLD"), it will
#use the pygame library to open a window with a huge, blinking red box as an
#alert. The alert goes away if it detects the price has risen back above the
#THRESHOLD.
#If it encounters an error (in the program or in connecting to mtgox.com), it
#will raise a blinking yellow alert.

THRESHOLD = 0.2
WAIT = 60
URL = "https://mtgox.com/code/data/ticker.php"
BORDER = 20
WinH = 960
WinW = 1280

import pygame
from pygame.locals import *
import urllib2
import json

exceptionmsg = "uninitialized"
line = "uninitialized"
ticker = "uninitialized"
high = "uninitialized"
last = "uninitialized"
drop = -1
pct = "-1%"


def alarm(drop):
  
  r = 0
  g = 0
  b = 255
  
  if drop > THRESHOLD:
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
    print "line:\t", line
    print "ticker:\t", ticker
    print "high:\t", high
    print "last:\t", last
    print "drop:\t", drop
    print "THRESHOLD:\t", THRESHOLD
    print "Error Message: ", exceptionmsg
    print ""
  
  pygame.init()
  screen = pygame.display.set_mode((WinW,WinH))
  pygame.display.set_caption(message)
  
  background = pygame.Surface(screen.get_size())
  background.fill((0, 0, 0))
  windowSize = (BORDER,BORDER,WinW-(BORDER*2),WinH-(BORDER*2))
  
  for i in range(0,WAIT,2):
    pygame.draw.rect(screen, (r,g,b), windowSize)
    pygame.display.flip()
    pygame.time.wait(1000)
    pygame.draw.rect(screen, (0,0,0), windowSize)
    pygame.display.flip()
    pygame.time.wait(1000)
  pygame.display.quit()


########## MAIN LOOP ##########

while True:
  
  try:
    line = urllib2.urlopen(URL).readline()
  except urllib2.URLError:
    exceptionmsg = "url open error"
    print exceptionmsg
    alarm(-1)
    continue
  
  #line = '{"ticker":{"high":18.998,"low":15.5,"vol":35381,"buy":17.8002,"sell":18,"last":17.8002}}'
  #line = '{"ticker":{"high":18.998,"low":15.5,"vol":35381,"buy":17.8002,"sell":18,"last":14.8002}}'
  
  try:
    jdata = json.loads(line)
  except:
    exceptionmsg = "json parsing error: site data not expected format?"
    print exceptionmsg
    alarm(-1)
    continue
  
  ticker = jdata.get('ticker', 'error')
  high = ticker.get('high', 'error')
  last = ticker.get('last', 'error')
  
  if ticker == 'error' or high == 'error' or last == 'error':
    exceptionmsg = "ticker data not found: format error?"
    print exceptionmsg
    alarm(-1)
    continue
  else:
    high = float(high)
    last = float(last)
    drop = (high - last)/high
    print high, last, str(int(drop * 100)) + "%"
  
  if drop > THRESHOLD:
    print "drop > threshold"
    alarm(drop)
    continue
  
  pygame.time.wait(WAIT * 1000)