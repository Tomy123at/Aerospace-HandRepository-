import pandas as pd
# ...........................................................................
# ...........................................................................
# --- 1. Definición de Constantes y Conversiones ---
# Las ubicaciones de la carga útil están en metros, las del peso vacío en mm.
# Convertiremos todo a milímetros [mm] para consistencia.
M_TO_MM = 1000
# Peso del combustible (Jet A)
GAL_TO_LB = 5.64



# --- 2. Definición de Componentes ---
# Combinamos los datos de la tabla de peso vacío (imagen) y las especificaciones iniciales.

# Cálculo del peso total del combustible
fuel_volume_gal = 69
total_fuel_weight_lb = fuel_volume_gal * GAL_TO_LB  # 389.16 lb

data = [
    # === Componentes del Peso Vacío (de la tabla de la imagen) ===
    {'component': 'Wing', 'weight_lb': 320.00, 'x_mm': 2080, 'y_mm': 0, 'z_mm': 1280},
    {'component': 'Horizontal Tail', 'weight_lb': 74.00, 'x_mm': 6120, 'y_mm': 0, 'z_mm': 1480},
    {'component': 'Vertical Tail', 'weight_lb': 26.00, 'x_mm': 6630, 'y_mm': 0, 'z_mm': 2010},
    {'component': 'Fuselaje', 'weight_lb': 230.00, 'x_mm': 3120, 'y_mm': 0, 'z_mm': 1410},
    {'component': 'NLG', 'weight_lb': 38.00, 'x_mm': 563, 'y_mm': 0, 'z_mm': 530},
    {'component': 'MLG', 'weight_lb': 116.00, 'x_mm': 2855, 'y_mm': 0, 'z_mm': 550},
    {'component': 'Engine & Install', 'weight_lb': 280.00, 'x_mm': 1020, 'y_mm': 0, 'z_mm': 1380},
    {'component': 'Propeller', 'weight_lb': 40.00, 'x_mm': 360, 'y_mm': 0, 'z_mm': 1420},
    {'component': 'Fixed Equipment', 'weight_lb': 133.24, 'x_mm': 2410, 'y_mm': 0, 'z_mm': 1320},
    {'component': 'Trapped Fuel/Oil', 'weight_lb': 44.00, 'x_mm': 1810, 'y_mm': 0, 'z_mm': 1320},
    
    # === Componentes de Carga Útil (de las especificaciones iniciales) ===
    # Esta es la condición de MTOW
    
    # --- Tripulación ---
    {'component': 'Crew 1 (Student)', 'weight_lb': 220.00, 
     'x_mm': 2.45 * M_TO_MM, 'y_mm': 0, 'z_mm': 1.52 * M_TO_MM},
    
    {'component': 'Crew 2 (Instructor)', 'weight_lb': 220.00, 
     'x_mm': 3.49 * M_TO_MM, 'y_mm': 0, 'z_mm': 1.57 * M_TO_MM},
    
    # --- Combustible (dividido en 2 tanques simétricos) ---
    {'component': 'Fuel Tank (Left)', 'weight_lb': total_fuel_weight_lb / 2, 
     'x_mm': 2.75 * M_TO_MM, 'y_mm': -1.32 * M_TO_MM, 'z_mm': 1.24 * M_TO_MM},
    
    {'component': 'Fuel Tank (Right)', 'weight_lb': total_fuel_weight_lb / 2, 
     'x_mm': 2.75 * M_TO_MM, 'y_mm': 1.32 * M_TO_MM, 'z_mm': 1.24 * M_TO_MM},
    
    # --- Carga Externa (dividida en 2 pilones simétricos) ---
    {'component': 'Payload (Left)', 'weight_lb': 502.05, 
     'x_mm': 2.944 * M_TO_MM, 'y_mm': -1.75 * M_TO_MM, 'z_mm': 0.95 * M_TO_MM},
    
    {'component': 'Payload (Right)', 'weight_lb': 502.05, 
     'x_mm': 2.944 * M_TO_MM, 'y_mm': 1.75 * M_TO_MM, 'z_mm': 0.95 * M_TO_MM},
]

# --- 3. Cálculo con Pandas ---
# Usando listas para optimizar esta vaina 

# Crear el DataFrame
df = pd.DataFrame(data)

# Calcular los momentos para cada componente
# Momento = Peso * Brazo (Arm)
df['moment_x_lb_mm'] = df['weight_lb'] * df['x_mm']
df['moment_y_lb_mm'] = df['weight_lb'] * df['y_mm']
df['moment_z_lb_mm'] = df['weight_lb'] * df['z_mm']

# Calcular los totales
total_weight = df['weight_lb'].sum()
total_moment_x = df['moment_x_lb_mm'].sum()
total_moment_y = df['moment_y_lb_mm'].sum()
total_moment_z = df['moment_z_lb_mm'].sum()

# Calcular el Centro de Gravedad (CG) final
# CG = Suma de Momentos / Suma de Pesos
mtow_cg_x = total_moment_x / total_weight
mtow_cg_y = total_moment_y / total_weight
mtow_cg_z = total_moment_z / total_weight

# --- 4. Mostrar Resultados ---
print("--- Análisis de Peso y Balance: Tayrona I ---")
print("\n--- 1. Condición de Peso Máximo al Despegue (MTOW) ---")
print("\nDesglose de Componentes y Momentos:")
print(df.to_string())
print("\n--- Resultados Finales (MTOW) ---")
print(f"Peso Máximo de Despegue (MTOW): {total_weight:,.2f} [lb]")
print("\nCentro de Gravedad (CG) en MTOW:")
print(f"  X_cg (F.S.): {mtow_cg_x:,.2f} [mm]")
print(f"  Y_cg (B.L.): {mtow_cg_y:,.2f} [mm]")
print(f"  Z_cg (W.L.): {mtow_cg_z:,.2f} [mm]")



# ...........................................................................
# ...........................................................................

# --- 2) Análisis de Escenarios Operacionales (Diagrama de Excursión) ---

# Definición de grupos de componentes según el diagrama
empty_weight_components = ['Wing', 'Horizontal Tail', 'Vertical Tail', 'Fuselaje', 'NLG', 'MLG', 
                           'Engine & Install', 'Propeller', 'Fixed Equipment']
trapped_fuel_oil = ['Trapped Fuel/Oil']
crew_front = ['Crew 1 (Student)']
crew_aft = ['Crew 2 (Instructor)']
fuel = ['Fuel Tank (Left)', 'Fuel Tank (Right)']
payload = ['Payload (Left)', 'Payload (Right)']

# Definición de los 14 escenarios del diagrama de excursión
excursion_scenarios = {
    '1: WE': empty_weight_components,
    '2: WE + Wtfo': empty_weight_components + trapped_fuel_oil,
    '3: WE + Wtfo + Wcrew_f': empty_weight_components + trapped_fuel_oil + crew_front,
    '4: WE + Wtfo + Wcrew_a': empty_weight_components + trapped_fuel_oil + crew_aft,
    '5: WE + Wtfo + Wcrew_f+a': empty_weight_components + trapped_fuel_oil + crew_front + crew_aft,
    '6: WE + Wtfo + Wcrew_f + Wf': empty_weight_components + trapped_fuel_oil + crew_front + fuel,
    '7: WE + Wtfo + Wcrew_a + Wf': empty_weight_components + trapped_fuel_oil + crew_aft + fuel,
    '8: WE + Wtfo + Wcrew_f+a + Wf': empty_weight_components + trapped_fuel_oil + crew_front + crew_aft + fuel,
    '9: WE + Wtfo + Wcrew_f + Wf + Wpl': empty_weight_components + trapped_fuel_oil + crew_front + fuel + payload,
    '10: WE + Wtfo + Wcrew_a + Wf + Wpl': empty_weight_components + trapped_fuel_oil + crew_aft + fuel + payload,
    '11: MTOW': empty_weight_components + trapped_fuel_oil + crew_front + crew_aft + fuel + payload,
    '12: WE + Wtfo + Wf': empty_weight_components + trapped_fuel_oil + fuel,
    '13: WE + Wtfo + Wpl': empty_weight_components + trapped_fuel_oil + payload,
    '14: WE + Wtfo + Wf + Wpl': empty_weight_components + trapped_fuel_oil + fuel + payload,
}

results = []
for name, components in excursion_scenarios.items():
    scenario_df = df[df['component'].isin(components)]
    
    total_w = scenario_df['weight_lb'].sum()
    total_m_x = scenario_df['moment_x_lb_mm'].sum()
    
    cg_x = total_m_x / total_w if total_w > 0 else 0
    
    results.append({'Scenario': name, 'Total Weight [lb]': total_w, 'X_cg [mm]': cg_x})

results_df = pd.DataFrame(results)

print("\n\n--- 2. Límites del Centro de Gravedad (x_cg) para Escenarios Operacionales ---")
print(results_df.to_string(index=False))

# --- 6. Encontrar los Límites de la Envolvente ---
print("\n\n--- 3. Límites de la Envolvente x_cg ---")

# Encontrar el x_cg mínimo (más adelantado)
forward_limit_scenario = results_df.loc[results_df['X_cg [mm]'].idxmin()]
print(f"\n Límite MÁS ADELANTADO (Forward):")
print(f"   x_cg:     {forward_limit_scenario['X_cg [mm]']:.2f} [mm]")
print(f"   Peso:     {forward_limit_scenario['Total Weight [lb]']:.2f} [lb]")
print(f"   Escenario: {forward_limit_scenario['Scenario']}")

# Encontrar el x_cg máximo (más atrasado)
rearward_limit_scenario = results_df.loc[results_df['X_cg [mm]'].idxmax()]
print(f"\n Límite MÁS ATRASADO (Aft/Rearward):")
print(f"   x_cg:     {rearward_limit_scenario['X_cg [mm]']:.2f} [mm]")
print(f"   Peso:     {rearward_limit_scenario['Total Weight [lb]']:.2f} [lb]")
print(f"   Escenario: {rearward_limit_scenario['Scenario']}")

# Calcular el rango
cg_range = rearward_limit_scenario['X_cg [mm]'] - forward_limit_scenario['X_cg [mm]']
print(f"\n--- Resumen del Rango ---")
print(f"   Rango total de x_cg: {cg_range:.2f} [mm]")

# ----------------------------- SUPOSICIONES -.........----------------
# --- 7. Conversión a %MAC (Basado en Asunciones) ---
print("\n\n--- 4. Límites de la Envolvente en %MAC ---")

# --- (a) Calcular Longitud de la c_MAC ---
# Datos de geometría del ala (de las especificaciones iniciales)
c_root_ft = 6.234  # Cuerda en la raíz [ft]
taper_ratio = 0.614 # Estrechamiento [lambda]
ft_to_mm = 304.8   # Conversión de pies a mm

# Fórmula para la longitud de la MAC en un ala trapezoidal
# c_MAC = (2/3) * c_r * (1 + lambda + lambda^2) / (1 + lambda)
c_mac_ft = (2/3) * c_root_ft * (1 + taper_ratio + taper_ratio**2) / (1 + taper_ratio)
c_mac_mm = c_mac_ft * ft_to_mm

print(f"\n--- Asunciones Geométricas (Paso 1) ---")
print(f"Longitud de c_MAC (calculada): {c_mac_mm:.2f} [mm] ({c_mac_ft:.3f} [ft])")

# --- (b) Calcular Ubicación de la X_LEMAC ---
# Asunción: El CG del componente "Ala" (x_mm = 2690) está al 40% de la c_MAC ------------------------------------------------
# Justificación: Rango estándar de 35-42% (segun la diapositiva 15)
wing_comp_cg_x = 2080.0  # [mm] (de la tabla de pesos vacíos)
assumed_wing_cg_perc = 0.40 # 40%

# X_LEMAC = X_cg_ala - (perc_asumido * long_c_MAC)
x_lemac_mm = wing_comp_cg_x - (assumed_wing_cg_perc * c_mac_mm)

print(f"Ubicación X_LEMAC (asumida al 40%): {x_lemac_mm:.2f} [mm]")

# --- (c) Función de Conversión ---
def convert_fs_to_mac_percent(xcg_mm, x_lemac, c_mac):
    """Convierte una ubicación F.S. (mm) a %MAC"""
    return ((xcg_mm - x_lemac) / c_mac) * 100

# --- (d) Calcular Límites Finales en %MAC ---
# Se usan las variables 'forward_limit_scenario' y 'rearward_limit_scenario'
# que ya se calcularon en la sección anterior (Paso 6).

fwd_limit_mac = convert_fs_to_mac_percent(
    forward_limit_scenario['X_cg [mm]'], 
    x_lemac_mm, 
    c_mac_mm
)

aft_limit_mac = convert_fs_to_mac_percent(
    rearward_limit_scenario['X_cg [mm]'], 
    x_lemac_mm, 
    c_mac_mm
)

range_mac = aft_limit_mac - fwd_limit_mac

print("\n--- Resultados Finales de la Envolvente (en %MAC) ---")
print(f"\n Límite MÁS ADELANTADO (Forward): {fwd_limit_mac:.2f} %MAC")
print(f" Límite MÁS ATRASADO (Aft/Rearward): {aft_limit_mac:.2f} %MAC")
print(f"\n Rango total en %MAC: {range_mac:.2f} %")

# --- 8. Generar Diagrama de Envolvente (Excursión) ---
import matplotlib.pyplot as plt

print("\n\n--- 5. Generando Diagrama de Envolvente ---")

# Definir las 8 secuencias operativas (usando los números de paso 1-14)
# (Basado en la imagen 'Possible operational scenarios')
scenarios_list = [
    [1, 2, 3, 6, 9],
    [1, 2, 4, 5, 8, 11],
    [1, 2, 4, 7, 10],
    [1, 2, 12, 6],
    [1, 2, 12, 7],
    [1, 2, 13, 14, 9],
    [1, 2, 13, 14, 10],
    [1, 2, 13, 14, 11]
]

# Crear la figura y los ejes
plt.figure(figsize=(12, 8))
ax = plt.gca()

# --- (a) Trazar las 8 secuencias operativas ---
# Iterar sobre cada una de las 8 secuencias para trazar las líneas
for i, scenario_steps in enumerate(scenarios_list):
    # Convertir los números de paso (1-14) a índices del DataFrame (0-13)
    indices = [step - 1 for step in scenario_steps]
    
    # Extraer los datos de X (CG) y Y (Peso) para esta secuencia
    x_cg_values = results_df.loc[indices]['X_cg [mm]']
    y_weight_values = results_df.loc[indices]['Total Weight [lb]']
    
    # Trazar la línea de la secuencia
    ax.plot(x_cg_values, y_weight_values, marker='o', linestyle='-', label=f'Secuencia {i+1}')

# --- (b) Anotar todos los 14 puntos de carga ---
# Usamos el results_df completo
for index, row in results_df.iterrows():
    step_label = str(index + 1) # type: ignore # Etiqueta '1', '2', ... '14'
    # Colocar la etiqueta numérica en el gráfico
    ax.text(row['X_cg [mm]'] + 5, row['Total Weight [lb]'], step_label, fontsize=9, ha='left')

# --- (c) Dibujar los límites de la envolvente ---
# (Usamos las variables 'forward_limit_scenario' y 'rearward_limit_scenario' del Paso 6)
fwd_limit_x = forward_limit_scenario['X_cg [mm]']
aft_limit_x = rearward_limit_scenario['X_cg [mm]']

ax.axvline(x=fwd_limit_x, color='red', linestyle='--', label=f'Límite Fwd ({fwd_limit_x:.2f} mm)') # type: ignore
ax.axvline(x=aft_limit_x, color='green', linestyle='--', label=f'Límite Aft ({aft_limit_x:.2f} mm)') # type: ignore

# --- (d) Configuración y visualización del gráfico ---
ax.set_title('Diagrama de Envolvente (Excursión) de CG - Tayrona I', fontsize=16)
ax.set_xlabel('Posición del X_cg (F.S.) [mm]', fontsize=12)
ax.set_ylabel('Peso Total de la Aeronave [lb]', fontsize=12)
ax.legend(loc='best', fontsize=8)
ax.grid(True, which='both', linestyle=':', linewidth=0.5)

# Ajustar los límites del eje x para dar espacio
plt.xlim(fwd_limit_x - 50, aft_limit_x + 50)

# JERO THIS IS THE GRAPH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! LOOK AT ME DUDE !!!!!!!!!
#------------------------------------------------------------------------------
# Mostrar el gráfico
#print("Mostrando gráfico... (Cierre la ventana del gráfico para finalizar el script)")
#plt.show()
#------------------------------------------------------------------------------


# ...........................................................................
# ...........................................................................
# --- 3. Verificación de Estabilidad Estática ---
print("\n\n--- 6. Verificación de Estabilidad Estática (Punto 3) ---")

# Datos del problema
X_NP_mm = 2.87 * M_TO_MM  # Punto Neutro dado en 2.87 m
print(f"\n--- Datos de Entrada ---")
print(f"Punto Neutro (X_NP): {X_NP_mm:.2f} [mm]")

# --- (a) Calcular S.M. en el Límite Adelantado ---
# (Usa 'forward_limit_scenario' y 'c_mac_mm' del script anterior)
xcg_fwd_mm = forward_limit_scenario['X_cg [mm]']
sm_fwd = ((X_NP_mm - xcg_fwd_mm) / c_mac_mm) * 100

print(f"\n--- Condición Más Estable (CG Adelantado) ---")
print(f"  X_cg (Fwd): {xcg_fwd_mm:.2f} [mm]")
print(f"  Margen Estático (S.M. fwd): {sm_fwd:.2f} %")

# --- (b) Calcular S.M. en el Límite Atrasado ---
# (Usa 'rearward_limit_scenario' y 'c_mac_mm' del script anterior)
xcg_aft_mm = rearward_limit_scenario['X_cg [mm]']
sm_aft = ((X_NP_mm - xcg_aft_mm) / c_mac_mm) * 100

print(f"\n--- Condición Menos Estable (CG Atrasado) ---")
print(f"  X_cg (Aft): {xcg_aft_mm:.2f} [mm]")
print(f"  Margen Estático (S.M. aft): {sm_aft:.2f} %")

# --- (c) Verificación del 15% S.M. ---
# Calcular qué CG nos daría el 15% S.M. de referencia
xcg_at_15_sm = X_NP_mm - (0.15 * c_mac_mm)
print(f"\n--- Verificación de Referencia ---")
print(f"  El S.M. de 15% se alcanzaría con un X_cg en: {xcg_at_15_sm:.2f} [mm]")
print(f"  Rango operativo de S.M.: [{sm_aft:.2f}%, {sm_fwd:.2f}%]")
if float(sm_fwd) > 0 and float(sm_aft) > 0: # type: ignore
    print(f"\n --------!! VERIFICACIÓN: La aeronave es estable en toda la envolvente (S.M. > 0).")
else:
    print(f"\n --------!!!!!!!!!!!!! ALERTA: La aeronave NO es estable en toda la envolvente (S.M. <= 0).")


