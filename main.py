# -*- coding: utf-8 -*-
from pygame import *
import sys
import os
import download_img
import pyperclip
from operazioni import generate

default_scale_format = 0.2
surface = None
screen = None
clock = None
lm = None
baseres = (630,891)
background_img = []#[image, x, y]
particles_bg = []  #[Surface, color, rectangle, width]
event_buffer = []
action_buffer_for_undo = [] #here are putted the actions made in order [ACTIONDEST, rollback_funct]
scale_format = 0.3
piib = 0
image_buffer = []
bool_flag = False #shared variable used by various methods
f = None  #Font
draw_left_bar = True

def main():
  global screen
  global surface
  global clock
  global lm
  init()
  display.set_caption("SchedeGenerator")
  screen= display.set_mode(baseres,HWSURFACE|DOUBLEBUF|RESIZABLE)
  surface = display.get_surface()
  surface.fill(Color(255,255,255,255),((0,0),baseres))
  load_images()
  img = image.load("img/img.gif")
  rct = img.get_rect()
  f_b = Button(rct, img, add_img)
  img1 = image.load("img/fb.bmp")
  rct = img1.get_rect()
  s_b = Button(rct, img1, move_table)
  img2 = image.load("img/text.gif")
  rct = img2.get_rect()
  t_b = Button(rct, img2, write )
  img3 = image.load("img/save.gif")
  rct = img3.get_rect()
  q_b = Button(rct, img3, save)
  img4 = image.load("img/rubber.gif")
  rct = img4.get_rect()
  f5_b = Button(rct, img4, delete)
  img5 = image.load("img/download.gif")
  rct = img5.get_rect()
  g7_b = Button(rct, img5, download)
  img5 = image.load("img/operations.gif")
  rct = img5.get_rect()
  g8_b = Button(rct, img5,operations)
  lm = LeftBar([f_b,s_b,t_b,q_b,f5_b, g7_b, g8_b])
  game()

def append_to_bg(value):
  global background_img
  action_buffer_for_undo.append([ActionDest.BACKGROUND_IMG,pop_background_img])
  background_img.append(value)
 
def pop_background_img():
  global background_img
  background_img.pop()  
  invalidate()
 
def operations():
  global draw_left_bar
  global bool_flag
  global f
  draw_left_bar = False
  bool_flag =""
  txt = str(bool_flag)
  f = font.Font("fonts/SquareDeal.ttf",int(scale_format / 0.01))
  txt = f.render(txt, True, (0,0,0,0))
  append_to_bg([txt,0,0])
  event_buffer.append([KEYDOWN, edit_text_for_operations])
  event_buffer.append([MOUSEMOTION, move_text])
  
def download():
  try:
    download_img.download(pyperclip.paste())
    load_images()
  except Exception as e:
    log(e.strerror)
  display.set_mode(baseres,HWSURFACE|DOUBLEBUF|RESIZABLE)
  invalidate()

def log(s):
  logger = open("logging.log",'w+')
  logger.write(s + '\n')
  logger.close()

def delete():
  global draw_left_bar
  draw_left_bar = False
  event_buffer.append([MOUSEBUTTONDOWN, rubber_click])
  event_buffer.append([KEYUP, stop_rubber])
  invalidate()

def stop_rubber(ev = None):
  global draw_left_bar
  global event_buffer
  if ev.key in [K_ESCAPE, K_RETURN]:
    event_buffer = []
    draw_left_bar = True
    invalidate()

def rubber_click(ev = None):
  global background_img
  global particles_bg
  x,y = ev.pos
  background_img = [ item for item in background_img if not collides(item,x,y) ]  
  particles_bg = [ item for item in particles_bg if not collides_part(item, x,y) ]
  invalidate()

def collides(item,x,y):
  _,_,w,h = item[0].get_rect()
  return item[1] <=x and item[2]<=y and (item[1] + w) >= x and (item[2] + h) >=y

def collides_part(item, xp,yp):
  cord, w= item[2]
  x,y = cord
  w,h = w
  return x<=xp and y <= yp and (x+w)>=xp and (y+h)>=yp

def save():
  global screen
  invalidate(True)
  image.save(screen, "prova.jpeg")
  invalidate()

def write():
  global bool_flag
  global f
  global draw_left_bar
  draw_left_bar = False
  bool_flag =""
  txt = str(bool_flag)
  f = font.Font("fonts/SquareDeal.ttf",int(scale_format / 0.01))
  txt = f.render(txt, True, (0,0,0,0))
  append_to_bg([txt,0,0])
  event_buffer.append([KEYDOWN, append_text])
  event_buffer.append([MOUSEMOTION, move_text])

def move_op_text(ev = None):
  return
  
def move_text(ev = None):
  background_img[-1][1],background_img[-1][2] = ev.pos
  invalidate()
    
def edit_text_for_operations(ev = None):  
  global bool_flag
  global f
  global event_buffer
  global scale_format
  global draw_left_bar
  if ev.key == K_BACKSPACE:
    bool_flag = bool_flag[0:-1]
  elif ev.key == K_ESCAPE:
    event_buffer = []
    draw_left_bar = True
    bool_flag = ""
    background_img.pop()
    invalidate()
    return
  elif ev.key == K_RETURN:
    operation =""
    try:
      operation = generate(bool_flag)
      background_img[-1][0] = f.render(operation,True,(0,0,0,0))
      txt = str(bool_flag)
      f = font.Font("fonts/SquareDeal.ttf",int(scale_format / 0.01))
      txt = f.render(txt, True, (0,0,0,0))
      append_to_bg([txt,0,0])
    except Exception:
      return 
  elif ev.key in [K_KP_PLUS,K_PLUS ]:
    scale_format+=0.01
    f = font.Font("fonts/SquareDeal.ttf",int(scale_format / 0.01))
  elif ev.key in [K_MINUS, K_KP_MINUS]:
    scale_format-=0.01
    f = font.Font("fonts/SquareDeal.ttf",int(scale_format / 0.01))
  elif ev.key in range(256):
    bool_flag+=ev.unicode
  background_img[-1][0] = f.render(bool_flag,True,(0,0,0,0))
  invalidate()
  
def append_text(ev = None):
  global bool_flag
  global f
  global event_buffer
  global scale_format
  global draw_left_bar
  if ev.key == K_BACKSPACE:
    bool_flag = bool_flag[0:-1]
  elif ev.key is K_ESCAPE:
    event_buffer = []
    draw_left_bar = True
  elif ev.key is K_RETURN:
    bool_flag = ""
    append_to_bg([None,0,0]) #gets sobstituted under, so it places and than writes another
  elif ev.key in [K_KP_PLUS]:
    scale_format+=0.01
    f = font.Font("fonts/SquareDeal.ttf",int(scale_format / 0.01))
  elif ev.key in [K_KP_MINUS]:
    scale_format-=0.01
    f = font.Font("fonts/SquareDeal.ttf",int(scale_format / 0.01))
  elif ev.key in range(256):
    bool_flag+=ev.unicode
  background_img[-1][0] = f.render(bool_flag,True,(0,0,0,0))
  invalidate()

def move_table():
  global draw_left_bar
  draw_left_bar = False
  sur = display.get_surface()
  w = int(scale_format / 0.01)
  color = Color(0,0,0,0)
  x,y = 0,0
  particles_bg.append([sur, color, ((x,y),(w,w)),1])
  event_buffer.append([MOUSEMOTION,move_cell])
  event_buffer.append([KEYUP,alternative_noresize])

def move_cell(ev=None):
  w = int(scale_format / 0.01)
  xm,ym = ev.pos
  rec = (((xm-w/2),(ym - w/2)),(w,w))
  particles_bg[-1][2] = rec
  invalidate()

def load_images():
  for file in os.listdir("img\\download"):
    image_buffer.append(image.load("img\\download\\" + file).convert_alpha())

def add_img():
  global draw_left_bar
  draw_left_bar = False
  img = image_buffer[piib]
  x,y = mouse.get_pos()
  _,_,w,h = img.get_rect()
  img = transform.scale(img, (int(w*scale_format),int(h*scale_format)))
  append_to_bg([img,x,y])
  event_buffer.append([MOUSEMOTION, adjust_pos])
  event_buffer.append([KEYUP, keypressevents])
  invalidate()

def adjust_pos(ev = None):
  background_img[-1][1]=ev.pos[0]
  background_img[-1][2]=ev.pos[1]
  invalidate()

def move_box_in_grid(ev = None):
  global particles_bg
  coord,w = particles_bg[-1][4]
  xc, yc = coord
  x,y = ev.pos
  w,_ = w
  x = int((xc%w) + int((x - w/2)/w)*w)
  y = int((yc%w) + int((y - w/2)/w)*w)
  particles_bg[-1][2] = ((x,y),(w,w))
  invalidate()
  
def others_box_in_grid(ev = None):
  global event_buffer
  global draw_left_bar
  if ev.key in [13,271]:
    event_buffer = []
    particles_bg.append([particles_bg[-1][0],particles_bg[-1][1],particles_bg[-1][2],particles_bg[-1][3],particles_bg[-1][2]])
    event_buffer.append([MOUSEMOTION, move_box_in_grid])
    event_buffer.append([KEYUP, others_box_in_grid])
  elif ev.key == 27:
    event_buffer = []  
    del particles_bg[-1]
    draw_left_bar = True
    invalidate()

def alternative_noresize(ev=None):
  global event_buffer
  global particles_bg
  global scale_format
  global draw_left_bar
  if ev.key in [13,271]:
    event_buffer = []
    particles_bg.append([particles_bg[-1][0],particles_bg[-1][1],particles_bg[-1][2],particles_bg[-1][3],particles_bg[-1][2]])
    event_buffer.append([MOUSEMOTION, move_box_in_grid])
    event_buffer.append([KEYUP, others_box_in_grid])
    bool_flag = False
  elif ev.key == 27:
    event_buffer = []
    draw_left_bar = True
    del particles_bg[-1]
    bool_flag = False
    invalidate()
  elif ev.key in [270,93]: #  +
    scale_format+=0.01
    w = int(scale_format / 0.01)
    rec = particles_bg[-1][2]
    coord,_ = rec
    rec = (coord,(w,w))
    particles_bg[-1][2] = rec
    invalidate()
  elif ev.key in [269,47]:
    scale_format-=0.01
    w = int(scale_format / 0.01)
    rec = particles_bg[-1][2]
    coord,_ = rec
    rec = (coord,(w,w))
    particles_bg[-1][2] = rec
    invalidate()


def keypressevents(ev = None):
  global event_buffer
  global piib
  global scale_format
  global draw_left_bar
  if ev.key in [13,271]:
    event_buffer = []
    draw_left_bar = True
    invalidate()
  elif ev.key >=49 and ev.key < len(image_buffer)+49:
    old = piib
    piib = ev.key-49
    _,_,w,h = image_buffer[piib].get_rect()
    background_img[-1][0] = transform.scale(image_buffer[piib],(int(w*scale_format),int(h*scale_format)))
    invalidate()
  elif ev.key in [270,93]: #  +
    _,_,w,h = image_buffer[piib].get_rect()
    scale_format+=0.01
    background_img[-1][0] = transform.scale(image_buffer[piib],(int(w*scale_format),int(h*scale_format)))
    invalidate()
  elif ev.key in [269,47]:
    _,_,w,h = image_buffer[piib].get_rect()
    scale_format-=0.01
    background_img[-1][0] = transform.scale(image_buffer[piib],(int(w*scale_format),int(h*scale_format)))
    invalidate()

def game():
  global screen
  global surface
  global clock
  while 1:
    display.update()
    events_loop()
	
def invalidate(saving=None):
  global draw_left_bar
  if saving is None:
    saving = not draw_left_bar
  x,y = screen.get_size()
  surface.fill(Color(255,255,255,255),((0,0),(x,y)))
  lm.draw(saving)
  for img in background_img:
    _,_,w,h = img[0].get_rect()
    screen.blit(img[0],((img[1],img[2]),(w,h)))
  for rec in particles_bg:
    draw.rect(rec[0],rec[1],rec[2],rec[3])

def events_loop():
  global baseres
  global ballsack
  event.pump()
  for ev in event.get(): 
    if ev.type == QUIT:
      close()
    elif ev.type == MOUSEBUTTONDOWN:
      x,y = ev.pos
      lm.clicked(x,y)
    elif ev.type==VIDEORESIZE:
      x,y = ev.dict['size']
      bx,by = baseres
      y = float(by) * (float(x)/float(bx))
      screen=display.set_mode((int(x),int(y)),HWSURFACE|DOUBLEBUF|RESIZABLE)
      invalidate()
    elif ev.type == KEYDOWN:
      if ev.key is K_z and key.get_mods() is KMOD_LCTRL and len(action_buffer_for_undo)>0:
        rlback_ev = action_buffer_for_undo.pop()
        rlback_ev[1]()
        
    for eq in event_buffer:
        if eq[0] == ev.type:
          eq[1](ev)

def close():
  quit()
  sys.exit()
  
class LeftBar:
  color = Color(255,0,0,255)
  modules = []
  def __init__(self, modules):
    global surface
    global screen
    self.modules = modules
    self.draw()

 #gives a position where to draw and a limit_x
  def draw(self, saving = False):
    if saving:
      return
    x,y = screen.get_size()
    self.limit_x = 36
    self.limit_y = y
    surface.fill(self.color,((0,0),(self.limit_x,self.limit_y)))
    x,y = 6,10
    tmp =0
    for s in self.modules:
      s.draw(x,y+tmp,self.limit_x,screen)
      _,_,w,h = s.image.get_rect()
      tmp+=(h + 10)

  def clicked(self,x,y):
    for m in self.modules:
      m.click(x,y)

class Button:
  image = None
  def __init__(self, size, image, action):
    _,_,x,y = size
    self.limit_y = y
    self.image = image
    self.action = action

  def draw(self, x, y, limit_x, screen):
    self.x = x
    self.y = y
    self.limit_x = limit_x
    screen.blit(self.image,((x,y),(limit_x, self.limit_y)))
  def click(self,x,y):
    if(self.x <= x and self.x + self.limit_x >= x and self.y <= y and self.y + self.limit_y >= y):
      self.action()

class ActionDest():
  PARTICLES =0
  BACKGROUND_IMG = 1
  UNDO = 3
  DELETE = 4
  
main()











