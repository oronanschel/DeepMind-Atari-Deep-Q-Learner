import re
import matplotlib.pyplot as plt
import numpy as np;
from matplotlib.backends.backend_pdf import PdfPages

from matplotlib.pyplot import savefig
import os
import sys 

# last results file name



PATH = "results/res1/"

filename = "res"+str(sys.argv[1]);

filepath = PATH+filename+".txt"


pp = PdfPages(PATH+filename+'.pdf')

steps_re  = []
self_eps = []
eval_avg_reward = []
eval_time = []
evalEpiNum = []
step_time = []
V = []
TD = []
q_a1= []    
q_a2 = []
q_a12 = []

qt_a1= []    
qt_a2 = []
qt_a12 = []

nerrors = []

flag = False;

itr  = 0
itr2 =0
itr3 = 0
args=""
itr4=0
file = open(filepath,'r')
for line in file:

    if line.startswith('Step Time'):
    #elif line.startswith('Eval_Time_outer'):
        line_s = line.split(':')
       # print line_s
        step_time.append(min(10,float(line_s[1])))
    elif line.startswith('eval_steps'):
        eval_steps = line; 
    elif line.startswith('Epsilon'):
        self_eps_s = line.split(":");
	self_eps.append(float(self_eps_s[1]))
    elif line.startswith('Weight norms:'):
        line = file.next()
        line_s = [line[line.find("[")+1:line.find("]")]]
        line_s = line_s[0].split(" ")
        if(not flag):
            layers_num  = len(line_s)/2
            layers_names = [[] for i in range(layers_num)]
            Weight_norms = [[] for i in range(layers_num)]
            Weight_max   = [[] for i in range(layers_num)]
            Weight_g_norms  = [[] for i in range(layers_num)]
            Weight_g_max   = [[] for i in range(layers_num)]
            for i in range(0,layers_num):
                layers_names[i].append(line_s[i*2])
                Weight_norms[i].append(float(line_s[i*2+1]))
            flag=True
        else:
            for i in range(0,layers_num):
                Weight_norms[i].append(float(line_s[i*2+1]))
    elif line.startswith('Weight max:'):
        line = file.next()
        line_s = [line[line.find("[")+1:line.find("]")]]
        line_s = line_s[0].split(" ")
        for i in range(0,layers_num):
            Weight_max[i].append(float(line_s[i*2+1]))
    elif line.startswith('Weight grad norms:'):
        line = file.next()
        line_s = [line[line.find("[")+1:line.find("]")]]
        line_s = line_s[0].split(" ")
        for i in range(0,layers_num):
            Weight_g_norms[i].append(float(line_s[i*2+1]))                    
    elif line.startswith('Weight grad max:'):
        line = file.next()
        line_s = [line[line.find("[")+1:line.find("]")]]
        line_s = line_s[0].split(" ")
        for i in range(0,layers_num):
            Weight_g_max[i].append(float(line_s[i*2+1]))                    

    elif line.startswith('NERRORS'):
        line_s = line.split(":")
        nerrors.append(float(line_s[1]))
    elif line.startswith('V'):
        line_s = line.split()
        V.append(float(line_s[1]))
        TD.append(float(line_s[4]))
        line = file.next()
        line = file.next()
        line_s = line.split(',')
        epinum_s = line_s[8].split(":")
        evalEpiNum.append(float(epinum_s[1]))

        steps_re_s = line_s[0].split(":")
        steps_re_s = steps_re_s[1].split("(")
        steps_re.append(float(steps_re_s[0]))

        re_s = line_s[1].split(":")
        eval_avg_reward.append(float(re_s[1]))
    elif line.startswith('Q_VALS:'): 
        line = file.next()
        line_s = line.split(":")
        line_s = line_s[:-1]
	a1 = [float(i) for i in line_s]
	q_a1.append(a1)
	line = file.next()
        line_s = line.split(":")
        line_s = line_s[:-1]
	a2 = [float(i) for i in line_s]
	q_a2.append(a2)
                  
        
print ('')
print ('------Results summary------')


# TD ERROR
#fig001 = plt.figure()
#plt.title(args)
#plt.savefig(PATH+filename+'TD.png')
#plt.savefig(pp, format='pdf')


# print 'Average Eval Episoides'+np.average(evalEpiNum)
if len(evalEpiNum)>1: 
    avgEvalEp =  np.average(evalEpiNum);
    print('Average number of eps for eavl ' + str(avgEvalEp))
    fig1 = plt.figure()
    title = 'Avg Test Episoide Reward over ' + str(format(avgEvalEp,'.1f'))+ ' Episoides'
    plt.title( title)
    print(len(steps_re))
    print(len(self_eps))
    plt.plot(self_eps,label="epsilon",linestyle='--',color='g')
#    plt.hold(True)
    plt.stem(eval_avg_reward,label="avg reward")  
    plt.xlabel('Steps')
    plt.ylabel('avg reward')
    plt.xlabel('eval itr')
    plt.legend(loc='best')
#    plt.savefig(PATH+filename+'_fig1.png')
    plt.savefig(pp, format='pdf')
    plt.close()

if len(q_a1)>1 and len(q_a2)>1 :
    # Q_a1
    fig021 = plt.figure()
    plt.subplot(1,2,2)
    _vmin = min(min(min(q_a1)),min(min(q_a2)))
    _vmax = max(max(max(q_a1)),max(max(q_a2)))
    
    plt.title('Q(right,s)')
    plt.imshow(q_a1,vmin=_vmin, vmax=_vmax,cmap='Greys',interpolation='none')
    plt.colorbar()
    #print(q_a1)
    
    plt.xlabel('state')
    plt.ylabel('eval_itr-make steps')
    #plt.savefig(PATH+filename+'TD.png')
    #plt.savefig(pp, format='pdf')
    
    # Q_a2
    plt.subplot(1,2,1)
    #fig021 = plt.figure()
    plt.title('Q(left,s)')
    plt.imshow(q_a2,vmin=_vmin, vmax=_vmax, cmap='Greys',interpolation='none')
    plt.colorbar()
    #print(q_a2)
    plt.xlabel('state')
    plt.ylabel('eval_itr-make steps')
    #plt.savefig(PATH+filename+'TD.png')
    plt.savefig(pp, format='pdf')
    plt.close()
    
    # Q_a12
    fig021 = plt.figure()
    plt.subplot(1,2,1)
    plt.title('Q(right,s)-Q(left,s)')
    #print(np.multiply(np.subtract(q_a2,q_a1),10000))
    sub_q = np.subtract(q_a1,q_a2)
    plt.imshow(np.sign(sub_q),vmin=-1, vmax=1, cmap='jet',interpolation='none')
    plt.colorbar()
    plt.xlabel('state')
    plt.ylabel('eval_itr-make steps')
    #plt.savefig(PATH+filename+'TD.png')
    #plt.savefig(pp, format='pdf')
    
    plt.subplot(1,2,2)
    plt.title('Q(right,s)-Q(left,s)')
    #print(np.multiply(np.subtract(q_a2,q_a1),10000))
    plt.imshow((np.subtract(q_a1,q_a2)) ,cmap='Greys',interpolation='none')
    plt.colorbar()
    plt.xlabel('state')
    plt.ylabel('eval_itr-make steps')
    #plt.savefig(PATH+filename+'TD.png')
    plt.savefig(pp, format='pdf')
    plt.close()
    
    n_states = len(q_a1[1])
    
    for s in range(0,n_states): 
        plt.figure()
        plt.title('Q('+str(s)+',*)')
        q_right = []
        q_left = []
        for j in range(0,len(q_a1)):
            q_right.append(q_a1[j][s])
            q_left.append(q_a2[j][s])
        plt.plot(q_right,color='b',label='Q('+str(s)+',right)')
        plt.plot(q_left,color='g',label='Q('+str(s)+',left)')
        plt.legend(loc='best')
        plt.savefig(pp, format='pdf')
        plt.close()
    


# TD ERROR
fig01 = plt.figure()
plt.title('TD ERROR')
plt.plot(TD)
plt.xlabel('eval itr')
#plt.savefig(PATH+filename+'TD.png')
plt.savefig(pp, format='pdf')
plt.close()

# V
fig02 = plt.figure()
plt.title('V')
plt.plot(V)
plt.xlabel('eval itr')
#plt.savefig(PATH+filename+'V.png')
plt.savefig(pp, format='pdf')
plt.close()

if(layers_num>0):
    # weights norm/max
    for i in range(0,layers_num):
        plt.figure()
        plt.title(layers_names[i])
        plt.plot(Weight_norms[i],label="Weight norm ")
        plt.plot(Weight_max[i],label="Weight max")
        plt.xlabel('eval itr')
        plt.legend(loc='best')
        plt.savefig(pp, format='pdf')
        plt.close()
    
        
    # weights g norm/max
    for i in range(0,layers_num):
        plt.figure()
        plt.title(layers_names[i])
        plt.plot(Weight_g_norms[i],label="Weight grad norm ")
        plt.plot(Weight_g_max[i],label="Weight grad max")
        plt.xlabel('eval itr')
        plt.legend(loc='best')
        plt.savefig(pp, format='pdf')
        plt.close()
        
    
    

pp.close()


