import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import make_interp_spline

# =============================================================================
# 1. INITIAL PARAMETERS
# =============================================================================
# V-N Diagram for a typical TRANSPORT aircraft, FAR 23
# Macaco's Unit System (Imperial, ft, lb, s)

MTOW    = 108000           # Maximum Takeoff Weight [lb]
h       = 0                # Altitude [ft]
Vc      = 325              # Design Cruise Speed [KEAS] (Equivalent Airspeed)
Vd      = 420              # Design Dive Speed [KEAS] (Equivalent Airspeed)
Cse     = 548.6            # Altitude Speed of Sound [ft/s]
Clmax   = 1.35             # Maximum Lift Coefficient
Clmin   = 1.35             # Minimum Lift Coefficient (-)
g       = 32.174           # Acceleration due to gravity [ft/s^2]
b_span  = 98               # Wing Span [ft]
S       = 1200             # Wing Area [ft^2]
n       = 2.1 + (24000/(MTOW + 10000))  # Load Factor (to FAR 23 Transport)
if n < 2.5:
    n = 2.5
nneg    = -1               # Negative Load Factor
AR      = 8                # Aspect Ratio (b_span^2/S)
taper   = 0.3              # Taper Ratio
Swept   = 0                # Wing Sweep [rad]
beta    = 1                # Compressibility Correction Factor
k       = 1                # k = 1 for FAR 25 Transport Category
betaAR_K = beta * AR / k
clalphaw = 0.0825 * 180/np.pi   # Wing Lift Curve Slope [1/rad] (from tables)
clalphaaircraft = clalphaw * 1.1  # Aircraft Lift Curve Slope [1/rad] (assumed 10% higher)
AirDensity = 0.00238       # Air Density [slug/ft^3] (ISA at 10000 ft)
c_bar   = 13               # Mean Aerodynamic Chord [ft]
passengers = 1             # Number of Passengers
gust    = 56 * 0.592484    # Gust Load [ft/s^2] (56 ft/s^2 = 1.5 m/s^2) # SEA LEVEL VALUE -----------------

# =============================================================================
# 2. CALCULATIONS BEFORE STARTING
# =============================================================================
W_S   = MTOW / S          # Wing Loading [lb/ft^2]
step  = Vd / 20           # Step size for velocity vector 

# Base velocity vector
velocities_base = np.arange(0, Vd + step, step)

# Calculate critical speeds
Vstall   = np.sqrt((2*MTOW) / (AirDensity * S * Clmax)) * 0.592  # Stall speed [KEAS] (approx. conversion)
Vcruise  = Vc              # Cruise speed already in KEAS
Vmaneuver = Vstall * np.sqrt(n)   # Maneuvering speed

# Combine base velocities with critical speeds, sort and remove duplicates 
velocities_all = np.unique(np.sort(np.concatenate((velocities_base, [Vstall, Vcruise, Vmaneuver]))))

# =============================================================================
# 3. DATAFRAME SETUP (COLUMN NAMES)
# =============================================================================
# Columns for maneuver and gust calculations
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

# Combined columns
columns_total = columns_maneuver + columns_gust + Positive_load_flaps

# =============================================================================
# 4. FUNCTION TO CALCULATE PARAMETERS GIVEN A VELOCITY VECTOR
# =============================================================================
def calc_parameters(velocities):
    # Create a data dictionary with NaN values for all columns
    data = {col: np.nan * np.ones(len(velocities)) for col in columns_total}
    data["V eq. KEAS"] = velocities
    df_local = pd.DataFrame(data)
    
    # Ensure all columns are of float type
    df_local = df_local.astype(float)
    
    # ---------------------------
    # Dynamic Pressure and Mach Number
    # ---------------------------
    df_local['Mach (Ve/Cse)'] = df_local['V eq. KEAS'] / Cse
    df_local['q dynamic pressure (lb/ft^2)'] = (df_local['V eq. KEAS']**2) / 296  # Macaco system trick
    
    # ---------------------------
    # Calculation for Clmax ratio (mach dependency)
    # ---------------------------
    df_local['Clmax_m/Clmax_0'] = (-142.6101 * df_local['Mach (Ve/Cse)']**7 +
                                   479.0665 * df_local['Mach (Ve/Cse)']**6 -
                                   617.1383 * df_local['Mach (Ve/Cse)']**5 +
                                   385.2554 * df_local['Mach (Ve/Cse)']**4 -
                                   121.3842 * df_local['Mach (Ve/Cse)']**3 +
                                   17.7945  * df_local['Mach (Ve/Cse)']**2 -
                                   0.99    * df_local['Mach (Ve/Cse)'] + 1)
    
    # ---------------------------
    # Lift Coefficient calculations
    # ---------------------------
    df_local['Cl max_m']   = df_local['Clmax_m/Clmax_0'] * Clmax
    df_local['Cl max_m (-)'] = df_local['Clmax_m/Clmax_0'] * Clmin
    df_local['positive load factor n+'] = (df_local['q dynamic pressure (lb/ft^2)'] * df_local['Cl max_m']) / W_S
    df_local['negative load factor n-'] = (-df_local['q dynamic pressure (lb/ft^2)'] * df_local['Cl max_m (-)']) / W_S
    
    # ---------------------------
    # Gust load calculations
    # ---------------------------
    df_local['Cl alpha_m/cl alpha 0'] = (2.0581 * df_local['Mach (Ve/Cse)']**3 -
                                           1.4356 * df_local['Mach (Ve/Cse)']**2 +
                                           0.3169 * df_local['Mach (Ve/Cse)'] + 1)
    df_local['Cl alpha_m'] = clalphaaircraft * df_local['Cl alpha_m/cl alpha 0']
    df_local['µ'] = 2 * MTOW / (AirDensity * c_bar * df_local['Cl alpha_m'] * S * g)
    df_local['Kg'] = 0.88 * df_local['µ'] / (5.3 + df_local['µ'])
    df_local['positive gust load factor V_B'] = 1 + (df_local['Kg'] * gust * 0.5925 * df_local['V eq. KEAS'] * df_local['Cl alpha_m']) / (498 * W_S)
    df_local['negative gust load factor V_B'] = 1 - (df_local['Kg'] * gust * 0.5925 * df_local['V eq. KEAS'] * df_local['Cl alpha_m']) / (498 * W_S)
    df_local['positive gust load factor V_C'] = 1 + (df_local['Kg'] * (gust / 2) * 0.5925 * df_local['V eq. KEAS'] * df_local['Cl alpha_m']) / (498 * W_S)
    df_local['negative gust load factor V_C'] = 1 - (df_local['Kg'] * (gust / 2) * 0.5925 * df_local['V eq. KEAS'] * df_local['Cl alpha_m']) / (498 * W_S)
    
    # ---------------------------
    # Load factor with flaps
    # ---------------------------
    df_local['Positive load factor n+ with flaps'] = (df_local['q dynamic pressure (lb/ft^2)'] * df_local['Cl max_m']) / W_S * 1.15
    
    return df_local

# =============================================================================
# 5. CALCULATE PARAMETERS AND ADDITIONAL VELOCITIES
# =============================================================================
# Calculate parameters for the initial velocity vector
df = calc_parameters(velocities_all)

# Recalculate speeds (already computed previously)
Vstall   = np.sqrt((2 * MTOW) / (AirDensity * S * Clmax)) * 0.592
Vcruise  = Vc
Vdive    = Vd

# ---------------------------
# Bisection Method to find speed where "Positive load factor n+ with flaps" equals 2
# ---------------------------
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
    return (a + b) / 2.0

def f_nplus_flaps(V):
    Mach = V / Cse
    clmax_ratio = (-142.6101 * Mach**7 + 479.0665 * Mach**6 - 617.1383 * Mach**5 +
                   385.2554 * Mach**4 - 121.3842 * Mach**3 + 17.7945 * Mach**2 -
                   0.99 * Mach + 1)
    Cl_max_m = clmax_ratio * Clmax
    q = (V**2) / 296
    n_plus_flaps = (q * Cl_max_m) / W_S * 1.15
    return n_plus_flaps - 2

# Find Vmaneuver (maneuvering speed)
Vmaneuver = Vstall * np.sqrt(n)
print("Vmaneuver (defined) =", Vmaneuver)

# Solve for the speed with flaps where Positive load factor n+ with flaps = 2
V_lower = 0.1   # Avoid zero to prevent division by zero
V_upper = Vd
V_target_flaps = bisect(f_nplus_flaps, V_lower, V_upper)
print("Solved speed for Positive load factor n+ with flaps = 2:", V_target_flaps)

# Add Vmaneuver and V_target_flaps to the velocity vector and recalc parameters
velocities_all_new = np.unique(np.sort(np.concatenate((velocities_all, [Vmaneuver, V_target_flaps]))))
df = calc_parameters(velocities_all_new)

# ---------------------------
# Additional Bisection for negative load factor (n-)
# ---------------------------
NegativeVstall = np.sqrt((2 * MTOW) / (AirDensity * S * Clmin)) * 0.592

def f_nminus(V):
    # Using q = V^2/296 and Cl max_m (-) = Clmin (if Clmax_m/Clmax_0 = 1)
    return -((V**2) / 296 * Clmin) / W_S - nneg

V_lower = 0.1
V_upper = Vd
V_target_nneg = bisect(f_nminus, V_lower, V_upper)
print("Solved speed for negative load factor n- = nneg:", V_target_nneg)

# Add V_target_nneg to velocity vector and recalc parameters
velocities_all_new = np.unique(np.sort(np.concatenate((velocities_all, [V_target_nneg]))))
df = calc_parameters(velocities_all_new)

# Ensure NegativeVstall is in the DataFrame; if not, add it.
if not np.any(np.isclose(df["V eq. KEAS"].values, NegativeVstall, atol=1e-6)):
    extra_row = calc_parameters(np.array([NegativeVstall]))
    df = pd.concat([df, extra_row], ignore_index=True)
    df = df.sort_values("V eq. KEAS").reset_index(drop=True)

# =============================================================================
# 6. PREDEFINED VALUES
# =============================================================================
# Force the "positive load factor n+" at Vmaneuver to be n (2.5)
df.loc[np.isclose(df["V eq. KEAS"], Vmaneuver, atol=1e-6), "positive load factor n+"] = n

# Force the "Positive load factor n+ with flaps" at V_target_flaps to be 2
df.loc[np.isclose(df["V eq. KEAS"], V_target_flaps, atol=1e-6), "Positive load factor n+ with flaps"] = 2

# Create velocity (x) and load (y) vectors for plotting the V-N diagram
x = np.zeros(24)
# Velocity Vector (KEAS)
x[0]  = Vstall          # Positive stall speed
x[1]  = Vstall
x[2]  = NegativeVstall
x[3]  = NegativeVstall
x[4]  = Vmaneuver       # Maneuvering speed
x[5]  = Vd
x[6]  = V_target_nneg
x[7]  = Vcruise
x[8]  = 0               # Flaps segment
x[9]  = 0               # Flaps segment
x[10] = Vmaneuver
x[11] = Vmaneuver
x[12] = Vcruise
x[13] = Vcruise
x[14] = 0               # Never Exceed segment
x[15] = 0               # Never Exceed segment
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
y[0]  = 1
y[1]  = 0
y[2]  = 0
# For NegativeVstall, extract the corresponding n- value from the DataFrame
idx = np.argmin(np.abs(df["V eq. KEAS"].values - NegativeVstall))
y[3]  = df.iloc[idx]["negative load factor n-"]
y[4]  = n
y[5]  = n
y[6]  = nneg
y[7]  = nneg
y[8]  = 0              # Flaps segment
y[9]  = 0              # Flaps segment
y[10] = nneg
y[11] = n
y[12] = nneg
y[13] = n
y[14] = 0             # Never Exceed segment
y[15] = 0             # Never Exceed segment
y[16] = n
y[17] = 0
y[18] = nneg
y[19] = 0
y[20] = n * 1.25
y[21] = n * 1.25
y[22] = n * 1.5
y[23] = n * 1.5

# =============================================================================
# 7. PLOTTING THE V-N DIAGRAM
# =============================================================================
plt.figure(figsize=(16, 9))

# ---------------------------
# Plot individual segments
# ---------------------------
line1 = plt.plot([x[0], x[1]], [y[0], y[1]], marker='.', linestyle='-')[0]
line1.set_color('black')
line2 = plt.plot([x[2], x[3]], [y[2], y[3]], marker='.', linestyle='-')[0]
line2.set_color('black')
lineextra = plt.plot([x[1], x[2]], [y[1], y[2]], marker='.', linestyle='-')[0]
lineextra.set_color("black")
line3 = plt.plot([x[4], x[5]], [y[4], y[5]], marker='.', linestyle='-')[0]
line3.set_color('black')
line4 = plt.plot([x[6], x[7]], [y[6], y[7]], marker='.', linestyle='-')[0]
line4.set_color('black')
line5 = plt.plot([x[10], x[11]], [y[10], y[11]], marker='.', linestyle='--')[0]
line5.set_color('blue')
line6 = plt.plot([x[12], x[13]], [y[12], y[13]], marker='.', linestyle='--')[0]
line6.set_color('black')
line7 = plt.plot([x[16], x[17]], [y[16], y[17]], marker='.', linestyle='-')[0]
line7.set_color('black')
line8 = plt.plot([x[18], x[19]], [y[18], y[19]], marker='.', linestyle='-')[0]
line8.set_color('black')
line9 = plt.plot([x[20], x[21]], [y[20], y[21]], marker='.', linestyle='--')[0]
line9.set_color('gray')
line10 = plt.plot([x[22], x[23]], [y[22], y[23]], marker='.', linestyle='--')[0]
line10.set_color('black')

# ---------------------------
# Plot curves from the DataFrame
# ---------------------------
# n+ vs V eq (up to Vstall)
df_subset = df[df["V eq. KEAS"] <= Vstall]
line_curve = plt.plot(df_subset["V eq. KEAS"], df_subset["positive load factor n+"],
                      linestyle="--", color="black", marker='',
                      label="n+ vs V eq (up to Vstall)")[0]

# n- vs V eq (up to V_target_nneg)
df_subset_nminus = df[df["V eq. KEAS"] <= V_target_nneg]
line_curve_nminus = plt.plot(df_subset_nminus["V eq. KEAS"], df_subset_nminus["negative load factor n-"],
                             linestyle="--", color="black", marker='',
                             label="n- vs V eq (up to n- = nneg)")[0]

# Curve between Vstall and Vmaneuver for n+
df_subset2 = df[(df["V eq. KEAS"] >= Vstall) & (df["V eq. KEAS"] <= Vmaneuver)]
x_vals = df_subset2["V eq. KEAS"].values
y_vals = df_subset2["positive load factor n+"].values
p = np.polyfit(x_vals, y_vals, deg=2)
poly = np.poly1d(p)
x_smooth = np.linspace(x_vals.min(), x_vals.max(), 300)
y_smooth = poly(x_smooth)
line_curve2 = plt.plot(x_smooth, y_smooth, linestyle="-", color="black", marker='',
                       label="n+ vs V eq (from Vstall to Vmaneuver)")[0]

# Gust load factors V_B
df_subset_gust = df[df["V eq. KEAS"] <= Vd]
line_gust_positive = plt.plot(df_subset_gust["V eq. KEAS"], df_subset_gust["positive gust load factor V_B"],
                              linestyle="-", color="blue", marker='',
                              label="Positive Gust Load (V_B)")[0]
line_gust_negative = plt.plot(df_subset_gust["V eq. KEAS"], df_subset_gust["negative gust load factor V_B"],
                              linestyle="-", color="blue", marker='',
                              label="Negative Gust Load (V_B)")[0]

# Gust load factors V_C
df_subset_vc = df[df["V eq. KEAS"] <= Vcruise]
line_vc_positive = plt.plot(df_subset_vc["V eq. KEAS"], df_subset_vc["positive gust load factor V_C"],
                            linestyle="-", color="lightgreen", marker='',
                            label="Positive Gust Load (V_C)")[0]
line_vc_negative = plt.plot(df_subset_vc["V eq. KEAS"], df_subset_vc["negative gust load factor V_C"],
                            linestyle="-", color="lightgreen", marker='',
                            label="Negative Gust Load (V_C)")[0]

# n+ with flaps curve (up to V_target_flaps)
df_subset_flaps = df[df["V eq. KEAS"] <= V_target_flaps]
line_flaps = plt.plot(df_subset_flaps["V eq. KEAS"], df_subset_flaps["Positive load factor n+ with flaps"],
                      linestyle="-", color="orange", marker='',
                      label="n+ with flaps vs V eq (up to Vflaps)")[0]

# ---------------------------
# Figure settings
# ---------------------------
plt.xlabel("Speed (KEAS)")
plt.ylabel("Load Factor")
plt.title("V-N Diagram")
plt.grid(True)
plt.legend(loc='upper left', bbox_to_anchor=(0.9, 1), borderaxespad=0.)
plt.show()

# =============================================================================
# EXPORT DATAFRAME
# =============================================================================
df.to_csv("vn_diagram_with_critical_speeds_FAR25.csv", index=False)
