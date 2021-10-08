from Classes import *
import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation
def create_classes(num_professor, unicamp_dict):  # num_professor é um dicionário para a quantidade de professores para cada instituto
  #Esta função vai gerar a quantidade de professores desejada e vai preencher a agenda deles com duas aulas (4 horas na semana, cada) especificando lugar, hora e dia
  # É preciso fazer uma ginastica, registrando os horários já ocupados para que duas aulas não ocupem o mesmo ponto no espaço-tempo
  professors = {}
  for inst in num_professor:
    professors[inst] = []
    for j in num_professor[inst]:
      professors.append(Professor(inst, 0, np.array([0,0]), False, np.array([0,0]), False, False, np.array([0,0]), ["Mon",7], 40, 1,1,1,1))
  for inst in professors:
    for Tessler in professors[inst]:
      for n in range(2):  #Num de aulas que um professor ministra
        possible_places = list(unicamp_dict['Classroom'].keys())+[inst]
        for k in possible_places:
          if k in unicamp_dict['Classroom']:
            if list(unicamp_dict['Classroom'][k].free_date.keys()) == 0:
              possible_places.remove(k)
          else:
            if list(unicamp_dict['Institute'][k].free_date.keys()) == 0:
              possible_places.remove(k)
        if len(possible_places) != 0:
          place = np.random.choice(possible_places)
          if place in unicamp_dict['Classroom']:
            aux = 0
          else:
            aux = 1
          specie = ['Classroom', 'Institute'] #Apenas para facilitar o tipo de sala que estamos acessando, que será especificado pela variável "aux"
          day = np.random.choice(list(unicamp_dict[specie[aux]][place].free_date.keys()))
          hour = np.random.choice(unicamp_dict[specie[aux]][place].free_date[day])
          unicamp_dict[specie[aux]][place].free_date[day].remove(hour)
          if len(unicamp_dict[specie[aux]][place].free_date[day]) == 0:
            del unicamp_dict[specie[aux]][place].free_date[day]
          Tessler.Add_class(day, hour, place)
      Tessler.Fill_schedule()

  return professors


def Generate_Schedule(inst, professor):
# Create a schedule based on the institute that you specified
# Note that the inst_list needs to have the institutes listed in the same order as the institutes in the p_list

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
  Schedule = {}
  for i in d:
    Schedule[i] = {}                      # Times in wich you may have classes
    for j in t:
      Schedule[i][j] = ''
    if random.randint(1,2) == 1:
      Schedule[i][12] = 'Bandeco'
      Schedule[i][13] = ''
    else:
      Schedule[i][13] = 'Bandeco'
      Schedule[i][12] = ''
    Schedule[i][18] = 'Bandeco'
  for j in range(6):                                             # In the future I might change this to take in consideration the distribution of classes in a certain time, in order to be more realistic
    inst_class= np.random.choice(inst_list,p =p_list)
    possible_professor = professor[inst_class]
    Tessler = np.random.choice(possible_professor)
    while not Tessler.working:                     # Não podemos escolher um professor que não está dando aula
      possible_professor.remove(Tessler)           # Pode acontecer de termos professores que dão aula, mas não tem aluno
      Tessler = np.random.choice(possible_professor)
    n = random.randint(1,len(Tessler.classes))            # Sorteio o professor e depois sorteio a aula, dentre as ministradas pelo professor
    day, hour, place = Tessler.classes[n]
    Schedule[day][hour] = place
    Schedule[day][hour + 1] = place         # Se o sorteio cair dias vezes no mesmo lugar, o aluno fica com aula a menos
    if day == 'Mon':
      Schedule['Wed'][hour] = place
      Schedule['Wed'][hour + 1] = place     # Apenas aumenta a semelhança com os horários da Unicamp
    elif day == 'Thu':
      Schedule['Tue'][hour] = place
      Schedule['Tue'][hour + 1] = place
    else:
      Schedule[day][hour + 2] = place
      Schedule[day][hour + 3] = place
  return Schedule



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
        schedule = Generate_Schedule(inst, professor)
        student = Student(inst,infect,np.array([x,y]),vaci,np.array([0,0]),False,  imune,np.array([0,0]),["Mon",7,1],20,incub_period,death_period,recov_period,infectivity, schedule)
        pop.append(student)

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
        #print("Um "+ str(p1.Infect) + " expos um " + str(p2.Infect))
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
