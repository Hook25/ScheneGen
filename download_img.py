import urllib
import pygame
import time
import sys
from math import sqrt
import os

IMG_SAVE_PATH = "img//download//"
baseres = (800,600)
img = None
end_download = 0

def download(url):
  global img
  global end_download
  end_download = 0
  resize(baseres)
  i = Image(url)
  img = pygame.image.load(i.path)
  x,y,w,h = img.get_rect()
  img = pygame.image.tostring(img,"RGBA")
  img = pygame.image.fromstring(img,(w,h),"RGBA")
  sur = pygame.display.get_surface()
  screen = resize((w,h))
  img = trasp(img)
  pygame.image.save(img,i.path[0:-4] + ".png")
  os.remove(i.path)
  while not end_download:
    pygame.display.update()
    events_loop()
    invalidate()

def resize(size):
  return pygame.display.set_mode(size,pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)

def invalidate():
  surface = pygame.display.get_surface()
  x,y,w,h = surface.get_rect()
  surface.fill(pygame.Color(255,0,0,255),((0,0),(w,h)))
  surface.blit(img, img.get_rect())


def trasp(img):
  _,_,w,h = img.get_rect()
  for x in range(0,w):
    for y in range(0,h):
      color = img.get_at((x,y))
      if dist(color, (255,255,255,255)) < 250:
		img.set_at((x,y),pygame.Color(0,0,0,0))
  return img

def dist(first, second):
  r1, g1, b1,_ = first
  r2, g2, b2,_ = second
  return abs(sqrt((r1*r1)+(g1*g1)+(b1*b1)) - sqrt((r2*r2)+(g2*g2)+(b2*b2)))

def events_loop():
  global end_download
  pygame.event.pump()
  for ev in pygame.event.get(): 
    if ev.type == pygame.QUIT:
      end_download = 1
    elif ev.type== pygame.VIDEORESIZE:
      resize(ev.dict['size'])


class Image:
  def __init__(self, url):
    ext = url.split('/')[-1].split('.')[-1]
    self.path = IMG_SAVE_PATH + self.generate_name() + "." + ext
    urllib.urlretrieve(url,self.path)
  def generate_name(self):
    return time.strftime("%d%m%Y%H%M%S")
