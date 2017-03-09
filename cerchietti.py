from pygame import Surface
space_to_circle_rateo = 25/9 #a circle is 25/9 of space
total_size = 100
def get_to_blit(scale):
  global space_to_circle_rateo
  global total_size
  size = total_size*scale
  space = space_to_circle_rateo * scale
  total_width = (4*(6*space)) + (4*(5*(6*space))) # a circle is 6 times a space
  for i in range(20):
    