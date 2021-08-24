import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation

class Institute:
  def __init__ (self,location, area, name):
    self.location = location
    self.name = name
    self.area = area

class Student:
  global dt

  dt = 0.1
  def __init__ (self,Inst, Infect, Position, Vaci, Velocity, Quaren, Schedule,Imune, V0,Time):
    self.Inst = Inst
    self.Infect = Infect
    self.Position = Position
    self.Vaci = Vaci
    self.Velocity = Velocity
    self.Quaren = Quaren
    self.Schedule = Schedule
    self.Imune = Imune
    self.V0 = V0
    self.Time = Time
    self.Goal = Schedule[Time[0]][Time[1]]



  def Set_Goal(self,time):
    self.Goal = self.Schedule[time[0]][time[1]]


  def Set_P0(self, PosiInicial):
    self.Position = PosiInitial
  
  def Set_V0(self, v0):
    self.Velocity = v0

  def att_posi(self):
    self.Position = self.Position + self.Velocity*dt
  
  def att_velo(self):
    self.Velocity = self.Velocity +a*dt
