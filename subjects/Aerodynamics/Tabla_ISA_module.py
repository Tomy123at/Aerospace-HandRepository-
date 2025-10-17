#%%
import numpy as np
import math 

#%%
#Datos conocidos en el diagrama ISA
#Gradientes:
avalues = [-6.5*10**(-3), 3.0*10**(-3), -4.5*10**(-3), 4.0*10**(-3)]
a = np.array(avalues)


#%%
#Cálculo de los puntos en las isotermas
def Temp_Presion_Densidad(altitude):
    if altitude>=0 and altitude<=11000:
        section=1
    if altitude>11000 and altitude<=25000:
        section=2
    if altitude>25000 and altitude<=47000:
        section=3
    if altitude>47000 and altitude<=53000:
        section=4
    if altitude>53000 and altitude<=79000:
        section=5
    if altitude>79000 and altitude<=90000:
        section=6
    if altitude>90000 and altitude<=105000:
        section=7
    
    j=0
    #Variables inciales
    p0 = 101325 #Pa
    rho0 = 1.2250 #kg/m3
    T0 = 288.16 #K
    h0 = 0 #Km
    g0 = 9.80665 #m/s2
    R = 287 #ni idea
    for i in range(section):
        if i%2==0:
            if altitude>11000 and i==0:
                h=11000
            elif altitude>47000 and i==2:
                h=47000
            elif altitude>79000 and i==4:
                h=79000
            elif altitude>105000 and i==6:
                h=105000
            else:
                h=altitude
            T = T0+a[j]*(h-h0)
            p = p0*(T/T0)**(-(g0/(a[j]*R)))
            rho = rho0*(T/T0)**(-((g0/(a[j]*R))+1))
            T0 = T
            p0 = p
            rho0 = rho
            j = j+1
            h0=h
            

        elif i%2==1:
            if altitude>25000 and i==1:
                h=25000
            elif altitude>53000 and i==3:
                h=53000
            elif altitude>90000 and i==5:
                h=90000
            else:
                h=altitude
            p = p0*math.exp(-(g0/(R*T))*(h-h0))
            rho = rho0*math.exp(-(g0/(R*T))*(h-h0))
            p0 = p
            rho0 = rho
            h0=h
        avel = math.sqrt(1.4*287*T0)
    return T, p, rho, avel

#%%
def TempPresDensALTITUDE(Temp,Pres,Rho,Range):
    g0 = 9.80665 #m/s2
    R = 287 #ni idea
    if Range == 1:
        alt = 0
        T1,P1,rho1 = Temp_Presion_Densidad(alt)
        Pend = a[0]
        h1 = alt
        h_Temp = ((Temp-T1)/Pend)+h1
        h_Pres = (T1/Pend)*((Pres/P1)**(-(g0/(Pend*R))**(-1))-1)+h1
        h_Rho = (T1/Pend)*((Rho/rho1)**(-((g0/(Pend*R))+1)**(-1))-1)+h1

    elif Range == 2:
        h_Temp,h_Pres,h_Rho = Temp_Presion_Densidad(11000)

    elif Range == 3:
        alt = 25000
        T1,P1,rho1 = Temp_Presion_Densidad(alt)
        Pend = a[1]
        h1 = alt
        h_Temp = ((Temp-T1)/Pend)+h1
        h_Pres = (T1/Pend)*((Pres/P1)**(-(g0/(Pend*R))**(-1))-1)+h1
        h_Rho = (T1/Pend)*((Rho/rho1)**(-((g0/(Pend*R))+1)**(-1))-1)+h1

    elif Range == 4:
        h_Temp,h_Pres,h_Rho  = Temp_Presion_Densidad(47000)

    elif Range == 5:
        alt = 53000
        T1,P1,rho1 = Temp_Presion_Densidad(alt)
        Pend = a[2]
        h1 = alt
        h_Temp = ((Temp-T1)/Pend)+h1
        h_Pres = (T1/Pend)*((Pres/P1)**(-(g0/(Pend*R))**(-1))-1)+h1
        h_Rho = (T1/Pend)*((Rho/rho1)**(-((g0/(Pend*R))+1)**(-1))-1)+h1
    
    elif Range == 6:
        h_Temp,h_Pres,h_Rho  = Temp_Presion_Densidad(79000)

    elif Range == 7:
        alt = 90000
        T1,P1,rho1 = Temp_Presion_Densidad(alt)
        Pend = a[2]
        h1 = alt
        h_Temp = ((Temp-T1)/Pend)+h1
        h_Pres = (T1/Pend)*((Pres/P1)**(-(g0/(Pend*R))**(-1))-1)+h1
        h_Rho = (T1/Pend)*((Rho/rho1)**(-((g0/(Pend*R))+1)**(-1))-1)+h1
    

    return h_Temp,h_Pres,h_Rho

