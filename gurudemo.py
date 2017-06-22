from scipy.stats import expon
from scipy.stats import norm
from scipy.stats import foldnorm
from scipy.stats import gennorm
from scipy.stats import truncexpon
from scipy.stats import truncnorm
from scipy.stats import triang
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import Tkinter as Tk
import sys
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
import time


class Data:
    pass

data = Data()

def RBSimulation():
    global data
    data.nodes = []
    data.N=100
    data.repu = []
    data.malicious = []
    data.nrmember = []
    data.toStart = False
    data.total=0
    data.cycle=1
    data.success=0
    data.cyclesuccess=0
    data.badblocks = 0
    data.successcyclectr = 0
    data.cyclesuccessrate = [0]
    data.trustedfaultynoderate = []
    data.ogproportions = []
    data.successes=[]
    data.overallbadnodes = 0
    data.M= 5000

    #for i in range(0,data.M):
     #   tmprepu = float(InitialRepu(data.dist))
      #  data.nodes.append(guruNode(tmprepu,random.random()<((alpha0-0.05)*(1-tmprepu)+0.05)))
    #data.nodes.sort(key = lambda x: x.repu, reverse=True)   

    data.proprate = 10
    fig=plt.Figure()
    fig.set_size_inches(16,11,forward=True)
    repfig = fig.add_subplot(2,2,3)
    repfig.set_ylabel("Reputation")
    #repfig.xlabel("Nodes in order by Reputation")
    sucfig = fig.add_subplot(2,1,1)
    
    sucfig.set_ylim(ymax=100,ymin=0)
    #faultfig = fig.add_subplot(2,2,4)
    barfig = fig.add_subplot(2,2,4,axisbg='blue')
    repfig.set_ylabel("Reputation")
    repfig.set_xlabel("Nodes ordered by reputation")

    
    sucfig.set_ylabel("Successes over 100 rounds")
    sucfig.set_xlabel("Number of rounds x100")


    barfig.set_ylabel("Number of malicious nodes in a tuple")
    barfig.set_xlabel("Nodes grouped in 1/10th of all nodes sized tuples, ordered by reputation")
    fig.tight_layout()
    
    fig2 = plt.Figure()
    malfig = fig2.add_subplot(1,1,1,axisbg='blue')
    fig2.set_size_inches(5,1.5,forward=True)
    malfig.tick_params(
    axis='both', which='both', bottom='off', top='off', left='off', right='off', labelbottom='off', labelleft='off')
    

    #print('Overall portion of bad nodes', float(overallbadnodes)/float(M))
    #print(ogproportions)

    def StartSim(totalnodes,ogrepudist,alpha00,select):
        data.nodes = []
        data.repu = []
        data.malicious = []
        data.nrmember = []
        data.toStart=True
        data.total=0
        data.cycle=1
        data.success=0
        data.cyclesuccess=0
        data.badblocks = 0
        data.successcyclectr = 0
        data.cyclesuccessrate = [0]
        data.trustedfaultynoderate = []
        data.ogproportions = []
        data.successes=[]
        data.overallbadnodes = 0
        data.toTrack = False

        
        
        data.M = int(totalnodes)
        if ogrepudist == 'No Distribution':
            data.dist = "no"
        elif ogrepudist == 'Exponential':
            data.dist = "exp"
        elif ogrepudist == 'Normal':
            data.dist = "norm"
        data.alpha0 = float(alpha00)
        for i in range(0,data.M):
            tmprepu = float(InitialRepu(data.dist))
            data.nodes.append(guruNode(tmprepu,random.random()<((data.alpha0-0.05)*(1-tmprepu)+0.05)))
        data.nodes.sort(key = lambda x: x.repu, reverse=True)
        if select == 'Filter':
            data.sel = "filter"
        elif select == 'Triangular':
            data.sel = "triang"
        elif select == 'Exponential':
            data.sel = "exp"
        data.ogrepu = [node.ogrepu for node in data.nodes]


    def animate(i):
        animcount=0

        while animcount < 100 and data.toStart==True:
            #print(i)
            animcount += 1
            data.cycle += 1
            data.goodround, data.badround, data.nodes= RBRound(data.nodes, data.M, data.N, data.total, sum(data.successes),data.sel, data.dist)
            if data.goodround:
                data.success += 1
                data.cyclesuccess += 1
                data.successes.append(1)
                if len(data.successes)>100:
                    data.successes.pop(0)
            else:
                data.successes.append(0)
                if len(data.successes)>100:
                    data.successes.pop(0)
            if data.badround:
                data.badblocks += 1
            if data.cycle>100:
                data.cycle = 1
                data.successcyclectr += 1
                data.cyclesuccessrate.append(data.cyclesuccess)
                data.cyclesuccess = 0
            data.total += 1
         


        #faulty90=0
        #overall90=0
        #index=0
        if data.total>0:
            #while index<data.M/10 and overall90<data.M:
                #overall90 += 1
                #if data.nodes[index].malicious:
                    #faulty90 += 1
                #index += 1
            #print('Rate of faulty trusted nodes at round', data.total, float(faulty90)/float(overall90))
            #data.trustedfaultynoderate.append(float(faulty90)/float(overall90))
            propsets=[ps*(data.M/data.proprate) for ps in range(0,10)]
            proportions=[]
            allbadnodes = 0
            for i in range(0,data.proprate):
                badnode = 0
                for j in range(0,data.M/data.proprate):
                    if data.nodes[i*data.M/data.proprate+j].malicious:
                        badnode += 1
                        allbadnodes += 1
                proportions.append(float(badnode)/float(data.M/data.proprate))
            repfig.clear()
            sucfig.clear()
            #faultfig.clear()
            barfig.clear()
            sucfig.set_ylim(ymax=100,ymin=0)
            barfig.set_ylim(ymax=data.M/data.proprate,ymin=0)
            barfig.set_xlim(xmax=data.M,xmin=0) 
            repfig.set_xlim(xmax=data.M,xmin=0)
            repfig.plot([node.repu for node in data.nodes])
            repfig.plot(data.ogrepu,color='r')

            repfig.set_ylabel("Reputation")
            repfig.set_xlabel("Nodes ordered by reputation")

            
            sucfig.set_ylabel("Successes over 100 rounds")
            sucfig.set_xlabel("Number of rounds x100")


            barfig.set_ylabel("Number of malicious nodes in a tuple")
            barfig.set_xlabel("Nodes grouped in 1/10th of all nodes sized tuples, ordered by reputation")

            sucfig.plot(data.cyclesuccessrate) 
            #faultfig.plot(data.trustedfaultynoderate)
            barfig.bar(propsets,[pp*(data.M/data.proprate) for pp in proportions],width=data.M/data.proprate,color='orange')
            for vline in range(1,10):
                barfig.axvline(x=vline*(data.M/data.proprate),color='black')
            
            if data.toTrack:
                tn = data.M-1
                while not data.nodes[tn].isTracked:
                    tn -= 1
                ps=0
                while tn> ps*(data.M/data.proprate):
                    ps += 1
                ps = ps-1
                tn_local = ((ps+1)*(data.M/data.proprate)) - tn
                barfig.bar(ps*(data.M/data.proprate),5,bottom=tn_local-1,width=(data.M/data.proprate),color='green')
                repfig.plot(tn, data.nodes[tn].repu, color='g',marker = "o")
                #print(str(tn) + ' ' + str(tn_local))
            fig.tight_layout()
            
        #print(str(end-start))
    
    
    
        

    def BotnetTakeover(botnodes):
        if int(botnodes) < 0:
            allbadnodes = []
            for nd in range(0,data.M):
                if not data.nodes[nd].malicious:
                    allbadnodes.append(nd)
            btnd = abs(int(botnodes))
            while 0 < btnd and 0 < len(allbadnodes):
                bn = random.randint(0,len(allbadnodes)-1)
                data.nodes[allbadnodes[bn]].malicious = True
                data.nodes[allbadnodes[bn]].isTracked = False
                btnd -= 1
                allbadnodes.pop(bn)
        else:
            allbadnodes = []
            for nd in range(0,data.M):
                if data.nodes[nd].malicious:
                    allbadnodes.append(nd)
            btnd = abs(int(botnodes))
            while 0 < btnd and 0 < len(allbadnodes):
                bn = random.randint(0,len(allbadnodes)-1)
                data.nodes[allbadnodes[bn]].malicious = False
                btnd -= 1
                allbadnodes.pop(bn)

    def SybilJoin(sybilnodes):
        if int(sybilnodes) < 0:
            for bd in range(0,abs(int(sybilnodes))):
                data.nodes.append(guruNode(0,True))
        else:
            for bd in range(0,abs(int(sybilnodes))):
                data.nodes.append(guruNode(0,False))
        data.M = len(data.nodes)
        if data.M > 0:
            data.toStart = True
                
    def RemoveNodes(botnodes):
        if int(botnodes) > 0:
            allbadnodes = []
            for nd in range(0,data.M):
                if not data.nodes[nd].malicious:
                    allbadnodes.append(nd)
            btnd = abs(int(botnodes))
            toPop = []
            while 0 < btnd and 0 < len(allbadnodes):
                bn = random.randint(0,len(allbadnodes)-1)
                toPop.append(allbadnodes[bn])
                btnd -= 1
                allbadnodes.pop(bn)
            toPop.sort(reverse=True)
            for tp in toPop:
                data.nodes.pop(tp)
        else:
            allbadnodes = []
            for nd in range(0,data.M):
                if data.nodes[nd].malicious:
                    allbadnodes.append(nd)
            btnd = abs(int(botnodes))
            toPop = []
            while 0 < btnd and 0 < len(allbadnodes):
                bn = random.randint(0,len(allbadnodes)-1)
                toPop.append(allbadnodes[bn])
                btnd -= 1
                allbadnodes.pop(bn)
            toPop.sort(reverse=True)
            for tp in toPop:
                data.nodes.pop(tp)
        data.M = len(data.nodes)
        if data.M==0:
            data.nodes = []
            data.N=100
            data.repu = []
            data.malicious = []
            data.nrmember = []
            data.toStart = False
            data.total=0
            data.cycle=1
            data.success=0
            data.cyclesuccess=0
            data.badblocks = 0
            data.successcyclectr = 0
            data.cyclesuccessrate = [0]
            data.trustedfaultynoderate = []
            data.ogproportions = []
            data.successes=[]
            data.overallbadnodes = 0
            data.M= 5000 



    
    def SelectionFunc(select): 
        if select == 'Filter':
            data.sel = "filter"
        elif select == 'Triangular':
            data.sel = "triang"
        elif select == 'Exponential':
            data.sel = "exp"

    
    def malAnim(i):
        malfig.clear()
        malfig.set_xlim(xmin=0,xmax=1)
        malfig.set_ylim(ymin=0,ymax=1)
        allbadnodes = float(sum(int(nd.malicious) for nd in data.nodes))/data.M
        Tk.Label(root, text=("%.2f" % round(allbadnodes,2))).grid(column=1,row=44,sticky="w")
        Tk.Label(root, text=("%.2f" % round(1-allbadnodes,2))).grid(column=3,row=44,sticky="e")
        malfig.barh(0,allbadnodes,height=1, color='orange')

    def toTrackFunc(tracked):
        for nd in data.nodes:
            nd.isTracked = False
        tck = abs(int(tracked) % data.M)
        data.toTrack=True
        tckp = tck
        bbl = 0
        found = False
        fnl=0
        while not found:
            if tck < data.M:
                if not data.nodes[tck].malicious:
                    found = True
                    data.nodes[tck].isTracked = True
            if tckp >= 0:
                if not data.nodes[tckp].malicious:
                    found = True
                    data.nodes[tckp].isTracked = True
            bbl += 1
            tck += bbl
            tckp -= bbl


    root = Tk.Tk()
    root.geometry('{}x{}'.format(1700, 900))
    label = Tk.Label(root,text="Guru Simulation").grid(column=0, row=0, columnspan=4)
    canvas1 = FigureCanvasTkAgg(fig, master=root)
    canvas1.get_tk_widget().grid(column=0,row=1,rowspan=45)
   
    canvas2 = FigureCanvasTkAgg(fig2, master=root)
    canvas2.get_tk_widget().grid(column=1,row=45,rowspan=10,columnspan=3)
    

    Tk.Label(root, text="Botnet:").grid(column=1,row=5,sticky="w")
    botnetF = Tk.Entry(root)
    botnetF.grid(column=2,row=5,sticky="w")
    #botnetB.bind("<Return>",lambda:BotnetTakeover)
    botnetB = Tk.Button(root,text="Go!", command = lambda: BotnetTakeover(botnetF.get())).grid(column=3,row=5,sticky="w")
    
    Tk.Label(root, text="Sybil:").grid(column=1,row=6,sticky="w")
    sybilF = Tk.Entry(root)
    sybilF.grid(column=2,row=6,sticky="w")
    #botnetB.bind("<Return>",lambda:BotnetTakeover)
    sybilB = Tk.Button(root,text="Go!", command = lambda: SybilJoin(sybilF.get())).grid(column=3,row=6,sticky="w")
    
    Tk.Label(root, text="Remove:").grid(column=1,row=7,sticky="w")
    removeF = Tk.Entry(root)
    removeF.grid(column=2,row=7,sticky="w")
    #botnetB.bind("<Return>",lambda:BotnetTakeover)
    removeB = Tk.Button(root,text="Go!", command = lambda: RemoveNodes(removeF.get())).grid(column=3,row=7,sticky="w")   
    
    Tk.Label(root, text="Selection:").grid(column=1,row=4,sticky="w")
    selvar= Tk.StringVar(root)
    selchoices=('Exponential','Triangular','Filter')
    selvar.set('Exponential')
    selMenu = Tk.OptionMenu(root, selvar, *selchoices)
    selMenu.grid(row=4,column=2,sticky="w")
    selMenuB = Tk.Button(root, text="Go!", command = lambda: SelectionFunc(selvar.get())).grid(column=3, row=4,sticky="w")

    
    nrnodesF = Tk.Entry(root)
    nrnodesF.grid(row=1,column=2,sticky="w")
    Tk.Label(root, text="Number of Nodes:").grid(column=1,row=1,sticky="w")

    alpha0F = Tk.Entry(root)
    alpha0F.grid(row=2,column=2,sticky="w")
    Tk.Label(root, text="Maliciousness:").grid(column=1,row=2,sticky="w")

    Tk.Label(root, text="Source Reputation:").grid(column=1,row=3,sticky="w")
    repuvar= Tk.StringVar(root)
    repuchoices=('Normal','Exponential','No Distribution')
    repuvar.set('No Distribution')
    repuMenu = Tk.OptionMenu(root, repuvar, *repuchoices)
    repuMenu.grid(row=3,column=2,sticky="w")
    selMenuB = Tk.Button(root, text="Start!", command = lambda: StartSim(nrnodesF.get(),repuvar.get(),alpha0F.get(),selvar.get())).grid(column=3, row=3,sticky="w")
    
    Tk.Label(root, text="Track node").grid(column=1,row=8,sticky="w")
    toTrackF = Tk.Entry(root)
    toTrackF.grid(column=2,row=8,sticky="w")
    toTrackB = Tk.Button(root,text="Go!",command = lambda:toTrackFunc(toTrackF.get())).grid(column=3,row=8,sticky="w")
    

    anim = animation.FuncAnimation(fig,animate,7) 
    anim2 = animation.FuncAnimation(fig2,malAnim,1000) 

    Tk.mainloop()
        
def RBRound(nodes, M, N, total, cclsucc, sel, dist):
    global data 
    correctValidator = 0
    threshold = float(2*N) / 3
    badthreshold = float(N) / 3
    scrt = float(cclsucc)/100
    #print(scrt)
    fail = []
    validators = WeightedRandom(sel, M, N, total, dist)
    for i in range(0, N):
        #print(validators[i])
        if not nodes[validators[i]].malicious:
            correctValidator += 1
        nodes[validators[i]].nrmember += 1
    for i in range(0, N):
        if correctValidator>threshold or correctValidator<badthreshold:
            nodes[validators[i]].reward(scrt)
        else:
            nodes[validators[i]].penalty(scrt)
    def getKey(item):
        return item[0]
    nodes.sort(key = lambda x: x.repu, reverse=True)
    return correctValidator>threshold, correctValidator<badthreshold, nodes

def WeightedRandom(sel, M, N, total, dist):
    if dist == "no":
        if sel == "exp":
            rand = []
            expvar=M
            ctr = 100
            final = (-float(M))/math.log(0.05)
            while ctr<total and expvar > final:
                expvar = expvar - 500
                ctr += 100
            if expvar < final:
                expvar=final
            if total < 0:
                for i in range(0,N):
                    rand.append(random.randint(0,M-1))
                    while rand.count(rand[i]) > 1:
                        rand[i]=random.randint(0,M-1)
            else:
                for i in range(0,N):
                    rand.append(int(expon.rvs(scale=expvar)))
                    if rand[i]<0:
                        rand[i] = - rand[i]
                    while rand[i] >=M or rand.count(rand[i])>1:
                        rand[i] = int(expon.rvs(scale=expvar))
                        if rand[i]<0:
                            rand[i] = - rand[i]
        elif sel=="filter":
            rand = []
            epscale = M
            ctr = 100
            while ctr<total and epscale != 1000:
                epscale = epscale - 500
                ctr += 100
            if total < 0:
                for i in range(0,N):
                    rand.append(random.randint(0,M-1))
                    while rand.count(rand[i]) > 1:
                        rand[i]=random.randint(0,M-1)
            else:
                for i in range(0,N):
                    rand.append(int(gennorm.rvs(5,scale=epscale)))
                    if rand[i]<0:
                        rand[i] = - rand[i]
                    while rand[i] >=M or rand.count(rand[i])>1:
                        rand[i] = int(gennorm.rvs(5,scale=epscale))
                        if rand[i]<0:
                            rand[i] = - rand[i]
        elif sel == "triang":
            rand = []
            triscale = M*2
            ctr = 100
            final=M
            while ctr<total and triscale > M:
                triscale = triscale - 1000
                ctr += 100
            if triscale <= M:
                triscale = M+int(round(M/5))
            if total < 0:
                for i in range(0,N):
                    rand.append(random.randint(0,M-1))
                    while rand.count(rand[i]) > 1:
                        rand[i]=random.randint(0,M-1)
            else:
                for i in range(0,N):
                    rand.append(int(triang.rvs(0,loc=0,scale=triscale)))
                    if rand[i]<0:
                        rand[i] = - rand[i]
                    while rand[i] >=M or rand.count(rand[i])>1:
                        rand[i] = int(triang.rvs(0,loc=0,scale=triscale))
                        if rand[i]<0:
                            rand[i] = - rand[i]
    else:
        if sel == "exp":
            rand = []
            expvar=(-float(M))/math.log(0.05)
            if total < 0:
                for i in range(0,N):
                    rand.append(random.randint(0,M-1))
                    while rand.count(rand[i]) > 1:
                        rand[i]=random.randint(0,M-1)
            else:
                for i in range(0,N):
                    rand.append(int(expon.rvs(scale=expvar)))
                    if rand[i]<0:
                        rand[i] = - rand[i]
                    while rand[i] >=M or rand.count(rand[i])>1:
                        rand[i] = int(expon.rvs(scale=expvar))
                        if rand[i]<0:
                            rand[i] = - rand[i]
        elif sel=="filter":
            rand = []
            epscale = M/5
            if total < 0:
                for i in range(0,N):
                    rand.append(random.randint(0,M-1))
                    while rand.count(rand[i]) > 1:
                        rand[i]=random.randint(0,M-1)
            else:
                for i in range(0,N):
                    rand.append(int(gennorm.rvs(5,scale=epscale)))
                    if rand[i]<0:
                        rand[i] = - rand[i]
                    while rand[i] >=M or rand.count(rand[i])>1:
                        rand[i] = int(gennorm.rvs(5,scale=epscale))
                        if rand[i]<0:
                            rand[i] = - rand[i]
        elif sel == "triang":
            rand = []
            triscale = M+int(round(M/10))
            if total < 0:
                for i in range(0,N):
                    rand.append(random.randint(0,M-1))
                    while rand.count(rand[i]) > 1:
                        rand[i]=random.randint(0,M-1)
            else:
                for i in range(0,N):
                    rand.append(int(triang.rvs(0,loc=0,scale=triscale)))
                    if rand[i]<0:
                        rand[i] = - rand[i]
                    while rand[i] >=M or rand.count(rand[i])>1:
                        rand[i] = int(triang.rvs(0,loc=0,scale=triscale))
                        if rand[i]<0:
                            rand[i] = - rand[i]

    return rand

def InitialRepu(dist):
    if dist == "no":
        temp = 0
    elif dist == "norm":
        temp = norm.rvs(loc=0.5,scale=0.15)
        while temp<0 or 1<temp:
            temp = norm.rvs(loc=0.5, scale=0.5)
    elif dist == "exp":
        temp = expon.rvs(scale=0.3)
        while temp<0 or 1<temp:
            temp = expon.rvs(scale=0.3)
    return temp
   


class guruNode:
    global data
    def __init__(self, repu, malicious):
        self.repu = repu
        self.malicious = malicious
        self.maxrepu = repu
        self.minrepu = repu
        self.ogrepu = repu
        self.nrmember = 0
        self.isTracked = False

    def reward(self, scrt):
        if data.sel=="triang":
            self.repu += (1-scrt)*((1-self.repu)/(35))
        else:
            self.repu += (1-scrt)*((1-self.repu)/(10))
        if self.repu > self.maxrepu:
            self.maxrepu = self.repu

    def penalty(self, scrt):
        if data.sel=="triang":
            self.repu -= scrt*(self.repu/(35))
        else:
            self.repu -= scrt*(self.repu/(10))
        if self.repu < self.minrepu:
            self.minrepu = self.repu

    
RBSimulation()
    
   
#Arguments: 1. selection function(exp, triang, filter) 2. external repu distribution(norm, exp, no) 3. number of nodes 4. size of the committee 5. alpha0 6. alpha1 7. number of rounds 8. number of tests 9. nopic/pic (graphs or no graphs)
