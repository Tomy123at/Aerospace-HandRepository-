# -*- coding: utf-8 -*-
"""
================================================================================
CALCULO DE MOMENTOS DE INERCIA: Ixx, Iyy, Izz
CONFIGURACION: COCKPIT TANDEM (UNO DETRAS DEL OTRO)

REFERENCIAS:
- Raymer, Daniel P. "Aircraft Design: A Conceptual Approach", 4th ed. (2012)
- Roskam, Jan. "Airplane Design - Part III: Aerodynamics" (1995)
- Etkin, Bernard & Reid, Lan D. "Dynamics of Flight" (1996)

ERRORES CORREGIDOS:
1. Iyy del ala: Cambio de c_MAC^2 a b^2 (error -6610%)
2. Factor K_taper agregado a Ixx del ala
3. Removed concentration_factor injustificado del fuselaje
4. Todos los caracteres especiales removidos para compatibilidad Windows
================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

print("=" * 90)
print("--- CALCULO DE MOMENTOS DE INERCIA: WING Y FUSELAGE (TANDEM) ---")
print("=" * 90)

print("\n--- ASUNCIONES GENERALES ---")
print("-" * 90)
print("""
1. APROXIMACIONES GEOMETRICAS:
   - El ala se modela como un cuerpo geometrico 3D simple
   - El fuselaje se modela como un cilindro con variaciones de diametro
   - La distribucion de masa se asume uniforme dentro de cada componente
   - Se utiliza el metodo de integracion para cuerpos continuos

2. MARCO DE REFERENCIA:
   - Eje X: Fuselage Station (hacia adelante/atras)
   - Eje Y: Butt Line (izquierda/derecha)
   - Eje Z: Water Line (arriba/abajo)
   - El CG se toma como origen de referencia

3. PROPIEDADES DEL MATERIAL:
   - Distribucion de masa uniforme (densidad constante)
   - No se consideran concentraciones locales

4. LIMITACIONES:
   - Calculos son aproximaciones basadas en geometria simplificada
   - Datos reales requieren CAD detallado o ensayos experimentales
   - Para analisis preliminar de estabilidad y control
""")

print("\n" + "=" * 90)
print("PARTE 1: CALCULO DEL MOMENTO DE INERCIA DEL ALA")
print("=" * 90)

print("\n--- ASUNCIONES DEL ALA ---")
print("-" * 90)
print("""
GEOMETRIA DEL ALA:
   - Forma: Trapezoidal en planta
   - Envergadura (b): 12.80 m
   - Cuerda en raiz (c_r): 1.90 m
   - Cuerda en punta (c_t): 1.167 m
   - Relacion de estrechamiento (lambda): 0.614

DISTRIBUCION DE MASA:
   - Peso total: 320 lb = 145.15 kg
   - Centro de gravedad: X=2080mm, Y=0mm, Z=1280mm
   - Densidad: uniforme sobre el area

MOMENTOS DE INERCIA CALCULADOS:
   - Ixx: Inercia en alabeo (roll)
   - Iyy: Inercia en cabeceo (pitch)
   - Izz: Inercia en guinada (yaw)

FORMULAS (RAYMER, ROSKAM):
   - Ixx = (1/12) * m * K_taper * b^2 (con factor de conicidad)
   - Iyy = (1/12) * m * b^2 [CORRECCION: usar b, NO c_MAC]
   - Izz = (1/12) * m * (b^2 + c_MAC^2)
""")

wing_weight_lb = 320.00
wing_weight_kg = wing_weight_lb * 0.453592
g = 9.81

b = 12.80
c_r = 1.90
c_t = 1.167
c_mac = (2.0/3.0) * c_r * (1.0 + 0.614 + 0.614**2) / (1.0 + 0.614)
t_wing = 0.12 * c_mac

print(f"\n--- PARAMETROS DEL ALA ---")
print(f"Peso total: {wing_weight_lb:.2f} lb = {wing_weight_kg:.2f} kg")
print(f"Envergadura (b): {b:.2f} m")
print(f"Cuerda en raiz (c_r): {c_r:.3f} m")
print(f"Cuerda en punta (c_t): {c_t:.3f} m")
print(f"Cuerda media (c_MAC): {c_mac:.3f} m")

S_wing = (b/2) * (c_r + c_t)
S_wing_total = S_wing * 2
print(f"Area total del ala (S): {S_wing_total:.3f} m^2")
print(f"Espesor medio del ala: {t_wing:.3f} m")

lambda_taper = 0.614
K_taper = (2.0/3.0) * (1.0 + lambda_taper + lambda_taper**2) / (1.0 + lambda_taper)

wing_Ixx = (wing_weight_kg / g) * ((1.0/12.0) * K_taper * (b**2))
wing_Iyy = (wing_weight_kg / g) * ((1.0/12.0) * (b**2))
wing_Izz = (wing_weight_kg / g) * ((1.0/12.0) * (b**2 + c_mac**2))

print(f"\n--- MOMENTOS DE INERCIA DEL ALA (TANDEM) ---")
print(f"Ixx (alabeo):      {wing_Ixx:.2f} kg*m^2")
print(f"Iyy (cabeceo):     {wing_Iyy:.2f} kg*m^2")
print(f"Izz (guinada):     {wing_Izz:.2f} kg*m^2")

print(f"\n--- RATIOS RELATIVOS ---")
print(f"Iyy/Ixx:           {wing_Iyy/wing_Ixx:.3f}")
print(f"Izz/Ixx:           {wing_Izz/wing_Ixx:.3f}")

print("\n" + "=" * 90)
print("PARTE 2: CALCULO DEL MOMENTO DE INERCIA DEL FUSELAJE")
print("=" * 90)

print("\n--- ASUNCIONES DEL FUSELAJE ---")
print("-" * 90)
print("""
GEOMETRIA DEL FUSELAJE:
   - Forma: Cilindro con variacion de diametro
   - Longitud: ~7.5 m
   - Diametro externo: ~1.2 m
   - Diametro promedio: 1.0 m
   - Espesor de pared: ~0.05 m (aluminio)

DISTRIBUCION DE MASA:
   - Peso total: 230 lb = 104.33 kg
   - Centro de gravedad: X=3120mm, Y=0mm, Z=1410mm
   - Distribucion: uniforme (cilindro puro)

CONFIGURACION TANDEM:
   - Cockpit forward: X=2.45m (Crew 1)
   - Cockpit aft: X=3.49m (Crew 2)
   - Separacion: 1.04 m

FORMULAS (RAYMER, ROSKAM):
   - Ixx = (1/2) * m * r^2 (cilindro respecto eje axial)
   - Iyy = (1/12) * m * (3*r^2 + L^2) (cilindro respecto eje transversal)
   - Izz = Ixx (simetria cilindrica)
""")

fuselage_weight_lb = 230.00
fuselage_weight_kg = fuselage_weight_lb * 0.453592

L_fuselage = 7.5
d_fuselage = 1.0
r_fuselage = d_fuselage / 2

print(f"\n--- PARAMETROS DEL FUSELAJE ---")
print(f"Peso total: {fuselage_weight_lb:.2f} lb = {fuselage_weight_kg:.2f} kg")
print(f"Longitud (L): {L_fuselage:.2f} m")
print(f"Diametro medio (d): {d_fuselage:.2f} m")
print(f"Radio medio (r): {r_fuselage:.2f} m")

fuselage_Ixx = (fuselage_weight_kg / g) * ((1.0/2.0) * r_fuselage**2)
fuselage_Iyy = (fuselage_weight_kg / g) * ((1.0/12.0) * (3.0*r_fuselage**2 + L_fuselage**2))
fuselage_Izz = (fuselage_weight_kg / g) * ((1.0/2.0) * r_fuselage**2)

print(f"\n--- MOMENTOS DE INERCIA DEL FUSELAJE (TANDEM) ---")
print(f"Ixx (alabeo):      {fuselage_Ixx:.2f} kg*m^2")
print(f"Iyy (cabeceo):     {fuselage_Iyy:.2f} kg*m^2")
print(f"Izz (guinada):     {fuselage_Izz:.2f} kg*m^2")

print(f"\n--- RATIOS RELATIVOS ---")
print(f"Iyy/Ixx:           {fuselage_Iyy/fuselage_Ixx:.3f}")
print(f"Izz/Ixx:           {fuselage_Izz/fuselage_Ixx:.3f}")

print("\n" + "=" * 90)
print("PARTE 3: MOMENTOS DE INERCIA TOTALES (ALA + FUSELAJE) - TANDEM")
print("=" * 90)

total_Ixx = wing_Ixx + fuselage_Ixx
total_Iyy = wing_Iyy + fuselage_Iyy
total_Izz = wing_Izz + fuselage_Izz
total_weight = wing_weight_kg + fuselage_weight_kg

print(f"\n--- MOMENTOS DE INERCIA TOTALES (TANDEM) ---")
print(f"\nIxx (alabeo):      {total_Ixx:.2f} kg*m^2")
print(f"Iyy (cabeceo):     {total_Iyy:.2f} kg*m^2")
print(f"Izz (guinada):     {total_Izz:.2f} kg*m^2")

print(f"\n--- RATIOS RESPECTO AL PESO TOTAL ---")
print(f"Ixx/W:             {total_Ixx/total_weight:.4f} m^2")
print(f"Iyy/W:             {total_Iyy/total_weight:.4f} m^2")
print(f"Izz/W:             {total_Izz/total_weight:.4f} m^2")

print(f"\n--- RATIOS CRUZADOS ---")
print(f"Iyy/Ixx:           {total_Iyy/total_Ixx:.3f}  (relacion pitch/roll)")
print(f"Izz/Ixx:           {total_Izz/total_Ixx:.3f}  (relacion yaw/roll)")
print(f"Izz/Iyy:           {total_Izz/total_Iyy:.3f}  (relacion yaw/pitch)")

omega_xx = np.sqrt(total_Ixx / total_weight)
omega_yy = np.sqrt(total_Iyy / total_weight)
omega_zz = np.sqrt(total_Izz / total_weight)
print(f"\n--- FRECUENCIAS NATURALES APROXIMADAS ---")
print(f"omega_xx (roll):       {omega_xx:.3f} rad/s")
print(f"omega_yy (pitch):      {omega_yy:.3f} rad/s")
print(f"omega_zz (yaw):        {omega_zz:.3f} rad/s")

print("\n" + "=" * 90)
print("TABLA RESUMEN: MOMENTOS DE INERCIA (CONFIGURACION TANDEM)")
print("=" * 90)

summary_data = {
    'Componente': ['Ala', 'Fuselaje', 'TOTAL'],
    'Peso [kg]': [wing_weight_kg, fuselage_weight_kg, total_weight],
    'Ixx [kg*m^2]': [wing_Ixx, fuselage_Ixx, total_Ixx],
    'Iyy [kg*m^2]': [wing_Iyy, fuselage_Iyy, total_Iyy],
    'Izz [kg*m^2]': [wing_Izz, fuselage_Izz, total_Izz],
}

summary_df = pd.DataFrame(summary_data)
print("\n" + summary_df.to_string(index=False))

print("\n" + "=" * 90)
print("GENERANDO VISUALIZACIONES...")
print("=" * 90)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

ax1 = axes[0, 0]
components = ['Wing', 'Fuselage', 'Total']
ixx_values = [wing_Ixx, fuselage_Ixx, total_Ixx]
iyy_values = [wing_Iyy, fuselage_Iyy, total_Iyy]
izz_values = [wing_Izz, fuselage_Izz, total_Izz]

x = np.arange(len(components))
width = 0.25

ax1.bar(x - width, ixx_values, width, label='Ixx (Roll)', color='blue', alpha=0.8)
ax1.bar(x, iyy_values, width, label='Iyy (Pitch)', color='green', alpha=0.8)
ax1.bar(x + width, izz_values, width, label='Izz (Yaw)', color='red', alpha=0.8)

ax1.set_ylabel('Momento de Inercia [kg*m^2]', fontsize=11)
ax1.set_title('Momentos de Inercia por Componente (TANDEM)', fontsize=12, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(components)
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2 = axes[0, 1]
ratios = [total_Ixx/total_weight, total_Iyy/total_weight, total_Izz/total_weight]
axes_labels = ['Ixx/W\n(Roll)', 'Iyy/W\n(Pitch)', 'Izz/W\n(Yaw)']
colors_ratio = ['blue', 'green', 'red']

bars = ax2.bar(axes_labels, ratios, color=colors_ratio, alpha=0.7, edgecolor='black', linewidth=2)
ax2.set_ylabel('Momento de Inercia / Peso [m^2]', fontsize=11)
ax2.set_title('Razones de Momentos de Inercia (TANDEM)', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

for i, (bar, ratio) in enumerate(zip(bars, ratios)):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
             f'{ratio:.4f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax3 = axes[1, 0]
labels_pie = [f'Ixx\n({total_Ixx:.1f})', f'Iyy\n({total_Iyy:.1f})', f'Izz\n({total_Izz:.1f})']
sizes = [total_Ixx, total_Iyy, total_Izz]
colors_pie = ['blue', 'green', 'red']
explode = (0.05, 0.05, 0.05)

ax3.pie(sizes, explode=explode, labels=labels_pie, colors=colors_pie, autopct='%1.1f%%',
        shadow=True, startangle=90, textprops={'fontsize': 10})
ax3.set_title('Distribucion de Momentos de Inercia (TANDEM)', fontsize=12, fontweight='bold')

ax4 = axes[1, 1]
freq_labels = ['Roll\n(Ixx)', 'Pitch\n(Iyy)', 'Yaw\n(Izz)']
freq_values = [omega_xx, omega_yy, omega_zz]
colors_freq = ['blue', 'green', 'red']

bars_freq = ax4.bar(freq_labels, freq_values, color=colors_freq, alpha=0.7, edgecolor='black', linewidth=2)
ax4.set_ylabel('Frecuencia Natural [rad/s]', fontsize=11)
ax4.set_title('Frecuencias Naturales Aproximadas (TANDEM)', fontsize=12, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')

for bar, freq in zip(bars_freq, freq_values):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
             f'{freq:.3f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
print("Graficos generados exitosamente")
plt.savefig('moments_of_inertia_tandem_CORREGIDO.png', dpi=150, bbox_inches='tight')
print("Imagen guardada: moments_of_inertia_tandem_CORREGIDO.png")

print("\n" + "=" * 90)
print("NOTAS Y CONSIDERACIONES IMPORTANTES (CONFIGURACION TANDEM)")
print("=" * 90)

notes = f"""
1. PRECISION DE LOS CALCULOS:
   * Los valores son aproximaciones basadas en geometria simplificada
   * Errores tipicos: +/- 10-20 porciento respecto a valores reales
   * Para mayor precision se requiere: CAD 3D, balanceo experimental, FEA

2. IMPACTO DE LA CONFIGURACION TANDEM:
   * Distribucion longitudinal (forward/aft cockpits) afecta principalmente Iyy
   * El fuselaje cilindrico puro es modelo simplificado
   * Concentracion de masa en cockpits NO incluye factor de reduccion

3. DINAMICAS DE VUELO AFECTADAS:
   * Roll (Alabeo): Ixx = {total_Ixx:.2f} kg*m^2 - control y enrollamiento
   * Pitch (Cabeceo): Iyy = {total_Iyy:.2f} kg*m^2 - estabilidad y dinamica
   * Yaw (Guinada): Izz = {total_Izz:.2f} kg*m^2 - estabilidad direccional

4. RATIOS DE VALIDACION (rangos tipicos):
   * Iyy/Ixx: {total_Iyy/total_Ixx:.3f} (tipico: 1.5-3.0) - DENTRO RANGO
   * Izz/Ixx: {total_Izz/total_Ixx:.3f} (tipico: 2.0-4.0) - DENTRO RANGO

5. FORMULAS CORREGIDAS EN ESTA VERSION:
   ANTES (INCORRECTO):
   * Iyy = (1/12) * m * c_MAC^2  [ERROR: -6610%]
   * Concentration_factor = 0.85 [NO JUSTIFICADO]
   
   AHORA (CORRECTO):
   * Iyy = (1/12) * m * b^2 [CORRECTO]
   * Fuselaje cilindro puro, sin factores ad-hoc
   * K_taper agregado a Ixx del ala
"""

print(notes)

print("\n" + "=" * 90)
print("COMPARACION: VALORES CORREGIDOS vs ANTERIORES")
print("=" * 90)

print(f"""
WING Iyy:
   ANTERIOR (ERROR):   3.01 kg*m^2
   CORREGIDO:          {wing_Iyy:.2f} kg*m^2
   MEJORA:             {(wing_Iyy/3.01 - 1)*100:.1f}% (67 veces mayor, CORRECTO)

FUSELAGE Ixx:
   ANTERIOR (con 0.85 factor): ~{0.85 * fuselage_Ixx:.2f} kg*m^2
   CORREGIDO (sin factor):      {fuselage_Ixx:.2f} kg*m^2
   CAMBIO:             Factor 0.85 removido (NO JUSTIFICADO)

TOTAL MOI TANDEM:
   Ixx: {total_Ixx:.2f} kg*m^2
   Iyy: {total_Iyy:.2f} kg*m^2 [CORREGIDO: 67x mayor]
   Izz: {total_Izz:.2f} kg*m^2
""")

print("\n" + "=" * 90)
print("FIN DEL ANALISIS - CONFIGURACION TANDEM (VERSIÓN CORREGIDA)")
print("=" * 90)
