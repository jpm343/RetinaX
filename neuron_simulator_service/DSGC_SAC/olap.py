# -*- coding: utf-8 -*-
"""
Created on Fri Feb 05 20:10:26 2016

@author: Patricio
"""

import numpy as np
from neuron import h

def anglewithin(anglex, anglemin, anglemax):
    """
    Checks if anglex is within anglemin and anglemax
    """
    
    if anglemin > anglemax:
        if anglex < anglemax:
            anglex += np.pi*2
        anglemax += np.pi*2

    return anglemin < anglex and anglex < anglemax

def olap0(cell2,cell1,dend2,dend1,seg2,seg1,dx=1):
    """
    Calculates overlaping area between the arcs assigned to two segments
    
    --------------
    cell1: Neuron object. Must be of the DSRGC type
    cell2: Neuron object. Must be of SAC type
    dend1: Index of dendrite 1. Must be dend0
    dend2: Index of dendrite 2.
    seg1: Index of segment 1
    seg2: index of segment 2
    dx: spatial discretization for area calculation (default 1)
    
    returns
    -------
    Area of overlap
    """    
    
    x1=h.x3d(0,sec=cell1.soma)
    y1=h.y3d(0,sec=cell1.soma)
    x2=h.x3d(0,sec=cell2.soma)
    y2=h.y3d(0,sec=cell2.soma)
    l1=cell1.dend0[dend1].L
    l2=cell2.dend[dend2].L
    ns1=cell1.dend0[dend1].nseg
    ns2=cell2.dend[dend2].nseg    
    
    if (np.sqrt((x1-x2)**2+(y1-y2)**2)>=(l1+l2)):
        return 0

    ls=l1*(seg1+1)/ns1
    limoffset=np.array([[0, ls, -0.71*ls, 0.71*ls],
                        [-0.71*ls, 0.71*ls, 0, ls],
                        [-ls, 0, -0.71*ls, 0.71*ls],
                        [-0.71*ls, 0.71*ls, -ls, 0]])
    #Identificamos la posible area cubierta por la dendrita 1
    xmin1, xmax1, ymin1, ymax1 = np.array([x1,x1,y1,y1]) + limoffset[dend1]

    ls=l2*(seg2+1)/ns2
    limoffset=np.array([[0, ls, -0.71*ls, 0.71*ls],
                        [-0.71*ls, 0.71*ls, 0, ls],
                        [-ls, 0, -0.71*ls, 0.71*ls],
                        [-0.71*ls, 0.71*ls, -ls, 0]])
    #Identificamos la posible area cubierta por la dendrita 2
    xmin2, xmax2, ymin2, ymax2 = np.array([x2,x2,y2,y2]) + limoffset[dend2]

    if xmin1>xmax2 or xmin2>xmax1 or ymin1>ymax2 or ymin2>ymax1:
#        print " no overlap "
        return 0
                
    sumarea = 0
    
    #limites polares del segmento 1
    limd1 = seg1*l1/ns1			#limite segmento dendrita 1 (menor)	
    limd2 = (seg1+1)*l1/ns1		#limite segmento dendrita 1 (mayor)
    limang1 = (2*dend1-1)*np.pi/4  #limite angulo dendrita1
    limang2 = (2*dend1+1)*np.pi/4  #limite angulo dendrita2 (opuesta)
    limang1 -= 2*np.pi*(limang1>np.pi)
    limang2 -= 2*np.pi*(limang2>np.pi)    
    #limites polares del segmento 2
    limd3 = seg2*l2/ns2			#limite segmento dendrita 2 (menor)
    limd4 = (seg2+1)*l2/ns2		#limite segmento dendrita 2 (mayor)
    limang3 = (2*dend2-1)*np.pi/4		#limite angulo dendrita2
    limang4 = (2*dend2+1)*np.pi/4		#limite angulo dendrita1 (opuesta)
    limang3 -= 2*np.pi*(limang3>np.pi)
    limang4 -= 2*np.pi*(limang4>np.pi)    
    
    xlim1=max(xmin1,xmin2)    
    xlim2=min(xmax1,xmax2)
    ylim1=max(ymin1,ymin2)
    ylim2=min(ymax1,ymax2)    
    
    for x in np.arange(xlim1+dx/2,xlim2,dx):
        for y in np.arange(ylim1+dx/2,ylim2,dx): 
            #primero chequear que el punto pertenence al segmento 1
            d1 = np.sqrt((x-x1)**2+(y-y1)**2) 		#radio al segmento 1
            ang1 = np.arctan2(y-y1,x-x1)			#angulo al segmento 1

            if (d1>limd1 and d1<=limd2 and anglewithin(ang1,limang1,limang2)):	#Si limd1<d1<=limd2 y limang1 <ang1 <= limang2; osea si se encuentra en el rango
            #luego chequear si pertenece al segmento 2
                d2 = np.sqrt((x-x2)**2+(y-y2)**2)
                ang2 = np.arctan2(y-y2,x-x2)

                if (d2>limd3 and d2<=limd4 and anglewithin(ang2,limang3,limang4)):
                    sumarea += dx**2 # Eureka!!  Si limd3<d2<=limd4 y limang3<ang2<=limang4.
      #print x,y,d1,d2,ang1,ang2
  #print limd1,limd2,limd3,limd4
  #print limang1,limang2,limang3,limang4
    return sumarea
    
    
    
def olap1(cell2,cell1,dend2,dend1,seg2,seg1,dx=1):
    """
    Calculates overlaping area between the arcs assigned to two segments

    ----------------    
    cell1: Neuron object. Must be of the DSRGC type
    cell2: Neuron object. Must be of SAC type
    dend1: Index of dendrite 1. Must be dend1
    dend2: Index of dendrite 2.
    seg1: Index of segment 1
    seg2: index of segment 2
    dx: spatial discretization for area calculation (default 1)
    
    returns
    -------
    Area of overlap
    """    
    
    x1=h.x3d(0,sec=cell1.soma)
    y1=h.y3d(0,sec=cell1.soma)
    x2=h.x3d(0,sec=cell2.soma)
    y2=h.y3d(0,sec=cell2.soma)
    x10=h.x3d(0,sec=cell1.dend1[dend1])    
    x11=h.x3d(1,sec=cell1.dend1[dend1])    
    y10=h.y3d(0,sec=cell1.dend1[dend1])    
    y11=h.y3d(1,sec=cell1.dend1[dend1])    
    
    d1=np.sqrt(x10**2 + y10**2)    
    d2=np.sqrt(x11**2 + y11**2)
    
    l1=cell1.dend1[dend1].L
    l2=cell2.dend[dend2].L
    ns1=cell1.dend1[dend1].nseg
    ns2=cell2.dend[dend2].nseg    
    
    if (np.sqrt((x1-x2)**2+(y1-y2)**2)>=(l1+l2)):
        return 0
    
    limoffset=np.array([[d1*0.71, d2, -0.71*d2, 0],
                        [d1*0.71, d2, 0, 0.71*d2],
                        [0, 0.71*d2, 0.71*d1, d2],
                        [-0.71*d2, 0, 0.71*d1, d2],
                        [-d2, -0.71*d1, 0, 0.71*d2],
                        [-d2, -0.71*d1, -0.71*d2, 0],
                        [-0.71*d2, 0, -d2, -0.71*d1],
                        [0, 0.71*d2, -d2, -0.71*d1]])
    #Si distancia entre somas permite sobrelape de area entre dendritas, identificamos la posible area cubierta por la dendrita 1 para iterar ahí
    xmin1, xmax1, ymin1, ymax1 = np.array([x1,x1,y1,y1]) + limoffset[dend1]

    ls=l2*(seg2+1)/ns2
    limoffset=np.array([[0, ls, -0.71*ls, 0.71*ls],
                        [-0.71*ls, 0.71*ls, 0, ls],
                        [-ls, 0, -0.71*ls, 0.71*ls],
                        [-0.71*ls, 0.71*ls, -ls, 0]])
    #Si distancia entre somas permite sobrelape de area entre dendritas, identificamos la posible area cubierta por la dendrita 1 para iterar ahí
    xmin2, xmax2, ymin2, ymax2 = np.array([x2,x2,y2,y2]) + limoffset[dend2]

    if xmin1>xmax2 or xmin2>xmax1 or ymin1>ymax2 or ymin2>ymax1:
#        print " no overlap "
        return 0
        
    sumarea = 0
    
    #limites polares del segmento 1
    limd1 = d1 + (d2-d1)*seg1/ns1			#limite segmento dendrita 1 (menor)	
    limd2 = d1 + (d2-d1)*(seg1+1)/ns1		#limite segmento dendrita 1 (mayor)
    limang1 = (dend1-1)*np.pi/4  #limite angulo dendrita1
    limang2 = dend1*np.pi/4  #limite angulo dendrita2 (opuesta)
    limang1 -= 2*np.pi*(limang1>np.pi)
    limang2 -= 2*np.pi*(limang2>np.pi)
    
    #limites polares del segmento 2
    limd3 = seg2*l2/ns2			#limite segmento dendrita 2 (menor)
    limd4 = (seg2+1)*l2/ns2		#limite segmento dendrita 2 (mayor)
    limang3 = (2*dend2-1)*np.pi/4		#limite angulo dendrita2
    limang4 = (2*dend2+1)*np.pi/4		#limite angulo dendrita1 (opuesta)
    limang3 -= 2*np.pi*(limang3>np.pi)
    limang4 -= 2*np.pi*(limang4>np.pi)    

    xlim1=max(xmin1,xmin2)    
    xlim2=min(xmax1,xmax2)
    ylim1=max(ymin1,ymin2)
    ylim2=min(ymax1,ymax2)    
        
    for x in np.arange(xlim1+dx/2,xlim2,dx):
        for y in np.arange(ylim1+dx/2,ylim2,dx): 
            #primero chequear que el punto pertenence al segmento 1
            d1 = np.sqrt((x-x1)**2+(y-y1)**2) 		#radio al segmento 1
            ang1 = np.arctan2(y-y1,x-x1)			#angulo al segmento 1
	#si la suma es menor a 0
            if (d1>limd1 and d1<=limd2 and anglewithin(ang1,limang1,limang2)):	#Si limd1<d1<=limd2 y limang1 <ang1 <= limang2; osea si se encuentra en el rango
            #luego chequear si pertenece al segmento 2
                d2 = np.sqrt((x-x2)**2+(y-y2)**2)
                ang2 = np.arctan2(y-y2,x-x2)
                if (d2>limd3 and d2<=limd4 and anglewithin(ang2,limang3,limang4)):
                    sumarea += dx**2 # Eureka!!  Si limd3<d2<=limd4 y limang3<ang2<=limang4.
      #print x,y,d1,d2,ang1,ang2
  #print limd1,limd2,limd3,limd4
  #print limang1,limang2,limang3,limang4
    return sumarea

if __name__ == "__main__":
    h.load_file("SACtmp.hoc")
    h.load_file("dsrgc_temp.hoc")
    
    sac=h.SAC(4,120,0,0,3,3,1.5)
    ds1=h.DSRGC(120,0,0,3,1)
    
    print olap1(ds1,sac,7,3,1,2,1)
