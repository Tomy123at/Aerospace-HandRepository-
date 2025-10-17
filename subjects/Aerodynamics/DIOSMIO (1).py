import numpy as np
b=8 # envergadura
s=10.7 #area
ar=b**2/s #aspect ratio
cav=s/b #cuerda promedio
lambdax=0.45
croot=(2*s)/(b*(1+lambdax)) #cuerda root
ctip=lambdax*croot #cuerda tip
htip=0 #deflexion en la punta en altura
betatip=np.arcsin(htip/ctip) #angulo de twist geometrico
craya=(2/3)*croot*(1+lambdax+lambdax**2)/(1+lambdax) #cuerda aerodinamica promedio
densidad=1.225 # densidad
vinf=88.056 #velocidad
uinf=1.78e-5 #viscocidad
posy=(b/6)*((1+2*lambdax)/(1+lambdax))
alfa=np.deg2rad(2) #alfa geomterico

npuntos=4 #numero de puntos "N"
def y(k):
    z=-(b/2)*(1-(2*k-1)/(2*npuntos))
    return z 
def theta(k):
    theta = np.arccos(-2*y(k)/b)
    return theta
def c(k):
    cleng=croot*(1-2*y(k)*((lambdax-1)/(b)))
    return cleng  
    
a0tip=6.363 #pendiente punta
a0root=6.436 #pendiente raiz

al0tip=0 #al=0 punta
al0root=0 #al=0 raiz
def a0(k):
    a0 = a0root -2*y(k)*(a0tip-a0root)/b
    return a0
def al0(k):
    al0 = al0root -2*y(k)*(al0tip-al0root)/b
    return al0
def b2(k):
    b2=np.arcsin(-2*y(k)*htip/b*c(k))
    return b2
def d(k):
    d=alfa-al0(k)+b2(k)
    return d

print(np.sin(45))
yk=list()
for i in range(1,npuntos+1):
    yk.append(y(float(i)))
ck=list()
for i in range(1,npuntos+1):
    ck.append(c(float(i)))

bk=list()
for i in range(1,npuntos+1):
    bk.append(b2(float(i)))

a0k=list()
for i in range(1,npuntos+1):
    a0k.append(a0(float(i)))
al0k=list()
for i in range(1,npuntos+1):
    al0k.append(al0(float(i)))
    
thetak=list()
for i in range(1,npuntos+1):
    thetak.append(np.rad2deg(theta(float(i))))
    
dk=list()
for i in range(1,npuntos+1):
    dk.append(d(float(i)))
    

cx=np.zeros((npuntos,npuntos))

for n in range(0,npuntos):
    for k in range(0,npuntos):
        cx[k,n]=((4*b/(a0k[k]*ck[k]))+(2*(n+1)-1)/(np.sin(np.deg2rad(thetak[k]))))*np.sin(np.deg2rad((2*(n+1)-1))*thetak[k])
        
        
XD=np.matmul(np.linalg.inv(cx),dk)
        
Clwing=np.pi*ar*XD[0]
print("el  cl del ala es:",Clwing)

delta=0
for i in range(2,npuntos+1):
    delta+=i*((XD[i-1])/(XD[0]))**2
e=(1+delta)**-1
print("el coeficiente de oswald es",e)
Cdi=((Clwing**2)/(np.pi*e*ar))
print("el cd inducido es:",Cdi)

#define los puntos de control
npuntos2=npuntos+2
yx=list()
yx.append(b/2)
for i in range(len(yk)):
    yx.append(-1*yk[i])
yx.append(0)

thetayx=list()
def theta2(k):
    theta = np.arccos(-2*k/b)
    return theta
thetayx.append(0) 
for i in range(1,npuntos2):
    thetayx.append(np.rad2deg(theta2(-1*yx[i])))
def gamma(y):
    gammaye=2*b*vinf*(XD[0]*np.sin(np.deg2rad(y))+XD[1]*np.sin(np.deg2rad(y)*3))
    return gammaye

gammayx=list()
for i in range(0,npuntos2):
    gammayx.append(gamma(thetayx[i]))

gammanorm=list()
def norm(y):
    normx=y/gammayx[len(gammayx)-1]
    return normx
for i in range(0,npuntos2):
    gammanorm.append(norm(gammayx[i]))

def ynorm(y):
    ynorm=y/(b/2)
    return ynorm
ynormx=list()
for i in range(0,npuntos2):
    ynormx.append(ynorm(yx[i]))
    
def clw(y,x):
    clw = (1/Clwing)*(2*y/(vinf*x))
    return clw
def c2(k):
    cleng=croot*(1+2*k*((lambdax-1)/(b)))
    return cleng  

ck2=list()
for i in range(npuntos2):
    ck2.append(c2(yx[i]))

clwy=list()
for i in range(npuntos2):
    clwy.append(clw(gammayx[i],ck2[i]))

def L(y,x):
    l = 0.5*densidad*(vinf**2)*x*y
    return l
ly=list()
for i in range(npuntos2):
    ly.append(L(clwy[i],ck2[i]))

import matplotlib.pyplot as plt

# Reorganizar los valores
yx_reversed = yx[::-1]  # Invertir el vector de yx
ly_reversed = ly[::-1]  # Invertir el vector de ly

# Crear la gráfica
plt.plot(yx_reversed, ly_reversed, 'r', label='Load distribution (L) [N]')
plt.scatter(yx_reversed, ly_reversed, color='red')  # Puntos para visualización
plt.xlabel('b_w/2 [m]')
plt.ylabel('L(y) [N]')
plt.title('Load Distribution over Span')
plt.legend()
plt.grid(True)
plt.show()
