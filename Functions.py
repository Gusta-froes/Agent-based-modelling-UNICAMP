from Classes import *
import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation

def Generate_Schedule(inst):
  # Create a schedule based on the institute that you specified 
  # Note that the inst_list needs to have the institutes listed in the same order as the institutes in the p_list

  inst_list = ["IFGW","IC", "IMECC"]

  if inst == "IFGW":                     # These are the probabilities of somoene who is in IFGW taking a class in each istitute
    p_IFGW = 0.7                          # For now, these are done manualy. We may need to find another way of doing it 
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
  d = ["Mon", "Tue", "Wed","Thu","Fri"]
  schedule = {}
  
  for i in range(5):
    schedule[d[i]] = {}
    t = [8,9,10,11,14,15,16,17,18,19,20]                      #  Times in wich you may have classes 
    for j in range(6):                                        # In the future I might change this to take in consideration the distribution of classes in a certain time, in order to be more realistic
       h = random.randint(0,len(t)-1)
       p = random.randint(1,100)/100
       schedule[d[i]][t[h]] = np.random.choice(inst_list,p =p_list)
       t.remove(t[h])
    for j in range(0,len(t)):
      schedule[d[i]][t[j]] = ""
    schedule[d[i]][12] = ""
    schedule[d[i]][13] = ""
    
  return schedule


def Create_Population(n,inst_distrib, vaci_prob, infect_prob, symp_prob, imune_prob, bus_prob):
  # Creates a population for the University 
  # n is the number of people you want to create
  # inst_distrib is the percentage of people in each institute: Needs to be a dictionary e.g.: {"IC": 0.25, "IFGW": 0.25, "IMECC": 0.5} 
  # vaci_prob is the probability of someone beeing vacinated 
  # infect_prob is the probaility of someone beeing infected in the beginning of the simulation
  # symp_prob is the probability of someone infected showing symptoms 
  # imune _prob is the probability of someone beeing imune in the beginning of the simulation 

  #adicionei prob de estar no onibus ?


  pop = []
  inst_list = list(inst_distrib.keys())
  inst_p = []
  n_inst = len(inst_list)
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


    schedule = Generate_Schedule(inst)
    pop.append(Student(inst,infect,np.array([0,0]),vaci,np.array([0,0]),False, schedule , imune,np.array([0,0]),["Mon",8], False))

  return pop

def Generate_University(Institute_list,fig,ax):
  for i in Institute_list:
    r = np.sqrt(i.area/np.pi)
    area = plt.Circle(i.location,r,fc = "lightblue", zorder = 0)      
    ax.scatter(i.location[0],i.location[1], color = "blue",zorder = 10)
    ax.add_patch(area)
  area_bus = plt.Rectangle((-10,10), 7, 5, fill=False, edgecolor = 'black') 
  ax.add_patch(area_bus) #gerar retangulo que é o busao


def random_walk (V):
  theta  = np.random.choice(360)*np.pi/180
  v = np.array([1,1])/(np.linalg.norm([1,1])) * V             #V = "Size" of the velocity vector 
  M = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta),np.cos(theta)]])
  v = M.dot(v)
  return v

