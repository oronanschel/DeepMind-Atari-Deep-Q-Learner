import re
import matplotlib.pyplot as plt
import numpy as np;
from matplotlib.pyplot import savefig
from ftplib import print_line

# last results file name
PATH = "DQN_unity/results/"
filename = "/res_67/res";

filepath = PATH+filename+".txt"


eval_avg_reward = []
eval_time = []
evalEpiNum = []
step_time = []
weights =  [[] for i in range(20)]
V = []
TD = []
    
flag = False;
itr  = 0
itr2 =0
itr3 = 0
file = open(filepath,'r')
for line in file:
#     if itr3 > 50000:
#         break
#     else:
#         itr3+=1
    if(flag):
        if itr == 0 or itr == 2 or itr == 4 or itr == 6 :
            line = line[:-2]
            for t in line.split():
                try:
                    w = float(t)
                    weights[itr2].append(w)
                    itr2+=1                   
                except ValueError:
                    pass
            if itr == 6:
                itr = 0
                itr2=0
                flag = False
                continue
        itr+=1
    
                

    if line.startswith('Eval report'):
        line_s = line.split(',')
        epinum_s = line_s[9].split(":")
        evalEpiNum.append(float(epinum_s[1]))
        re_s = line_s[2].split(":")
        eval_avg_reward.append(float(re_s[1]))
    elif line.startswith('Step Time'):
    #elif line.startswith('Eval_Time_outer'):
        line_s = line.split(':')
       # print line_s
        step_time.append(min(10,float(line_s[1])))
    elif line.startswith('eval_steps'):
        eval_steps = line;
    elif line.startswith('Weight norms:'):
        flag = True
    elif line.startswith('V'):
        line_s = line.split()
        V.append(float(line_s[1]))
        TD.append(float(line_s[4]))
    
                  
        
print ('')
print ('------Results summary------')
print (eval_steps)
# print 'Average Eval Episoides'+np.average(evalEpiNum)
if len(evalEpiNum)>1:
    avgEvalEp =  np.average(evalEpiNum);
    print('Average number of eps for eavl ' + str(avgEvalEp))
    # print('Average Steps Per Episoide:')
    
    # plot avg reward time
    fig1 = plt.figure()
    title = 'Avg Test Episoide Reward over ' + str(format(avgEvalEp,'.1f'))+ ' Episoides'
    plt.title( title)
    plt.plot(eval_avg_reward)
    plt.xlabel('Eval Session')
    plt.ylabel('avg reward')
    plt.savefig(PATH+filename+'_fig1.png')

# TD ERROR
fig01 = plt.figure()
plt.title('TD ERROR')
plt.plot(TD)
plt.xlabel('eval itr')
plt.savefig(PATH+filename+'TD.png')

# V
fig02 = plt.figure()
plt.title('V')
plt.plot(V)
plt.xlabel('eval itr')
plt.savefig(PATH+filename+'V.png')

# plot conv1 weight norm/max
fig3 = plt.figure()
plt.title('Conv 1')
plt.plot(weights[0],label="Weight norm ")
plt.plot(weights[5],label="Weight max")
plt.legend()
plt.xlabel('eval itr')
plt.savefig(PATH+filename+'Conv1.png')

# plot conv2 weight norm/max
fig4 = plt.figure()
plt.title('Conv 2')
plt.plot(weights[1],label="Weight norm")
plt.plot(weights[6],label="Weight max")
plt.legend()
plt.xlabel('eval itr')
plt.savefig(PATH+filename+'Conv2.png')

# plot conv3 weight norm/max
fig5 = plt.figure()
plt.title('Conv 3')
plt.plot(weights[2],label="Weight norm")
plt.plot(weights[7],label="Weight max")
plt.legend()
plt.xlabel('eval itr')
plt.savefig(PATH+filename+'Conv3.png')

# plot lin1 weight norm/max
fig5 = plt.figure()
plt.title('Linear 1')
plt.plot(weights[3],label="Weight norm")
plt.plot(weights[8],label="Weight max")
plt.legend()
plt.xlabel('eval itr')
plt.savefig(PATH+filename+'Lin1.png')

# plot lin2 weight norm/max
fig6 = plt.figure()
plt.title('Linear 2')
plt.plot(weights[4],label="Weight norm")
plt.plot(weights[9],label="Weight max")
plt.legend()
plt.xlabel('eval itr')
plt.savefig(PATH+filename+'Lin2.png')


# plot conv1 grad weight norm/max
fig7 = plt.figure()
plt.title('Conv 1 - grad')
plt.plot(weights[10],label="Weight Grad norm")
plt.plot(weights[15],label="Weight Grad max")
plt.legend()
plt.xlabel('eval itr')
plt.savefig(PATH+filename+'Conv1_g.png')

# plot conv2 grad weight norm/max
fig8 = plt.figure()
plt.title('Conv 2 - grad')
plt.plot(weights[11],label="Weight Grad norm")
plt.plot(weights[16],label="Weight Grad max")
plt.legend()
plt.xlabel('eval itr')
plt.savefig(PATH+filename+'Conv2_g.png')

# plot conv3 grad weight norm/max
fig5 = plt.figure()
plt.title('Conv 3 - grad')
plt.plot(weights[12],label="Weight Grad norm")
plt.plot(weights[17],label="Weight Grad max")
plt.legend()
plt.xlabel('eval itr')
plt.savefig(PATH+filename+'Conv3_g.png')


# plot lin1 grad weight norm/max
fig5 = plt.figure()
plt.title('Linear 1 - grad')
plt.plot(weights[13],label="Weight Grad norm")
plt.plot(weights[18],label="Weight Grad max")
plt.legend()
plt.xlabel('eval itr')
plt.savefig(PATH+filename+'Lin1_g.png')

# plot lin2 weight norm/max
fig6 = plt.figure()
plt.title('Linear 2 - grad')
plt.plot(weights[14],label="Weight Grad norm")
plt.plot(weights[19],label="Weight Grad max")
plt.legend()
plt.xlabel('eval itr')
plt.savefig(PATH+filename+'Lin2_g.png')


if False:
    # plot step time
    fig2 = plt.figure()
    plt.title('Step time in sec')
    plt.stem(step_time)
    plt.xlabel('Step')
    plt.ylabel('time[sec]')
    plt.savefig(PATH+filename+'_fig2.png')






