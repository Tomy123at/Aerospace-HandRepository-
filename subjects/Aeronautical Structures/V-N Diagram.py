import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import make_interp_spline

# V-N Diagram for a typical TRANSPORT aircraft, FAR 25
# Macaco's Units Sytem (Imperial, ft, lb, s)
# Espaninglish version

# Initial Parameters
MTOW = 108000           # Maximum Takeoff Weight [lb]
h = 10000               # Altitude [ft]
Vc = 325                # Design Cruise Speed [KEAS] (Equivalent Airspeed)
Vd = 420                # Design Dive Speed [KEAS] (Equivalent Airspeed)
Cse = 548.6             # Altitude Speed of Sound [ft/s]
Clmax = 1.35            # Maximum Lift Coefficient
Clmin = 1.35            # Minimum Lift Coefficient (-)
g = 32.174              # Acceleration due to gravity [ft/s^2]
b_span = 98             # Wing Span [ft]
S = 1200                # Wing Area [ft^2]
n = 2.5                 # Load Factor (para FAR 25 Transport) -> example says n = 2.5
nneg = -1               # Negative Load Factor
AR = 8                  # span**2/S # Aspect Ratio
taper = 0.3             # Taper Ratio
Swept = 0               # Swept Wing [rad] (Aflechamiento)
beta = 1                # Compressibility Correction Factor
k = 1                   # k = 1 for FAR 25 Transport Category assume 
betaAR_K = beta*AR/k
clalphaw = 0.0825*180/np.pi   # [1/rad] # Wing Lift Curve Slope (tablas)
clalphaaircraft = clalphaw*1.1  # [1/rad] # Aircraft Lift Curve Slope (assumed 10% higher than wing)
AirDensity = 0.00238          # Air Density [slug/ft^3] (ISA at 10000 ft)
c_bar = 13                    # Mean Aerodynamic Chord [ft]

# Calculations
W_S = MTOW/S  # Wing Loading [lb/ft^2]

step = Vd / 20  # Step size for velocity vector ------------------

# Velocity vector base
velocities_base = np.arange(0, Vd + step, step)

# Calculate critical speeds
Vstall = np.sqrt((2*MTOW)/(AirDensity*S*Clmax)) * 0.592  # Vstall en KEAS (aprox. conversion)
Vcruise = Vc  # Vcruise ya está en KEAS

# Vmaneuver calculation
Vmaneuver = Vstall * np.sqrt(n)

# Combine the base vector with Vstall, Vcruise and Vmaneuver, order and remove duplicates
velocities_all = np.unique(np.sort(np.concatenate((velocities_base, [Vstall, Vcruise, Vmaneuver]))))

#------------------------------------------------------------------------------
# Column names for the DataFrame
columns_maneuver = [
    "V eq. KEAS",
    "Mach (Ve/Cse)",
    "q dynamic pressure (lb/ft^2)",
    "Clmax_m/Clmax_0",
    "Cl max_m",
    "Cl max_m (-)",
    "positive load factor n+",
    "negative load factor n-"
]

columns_gust = [
    "Cl alpha_m/cl alpha 0",
    "Cl alpha_m",
    "µ",
    "Kg",
    "positive gust load factor V_B",
    "negative gust load factor V_B",
    "positive gust load factor V_C",
    "negative gust load factor V_C",
]

Positive_load_flaps = [
    'Positive load factor n+ with flaps',
]

# Combine
columns_total = columns_maneuver + columns_gust + Positive_load_flaps

#------------------------------------------------------------------------------
# Define a function to calculate all parameters given a vector of velocities
def calc_parameters(velocities):
    # Data dictionary with Velocity and NaN values 
    data = {col: np.nan * np.ones(len(velocities)) for col in columns_total}
    data["V eq. KEAS"] = velocities
    df_local = pd.DataFrame(data)
    
    # Convert all columns to float
    df_local = df_local.astype(float) # 2 HOURS TO FIND THIS
    
    # Calculation 
    df_local['Mach (Ve/Cse)'] = df_local['V eq. KEAS'] / Cse
    df_local['q dynamic pressure (lb/ft^2)'] = (df_local['V eq. KEAS']**2)/296  # Macaco system tricks
    # ----------------------------------------------------------------------------
    # Se asume que Clmax_m = Clmax en el parcial, aqui no
    df_local['Clmax_m/Clmax_0'] = (-142.6101*df_local['Mach (Ve/Cse)']**7 + 
                                   479.0665*df_local['Mach (Ve/Cse)']**6 - 
                                   617.1383*df_local['Mach (Ve/Cse)']**5 + 
                                   385.2554*df_local['Mach (Ve/Cse)']**4 - 
                                   121.3842*df_local['Mach (Ve/Cse)']**3 + 
                                   17.7945*df_local['Mach (Ve/Cse)']**2 - 
                                   0.99*df_local['Mach (Ve/Cse)'] + 1)
    # ----------------------------------------------------------------------------
    df_local['Cl max_m'] = df_local['Clmax_m/Clmax_0'] * Clmax
    df_local['Cl max_m (-)'] = df_local['Clmax_m/Clmax_0'] * Clmin
    df_local['positive load factor n+'] = (df_local['q dynamic pressure (lb/ft^2)'] * df_local['Cl max_m']) / W_S
    df_local['negative load factor n-'] = (-df_local['q dynamic pressure (lb/ft^2)'] * df_local['Cl max_m (-)']) / W_S
    # ----------------------------------------------------------------------------
    # Se asume que Cl alpha_m = Cl alpha0 en el parcial, aqui abajo no
    df_local['Cl alpha_m/cl alpha 0'] = (2.0581*df_local['Mach (Ve/Cse)']**3 - 
                                          1.4356*df_local['Mach (Ve/Cse)']**2 + 
                                          0.3169*df_local['Mach (Ve/Cse)'] + 1)
    # ----------------------------------------------------------------------------
    df_local['Cl alpha_m'] = clalphaaircraft * df_local['Cl alpha_m/cl alpha 0']
    df_local['µ'] = 2*MTOW/(AirDensity*c_bar*df_local['Cl alpha_m']*S*g)
    df_local['Kg'] = 0.88*df_local['µ']/(5.3+df_local['µ'])
    df_local['positive gust load factor V_B'] = 1 + (df_local['Kg']*56*0.5925*df_local['V eq. KEAS']*df_local['Cl alpha_m'])/(498*W_S)
    df_local['negative gust load factor V_B'] = 1 - (df_local['Kg']*56*0.5925*df_local['V eq. KEAS']*df_local['Cl alpha_m'])/(498*W_S)
    df_local['positive gust load factor V_C'] = 1 + (df_local['Kg']*(56/2)*0.5925*df_local['V eq. KEAS']*df_local['Cl alpha_m'])/(498*W_S)
    df_local['negative gust load factor V_C'] = 1 - (df_local['Kg']*(56/2)*0.5925*df_local['V eq. KEAS']*df_local['Cl alpha_m'])/(498*W_S)
    df_local['Positive load factor n+ with flaps'] = (df_local['q dynamic pressure (lb/ft^2)'] * df_local['Cl max_m']) / W_S * 1.15
    return df_local

#------------------------------------------------------------------------------
# Calculate parameters for the initial velocity vector
df = calc_parameters(velocities_all)

# Recalculate speeds (ya se han calculado previamente)
Vstall = np.sqrt((2*MTOW)/(AirDensity*S*Clmax)) * 0.592
Vcruise = Vc
Vdive = Vd

#------------------------------------------------------------------------------
# Dark Magic to find the speed where n+ with flaps = 2

def bisect(f, a, b, tol=1e-6, max_iter=100):
    fa = f(a)
    fb = f(b)
    if fa * fb > 0:
        raise ValueError("No root found in the interval [{}, {}]".format(a, b))
    for i in range(max_iter):
        mid = (a + b) / 2.0
        fm = f(mid)
        if abs(fm) < tol:
            return mid
        if fa * fm < 0:
            b = mid
            fb = fm
        else:
            a = mid
            fa = fm
    return (a+b) / 2.0

def f_nplus_flaps(V):
    Mach = V / Cse
    clmax_ratio = (-142.6101*Mach**7 + 479.0665*Mach**6 - 617.1383*Mach**5 +
                   385.2554*Mach**4 - 121.3842*Mach**3 + 17.7945*Mach**2 -
                   0.99*Mach + 1)
    Cl_max_m = clmax_ratio * Clmax
    q = (V**2) / 296
    n_plus_flaps = (q * Cl_max_m) / W_S * 1.15
    return n_plus_flaps - 2

#------------------------------------------------------------------------------
# Find Vmaneuver
Vmaneuver = Vstall * np.sqrt(n)
print("Vmaneuver (definida) =", Vmaneuver)

# Resolver para la velocidad con flaps (donde Positive load factor n+ with flaps = 2)
V_lower = 0.1   # Evitamos cero para evitar división por cero
V_upper = Vd
V_target_flaps = bisect(f_nplus_flaps, V_lower, V_upper)
print("Solved speed for Positive load factor n+ with flaps = 2:", V_target_flaps)

#------------------------------------------------------------------------------
# Añadir Vmaneuver y la velocidad de flaps al vector de velocidades
velocities_all_new = np.unique(np.sort(np.concatenate((velocities_all, [Vmaneuver, V_target_flaps]))))
df = calc_parameters(velocities_all_new)

# Forzar que, en la fila donde "V eq. KEAS" es igual a Vmaneuver,
# el valor de "positive load factor n+" sea n (2.5)
df.loc[np.isclose(df["V eq. KEAS"], Vmaneuver, atol=1e-6), "positive load factor n+"] = n

# Forzar que, en la fila donde "V eq. KEAS" es igual a V_target_flaps,
# el valor de "Positive load factor n+ with flaps" sea 2
df.loc[np.isclose(df["V eq. KEAS"], V_target_flaps, atol=1e-6), "Positive load factor n+ with flaps"] = 2

# Exportar el DataFrame a CSV con las velocidades halladas incluidas
df.to_csv("vn_diagram_with_critical_speeds.csv", index=False)


#------------------------------------------------------------------------------
# Para graficar, definimos algunos valores para el diagrama V-N

# Asumimos que para el diagrama:
PositiveVstall = Vstall
PositiveVmaneuver = Vmaneuver    # Esta es la velocidad de maniobra (donde n+ se asume 2.5)
NegativeVstall = np.sqrt((2*MTOW)/(AirDensity*S*Clmin)) * 0.592
Vflaps = 0

x = np.zeros(24)
# Velocity Vector
x[0] = PositiveVstall
x[1] = PositiveVstall
x[2] = NegativeVstall
x[3] = NegativeVstall
x[4] = PositiveVmaneuver
x[5] = Vd
x[6] = NegativeVstall
x[7] = Vcruise
x[8] = 0             # Flaps
x[9] = 0             # Flaps
x[10] = PositiveVmaneuver
x[11] = PositiveVmaneuver
x[12] = Vcruise
x[13] = Vcruise
x[14] = 0            # Never Exceed
x[15] = 0            # Never Exceed
x[16] = Vd
x[17] = Vd
x[18] = Vcruise
x[19] = Vd
x[20] = 0
x[21] = Vd
x[22] = 0
x[23] = Vd

y = np.zeros(24)
# Load Vector
y[0] = 1
y[1] = 0
y[2] = 0
y[3] = -1
y[4] = n   # n = 2.5
y[5] = n
y[6] = nneg
y[7] = nneg
y[8] = 0            # Flaps
y[9] = 0            # Flaps
y[10] = nneg
y[11] = n
y[12] = nneg
y[13] = n
y[14] = 0           # Never Exceed
y[15] = 0           # Never Exceed
y[16] = n
y[17] = 0
y[18] = nneg
y[19] = 0
y[20] = n*1.25
y[21] = n*1.25
y[22] = n*1.5
y[23] = n*1.5

plt.figure(figsize=(16, 9))

#------------------------------------------------------------------------------
# Individual Segments Plotting
line1 = plt.plot([x[0], x[1]], [y[0], y[1]], marker='.', linestyle='-',)[0]
line1.set_color('black')
line2 = plt.plot([x[2], x[3]], [y[2], y[3]], marker='.', linestyle='-',)[0]
line2.set_color('black')
line3 = plt.plot([x[4], x[5]], [y[4], y[5]], marker='.', linestyle='-',)[0]
line3.set_color('black')
line4 = plt.plot([x[6], x[7]], [y[6], y[7]], marker='.', linestyle='-',)[0]
line4.set_color('black')
line5 = plt.plot([x[10], x[11]], [y[10], y[11]], marker='.', linestyle='--',)[0]
line5.set_color('blue')
line6 = plt.plot([x[12], x[13]], [y[12], y[13]], marker='.', linestyle='--',)[0]
line6.set_color('black')
line7 = plt.plot([x[16], x[17]], [y[16], y[17]], marker='.', linestyle='-',)[0]
line7.set_color('black')
line8 = plt.plot([x[18], x[19]], [y[18], y[19]], marker='.', linestyle='-',)[0]
line8.set_color('black')
line9 = plt.plot([x[20], x[21]], [y[20], y[21]], marker='.', linestyle='--',)[0]
line9.set_color('gray')
line10 = plt.plot([x[22], x[23]], [y[22], y[23]], marker='.', linestyle='--',)[0]
line10.set_color('black')

#------------------------------------------------------------------------------
# Lets Plot the V-N Diagram with the DataFrame

# To Vstall
df_subset = df[df["V eq. KEAS"] <= Vstall]
line_curve = plt.plot(df_subset["V eq. KEAS"], df_subset["positive load factor n+"],
                        linestyle="--", color="black", marker='',
                        label="n+ vs V eq (hasta Vstall)")[0]

# Verificamos si NegativeVstall ya existe en el DataFrame (dentro de una tolerancia)
if not np.any(np.isclose(df["V eq. KEAS"].values, NegativeVstall, atol=1e-6)):
    # Si no existe, lo añadimos
    extra = calc_parameters(np.array([NegativeVstall]))
    df = pd.concat([df, extra], ignore_index=True)
    df = df.sort_values("V eq. KEAS").reset_index(drop=True)

# Luego filtramos todos los puntos hasta NegativeVstall
df_subset_neg = df[df["V eq. KEAS"] <= NegativeVstall]
line_curve_neg = plt.plot(df_subset_neg["V eq. KEAS"], df_subset_neg["negative load factor n-"],
                          linestyle="--", color="black", marker='',
                          label="n- vs V eq (hasta NegativeVstall)")[0]



# Vstall and Vmaneuver
df_subset2 = df[(df["V eq. KEAS"] >= Vstall) & (df["V eq. KEAS"] <= Vmaneuver)]
x_vals = df_subset2["V eq. KEAS"].values
y_vals = df_subset2["positive load factor n+"].values
p = np.polyfit(x_vals, y_vals, deg=2)
poly = np.poly1d(p)
x_smooth = np.linspace(x_vals.min(), x_vals.max(), 300)
y_smooth = poly(x_smooth)
line_curve2 = plt.plot(x_smooth, y_smooth, linestyle="-", color="black", marker='',
                       label="n+ vs V eq (de Vstall a Vmaneuver)")[0]

#Vgust Positive and Negative Gust Load Factor V_B
df_subset_gust = df[df["V eq. KEAS"] <= Vd]
line_gust_positive = plt.plot(df_subset_gust["V eq. KEAS"], df_subset_gust["positive gust load factor V_B"],
                              linestyle="-", color="blue", marker='',
                              label="Positive Gust Load (V_B)")[0]
line_gust_negative = plt.plot(df_subset_gust["V eq. KEAS"], df_subset_gust["negative gust load factor V_B"],
                              linestyle="-", color="blue", marker='',
                              label="Negative Gust Load (V_B)")[0]

#--------------------------------------------------------------------------
#Vgust Positive and Negative Gust Load Factor V_C
df_subset_vc = df[df["V eq. KEAS"] <= Vcruise]
line_vc_positive = plt.plot(df_subset_vc["V eq. KEAS"], df_subset_vc["positive gust load factor V_C"],
                              linestyle="-", color="lightgreen", marker='',
                              label="Positive Gust Load (V_C)")[0]
line_vc_negative = plt.plot(df_subset_vc["V eq. KEAS"], df_subset_vc["negative gust load factor V_C"],
                              linestyle="-", color="lightgreen", marker='',
                              label="Negative Gust Load (V_C)")[0]

df_subset_flaps = df[df["V eq. KEAS"] <= V_target_flaps]
line_flaps = plt.plot(df_subset_flaps["V eq. KEAS"], df_subset_flaps["Positive load factor n+ with flaps"],
                        linestyle="-", color="orange", marker='',
                        label="n+ with flaps vs V eq (hasta Vflaps)")[0]


plt.xlabel("Velocidad (KEAS)")
plt.ylabel("Factor de carga")
plt.title("Diagrama V-N")
plt.grid(True)
plt.legend(loc='upper left', bbox_to_anchor=(0.9, 1), borderaxespad=0.)
plt.show()