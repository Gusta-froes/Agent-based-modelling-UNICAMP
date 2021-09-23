from Classes import *
from Functions import *
import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation

inst_distrib = {}
inst_distrib["IMECC"] = 50
inst_distrib["IFGW"] = 80
inst_distrib["IC"] = 30

buff = 0
for i in inst_distrib:
  buff += inst_distrib[i]

for i in inst_distrib:
  inst_distrib[i] = inst_distrib[i]/buff

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

IFGW = Institute(np.array([30,30]), 150, "IFGW", 'blue')
IMECC = Institute(np.array([30,-30]), 150, "IMECC", 'blue')
IC = Institute(np.array([-30,-30]), 150, "IC", 'blue')
CB01 = Classroom(np.array([10,10]), 50, 'CB01', 'gray')
CB02 = Classroom(np.array([10,-10]), 50, 'CB02', 'gray')
CB03 = Classroom(np.array([-10,10]), 50, 'CB03', 'gray')
Bandeco = Restaurant(np.array([-45,45]), 300, 'Bandeco', 'pink')
Unicamp = University(np.array([0,0]), 1000)
unicamp_dict = {'institute':{"IFGW":IFGW,"IC":IC, "IMECC": IMECC}, 'classroom':{'CB01': CB01, 'CB02': CB02, 'CB03':CB03}}
num_class = {'IFGW': 12, 'IMECC': 12, 'IC': 12}

class_offered = create_classes(num_class, unicamp_dict)

people = Create_Population(100, class_offered ,inst_distrib,10/100,10/100,10/100,10/100)



inst_dict = {"IFGW":IFGW,"IC":IC, "IMECC": IMECC, 'CB01': CB01, 'CB02': CB02, 'CB03':CB03, 'Bandeco': Bandeco}
inst_list = [IFGW,IC,IMECC, CB01, CB02, CB03, Bandeco]

frames =1700
d = 0
day ='Mon'
h = 0
hour =7
hour_dict = {0:7,1:8,2:9,3:10,4:11,5:12,6:13,7:14,8:15,9:16,10:17,11:18,12:19,13:20,14:21,15:22,16:23}
day_dict = {0:"Mon",1:"Tue",2:"Wed",3:"Thu",4:"Fri"}

time = ["Mon",7,0]


def animate (p,frames):
  global d,h,day,day_dict,hour_dict,hour,time
  ax.clear()
  Generate_University(inst_list,fig,ax)
  d_time = int(frames/5)
  h_time = int(d_time/17)
  aux = 0

  if p > d_time*(d+1):
    d += 1
    h = 0
    day = day_dict[d%5]
    hour = hour_dict[h]
    for k in people:
        time = [day,hour,d]
        k.Att_Time(time)
        k.Att_State()
        k.Att_Quarentine()


  if  p > d_time*(d) + h_time*(h+1):
    h += 1
    hour = hour_dict[h]
    time = [day,hour,d]


  if h == 16:
    aux = 1

  run_clas = int(h_time/3) - 1

  time = [day,hour,d]
  for i in people:
    i.Att_Time(time)
    i.Att_State()
    if i.Quaren == False:
        if not i.Goal == "":

          if (i.Position[0]-inst_dict[i.Goal].location[0])**2 + (i.Position[1]-inst_dict[i.Goal].location[1])**2 <= inst_dict[i.Goal].area / (2*np.pi):
            if p - int(h_time/4) < d_time*(d) + h_time*(h):
              i.Velocity = random_walk(16)
            else:
              i.Velocity = random_walk(1)
          else:
            v0 = (inst_dict[i.Goal].location - i.Position)/(np.linalg.norm((inst_dict[i.Goal].location - i.Position))) * 16
            i.Set_V0(v0 + random_walk(0.1))

        else:
          i.Set_V0( random_walk(8))
          for k in inst_list:
            if (i.Position[0]-k.location[0])**2 + (i.Position[1]-k.location[1])**2 <= k.area / (np.pi/2):
               v0 = (k.location - i.Position)/(np.linalg.norm((k.location - i.Position))) * (-16)
               i.Set_V0( v0 + random_walk(0.1))
        if aux == 0:
            if not i.Schedule[time[0]][time[1]+1] == '':
              if p + run_clas > d_time*(d) + h_time*(h+1):
                v0 = (inst_dict[i.Schedule[time[0]][time[1]+1]].location - i.Position)/(0.05* (run_clas))
                i.Set_V0( v0 + random_walk(0.1))
        else:
          v0 = (Unicamp.location - i.Position)/(np.linalg.norm((Unicamp.location - i.Position))) * (-16)
          i.Set_V0( v0 + random_walk(4))

        i.Att_Posi()

    ax.scatter(i.Position[0],i.Position[1], color = i.color ,marker = "o")

  ax.set_title( str(time[0]) + " - " + str(time[1])+ "hrs - Dia:" +str(time[2]+1))
  Sweep_n_prune(people, 2)


#ax.set_xlim(30)
#ax.set_ylim(30)

anim = animation.FuncAnimation(fig, animate, interval = 100, fargs = [frames], save_count = frames )

anim.save("Simu.mp4")
