# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 18:43:40 2019

@author: lukab
"""
import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import factorial
import math
smjer=1
brojac=0.1
tocke=[]



tocke=[]
tocke.append([0,0,0,1])
tocke.append([0, 10, 5, 1])
tocke.append([10, 10, 10, 1])
tocke.append([10, 0, 15 ,1])
tocke.append([0, 0, 20 ,1])
tocke.append([0, 10, 25 ,1])
tocke.append([10, 10, 30 ,1])
tocke.append([10, 0, 35 ,1])
tocke.append([0, 0, 40 ,1])
tocke.append([0, 10, 45 ,1])
tocke.append([10, 10, 50 ,1])
tocke.append([10, 0, 55 ,1])
tocke = np.array(tocke)
n=len(tocke)



# ČITANJE IZ DATOTEKE .obj
with open("prica.txt", "r") as f:
    txt=f.readlines()
v=[]
f=[]
for line in txt:
    if(line[0] == 'v'):
        v.append(line[1:].split())
    elif(line[0] == 'f'):
        f.append(line[1:].split())

for i in range(len(f)):
    for j in range(3):
        f[i][j] = int(f[i][j])
        f[i][j]-=1
for i in range(len(v)):
    for j in range(3):
        v[i][j] = float(v[i][j])
v=np.array(v)


def makeT(t):
    #prvi = (-1/6)*t*t*t + (3/6)*t*t - (3/6)*t + 1/6
    #drugi= (3/6) *t*t*t - 1*t*t     + (3/6)*t + 0
    #treci= (-3/6)*t*t*t + 0         + (3/6)*t + 0
    #cetvr= (1/6) *t*t*t + (4/6)*t*t + (1/6)*t + 0
    prvi = (-1/6)*t*t*t + (3/6)*t*t - (3/6)*t + 1/6
    drugi= (3/6) *t*t*t - 1*t*t     + 0 + 4/6
    treci= (-3/6)*t*t*t + (3/6)*t*t + (3/6)*t + 1/6
    cetvr= (1/6) *t*t*t 
    return np.array([prvi,drugi,treci,cetvr])

def makeTder(t):
    #prvi = (-1/2)*t*t + (3/2)*t - 3/2
    #drugi=        t*t -     2*t + 1
    #treci= (-1/2)*t*t +       0 + 1/2
    #cetvr= 0
    prvi = (-1/2)*t*t + t - 1/2
    drugi=  (3/2)*t*t -2*t
    treci= (-3/2)*t*t + t + 1/2
    cetvr=  (1/2)*t*t
    
    return np.array([prvi,drugi,treci,cetvr])


def vrati4Tocke(tocke, t):
    n=len(tocke)
    razmak = round(1/n,3)
    i=0

    while((n-4) != i):
        if(t>=i*razmak and t<=(i+1)*razmak):
            break
        i+=1
    return np.array([tocke[i], tocke[i+1], tocke[i+2], tocke[i+3]])

def norm_vector(vector):
    suma=0
    for i in range(len(vector)):
        suma+=vector[i]
    dj=np.sqrt(suma)
    return np.array([vector[0]/dj, vector[1]/dj, vector[2]/dj])
def mat_rot(os, alfa):
    os=norm_vector(os)
    sigma1 = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0], [-os[0], -os[1], -os[2], 1]])
    #sigma1 = np.array([[1,0,0,-os[0]],[0,1,0,-os[1]],[0,0,1,-os[2]],[0,0,0, 1]])
    
    sigma2 = np.array([[math.cos(alfa), math.sin(alfa), 0, 0], [-math.sin(alfa), math.cos(alfa), 0, 0],[0,0,1,0],[0,0,0,1]])
    
    sigma3 = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0], [os[0], os[1], os[2], 1]])
    #sigma3 = np.array([[1,0,0,os[0]],[0,1,0,os[1]],[0,0,1,os[2]],[0,0,0, 1]])
    
    #return np.dot(sigma1, np.dot(sigma2,sigma3))
    return np.dot(np.dot(sigma1,sigma2), sigma3)
    
    #return np.array([[math.cos(alfa),-math.sin(alfa),0,0],[math.sin(alfa),math.cos(alfa),0,0],[0,0,1,0],[0,0,0,1]])

    #return np.array([[math.cos(alfa),-math.sin(alfa),0,0],[math.sin(alfa),math.cos(alfa),0,0],[0,0,1,0],[0,0,0,1]])
def mat_trans(pt):
    return np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[pt[0], pt[1], pt[2], 1]])
    #return np.array([[1,0,0,os[0]],[0,1,0,os[1]],[0,0,1,os[2]],[0,0,0, 1]])


def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(round(dotproduct(v1, v2) / (length(v1) * length(v2)),3))
def convertToDeg(kut):
    return kut *180/math.pi

def racunajOS(poc, cilj, t):
    os = np.cross(poc[:3], cilj[t][:3])
    kut = angle(poc, cilj[round(t,2)])
    kutUStupnjevima = convertToDeg(kut)
    return os, kutUStupnjevima

def vrati4tockice(index):
    return np.array([tocke[index], tocke[index+1], tocke[index+2], tocke[index+3]])

#matrica = np.array([[-0.5,1.5,-1.5,0.5],[1,-2,1,0],[-0.5,0,0.5,0]])
#matrica2 = np.array([[-1/6,3/6,-3/6,1/6],[3/6,-1,3/6,0],[-3/6,0,3/6,0],[1/6,4/6,1/6,0]])

matrica2 = np.array([[-1/6,3/6,-3/6,1/6],[3/6,-1,3/6,0],[-3/6,0,3/6,0],[1/6,4/6,1/6,0]])
matrica  = np.array([[-0.5,1.5,-1.5,0.5],[1,-2,1,0],[-0.5,0,0.5,0]])

#poc= np.array([0.11833208, 2.4855998, 1.30321813, 0.0])#0,0,1,1
poc= np.array([0,0,1, 1])

def izrCilj():
    global koje_tocke
    global poc
    global tocke
    lista_ciljeva=[]
    #cilj=dict()
    #cilj = {round(new_list,2): [] for new_list in np.arange(0,1,0.01)}

    
    koje_tocke=0
    for i in range(len(tocke)-3):
        cilj=dict()
        cilj = {round(new_list,2): [] for new_list in np.arange(0,1,0.01)}
        chosen_tocke=None
        chosen_tocke = vrati4tockice(koje_tocke)
        print(chosen_tocke)
        
        for t in np.arange(0, 1, 0.01):
            t=round(t,2)

            uk = np.dot((3/8)*np.array([t*t*t, t*t, t, 1]), np.dot(matrica2, chosen_tocke))
            #parametrizitaniT =  makeT(t)
            #uk = parametrizitaniT[0]*chosen_tocke[0] + parametrizitaniT[1]*chosen_tocke[1] + \
            #     parametrizitaniT[2]*chosen_tocke[2] + parametrizitaniT[3]*chosen_tocke[3]
            cilj[t] = uk
        lista_ciljeva.append(cilj)
        koje_tocke+=1
    return lista_ciljeva


def izrOrj():
    global koje_tocke
    global poc
    global tocke
    lista_orjentira=[]
    koje_tocke=0
    for i in range(len(tocke)-3):
        orj =dict()
        orj = {round(new_list,2): [] for new_list in np.arange(0,1,0.01)}
        chosen_tocke=None
        chosen_tocke = vrati4tockice(koje_tocke)
        
        for t in np.arange(0, 1, 0.01):
            t=round(t,2)
            uk=np.dot(np.array([t*t, t, 1]), np.dot(matrica,chosen_tocke))
            #parametrizitaniTder =  makeTder(t)
            #uk = parametrizitaniTder[0]*chosen_tocke[0] + parametrizitaniTder[1]*chosen_tocke[1] + \
            #     parametrizitaniTder[2]*chosen_tocke[2] + parametrizitaniTder[3]*chosen_tocke[3]
            orj[t] = uk
        lista_orjentira.append(orj)
        koje_tocke+=1
    return lista_orjentira

lista_ciljeva = izrCilj()
lista_ciljna_orijentacija = izrOrj()# formula 1.4
koja_tocka=0
def tempf():
    global v, f
    global brojac
    global cilj
    global poc
    global lista_ciljna_orijentacija
    global koja_tocka

    Ap_crtaj3 = []
    Ap_crtaj4 = []

    os, alfa = racunajOS(poc, lista_ciljna_orijentacija[koja_tocka], brojac)
    print(brojac)
    print("aaaaa",str(koja_tocka))
    #potrebna_translacija = racunajPrvuFormulu(brojac)
    potrebna_translacija = lista_ciljeva[koja_tocka][brojac]

    matrica_rotacije = mat_rot(os, alfa)

    matrica_translac = mat_trans(potrebna_translacija)
    #print(os,alfa)
    for i,tocka in enumerate(v):
        tockaV = np.insert(tocka, len(tocka), 1)
        Ap_crtaj4.append(tockaV)
    
    
    #for i,tocka in enumerate(v):
    #    tockaV = np.insert(tocka, len(tocka), 1)
    #    Ap_crtaj4.append(np.dot(tockaV, np.dot(matrica_rotacije,matrica_translac)))
    
    
    #for i,tocka in enumerate(v):
     #   tockaV = np.insert(tocka, len(tocka), 1)
     #   Ap_crtaj3.append(np.dot(tockaV, matrica_translac))

 #   [0. 0. 0. 1.]
#[0.11833208 2.4855998  1.30321813 1.        ]
#[0.45078888 4.51289757 2.49186076 1.        ]
#[0.96356123 6.11945905 3.57531931 1.        ]
#[1.62283997 7.34284999 4.56298522 1.        ]
#[2.39481593 8.22063611 5.46424994 1.        ]#

    #for i,tocka in enumerate(Ap_crtaj3):
      #  Ap_crtaj4.append(np.dot(tocka, matrica_rotacije))

    #print(cilj[0.00])
    #print(cilj[0.01])
    #print(cilj[0.02])
    #print(cilj[0.03])
    #print(cilj[0.04])
    #print(cilj[0.05])



    x1l=[]
    y1l=[]
    x2l=[]
    y2l=[]
    x3l=[]
    y3l=[]
    z1l=[]
    z2l=[]
    z3l=[]

    for i,poligon in enumerate(f):
        for j,svaki in enumerate(poligon):
            if j==0:
                x1=Ap_crtaj4[svaki][0]
                y1=Ap_crtaj4[svaki][1]
                z1=Ap_crtaj4[svaki][2]
                x1l.append(x1)
                y1l.append(y1)
                z1l.append(z1)
            elif j==1:
                x2=Ap_crtaj4[svaki][0]
                y2=Ap_crtaj4[svaki][1]
                z2=Ap_crtaj4[svaki][2]
                x2l.append(x2)
                y2l.append(y2)
                z2l.append(z2)
            elif j==2:
                x3=Ap_crtaj4[svaki][0]
                y3=Ap_crtaj4[svaki][1]
                z3=Ap_crtaj4[svaki][2]
                x3l.append(x3)
                y3l.append(y3)
                z3l.append(z3)
    print()
    #print(Ap_crtaj4)
    #print(k)
    return x1l,y1l,x2l,y2l,x3l,y3l,z1l,z2l,z3l,os,alfa,potrebna_translacija,lista_ciljeva,lista_ciljna_orijentacija


def nacrtajObjekt2(x1l,y1l,x2l,y2l,x3l,y3l,z1l,z2l,z3l):
    #glScalef(0.15,0.15,0.15)
    for i in range(len(x1l)):
        glBegin(GL_LINE_LOOP)
        glVertex3f(x1l[i],y1l[i],z1l[i])
        glVertex3f(x2l[i],y2l[i],z2l[i])
        glVertex3f(x3l[i],y3l[i],z3l[i])
        glEnd()

def nacrtajKrivulju(cilj):
    glColor3f(1, 1.0, 1.0)
    
    for segment in range(len(cilj)):
        glBegin(GL_LINE_STRIP)
        for i in np.arange(0, 1, 0.01):
            i=round(i,2)
            glVertex3f(cilj[segment][i][0], cilj[segment][i][1], cilj[segment][i][2])
        glEnd()

def nacrtajTangentu(cilj, brojac, orijentir):
    global koja_tocka
    #if(brojac <0.79):
    #    konst = 0.20
    #else:
    #    konst = 0.01
    glColor3f(1.0,0.0,128/255)
    #glPointSize(7.5)
    glLineWidth(5)
    
    glBegin(GL_LINES)
    glVertex3f(cilj[koja_tocka][brojac][0], cilj[koja_tocka][brojac][1], cilj[koja_tocka][brojac][2])
    
    glVertex3f((1/6)*orijentir[koja_tocka][brojac][0], (1/6)*orijentir[koja_tocka][brojac][1], (1/6)*orijentir[koja_tocka][brojac][2])

    #glVertex3f(cilj[round(brojac+konst,2)][0], cilj[round(brojac+konst,2)][1], cilj[round(brojac+konst,2)][2])
    glEnd()
    


def nacrtajTocke():
    global tocke
    glPointSize(16)
    glBegin(GL_POINTS)
    glColor3f(0.5, 0.0, 1.0)
    glVertex3f(0,0,0)
    glEnd()
    
    glPointSize(16)
    glBegin(GL_POINTS)
    glColor3f(0.5, 0.0, 1.0)
    glVertex3f(0,10,5)
    glEnd()
    
    glPointSize(16)
    glBegin(GL_POINTS)
    glColor3f(0.5, 0.0, 1.0)
    glVertex3f(10,10,10)
    glEnd()
    
    glPointSize(16)
    glBegin(GL_POINTS)
    glColor3f(0.5, 0.0, 1.0)
    glVertex3f(10,0,15)
    glEnd()
    
    glPointSize(16)
    glBegin(GL_POINTS)
    glColor3f(0.5, 0.5, 1.0)
    glVertex3f(10,0,0)
    glEnd()
    
    glPointSize(16)
    glBegin(GL_POINTS)
    glColor3f(0.5, 0.5, 1.0)
    glVertex3f(0,10,0)
    glEnd()

    glPointSize(16)
    glBegin(GL_POINTS)
    glColor3f(0.5, 0.5, 1.0)
    glVertex3f(0,0,10)
    glEnd()
    
def crtajOsi():
    
    glColor3f(1.0,0.0,0.0) #red x
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex3f(-4.0, 0.0, 0.0)
    glVertex3f(16.0, 0.0, 0.0)
    glEnd()

    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex3f(16.0, 0.0, 0.0)
    glVertex3f(15.0, 1.0, 0.0)

    glVertex3f(16.0, 0.0, 0.0)
    glVertex3f(15.0, -1.0, 0.0)
    glEnd()
    glFlush()
    
    
    glLineWidth(1)
    glColor3f(0.0,1.0,0.0) #green y
    glBegin(GL_LINES)
    glVertex3f(0.0, -4.0, 0.0)
    glVertex3f(0.0, 16.0, 0.0)
    glEnd()

    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex3f(0.0, 16.0, 0.0)
    glVertex3f(1.0, 15.0, 0.0)
    
    glVertex3f(0.0, 16.0, 0.0)
    glVertex3f(-1.0, 15.0, 0.0)
    glEnd()
    glFlush()

    
    
    glColor3f(0.0,0.0,1.0) # blue z
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0 , -4.0 )
    glVertex3f(0.0, 0.0 , 16.0)
    glEnd()
    
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0 ,16.0)
    glVertex3f(0.0, 1.0 ,15.0)
 
    glVertex3f(0.0, 0.0, 16.0)
    glVertex3f(0.0, -1.0, 15.0)
    glEnd()
    #glFlush()
def renderScene():
    
    x1l,y1l,x2l,y2l,x3l,y3l,z1l,z2l,z3l,os,alfa,pot_tra,lista_ciljeva,lista_ciljna_orijentacija = tempf()

    #glTranslatef(350.0, 350.0, 0.0) # avion
    #glScalef(7.0, 7.0, 7.0) #avion

    #nacrtajOSI()
    #glTranslatef(-pot_tra[0], -pot_tra[1], -pot_tra[2])
    glPushMatrix()
    glTranslate(pot_tra[0],pot_tra[1],pot_tra[2])
    glRotate(alfa,os[0],os[1],os[2])
    glScale(.55,.55,.55)
    nacrtajObjekt2(x1l,y1l,x2l,y2l,x3l,y3l,z1l,z2l,z3l)
    glPopMatrix()

    nacrtajKrivulju(lista_ciljeva)
    
    nacrtajTangentu(lista_ciljeva, brojac,lista_ciljna_orijentacija)
    
    nacrtajTocke()
    
    crtajOsi()
    
    mijenjajOcisteIGledistePoBezierovojKrivulji()

    

def display():
    glClear(GL_COLOR_BUFFER_BIT)#| GL_DEPTH_BUFFER_BITclear buffers to preset values, | GL_DEPTH_BUFFER_BIT
    glColor3f(1.0, 1.0, 1.0)
    glLoadIdentity()
    glPushMatrix()
    glTranslatef(-3, -1, -13.0); # translatiraj z kameru uzrak ili ju priblizi
    glRotate(10, 1, 0, 0)
    glRotate(30, 0, 1, 0)  #2 reda prije pomaknes kameru ulijevo, ali onda treba rotirati sve oko y osi LOGICNO
    #glRotate(10, 0, 0, 1)
    glScalef(0.55,0.55,0.55)
    renderScene()
    
    glPopMatrix()
    glutSwapBuffers()


def reshape(width,height):
    #glDisable(GL_DEPTH_TEST)
    glViewport(0, 0, GLsizei(width) , GLsizei(height))
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
    #glOrtho(0,width-1, height-1,0,0,1)
    glMatrixMode(GL_MODELVIEW)
    #glLoadIdentity()
    #pass
    



def mijenjajOcisteIGledistePoBezierovojKrivulji():
    global O,G,p,smjer,brojac,koja_tocka
    #if(brojac < 0.20):
    #brojac += 0.01
    #if(brojac < 0.20):
    #brojac+=0.01
    #brojac = round(brojac, 2)
    if(brojac ==  0.99):
        koja_tocka+=1
        brojac = 0.00
    elif(brojac == 0.99 and koja_tocka==len(tocke)-3):
        smjer = (-1)*smjer
    #if(brojac == 0.00 and koja_tocka==0):
    else:
        brojac+=0.01
        brojac=round(brojac,2)
    print(koja_tocka)
    #if(brojac==0.98 or brojac==0.01):
     #   smjer = (-1)*smjer
    
    #if(smjer == 1):
    #    brojac+=0.01
    #    brojac=round(brojac,2)
        #O = p[brojac]
    #elif(smjer == -1):
    #    brojac-=0.01
    #    brojac=round(brojac,2)
    
    #if(brojac==0.99):
    #    brojac-=0.01
    #    brojac=round(brojac,2)
    #elif(brojac==0.00):
    #    brojac+=0.01
    #    brojac=round(brojac,2)

#INIT
glutInit()
glutInitDisplayMode(GLUT_DOUBLE) # dva graficka spremnika- prikaz na zaslonu a u drugi se crta slijedeca scena
#glutInitWindowSize(1024,768)
glutInitWindowSize(1900,900)
#glutInitWindowPosition(200,200)
glutInitWindowPosition(5,5)
glutCreateWindow("1. domaca zadaca u Pythonu iz RA")
glutDisplayFunc(display)# bez ovoga no display callbackregistered for window 1
glutReshapeFunc(reshape)

#glutTimerFunc(20,timer,0)
glutIdleFunc(display)
glutMainLoop()