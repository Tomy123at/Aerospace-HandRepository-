import math 
import numpy as np

# 1
Weight_Payload = 0 #lb

a = True
while a == True:
    # 2
    W_TOguess = 60000

    # Engine Startup
    # Taxi
    # Takeoff
    # Climb
    # Cruise-out 300 nm
    # Loiter 30 min
    # Descent 
    # Dash-out 100 nm
    # Drop bombs
    # Strafe 5 min
    # Dash-in 100 nm
    # Climb
    # Cruise-in 300 nm
    # Descent
    # Landing
    # Shutdown

    # region Wf

    mff_startup = 0.99   #Table 2.1
    mff_taxi = 0.99      #Table 2.1
    mff_takeoff = 0.99   #Table 2.1
    mff_climb = 0.971

    #Cruise-out
    R_cruise_out = 253           #nm 
    V_cruise_out = 459           #kts
    cj_cruise_out = 0.6          #lb/lb/hr
    L_D_cruise_out = 7           #Table 2.2
    mff_cruise_out = math.exp(-R_cruise_out / ((V_cruise_out/cj_cruise_out) * L_D_cruise_out))

    #Loiter
    E_loiter = 0.5               #Hours
    cj_loiter = 0.6              #lb/lb/hr
    L_D_loiter = 9.0             #Table 2.2
    mff_loiter = math.exp(-E_loiter/((1/cj_loiter)*L_D_loiter))

    # Descent
    mff_descent = 0.99    #Table 2.1

    # Dash-out
    R_dash_out = 100             #nm
    V_dash_out = 400             #kts
    cj_dash_out = 0.9            #lb/lb/hr
    L_D_dash_out = 4.5           #Table 2.2
    mff_dash_out = math.exp(-R_dash_out / ((V_dash_out/cj_dash_out) * L_D_dash_out))

    # Drop bombs
    mff_drop_bombs = 1 # No fuel penalties are assessed
    W_bombs = 10000 #lb -----------------
    mff_to_9 = mff_startup * mff_taxi * mff_takeoff * mff_climb * \
               mff_cruise_out * mff_loiter * mff_descent * \
               mff_dash_out * mff_drop_bombs
    W_TOtemp = 1 - mff_to_9
    W_airplane_to8 = W_TOguess * mff_to_9
    W_airplane_to9 = W_airplane_to8 - W_bombs

    # Strafe
    W_ammo = 2000 #lb
    E_strafe = 5/60              # Hours
    cj_strafe = 0.9              #lb/lb/hr
    L_D_strafe = 4.5             #Table 2.2
    mff_strafe = math.exp(-E_strafe/((1/cj_strafe)*L_D_strafe))
    #Correction 
    Bomb_drop_weightfactor = W_airplane_to9/W_airplane_to8
    mff_10_9_corrected = (1-(1-mff_strafe)*Bomb_drop_weightfactor)

    W_airplane_strafe = W_airplane_to9 - W_airplane_to9*(1-mff_strafe)
    W_airplane_to10 = W_airplane_strafe - W_ammo

    # Dash-in
    R_dash_in = 100              #nm
    V_dash_in = 450              #kts 
    cj_dash_in = 0.9             #lb/lb/hr
    L_D_dash_in = 5.5            #Table 2.2
    mff_dash_in = math.exp(-R_dash_in / ((V_dash_in/cj_dash_in) * L_D_dash_in))
    strafe_weightfactor = W_airplane_to10/W_airplane_to9
    mff_11_10_corrected = (1-(1-mff_dash_in)*strafe_weightfactor)

    # Climb
    mff_climb_2 = 0.971
    
    # Cruise-in
    R_cruise_in = 300-47        #nm
    V_cruise_in = 488           #kts
    cj_cruise_in = 0.6          #lb/lb/hr
    L_D_cruise_in = 7.5        #Table 2.2
    mff_cruise_in = math.exp(-R_cruise_in / ((V_cruise_in/cj_cruise_in) * L_D_cruise_in))

    # Descent and shutdown
    mff_descent_2 = 0.99        #Table 2.1
    mff_shutdown = 0.995         #Table 2.1

    mff_total = mff_startup * mff_taxi * mff_takeoff * mff_climb * \
               mff_cruise_out * mff_loiter * mff_descent * \
               mff_dash_out * mff_drop_bombs * mff_10_9_corrected * \
               mff_11_10_corrected * mff_climb_2 * mff_cruise_in * \
               mff_descent_2 * mff_shutdown
    
    print("mff_total: ", mff_total)

    a = False
