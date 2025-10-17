import math 
import numpy as np
#By: Tomy
#Based from: Lifting Line Theory - Juan Pablo Alvarado

#Datos
rho = 1.201 #Kg/m3
visc = 1.82*10**(-5) 

###------AoA = 2 #Deg
MTOW = 950 #Kg
bw = 0.385 #m
C_root = 0.177
C_tip = 0.061
taper_ratio = C_tip/C_root
Sw = 0.045815 #m2
B_tip = 0

V_cruise = 35 #m/s

a0_root = 5.7295 #Rad
a0_tip = 5.7295 #Rad

aL0_root = 2 #Deg
aL0_tip = 2 #Deg

Cd_0 = 0.0054

#Correciones de unidades
MTOW = MTOW*9.81 #N

AoA = 2 #deg


#Calculos geometricos
AR = (bw**2)/Sw
C_av = Sw/bw

C_mean = (2/3)*C_root*((1+taper_ratio+taper_ratio**2)/(1+taper_ratio))
Y = (bw/6)*((1+2*taper_ratio)/(1+taper_ratio))

#Reynolds
Re = (rho*V_cruise*C_mean)/visc

#-----------------------------------
#Funciones y(k) y c(k)
def yk(bw,k,N):
    YK = -(bw/2)*(1-(2*k-1)/(2*N))
    return YK

def ck(C_root,lamba,bw,k,N):
    CK = C_root*(1-2*((lamba-1)/bw)*yk(bw,k,N))
    return CK
#-----------------------------------

N = 4

y_k = np.zeros(N)
c_k = np.zeros(N)

for i in range(N):
    k = i+1
    y_k[i] = yk(bw,k,N) 
    c_k[i] = ck(C_root,taper_ratio,bw,k,N)

#Funcion B(k)
B_k = np.zeros(N)
h_tip = C_tip*math.sin(B_tip)
def Bk(bw,k,N,C_root,lamba,h_tip):
    BK = math.asin(-((2*yk(bw,k,N))/(bw*ck(C_root,lamba,bw,k,N)))*h_tip)
    return BK

for i in range(N):
    k = i+1
    B_k[i] = Bk(bw,k,N,C_root,taper_ratio,h_tip)

#Funciones alfa 
a0_k = np.zeros(N)
aL0_k = np.zeros(N)
def a0k(a0_root,a0_tip,bw,k,N):
    A0K = a0_root-2*((a0_tip-a0_root)/bw)*yk(bw,k,N)
    return A0K

def aL0k(aL0_root,aL0_tip,bw,k,N):
    AL0K = aL0_root-2*((aL0_tip-aL0_root)/bw)*yk(bw,k,N)
    return AL0K

for i in range(N):
    k = i+1
    a0_k[i] = a0k(a0_root,a0_tip,bw,k,N)
    aL0_k[i] = aL0k(aL0_root,aL0_tip,bw,k,N)

#Transformación
theta_k = np.zeros(N)
def thetak(k,bw,N):
    THETAK = math.acos(-(2*yk(bw,k,N))/bw)
    return THETAK

for i in range(N):
    k = i+1
    theta_k[i] = thetak(k,bw,N) #Rad              #UNI
    theta_k[i] = theta_k[i]*180/math.pi #Deg       DADES

#D(k)
D_k = np.zeros(N)
def Dk(AoA,aL0_root,aL0_tip,bw,k,N,C_root,taper_ratio,h_tip):
    DK = AoA*math.pi/180 - aL0k(aL0_root,aL0_tip,bw,k,N) + Bk(bw,k,N,C_root,taper_ratio,h_tip)
    return DK

for i in range(N):
    k = i+1
    D_k[i] = Dk(AoA,aL0_root,aL0_tip,bw,k,N,C_root,taper_ratio,h_tip)


#MATRIZ -----------------------------------
C_kn = np.zeros((4,4))
def Ckn(k,n,bw,a0_root,a0_tip,N,C_root,taper_ratio):
    CKN = ((((4*bw)/(a0k(a0_root,a0_tip,bw,k,N)*ck(C_root,taper_ratio,bw,k,N)))+((2*n-1)/(math.sin(thetak(k,bw,N)))))*math.sin((2*n-1)*thetak(k,bw,N)))
    return CKN

for i in range(N):
    k = i+1
    for j in range(N):
        n = j+1
        C_kn[i,j] = Ckn(k,n,bw,a0_root,a0_tip,N,C_root,taper_ratio)


# Solucion del sistema de ecuaciones
A = np.linalg.solve(C_kn, D_k)
print(A)

# Calculo del Cl_w
CL_w = math.pi*AR*A[0]
print("El Cl del ala es: ",round(CL_w,3))

#Calculo del Lift
q = (1/2)*rho*(V_cruise**2)   #Pa
Lforce = q*Sw*CL_w            #N

print("La fuerza de lift ejercida por el ala es de: ",round(Lforce,3),"N")

#Delta coeficient
delta_coeficient = 0
for i in range(1,N):
    delta_coeficient = delta_coeficient+(i+1)*(A[i]/A[0])**2

#Eficiencia Oswald
e = (1+delta_coeficient)**(-1)

#Drag inducido
CD_i = (CL_w**2)/(math.pi*e*AR)

#Drag Total
CD_w = Cd_0+CD_i
Dforce = q*CD_w

print("La fuerza de drag ejercida por el ala es de: ",round(Dforce,3),"N")

#Distribucion de cargas en el ala
y_k = np.zeros(N+2)
theta_y = np.zeros(N+2)
T_y = np.zeros(N+2)

def ykk(bw,k,N):
    if k==0:
        YK = bw/2
    elif k==N+1:
        YK = 0
    else:
        YK = -(yk(bw,k,N))
    return YK

def thetay(k,bw,N):
    THETAY = -(math.acos(-(2*ykk(bw,k,N))/bw)-math.pi) 
    return THETAY

def Ty(k,bw,N,V_cruise,A1,A2):
    TY = 2*bw*V_cruise*(A1*math.sin(thetay(k,bw,N))+(A2*math.sin(3*thetay(k,bw,N))))
    return TY

for i in range(N+2):
    k = i
    y_k[i] = ykk(bw,k,N)  #m
    theta_y[i] = thetay(k,bw,N)
    theta_y[i] = (theta_y[i]*180/math.pi) #Deg
    #Circulacion
    T_y[i] = Ty(k,bw,N,V_cruise,A[0],A[1]) #m2/sec

#Circulacion normalizada
T_ND = np.zeros(N+2)
for i in range(N+2):
    T_ND[i] = T_y[i]/T_y[N+1]


#C_LW(y)
c_y =  np.zeros(N+2)
C_LW = np.zeros(N+2)
C_LWN = np.zeros(N+2)
L_y = np.zeros(N+2)

for i in range (N+2):
    if i==0:
        c_y[i] = C_tip
    elif i==(N+1):
        c_y[i] = C_root
    else:
        c_y[i] = c_k[i-1]


def C_Lw(k,bw,N,V_cruise,A1,A2,CL_w):
    CLW = (1/CL_w)*((2*Ty(k,bw,N,V_cruise,A1,A2))/(V_cruise*c_y[k]))
    return CLW

def Ly(q,k,CL_w):
    LY = q*c_y[k]*(C_LW[k])
    return LY

for i in range(N+2):
    k = i
    C_LW[i] = C_Lw(k,bw,N,V_cruise,A[0],A[1],CL_w)
    L_y[i] = Ly(q,k,CL_w)


print(y_k)
print(theta_y)
print(T_y)
print(C_LW)
print(L_y)






ynorm = np.zeros(N+2)
for i in range(N+2):
    ynorm[i] = y_k[i]/(bw/2)



