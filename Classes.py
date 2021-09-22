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
    self.V0 = V0
    self.Time = Time
    self.Age = Age
    self.Prob_Die = 0.0000457*np.exp(0.08952*self.Age)
    self.Death_period = Death_period
    self.Incub_period = Incub_period
    self.Recov_period = Recov_period
    self.Infectivity = Infectivity
    self.Is_Going_2_Die = False
    self.timer = [7,"Mon",0]
    



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
    if not self.Infect == 2:
      if len(args) > 0:
        self.timer = self.Time
        self.Infect = args[0]
        self.color =  {0:"Green",2:"Red",3:"Blue",1:"Green", -1:"Gray", -2:"Black"}[self.Infect]
      else:
        if (self.Time[2] - self.timer[2]) >= self.Death_period and self.Is_Going_2_Die == True:
          self.Infect = -2
          self.color =  "Black"

        elif (self.Time[2] - self.timer[2]) >= self.Incub_period:

          if np.random.uniform(0,1) <= self.Porb_Die:
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
          
        elif (self.Time[2] - self.timer[2]) >= self.Recov_period:
          self.Infect = -1
          self.color = "Grey"
          self.Is_Going_2_Die = False

      if self.Quarentine == True and self.Infected < 0:
        self.Quaretine = False
      elif self.Quarentine == False and np.random.uniform(0,1) <= 0.98:
        if self.Infect == 2 and np.random.uniform(0,1) <= p_test_symp:
          self.Quarentine = True
        elif self.Infect == 3 and np.random.uniform(0,1) <= p_test_asymp:
          self.Quarentine = True

  def Att_Quarentine(self):
    if self.Infect < 0:
      self.Quarentine = False

    elif self.Quarentine == True:
      self.Set_P0(np.array([100,100]))            # Still need to think where quarentine will ocour.

class Student(People):
  def __init__(self, Inst, Infect, Position, Vaci, Velocity, Quaren, Imune, V0, Time, Age, Incub_period, Death_period, Recov_period, Infectivity):
      super().__init__(Inst, Infect, Position, Vaci, Velocity, Quaren, Imune, V0, Time, Age, Incub_period, Death_period, Recov_period, Infectivity)
      self.color =  {0:"Green",1:"Red",2:"Blue"}[Infect]
      self.Schedule = {}

  def schedule(self, inst, initial_class_offered):
  # Create a schedule based on the institute that you specified 
  # Note that the inst_list needs to have the institutes listed in the same order as the institutes in the p_list
    class_offered = initial_class_offered

    inst_list = ["IFGW","IC", "IMECC"]
    if inst == "IFGW":                                        # These are the probabilities of somoene who is in IFGW taking a class in each istitute
      p_IFGW = 0.7                                            # For now, these are done manualy. We may need to find another way of doing it 
      p_IC = 0.1                                               
      p_IMECC = 0.2
      
    if inst == "IMECC":
      p_IFGW = 0.05
      p_IC = 0.25
      p_IMECC = 0.7

    if inst == "IC":
      p_IFGW = 0
      p_IC = 0.8
      p_IMECC = 0.2

    p_list =  [p_IFGW,p_IC,p_IMECC]
    d = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    t = [7,8,9,10,11,14,15,16,17,19,20,21,22,23]
    for i in d:
      self.Schedule[i] = {}                      # Times in wich you may have classes
      for j in t:
        self.Schedule[i][j] = ''
      if random.randint(1,2) == 1:
        self.Schedule[i][12] = 'Bandeco'
        self.Schedule[i][13] = ''
      else:
        self.Schedule[i][13] = 'Bandeco'
        self.Schedule[i][12] = ''
      self.Schedule[i][18] = 'Bandeco'
    student_classes = []
    for j in range(12):                                             # In the future I might change this to take in consideration the distribution of classes in a certain time, in order to be more realistic
      inst_class= np.random.choice(inst_list,p =p_list)
      if len(class_offered[inst_class]) != 0:
        a = random.randint(0, len(class_offered[inst_class]) - 1)
        day, hour, place = class_offered[inst_class][a]
        class_offered[inst_class].pop(a)
        self.Schedule[day][hour] = place
        self.Schedule[day][hour + 1] = place
        student_classes.append([day, hour, place, inst_class])
    return student_classes

class Professor(People):
  def __init__(self, Inst, Infect, Position, Vaci, Velocity, Quaren, Imune, V0, Time, Age, Incub_period, Death_period, Recov_period, Infectivity):
      super().__init__(Inst, Infect, Position, Vaci, Velocity, Quaren, Imune, V0, Time, Age, Incub_period, Death_period, Recov_period, Infectivity)
      self.color =  {0:"black",1:"Red",2:"Blue"}[Infect]
      self.Schedule = {}
      d = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
      t = [7,8,9,10,11,14,15,16,17,19,20,21,22,23]
      for i in d:
        self.Schedule[i] = {}                      # Times in wich you may have classes
        for j in t:
          self.Schedule[i][j] = ''
        if random.randint(1,2) == 1:
          self.Schedule[i][12] = 'Bandeco'
          self.Schedule[i][13] = ''
        else:
          self.Schedule[i][13] = 'Bandeco'
          self.Schedule[i][12] = ''
        self.Schedule[i][18] = 'Bandeco'
      self.cont = 0

  def Add_class(self, day, hour, place):
    self.cont = self.cont + 1
    self.Schedule[day][hour] = place
    self.Schedule[day][hour + 1] = place
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

