import numpy as np




class Institute:
  def __init__ (self,location, area, name):
    self.location = location
    self.name = name
    self.area = area

class People:
  asym = 0.3
  global dt
  dt = 0.1
  p_test_symp = 0.7
  p_test_asymp = 0.1

  def __init__ (self,Inst, Infect, Position, Vaci, Velocity, Quaren, Schedule,Imune,Time, Age, Incub_period, Death_period, Recov_period, Infectivity):
    self.Inst = Inst
    self.Infect = Infect
    self.Position = Position
    self.Vaci = Vaci
    self.Velocity = Velocity
    self.Quaren = Quaren
    self.Schedule = Schedule
    self.Imune = Imune
    self.Time = Time
    self.Goal = Schedule[Time[0]][Time[1]]
    self.Age = Age
    self.Prob_Die = 0.0000457*np.exp(0.08952*self.Age)
    self.color =  {0:"Green",2:"Red",3:"Blue"}[Infect]
    self.Death_period = Death_period
    self.Incub_period = Incub_period
    self.Recov_period = Recov_period
    self.Infectivity = Infectivity
    self.Is_Going_2_Die = False
    self.timer = ["Mon",8,0]




  def Set_Goal(self):
    self.Goal = self.Schedule[self.Time[0]][self.Time[1]]


  def Att_Posi(self):
    self.Position = self.Position + self.Velocity*dt

  def Att_Time (self, Time):
    self.Time = Time
    self.Set_Goal()

  def Att_State (self, *args):
    if not self.Infect == -2:
      if len(args) > 0:
        self.timer = self.Time
        self.Infect = args[0]
        self.color =  {0:"Green",2:"Red",3:"Blue",1:"Green", -1:"Gray", -2:"Black"}[self.Infect]
      else:
        if (self.Time[2] - self.timer[2]) >= self.Death_period and self.Is_Going_2_Die == True:
          self.Infect = -2
          self.color =  "Black"

        elif (self.Time[2] - self.timer[2]) >= self.Incub_period and self.Infect == 1:

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

        elif (self.Time[2] - self.timer[2]) >= self.Recov_period and self.Infect >= 2:
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
    if self.Infect <= 1:
      self.Quarentine = False

    elif self.Quarentine == True:
      self.Set_P0(np.array([100,100]))            # Still need to think where quarentine will ocour.
