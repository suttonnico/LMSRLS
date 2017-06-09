import numpy as np
import math
import cmath
from scipy import signal

class lms(object):
    def __init__(self,N):
        self.N=N
        self.w=np.random.rand(N)*0.01
        self.x=np.zeros(N)
        self.y=0
    def update(self,x,d,eta):
        self.x=self.x[:-1]
        self.x=np.insert(self.x,0,x)
        y=np.dot(self.x,self.w)
        self.w=self.w+2*eta*(d-y)*self.x
        self.y=y
        return y
    def coef(self):
        return self.w

class filtroTP(object):
        def __init__(self,ro,alpha,radio,periodo):
            self.ro=ro
            self.alpha=alpha
            self.periodo=periodo
            self.iteracion=0
            self.radio=radio
            self.y=np.zeros(4) #Arreglo para guardar y(n), y(n-1) e y(n-2)
            self.polo1=self.ro*cmath.exp(1.j*self.alpha)+self.radio*cmath.exp(1.j*(self.iteracion*2*math.pi/self.periodo+self.alpha))
            self.polo2=np.conjugate(self.polo1)
            self.a=signal.convolve([1.,-1],[1.,-2*np.absolute(self.polo1)*math.cos(np.angle(self.polo1)),np.absolute(self.polo1)**2])
            self.x=0
        def run(self,x):
            self.x=x
            self.polo1=self.ro*cmath.exp(1.j*self.alpha)+self.radio*cmath.exp(1.j*(self.iteracion*2*math.pi/self.periodo+self.alpha))
            self.polo2=np.conjugate(self.polo1)
            self.a=signal.convolve([1.,-1.],[1.,-2*np.absolute(self.polo1)*math.cos(np.angle(self.polo1)),np.absolute(self.polo1)**2])
            y=self.x-self.y[0]*self.a[1]-self.y[1]*self.a[2]-self.y[2]*self.a[3]
            self.y=self.y[:-1]
            self.y=np.insert(self.y,0,y)
            self.iteracion+=1
            if self.iteracion==self.periodo:
                self.iteracion=0
            return y
