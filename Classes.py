import numpy as np
import random




class University:
  def __init__ (self,location, area):
    self.location = location
    self.area = area

class Institute(University):
  def __init__(self, location, area, name, color):
      super().__init__(location, area)
      self.name = name
      self.color = color
      self.free_date = {"Mon":[8,10,14,16,19,21]}
      #, "Tue":[8,10,14,16,19,21],"Fri":[8,14,19]}

class Classroom(University):
  def __init__(self, location, area, name, color):
      super().__init__(location, area)
      self.name = name
      self.color = color
      self.free_date = {"Mon":[8,10,14,16,19,21]}
      #, "Tue":[8,10,14,16,19,21],"Fri":[8,14,19]}

class Restaurant(University):
  def __init__(self, location, area, name, color):
      super().__init__(location, area)
      self.name = name
      self.color = color

class People:
  global dt, asym, p_test_symp, p_test_asymp
  asym = 0.3
  dt = 0.1
  p_test_symp = 0.7
  p_test_asymp = 0.1

  def __init__ (self,Inst, Infect, Position, Vaci, Velocity, Quaren,Imune, V0,Time, Age, Incub_period, Death_period, Recov_period, Infectivity):
    self.Inst = Inst
    self.Infect = Infect
    self.Position = Position
    self.Vaci = Vaci
    self.Velocity = Velocity
    self.Quaren = Quaren
    self.Imune = Imune
    self.Time = Time
    self.Age = Age
    self.Prob_Die = 0.0000457*np.exp(0.08952*self.Age)
    self.color =  {0:"Green",2:"Red",3:"Blue"}[self.Infect]
    self.Death_period = Death_period
    self.Incub_period = Incub_period
    self.Recov_period = Recov_period
    self.Infectivity = Infectivity
    self.Is_Going_2_Die = False
    self.timer = ["Mon",8,0]
    self.Going_2_Quaren = False




  def Set_Goal(self):
    self.Goal = self.Schedule[self.Time[0]][self.Time[1]]


  def Set_P0(self, PosiInicial):
    self.Position = PosiInicial

  def Set_V0(self, v0):
    self.Velocity = v0

  def Att_Posi(self):
    self.Position = self.Position + self.Velocity*dt

  def Att_Time (self, time):
    self.Time = time
    self.Set_Goal()

  def Att_State (self, *args):
    if not self.Infect == -2:
      if len(args) > 0:
        self.timer = self.Time
        self.Infect = args[0]
        self.color =  {0:"Green",2:"Red",3:"Blue",1:"purple", -1:"Gray", -2:"Black"}[self.Infect]
      else:
        if ((self.Time[2] - self.timer[2]) >= self.Death_period) and (self.Is_Going_2_Die == True):
          self.Infect = -2
          self.color =  "Black"

        elif (self.Time[2] - self.timer[2]) >= self.Incub_period and self.Infect == 1:

          if np.random.uniform(0,1) <= self.Prob_Die:
            self.Is_Going_2_Die = True

          if np.random.uniform(0,1) <= asym:
            self.Infect = 3
            self.color =  "Blue"


          else:
            self.Infect = 2
            self.color =  "Red"
            self.Infectivity = np.random.gamma(1.3, 0.2)
            while self.Infectivity > 1:
                  self.Infectivity = np.random.gamma(1.3, 0.2)

          self.timer = self.Time

        elif (self.Time[2] - self.timer[2]) >= self.Recov_period and self.Infect >= 2:
          self.Infect = -1
          self.color = "Grey"
          self.Is_Going_2_Die = False

      if self.Quaren == True and self.Infect < 0:
        self.Quaren = False
      elif self.Quaren == False and np.random.uniform(0,1) <= 0.98:
        if self.Infect == 2 and np.random.uniform(0,1) <= p_test_symp:
          self.Going_2_Quaren = True
        elif self.Infect == 3 and np.random.uniform(0,1) <= p_test_asymp:
          self.Going_2_Quaren = True

  def Att_Quarentine(self):
    if self.Infect == -1:
      self.Quaren = False
      self.Going_2_Quaren == False
      x = np.random.randint(-15,15)
      y = np.random.randint(-15,15)
      self.Position = np.array([x,y])

    elif self.Going_2_Quaren == True:
      self.Quaren =True
      self.Position = np.array([100,100])           # Still need to think where quarentine will ocour.



class Student(People):
  def __init__(self, Inst, Infect, Position, Vaci, Velocity, Quaren, Imune, V0, Time, Age, Incub_period, Death_period, Recov_period, Infectivity, Schedule):
      super().__init__(Inst, Infect, Position, Vaci, Velocity, Quaren, Imune, V0, Time, Age, Incub_period, Death_period, Recov_period, Infectivity)
      self.Schedule = Schedule



class Professor(People):
  def __init__(self, Inst, Infect, Position, Vaci, Velocity, Quaren, Imune, V0, Time, Age, Incub_period, Death_period, Recov_period, Infectivity):
      super().__init__(Inst, Infect, Position, Vaci, Velocity, Quaren, Imune, V0, Time, Age, Incub_period, Death_period, Recov_period, Infectivity)
      self.Schedule = {}
      d = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
      t = [7,8,9,10,11,14,15,16,17,19,20,21,22,23]
      for i in d:
        self.Schedule[i] = {}                     
        for j in t:
          self.Schedule[i][j] = ''
        if random.randint(1,2) == 1:
          self.Schedule[i][12] = 'Bandeco'
          self.Schedule[i][13] = ''
        else:
          self.Schedule[i][13] = 'Bandeco'
          self.Schedule[i][12] = ''
        self.Schedule[i][18] = 'Bandeco'
      self.working = False
      self.classes = []

  def Add_class(self, day, hour, place):
    self.Schedule[day][hour] = place
    self.Schedule[day][hour + 1] = place
    if day == 'Mon':
      self.Schedule['Wed'][hour] = place
      self.Schedule['Wed'][hour + 1] = place
    elif day == 'Tue':
      self.Schedule['Thu'][hour] = place
      self.Schedule['Thu'][hour + 1] = place
    else:
      self.Schedule[day][hour + 2] = place
      self.Schedule[day][hour + 3] = place
    self.classes.append([day, hour, place])
    self.working = True      #Serve para não escolhermos um professor que não dê aulas para algum aluno
  def Fill_schedule(self):
    for i in list(self.Schedule.keys()):
      for j in list(self.Schedule[i].keys()):
        if self.Schedule[i][j] == '':
          self.Schedule[i][j] = self.Inst
class Worker(People):
  def __init__(self, Inst, Infect, Position, Vaci, Velocity, Quaren, Schedule, Imune, V0, Time, Age, Incub_period, Death_period, Recov_period, Infectivity):
      super().__init__(Inst, Infect, Position, Vaci, Velocity, Quaren, Schedule, Imune, V0, Time, Age, Incub_period, Death_period, Recov_period, Infectivity)
      self.color =  {0:"gray",1:"Red",2:"Blue"}[Infect]

class Outsourced(People):
  def __init__(self, Inst, Infect, Position, Vaci, Velocity, Quaren, Schedule, Imune, V0, Time, Age, Incub_period, Death_period, Recov_period, Infectivity):
      super().__init__(Inst, Infect, Position, Vaci, Velocity, Quaren, Schedule, Imune, V0, Time, Age, Incub_period, Death_period, Recov_period, Infectivity)
      self.color =  {0:"purple",1:"Red",2:"Blue"}[Infect]
