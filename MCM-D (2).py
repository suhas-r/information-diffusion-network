#random assignment case

#imports
from random import uniform,normalvariate,expovariate,shuffle
from math import log,exp,sqrt,factorial,floor

#define nodes, info classes; A, D, and P functions
class node(object):
    def __init__(self,x,y,ivector,age,cls,I,mvector):
        self.x = x
        self.y = y
        self.ivector = ivector
        self.age = age
        self.cls = cls
        self.I = I
        self.pvector = [x,y] + ivector + [age,cls]
        self.mvector = mvector

class info(object):
    def __init__(self,ivector):
        self.ivector = ivector

def A(teacher,info,t):
    k = 1
    total = 0
    for x in range(len(teacher.ivector)):
        total += teacher.ivector[x]*info.ivector[x]
    total = k * total * (1/(1+0.001001*1.467718**t))
    return total

def D(teacher,learner):
    k = 120
    total = 0
    ovector = [0.5,0.5] + [1/17]*17 + [0.5,0.5]
    for x in range(len(teacher.pvector)):
        total += ovector[x]*(teacher.pvector[x]-learner.pvector[x])**2
    total = (1+k*sqrt(total))/teacher.I
    return total

def P(K,learner,info,t,dispatcher):
    inv = 1
    for teacher in K:
        inv = inv * (1 - A(teacher,info,t)/D(teacher,learner))
    for x in range(4):
        inv = inv * (1 - learner.mvector[x] * dispatcher[x](t)) #dispatcher -- depends on time period
    return 1-inv

#create the population
n = 39   #population size
m1870 = [0.3118,0.0000,0.0000,0.0000]   #proportions of media usage -- depends on time period
m1920 = [0.3088,0.1425,0.0000,0.0000]
m1970 = [0.3028,0.7250,0.3184,0.0000]
m1990 = [0.2496,1.0000,0.3596,0.0920]
m2010 = [0.1403,0.8500,0.8918,0.8740]

L = []
for times in range(n):
    x = -1
    while x < 0 or x > 1:
        x = normalvariate(0.5,0.5/3)
    y = -1
    while y < 0 or y > 1:
        y = normalvariate(0.5,0.5/3)

    probsList = [
        [0.07,0.13,0.35,0.45],
        [0.07,0.15,0.34,0.44],
        [0.08,0.16,0.35,0.41],
        [0.15,0.21,0.33,0.30],
        [0.16,0.20,0.33,0.30],
        [0.18,0.22,0.32,0.27],
        [0.20,0.22,0.32,0.26],
        [0.19,0.22,0.33,0.25],
        [0.21,0.22,0.31,0.25],
        [0.30,0.20,0.25,0.24],
        [0.19,0.24,0.34,0,23],
        [0.24,0.24,0.30,0.21],
        [0.22,0.25,0.32,0.20],
        [0.26,0.27,0.29,0.17],
        [0.30,0.27,0.26,0.16],
        [0.25,0.29,0.31,0.14],
        [0.38,0.25,0.22,0.14]
            ]

    ivector = []
    for prob in probsList:
        rand = uniform(0,1)
        if rand < prob[0]:
            ivector.append(0)
        elif rand < prob[0]+prob[1]:
            ivector.append(1/3)
        elif rand < prob[0]+prob[1]+prob[2]:
            ivector.append(2/3)
        else:
            ivector.append(1)
    
    age = uniform(0,1)
    cls = -1
    while cls < 0 or cls > 1:
        cls = normalvariate(0.2,0.8/3)
    I = -1
    while I < 0 or I > 1:
        I = expovariate(log(1000))

    mvector = []
    rand = uniform(0,1)
    if rand < m1970[0]:
        mvector.append(1)
    else:
        mvector.append(0)
    rand = uniform(0,1)
    if rand < m1970[1]:
        mvector.append(1)
    else:
        mvector.append(0)
    rand = uniform(0,1)
    if rand < m1970[2]:
        mvector.append(1)
    else:
        mvector.append(0)
    rand = uniform(0,1)
    if rand < m1970[3]:
        mvector.append(1)
    else:
        mvector.append(0)

    L.append(node(x,y,ivector,age,cls,I,mvector))

#create the information
temporary = [0]*17
temporary[11] = 1
eisenhower = info(temporary)
temporary = [0]*17
temporary[8] = 1
explorer1 = info(temporary)

#initial conditions
t = 0
end = 36
DK = L
K = []

def zero(t):
    return 0

def one(t):
    return 1

#Poisson people
def crt_m(S):
    lambd = S/24
    rolling = 0
    for k in range(1,50):
        rolling += (exp(-lambd)*lambd**k)/factorial(k)

    rand = uniform(0, rolling)
    donkey = 0
    for k in range(1,S+1):
        donkey += (exp(-lambd)*lambd**k)/factorial(k)
        if rand < donkey:
            f0 = k/S
            break
    b = (1/f0) - 1
    q = (1/(999*b))**(1/24)
    def m(x):
        return ((1/(1+b*q**(x+1))) - (1/(1+b*q**(x)))) / (1 - (1/(1+b*q**(x))))
    return m

#dispatchers
IC = {0:one,1:one,2:one,3:one}
d1870 = {0:crt_m(floor(n*m1870[0])),1:zero,2:zero,3:zero}
d1920 = {0:crt_m(floor(n*m1920[0])),1:crt_m(floor(n*m1920[1])),2:zero,3:zero}
d1970 = {0:crt_m(floor(n*m1970[0])),1:crt_m(floor(n*m1970[1])),2:crt_m(floor(n*m1970[2])),3:zero}
d1990 = {0:crt_m(floor(n*m1990[0])),1:crt_m(floor(n*m1990[1])),2:crt_m(floor(n*m1990[2])),3:crt_m(floor(n*m1990[3]))}
d2010 = {0:crt_m(floor(n*m2010[0])),1:crt_m(floor(n*m2010[1])),2:crt_m(floor(n*m2010[2])),3:crt_m(floor(n*m2010[3]))}

#run model
while len(K) != n and t < end:
    switchList = []
    for person in DK:
        rand = uniform(0,1)
        prob = P(K,person,explorer1,t,d1970)
        if rand < prob:
            switchList.append(person)
    for switcher in switchList:
        K.append(switcher)
        DK.remove(switcher)
    print('K: ',len(K),' ','t: ',t)
    t += 1
