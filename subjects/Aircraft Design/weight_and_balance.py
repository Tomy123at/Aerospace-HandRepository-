import pandas as pd

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
    {'component': 'Wing', 'weight_lb': 320.00, 'x_mm': 2690, 'y_mm': 0, 'z_mm': 1280},
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


# --- 5. Análisis de Escenarios Operacionales (Diagrama de Excursión) ---

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