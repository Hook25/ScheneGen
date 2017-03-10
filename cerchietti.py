from pygame import Surface, draw,SRCALPHA
from random import randint
space_to_circle_rateo = 25/9 #a circle is 25/9 of space
total_size = 10
BLACK=(0,0,0,255)
WHITE=(255,255,255,0)
def get_to_blit(scale):
  global BLACK
  global WHITE
  global space_to_circle_rateo
  global total_size
  size = total_size*scale
  space = space_to_circle_rateo * size
  total_width = (4*(6*space)) + (4*(5*(6*space))) # a circle is 6 times a space
  sur = Surface((total_width, 5*space),flags=SRCALPHA)
  sur.fill(WHITE)
  counter = 0
  l = range(0,randint(1,9))
  for i in range(20):
    counter += space
    draw.circle(sur, BLACK, (int(counter + 3*space), int(2.5*space)), int(2*space),1 if i in l else 0)
    counter += 3*space
  return sur