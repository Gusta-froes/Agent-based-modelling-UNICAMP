from Classes import *
import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation
def create_classes(num_class, unicamp_dict):
  classes = {}

  for i in num_class:
    classes[i] = []
    for j in range(num_class[i]):
     # day = -1
     # hour = -1
      aux = 0
      options = list(unicamp_dict['classroom'].keys()) + [i]
      while aux == 0 and len(options) != 0:
        place = np.random.choice(options)
        if place in unicamp_dict['classroom']:
          type_place = 'classroom'
        else:
          type_place = 'institute'
        if len(list(unicamp_dict[type_place][place].free_date.keys())) != 0:
          aux = 1
          day = np.random.choice(list(unicamp_dict[type_place][place].free_date.keys()))
          hour = np.random.choice(unicamp_dict[type_place][place].free_date[day])
          unicamp_dict[type_place][place].free_date[day].remove(hour)
          if len(unicamp_dict[type_place][place].free_date[day]) == 0:
            del unicamp_dict[type_place][place].free_date[day]
          classes[i].append([day, hour, place])
        else:
          options.remove(place)

  return classes


def Create_Population(n, class_offered, inst_distrib, vaci_prob, infect_prob, symp_prob, imune_prob):
  # Creates a population for the University
  # n is the number of people you want to create
  # inst_distrib is the percentage of people in each institute: Needs to be a dictionary e.g.: {"IC": 0.25, "IFGW": 0.25, "IMECC": 0.5}
  # vaci_prob is the probability of someone beeing vacinated
  # infect_prob is the probaility of someone beeing infected in the beginning of the simulation
  # symp_prob is the probability of someone infected showing symptoms
  # imune _prob is the probability of someone beeing imune in the beginning of the simulation


  pop = []
  professor = []
  inst_list = list(inst_distrib.keys())
  inst_p = []
  buff = 0
  vac_efi = 97/100

  for i in inst_list:
    buff += inst_distrib[i]
    inst_p.append(buff)


  for i in range(n):
    p_inst = random.randint(1,100)/100
    p_infect = random.randint(1,100)/100
    p_vaci =  random.randint(1,100)/100
    p_vaci_efi = random.randint(1,100)/100
    p_symp =  random.randint(1,100)/100
    p_imune =  random.randint(1,100)/100

    index = 0
    for j in inst_p:
      if p_inst <= inst_p[index]:
        inst = inst_list[index]
        index = 0
        break
      index += 1


    pop = []
    inst_list = list(inst_distrib.keys())
    inst_p = []
    n_inst = len(inst_list)
    buff = 0
    vac_efi = 0

    for i in inst_list:
        buff += inst_distrib[i]
        inst_p.append(buff)


    for i in range(n):
        p_inst = random.randint(1,100)/100
        p_infect = random.randint(1,100)/100
        p_vaci =  random.randint(1,100)/100
        p_vaci_efi = random.randint(1,100)/100
        p_symp =  random.randint(1,100)/100
        p_imune =  random.randint(1,100)/100

        index = 0
        for j in inst_p:
            if p_inst <= inst_p[index]:
                inst = inst_list[index]
                index = 0
                break
            index += 1

        imune = False
        if p_imune <= imune_prob:
            imune = True

        vaci = False
        if p_vaci <= vaci_prob and imune == False:
            vaci = True
        if p_vaci_efi <= vac_efi:
            imune = True

        infect = 0
        if p_infect <= infect_prob and imune == False:
            if p_symp <= symp_prob:
                infect = 2
            else:
                infect = 3                  # Infected and symptomatic: infect = 2, Infected and Assymptomatic: infect = 3, Exposed: infect = 1, Susceptible: infect = 0, Recovered: infect = -1, Dead: infect = -2


        incub_period = np.round(np.random.lognormal(1.5, 0.6, 1))[0]
        death_period = np.round(np.random.lognormal(2.84, 0.58,1))[0]
        recov_period = np.round(np.random.gamma(2.2, 6.36, 1))[0]
        infectivity = np.random.gamma(1, 0.2, 1)[0]
        while infectivity > 1:
                            infectivity = np.random.gamma(1, 0.2, 1)[0]

        x = np.random.randint(-15,15)
        y = np.random.randint(-15,15)
        student = Student(inst,infect,np.array([x,y]),vaci,np.array([0,0]),False,  imune,np.array([0,0]),["Mon",7,1],20,incub_period,death_period,recov_period,infectivity)
        student_classes = student.schedule(inst, class_offered)
        pop.append(student)

        for s in student_classes:
          aux = 0
          day = s[0]
          hour = s[1]
          place = s[2]
          inst_class = s[3]
          for b in professor:
            if b.Schedule[day][hour] == '' and b.cont <=4 and b.Inst == inst_class and aux == 0:
              b.Add_class(day, hour, place)
              aux = 1
          if aux == 0:
            Tessler = Professor(inst_class, 0, np.array([0,0]), False, np.array([0,0]), False, False, np.array([0,0]), ["Mon",7], 40, 1,1,1,1)
            Tessler.Add_class(day, hour, place)
            professor.append(Tessler)
            pop.append(Tessler)
        for s in professor:
          s.Fill_schedule()
    return pop

def Generate_University(Institute_list,fig,ax) -> None:
  for i in Institute_list:
    r = np.sqrt(i.area/np.pi)
    area = plt.Circle(i.location,r,fc = "lightblue", zorder = 0)
    ax.add_patch(area)

def random_walk (V) -> np.ndarray:
  theta  = np.random.choice(360)*np.pi/180
  v = np.array([1,1])/(np.linalg.norm([1,1])) * V             #V = "Size" of the velocity vector
  M = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta),np.cos(theta)]])
  v = M.dot(v)
  return v


def detect_collision (p1, p2,R) -> bool:
  if abs(p2.Position[0]-p1.Position[0]) > R:
    return False
  if abs(p2.Position[1]-p1.Position[1]) > R:
    return False

  if (p1.Position[1] - p2.Position[1])**2 + (p1.Position[0] - p2.Position[0])**2 <= R**2:
    return True

def solve_collision(p1,p2) -> None:
    sig = 1.9/3
    d = (p1.Position[0]-p2.Position[0])**2 + (p1.Position[1]-p2.Position[1])**2
    prob = abs(-np.exp(-(1/2) * d/sig) - np.random.uniform(0,1))
    if prob <= p1.Infectivity:
        p2.Infectivity = np.random.gamma(0.65, 0.2)
        while p2.Infectivity > 1:
              p2.Infectivity = np.random.gamma(0.65, 0.2)
        print("Um "+ str(p1.Infect) + " expos um " + str(p2.Infect))
        p2.Att_State(1)


def Sweep_n_prune(People,R) -> None:
  """
  This function is responsible to detect all the possible "Collisions" ( pair of people that enter the maximum infectious radius of eachother) in a time complexity better than O(n^2), where n = len(People)
  """
  #Sort people by the x-axis
  People = sorted(People, key=lambda People: People.Position[0])
  active = []
  collision_set = set()
  for i in People:
    if i.Quaren == False:
        if len(active)>1:
          #If there is at least one person in the active list and the interval of all the list coincides
          if abs(active[0].Position[0] - i.Position[0]) <= R:
            active.append(i)
          # If the new person does not bellong to the currente interval we check all the collisions in the active list
          else:
            for j in active:
              for k in active:
                if (j.Infect >= 1 or k.Infect >=1) and not (j.Infect >= 1 and k.Infect >=1 ) and not(j.Infect <0 or k.Infect <0 ) and detect_collision(j, k, R):
                    if j.Infect>=1:
                        collision_set.add((j,k))
                    else:
                        collision_set.add((k,j))

            # We then remove the first item of the active list, since all of his possible collsions have been checked
            active.remove(active[0])

            # We now start to remove all the itens of the active list, until the new item is in the interval of someone inside the active list or the active list is empty
            for j in active:
              if abs(j.Position[0] - i.Position[0]) <= R or len(active) == 0:
                active.append(i)
                break

              else:
                active.remove(j)
        else:
            active.append(i)

  # We can now solve all the collisions
  for i in collision_set:
    solve_collision(i[0],i[1])
