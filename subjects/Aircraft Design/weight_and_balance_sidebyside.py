import pandas as pd
# ...........................................................................
# ...........................................................................
# CONFIGURACIÓN: COCKPIT SIDE-BY-SIDE
# ...........................................................................
# ...........................................................................

# --- ASUNCIONES DEL DISEÑO (SIDE-BY-SIDE) ---
# ==================================================================
# 1. POSICIÓN LONGITUDINAL (X):
#    - Configuración tandem original: Crew 1 @ X=2.45m, Crew 2 @ X=3.49m
#    - Configuración side-by-side: Ambos @ X=2.90m (promedio geométrico)
#    - Justificación: En cockpits side-by-side, los pilotos están alineados
#      longitudinalmente para mantener visibilidad y acceso a controles.
#
# 2. POSICIÓN LATERAL (Y):
#    - Configuración tandem original: Ambos @ Y=0 (centerline)
#    - Configuración side-by-side: Crew 1 @ Y=-0.75m (Left), Crew 2 @ Y=+0.75m (Right)
#    - Separación total: 1.50 m (típico para aeronaves de entrenamiento)
#    - Justificación: Ancho del fuselaje permite esta separación simétrica.
#
# 3. POSICIÓN VERTICAL (Z):
#    - Configuración tandem original: Crew 1 @ Z=1.52m, Crew 2 @ Z=1.57m
#    - Configuración side-by-side: Ambos @ Z=1.54m (promedio)
#    - Justificación: En side-by-side, ambos pilotos comparten la misma línea de visión.
#
# 4. PESO DE LA TRIPULACIÓN:
#    - Cada piloto: 220 lb (sin cambios)
#    - Total: 440 lb (sin cambios)
#
# 5. IMPACTO EN CG:
#    - CG_Y se desplazará hacia Y=0 (más simétrico lateralmente)
#    - CG_X se desplazará hacia atrás (~200mm respecto a tandem)
#    - Esto puede mejorar el margen estático (S.M.) en algunos escenarios
#
# ==================================================================

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
    
    # --- Tripulación (SIDE-BY-SIDE CONFIGURATION) ---
    # Asunción: Ambos pilotos en X=2.90m (promedio entre 2.45m y 3.49m del tandem)
    #           Separados lateralmente: -0.75m (izquierda) y +0.75m (derecha)
    #           Mismo nivel vertical: Z=1.54m (promedio de 1.52m y 1.57m)
    {'component': 'Crew 1 (Left Pilot)', 'weight_lb': 220.00, 
     'x_mm': 2.90 * M_TO_MM, 'y_mm': -0.75 * M_TO_MM, 'z_mm': 1.54 * M_TO_MM},
    
    {'component': 'Crew 2 (Right Pilot)', 'weight_lb': 220.00, 
     'x_mm': 2.90 * M_TO_MM, 'y_mm': 0.75 * M_TO_MM, 'z_mm': 1.54 * M_TO_MM},
    
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
print("=" * 80)
print("--- Análisis de Peso y Balance: Tayrona I (COCKPIT SIDE-BY-SIDE) ---")
print("=" * 80)
print("\n--- 1. Condición de Peso Máximo al Despegue (MTOW) - SIDE-BY-SIDE ---")
print("\nDesglose de Componentes y Momentos:")
print(df.to_string())
print("\n--- Resultados Finales (MTOW) - SIDE-BY-SIDE ---")
print(f"Peso Máximo de Despegue (MTOW): {total_weight:,.2f} [lb]")
print("\nCentro de Gravedad (CG) en MTOW - SIDE-BY-SIDE:")
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
crew_left = ['Crew 1 (Left Pilot)']
crew_right = ['Crew 2 (Right Pilot)']
fuel = ['Fuel Tank (Left)', 'Fuel Tank (Right)']
payload = ['Payload (Left)', 'Payload (Right)']

# Definición de los 14 escenarios del diagrama de excursión
# MODIFICACIÓN: En lugar de "Crew_f" y "Crew_a" (front/aft), ahora usamos
# "Crew_left" y "Crew_right" (izquierda/derecha). Sin embargo, para mantener
# el mismo análisis de envolvente, ambas tripulaciones estarán en la mayoría
# de escenarios (ya que están lado-a-lado, no es "solo piloto izquierdo" típicamente).
excursion_scenarios = {
    '1: WE': empty_weight_components,
    '2: WE + Wtfo': empty_weight_components + trapped_fuel_oil,
    '3: WE + Wtfo + Wcrew_L': empty_weight_components + trapped_fuel_oil + crew_left,
    '4: WE + Wtfo + Wcrew_R': empty_weight_components + trapped_fuel_oil + crew_right,
    '5: WE + Wtfo + Wcrew_L+R': empty_weight_components + trapped_fuel_oil + crew_left + crew_right,
    '6: WE + Wtfo + Wcrew_L + Wf': empty_weight_components + trapped_fuel_oil + crew_left + fuel,
    '7: WE + Wtfo + Wcrew_R + Wf': empty_weight_components + trapped_fuel_oil + crew_right + fuel,
    '8: WE + Wtfo + Wcrew_L+R + Wf': empty_weight_components + trapped_fuel_oil + crew_left + crew_right + fuel,
    '9: WE + Wtfo + Wcrew_L + Wf + Wpl': empty_weight_components + trapped_fuel_oil + crew_left + fuel + payload,
    '10: WE + Wtfo + Wcrew_R + Wf + Wpl': empty_weight_components + trapped_fuel_oil + crew_right + fuel + payload,
    '11: MTOW': empty_weight_components + trapped_fuel_oil + crew_left + crew_right + fuel + payload,
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

print("\n\n--- 2. Límites del Centro de Gravedad (x_cg) para Escenarios Operacionales - SIDE-BY-SIDE ---")
print(results_df.to_string(index=False))

# --- 6. Encontrar los Límites de la Envolvente ---
print("\n\n--- 3. Límites de la Envolvente x_cg - SIDE-BY-SIDE ---")

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
print("\n\n--- 4. Límites de la Envolvente en %MAC - SIDE-BY-SIDE ---")

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
# Asunción: El CG del componente "Ala" (x_mm = 2080) está al 40% de la c_MAC ------------------------------------------------
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

print("\n--- Resultados Finales de la Envolvente (en %MAC) - SIDE-BY-SIDE ---")
print(f"\n Límite MÁS ADELANTADO (Forward): {fwd_limit_mac:.2f} %MAC")
print(f" Límite MÁS ATRASADO (Aft/Rearward): {aft_limit_mac:.2f} %MAC")
print(f"\n Rango total en %MAC: {range_mac:.2f} %")

# --- 8. Generar Diagrama de Envolvente (Excursión) ---
import matplotlib.pyplot as plt

print("\n\n--- 5. Generando Diagrama de Envolvente - SIDE-BY-SIDE ---")

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
ax.set_title('Diagrama de Envolvente (Excursión) de CG - Tayrona I (SIDE-BY-SIDE)', fontsize=16)
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
print("\n\n--- 6. Verificación de Estabilidad Estática (Punto 3) - SIDE-BY-SIDE ---")

# Datos del problema
X_NP_mm = 2.87 * M_TO_MM  # Punto Neutro dado en 2.87 m
print(f"\n--- Datos de Entrada ---")
print(f"Punto Neutro (X_NP): {X_NP_mm:.2f} [mm]")

# --- (a) Calcular S.M. en el Límite Adelantado ---
# (Usa 'forward_limit_scenario' y 'c_mac_mm' del script anterior)
xcg_fwd_mm = forward_limit_scenario['X_cg [mm]']
sm_fwd = ((X_NP_mm - xcg_fwd_mm) / c_mac_mm) * 100

print(f"\n--- Condición Más Estable (CG Adelantado) - SIDE-BY-SIDE ---")
print(f"  X_cg (Fwd): {xcg_fwd_mm:.2f} [mm]")
print(f"  Margen Estático (S.M. fwd): {sm_fwd:.2f} %")

# --- (b) Calcular S.M. en el Límite Atrasado ---
# (Usa 'rearward_limit_scenario' y 'c_mac_mm' del script anterior)
xcg_aft_mm = rearward_limit_scenario['X_cg [mm]']
sm_aft = ((X_NP_mm - xcg_aft_mm) / c_mac_mm) * 100

print(f"\n--- Condición Menos Estable (CG Atrasado) - SIDE-BY-SIDE ---")
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

# ...........................................................................
# --- 7. COMPARACIÓN CON CONFIGURACIÓN TANDEM (ORIGINAL) ---
# ...........................................................................
print("\n\n" + "=" * 80)
print("--- CAMBIOS INTRODUCIDOS POR CONFIGURACIÓN SIDE-BY-SIDE ---")
print("=" * 80)

print("\nRESUMEN DE CAMBIOS EN POSICIONAMIENTO DE TRIPULACIÓN:")
print("-" * 80)
print("Parámetro              | Tandem (Original)  | Side-by-Side       | Cambio")
print("-" * 80)
print(f"Crew 1 - X [mm]        | {2.45*M_TO_MM:>17.0f} | {2.90*M_TO_MM:>17.0f} | {(2.90-2.45)*M_TO_MM:>+7.0f}")
print(f"Crew 1 - Y [mm]        | {0:>17.0f} | {-0.75*M_TO_MM:>17.0f} | {-0.75*M_TO_MM:>+7.0f}")
print(f"Crew 2 - X [mm]        | {3.49*M_TO_MM:>17.0f} | {2.90*M_TO_MM:>17.0f} | {(2.90-3.49)*M_TO_MM:>+7.0f}")
print(f"Crew 2 - Y [mm]        | {0:>17.0f} | {0.75*M_TO_MM:>17.0f} | {0.75*M_TO_MM:>+7.0f}")
print("-" * 80)

print("\nIMPACTO EN EL CENTRO DE GRAVEDAD (CG):")
print("-" * 80)
print(f"CG_X (MTOW):           {mtow_cg_x:.2f} mm")
print(f"CG_Y (MTOW):           {mtow_cg_y:.2f} mm  (más simétrico que tandem)")
print(f"CG_Z (MTOW):           {mtow_cg_z:.2f} mm")
print("-" * 80)

print("\nCAMBIOS EN ENVOLVENTE Y ESTABILIDAD:")
print("-" * 80)
print(f"Rango de CG (X):       {cg_range:.2f} mm")
print(f"Rango en %MAC:         {range_mac:.2f} %")
print(f"Margen Estático (Fwd): {sm_fwd:.2f} %")
print(f"Margen Estático (Aft): {sm_aft:.2f} %")
print("-" * 80)

print("\n" + "=" * 80)
