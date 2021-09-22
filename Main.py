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


Peoples = Create_Population(100,inst_distrib,10/100,3/100,10/100,0)
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

IFGW = Institute(np.array([10,10]), 100, "IFGW")
IMECC = Institute(np.array([10,-10]), 100, "IMECC")
IC = Institute(np.array([-10,-10]), 100, "IC")
inst_dict = {"IFGW":IFGW,"IC":IC, "IMECC": IMECC}
inst_list = [IFGW,IC,IMECC]

frames =1040*8
d = 0
day ='Mon'
h = 0
hour =8
hour_dict = {0:8,1:9,2:10,3:11,4:12,5:13,6:14,7:15,8:16,9:17,10:18,11:19,12:20}
day_dict = {0:"Mon",1:"Tue",2:"Wed",3:"Thu",4:"Fri"}
time = ["Mon",8,0]

def animate (i,frames):
  global d,h,day,day_dict,hour_dict,hour,time
  ax.clear()
  Generate_University(inst_list,fig,ax)
  d_time = int(frames/10)
  h_time = int(d_time/13)


  if i > d_time*(d+1):
    d += 1
    h = 0
    day = day_dict[d%5]
    hour = hour_dict[h]
    for k in Peoples:
        time = [day,hour,d]
        k.Att_Time(time)
        k.Att_State()
        k.Att_Quarentine()


  if  i > d_time*(d) + h_time*(h+1):
    h += 1
    hour = hour_dict[h]
    time = [day,hour,d]


  for j in Peoples:
    j.Att_Time(time)
    j.Att_State()
    if j.Quaren == False:
        if not j.Goal == "":
          if (j.Position[0]-inst_dict[j.Goal].location[0])**2 + (j.Position[1]-inst_dict[j.Goal].location[1])**2 <= inst_dict[j.Goal].area / (2*np.pi):
            j.Velocity = random_walk(2)
          else:
            v0 = (inst_dict[j.Goal].location - j.Position)/(np.linalg.norm((inst_dict[j.Goal].location - j.Position))) * 2
            j.Velocity =  v0 + random_walk(4)
        else:
          j.Velocity =  random_walk(4)


        People.Att_Posi(j)
    ax.scatter(j.Position[0],j.Position[1], color =j.color,marker = "o")


  ax.set_title( str(time[0]) + " - " + str(time[1])+ "hrs - Dia:" +str(time[2]+1))
  Sweep_n_prune(Peoples, 2)


ax.set_xlim(20)
ax.set_ylim(20)

anim = animation.FuncAnimation(fig, animate, interval = 100, fargs = [frames], save_count = frames )

anim.save("Simu.mp4")
