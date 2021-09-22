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
        infect = 1                  # Infected and symptomatic: infect = 2, Infected and Assymptomatic: infect = 1, Not infected = 0


    student = Student(inst,infect,np.array([0,0]),vaci,np.array([0,0]),False, imune,np.array([0,0]),["Mon",7], 20, 1,1,1,1)
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

def Generate_University(Institute_list,fig,ax):
  for i in Institute_list:
    r = np.sqrt(i.area/np.pi)
    area = plt.Circle(i.location,r,fc = "lightblue", zorder = 0)
    ax.scatter(i.location[0],i.location[1], color = "blue",zorder = 10)
    ax.add_patch(area)

def random_walk(V):
  theta  = np.random.choice(360)*np.pi/180
  v = np.array([1,1])/(np.linalg.norm([1,1])) * V             #V = "Size" of the velocity vector 
  M = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta),np.cos(theta)]])
  v = M.dot(v)
  return v

