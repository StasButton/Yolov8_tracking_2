from operator import attrgetter
from io import StringIO
import pandas as pd


#Классы
class Human():
  def __init__(self):
    self.id = -1
    self.z = []
    self.m = 0
    self.k = 0
#====================
class Box():
  def __init__(self):
    self.id = -1
    self.l = 0 
    self.t = 0 
    self.r = 0 
    self.b = 0
    self.cl = -1

    self.pk = []
    self.pu = []
    #self.ks = []
    self.mpk = 0.0
    self.mpu = 0.0
    self.k = -1
    self.u = -1
    #self.k_b = 0

class Frame():
  def __init__(self):
    self.fr = -1
    self.boxs = []

    self.hb = []
    self.kb = []
    self.ub = []

class PassCouter():
  def __init__(self):
    self.id = -1
    self.inc = 0
    self.out = 0

    self.frc = 0
    self.kc = 0
    self.uc = 0 
    #self.k_b = 0


#========  Функции учета касок на людях ==============


from operator import attrgetter


def PartKaski(h,k):
  l = max([ h[0] ,k[0] ])
  t = max([ h[1] ,k[1] ])
  r = min([ h[2] ,k[2] ])
  b = min([ h[3] ,k[3] ])
  area_k = (k[2]-k[0])*(k[3]-k[1])
  area_i =  (r-l)*(b-t)
  if  area_i<0:
    area_i = 0
  return area_i/area_k

def Frame_f(data,passlist):
  # перенос информации из датафрейма в список объектов класса Frame (Framelist), 
  # включающий в себя класс Box
  # объект Frame - поля - номере кадра, список объектов класса Box
  # объект Box - поля - id бокса, параметры бокса (left,top,right,bottom), класс бокса
  

  Framelist = []
  for i in range(len(data)):
    # перенос данных из датафрейма в класс Frame. Список  кадров  объектов Frame (Framelist).
    if i != 0:
      
      box = Box() 
      box.id = data.iloc[i].id
      box.l = data.iloc[i].left
      box.t = data.iloc[i].top
      box.r = data.iloc[i].width + data.iloc[i].left
      box.b = data.iloc[i].height + data.iloc[i].top
      box.cl = data.iloc[i].cl
      
      if (data.iloc[i].frame != data.iloc[i-1].frame): # новый кадр
        Framelist.append(f)
        f = Frame()
        f.fr = data.iloc[i].frame
        f.boxs.append(box)
      else:
        f.fr = data.iloc[i].frame
        f.boxs.append(box)
    if i == 0:                                  # первый кадр
      box = Box()
      box.id = data.iloc[i].id
      box.l = data.iloc[i].left
      box.t = data.iloc[i].top
      box.r = data.iloc[i].width + data.iloc[i].left
      box.b = data.iloc[i].height + data.iloc[i].top
      box.cl = data.iloc[i].cl

      f = Frame()
      f.fr = data.iloc[i].frame
      f.boxs.append(box) 

#-----------------------------------------------
  # ищем соответствие бокса каски боксу человека

  for f in Framelist:   # перебор кадров
    for i in f.boxs:
      if i.cl == 0: 
        f.hb.append(i)  # список всех id людей в кадре
      if i.cl == 1: 
        f.kb.append(i)  # список всех касок в кадре
      if i.cl == 2: 
        f.ub.append(i)  # список всех жилетов в кадре
 
    for h in f.hb:
      hl=[h.l,h.t,h.r,h.b]
      for k in f.kb:
        kl=[k.l,k.t,k.r,k.b]
        pk = PartKaski(hl,kl) # вероятность принадлежности бокса каски k к h (человеку)

        if pk > 1:
          pk = 0
        h.pk.append(pk) # сохраняем в классе
   
      for u in f.ub:
        ul=[u.l,u.t,u.r,u.b]
        pu = PartKaski(hl,ul) # вероятность принадлежности бокса каски k к h (человеку)

        if pu > 1:
          pu = 0
        h.pu.append(pu) # сохраняем в классе
  #-----------------------------------

  for f in Framelist:
    # максимальное соответствие бокса человека каске 
    for h in f.hb:  # f.hb - список боксов людей в кадре
      if len(h.pk) != 0:
        mp  =  max(h.pk)
        h.mpk = mp
        index_max = h.pk.index(mp)
        h.k = f.kb[index_max].id    # максимальное соответствие бокса человека каске

      if len(h.pu) != 0:
        mp  =  max(h.pu)
        h.mpu = mp
        index_max = h.pu.index(mp)
        h.u = f.ub[index_max].id    # максимальное соответствие бокса человека жилету

#-------------------------------------------------------------------------
    for k in f.kb: # f.kb - список боксов касок в кадре
      hls = []
      for h in f.hb:    
        if k.id == h.k: 
          hls.append(h)
      max_attr = h   
      if(len(hls)>1):
        max_attr = max(hls, key=attrgetter('mpk'))

      for h in f.hb:   
        if(max_attr.id == h.id):
          h.k = max_attr.k
        else: 
          h.k = -1


    for u in f.ub: # f.ub - список боксов жилетов в кадре
      hls = []
      for h in f.hb:    
        if u.id == h.u: 
          hls.append(h)
      max_attr = h   
      if(len(hls)>1):
        max_attr = max(hls, key=attrgetter('mpu'))

      for h in f.hb:   
        if(max_attr.id == h.id):
          h.u = max_attr.u
        else: 
          h.u = -1
 

  for f in Framelist:
    for i in  f.boxs:
      if i.cl == 0:
        for pl in passlist:
          if pl.id == i.id:
            pl.frc+=1
            if i.k != -1:
              pl.kc+=1

            if i.u != -1:
              pl.uc+=1
  
 
  return  passlist

#========== Функции счетчика прошедших через турникет людей===================================

def Human_f(Y,data):
  r_in =  r_out = 0
  humanIdList = []                                      # список id людей в ролике

  cls0 = data[data['cl'] == 0]                       # выделение датафрейма людей из общего датафрейма     
  for i in range(cls0['id'].min(),cls0['id'].max()+1):
    if len(cls0[cls0['id'] == i]) != 0:                 # перебор всех боксов людей в водеоролике

      h = Human(); h.id = i;y0 = None;                  # создание объекта класса 

      tmp_h = cls0[cls0['id'] == i]  # выборка датафрейма с конкретным id
      for q in range(len(tmp_h)):

        y = tmp_h.iloc[q].top + tmp_h.iloc[q].height   # положение нижнего края бокса
        #----  определение стартовой позиции бокса  ---------------
        if y0 == None:
          y0 = y    
          if (y0<Y+12)&(y0>Y-12):
            break
          if y < Y-10:
            h.z.append(1)
          if y > Y+10:
            h.z.append(2)

        #----- определение остальных позиций бокса ------------
        if (y < Y-10)&(h.z[-1] == 2):
          h.z.append(1)
        if (y > Y+10)&(h.z[-1] == 1):
          h.z.append(2)
    
      humanIdList.append(h)

  
  for j in humanIdList:   # определение наличия прохода через турникет и их подсчет
    if len(j.z) >1:
      if j.z[0] > j.z[-1]:
        j.m = 2
        r_out+=1
      if j.z[0] < j.z[-1]:
        j.m = 1
        r_in+=1

  PassList = []
  for j in humanIdList:
    if j.m != 0:
      pc = PassCouter()
      pc.id = j.id
      if j.m == 1:
        pc.inc = 1
        PassList.append(pc)
      if j.m == 2:
        pc.inc = 1
        PassList.append(pc)

  return  r_in,r_out, PassList     # колическтво входов и выходов, список id прошедщих турникет
 

def END(fstr,Y): # работа с файлом полученного трекером
  #df = pd.DataFrame(columns=['files','in','out','каски','жилеты'])
  df = pd.DataFrame(columns=['входящие','выходящие','каски','жилеты'])
  # конвертация строки в датафрейм
  data= StringIO(fstr)
  data = pd.read_csv(data,  sep=' ', header=None, usecols=[0,1,2,3,4,5,6] )
  data.columns = ['frame', 'id',   'left', 'top', 'width', 'height', 'cl']

  r_in,r_out,passlist =  Human_f(Y,data) # подсчет входов и выходов

  
  plist = Frame_f(data,passlist)

  k = 0; u = 0
  for i in plist:
    if i.kc/i.frc > 0.25:
      k+=1
    if i.uc/i.frc > 0.25:
      u+=1
  df.loc[0] = [r_in,r_out,k,u]
  
  return df

################################################################


