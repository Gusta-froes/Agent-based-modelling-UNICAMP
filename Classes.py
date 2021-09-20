import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation

class University:
  def __init__ (self,location, area):
    self.location = location
    self.area = area

class Institute(University):
  def __init__(self, location, area, name, color):
      super().__init__(location, area)
      self.name = name
      self.color = color
      self.free_date = {"Mon":[8,10,14,16,19,21], "Tue":[8,10,14,16,19,21], "Wed":[8,10,14,16,19,21],"Thu":[8,10,14,16,19,21],"Fri":[8,10,14,16,19,21]}

class Classroom(University):
  def __init__(self, location, area, name, color):
      super().__init__(location, area)
      self.name = name
      self.color = color
      self.free_date = {"Mon":[8,10,14,16,19,21], "Tue":[8,10,14,16,19,21], "Wed":[8,10,14,16,19,21],"Thu":[8,10,14,16,19,21],"Fri":[8,10,14,16,19,21]}

class Restaurant(University):
  def __init__(self, location, area, name, color):
      super().__init__(location, area)
      self.name = name
      self.color = color

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
