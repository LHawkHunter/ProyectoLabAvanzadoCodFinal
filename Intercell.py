#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 13:22:40 2021

@author: ging
"""

import numpy as np
import matplotlib.pyplot as plt

class Cell:
    population=[]
    def __init__(self,N,i,r):
        self.population = [1 for _ in range(i)] + [0 for _ in range(N - i)]
        
        self.counts = [(self.population.count(0), self.population.count(1))]
        while len(set(self.population))==2: #el proceso que sigue se repetira,
            G = np.random.rand()#genera un número aleatorio entre 0 y 1
            pBirth=[r*i/(r*i+N-i)]+[(N-i)/(r*i+N-i)] #vector probabilidad, de 1 y 0
            Birth=np.random.randint(N) 
            Death=np.random.randint(N)
            if Birth != Death: #aqui considero que la posicion del que nace y del que muere es distinta
                if G <=pBirth[0]: 
                    if self.population[Birth]==1 and self.population[Death]==0: #Añado las dos condiciones anteriores,
                #porque se deben cumplir ambas
                        self.population[Death] = self.population[Birth]
                        i=i+1
                    else:
                            if self.population[Birth]==1 and self.population[Death]==1:
                                self.population[Death] = self.population[Birth]
                  
                else:                
                        if self.population[Birth]==0 and self.population[Death]==1:
                            self.population[Death] = self.population[Birth]#aqui tambien se deben cumplir ambas
                            i=i-1
             
                        else:
                            if self.population[Birth]==0 and self.population[Death]==0:
                                self.population[Death] = self.population[Birth]
                            
            else:
                pass
            self.counts.append((self.population.count(0), self.population.count(1)))






            
            
#N=numero total de plasmidos
#i=número de plasmidos con mejor fitnes
#r=fitnes relativo
#m=numero de celulas
#k=número de celulas con plásmidos nb    
def morancell(Na,Nb,i,r,m,k,bc,tiempo):
    #se toma el fitness del plasmido cero, como igual a 1.
    
    #1ro: Se crea el grupo de células desde el laboratorio, es decir, nuestras condiciones iniciales
    pcell_ini=[Cell(Na,i,r).population for _ in range(k)] + [Cell(Nb,i,r).population for _ in range(m-k)]
#    print('celulas originales',pcell)#Imprime las celulas originales
    pcell=pcell_ini
    for _ in range(m):
        if set(pcell[_])=={1}:
            pcell[_].append(1)
    Nb = Na+1
#    print('celulas modificadas',pcell)#imprime las celulas originales con la modificacion
    #Esta parte es para el conteo.
    x=0

    for _ in range(m):
        if len(pcell[_])==Na:
            x=x+1
    
    counts = [(m-x,x)] #Donde m-x= a las celulas con Na+1 plásmidos
    
    y=[] #Esto me guarda el número de plásmidos fijados en cada competencia
    t2=[] #La generación en la cual ese número de plásmidos se fijaron.
#    print('Na=',Na)

    for t in range(tiempo):
        ##Aquí empezamos entonces, la competencia. 
#        print('Poblacion a competir', pcell)
        g=np.random.rand() #Esto genera el numero randon para hacer el proceso de seleccion
        f0=1/(1+bc*Na) #fitness de la célula tipo a
        f1=1/(1+bc*Nb) #fitness de la célula tipo b
        pBirth=[x*f0/((m-x)*f1+x*f0)]#probabilidad de nacer de la celula con plasmidos tipo Na
        Birth=np.random.randint(m) 
        Death=np.random.randint(m)
#        #De aquí para abajo comienza la competencia entre las células.
#        print('Na=',Na)
#        print('Nb=',Nb)
        if g<=pBirth[0]:
            if len(pcell[Birth])==Na and len(pcell[Death])==Nb:
                pcell[Death]=pcell[Birth]
                x=x+1
#                print('x sumado competencia=',x)
            else:
                if len(pcell[Birth])==Na and len(pcell[Death])==Na:
                    pcell[Death]=pcell[Birth]
        else:
            if len(pcell[Birth])==Nb and len(pcell[Death])==Na:
                pcell[Death]=pcell[Birth]
                x=x-1
#                print('x restado competencia=',x)
            else:
                if len(pcell[Birth])==Nb and len(pcell[Death])==Nb:
                    pcell[Death]=pcell[Birth]
        counts.append((m-x,x))
#        print('poblacion despues de la competencia',pcell)
#        print(counts[-1])
        
        
    #Generamos el numero aleatorio para ver si hay mutacion o no
        g2=np.random.rand()
        BirthMutada=np.random.randint(m) #elige al azar la celula que va a mutar

        #condicion que se debe cumplir para generar una mutacion
        z=[]
        for _ in range(m):
            z.append(len(pcell[_]))
        
            
       #Esta condición dice: Si la longitud del nñumero de entes
       #en el interior de la lista z es 1, lo cual significa que 
       #todas las celulas tienen el mismo numero de plasmidos.
        if len(set(z))==1 and g2<=0.2:
            t2.append(t)
            y.append(len(pcell[0]))
#            print('Mutacion!')
#            print('Mutó la célula=',BirthMutada)
            pcell[BirthMutada]=Cell(len(pcell[0]),1,1.1).population
#            print('P. Celulas despues de:',pcell)
#            print('Se ajusta el numero de plasmidos')
            if set(pcell[BirthMutada])=={1}:
                pcell[BirthMutada].append(1)
                Nb=len(pcell[BirthMutada])
                x=m-1
#                print('x mutacion 1:',x)
                if BirthMutada>=0 and BirthMutada<m-1:
                    Na=len(pcell[BirthMutada+1])
                elif BirthMutada==m-1:
                    Na=len(pcell[BirthMutada-1])
                
            else:
                pcell[BirthMutada].pop(0)
                Na=len(pcell[BirthMutada])
                x=1
#                print('x mutacion 0:',x)
                if BirthMutada>=0 and BirthMutada<m-1:
                    Nb=len(pcell[BirthMutada+1])
                elif BirthMutada==m-1:
                    Nb=len(pcell[BirthMutada-1])
        else:
            pass
#            print('no pasa nada')
#            print(pcell)
#            print(x,Na)
#            print(counts[-1])
    

    return pcell_ini,pcell,counts,t2,y

#morancell(Na,Nb,i,r,m,bc,tiempo)
#morancell(4,4,2,1.1,3,0.001,500)

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }
##Gráfica de competencia entre plásmidos: dos casos
#for _ in range(100):
#    a=np.array(Cell(100,20,1.1).counts)
#    plt.plot(a[:,0], color='blue')
#    plt.plot(a[:,1], color='orange')
#
#    plt.xlabel('Pasos',fontdict = font)
#    plt.ylabel('Población',fontdict = font, labelpad = 10)
#    plt.title('Naranja: plásmido con fitness relativo 1.1')
#plt.savefig("Comp_intracel_100p_20_with_1_1f.pdf",bbox_inches='tight')
#
#plt.figure()
#for _ in range(100):
#    a=np.array(Cell(100,50,1.1).counts)
#    plt.plot(a[:,0], color='blue')
#    plt.plot(a[:,1], color='orange')
#
#    plt.xlabel('Pasos',fontdict = font)
#    plt.ylabel('Población',fontdict = font, labelpad = 10)
#    plt.title('Naranja: plásmido con fitness relativo 1.1')
#plt.savefig("Comp_intracel_100p_50_with_1_1f.pdf",bbox_inches='tight')
#
#
##Gráfica de probabilidad de fijación en funcion del nñumero de plaśmidos.
#plt.figure()
#def fijacion(n,ii):
#    x=0
#    for j in range(n):
#        a=np.array(Cell(50,ii,1.1).population)
#        if a[0]==1:
#            x=x+1
#    return x
#def cerosVsfij(n,T):
#    counts2 = []
#    for p in range(T):
#        counts2.append((p,fijacion(n,p)))
#    gra=np.array(counts2)
#    plt.plot(gra[:,0], 1-gra[:,1]/n, 'o',color='blue')
#    plt.plot(gra[:,0], gra[:,1]/n, 'o',color='orange')
#    plt.xlabel('Número de plásmidos',fontdict = font)
#    plt.ylabel('Probabilidad de fijación',fontdict = font, labelpad = 10)
#    plt.savefig("fijacionplasmido_with_fitness_1_1.pdf",bbox_inches='tight')
#    return counts2
#
#cerosVsfij(100,50)

##Gráfica competencia intercelular 1

#p,c,t,y= morancell(5,5,2,1.1,100,50,0.00001,100000)
#
#plt.plot(c)
#plt.xlabel('Pasos',fontdict = font)
#plt.ylabel('Población',fontdict = font, labelpad = 10)
#plt.title('Naranja: células con menos plásmidos')
#plt.savefig("comp_intercell_5plas_2_100cel_50celNb_000001bc_100000t.pdf",bbox_inches='tight')

##Gráfica numero de plásmidos en función de la generacion

pini,p,c,t,y= morancell(10,10,5,1.1,20,1,0.00001,1000000000)
plt.plot(t,y)
plt.xlabel('Generación',fontdict = font)
plt.ylabel('Número de plásmidos',fontdict = font, labelpad = 10)
plt.savefig("NplasmidVsGeneracion_10plas_5_20cel_1celNb_000001bc_1000000000t.pdf",bbox_inches='tight')


##Gráfica número de plásmidos promedio en función del número de células
#l=[]
#for _ in range(2,50):
#    p,c,t,y= morancell(10,10,2,1.1,_,2,0.00001,200+_*500)
#    #print(y)
#    a=sum(y)/len(y)
#    l.append((_,a))
#
#u=np.array(l)
#print(u)
#plt.plot(u[:,0],u[:,1])
#plt.xlabel('Nñumero de células',fontdict = font)
#plt.ylabel('Número de plásmidos promedio',fontdict = font, labelpad = 10)
#plt.savefig("PlasVsCell_10plas_2celNb_000001bc.pdf",bbox_inches='tight')
#

