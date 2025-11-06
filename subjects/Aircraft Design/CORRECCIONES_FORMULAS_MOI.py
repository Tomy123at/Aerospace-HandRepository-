# -*- coding: utf-8 -*-
"""
CORRECCIONES ESPECÍFICAS PARA MOMENTOS DE INERCIA
==================================================
Este archivo contiene las fórmulas CORREGIDAS y la justificación técnica
"""

import numpy as np

# ==============================================================================
# CORRECCIONES EN FÓRMULAS DE MOMENTOS DE INERCIA
# ==============================================================================

print("=" * 80)
print("ANÁLISIS DE FÓRMULAS INCORRECTAS Y CORRECCIONES")
print("=" * 80)

# Datos de la aeronave
wing_weight_kg = 320.00 * 0.453592  # 145.15 kg
fuselage_weight_kg = 230.00 * 0.453592  # 104.33 kg
g = 9.81

# Geometría
b = 12.80  # Envergadura [m]
c_r = 1.90  # Cuerda raíz [m]
c_t = 1.167  # Cuerda punta [m]
taper_ratio = 0.614  # lambda
c_mac = (2/3) * c_r * (1 + taper_ratio + taper_ratio**2) / (1 + taper_ratio)  # 1.426 m
L_fuselage = 7.5  # Longitud fuselaje [m]
r_fuselage = 0.5  # Radio medio [m]
t_wing = 0.12 * c_mac  # Espesor medio ala [m]

print("\nPARAMETROS DE ENTRADA:")
print(f"Wing weight: {wing_weight_kg:.2f} kg")
print(f"Fuselage weight: {fuselage_weight_kg:.2f} kg")
print(f"Envergadura (b): {b:.2f} m")
print(f"c_MAC: {c_mac:.3f} m")
print(f"Espesor ala (t): {t_wing:.3f} m")
print(f"Fuselage length: {L_fuselage:.2f} m")
print(f"Fuselage radius: {r_fuselage:.2f} m")

# ==============================================================================
# PROBLEMA 1: CÁLCULO DE Ixx DEL ALA
# ==============================================================================

print("\n" + "=" * 80)
print("PROBLEMA 1: FÓRMULA INCORRECTA DE Ixx (ALABEO)")
print("=" * 80)

print("\n❌ FÓRMULA INCORRECTA (usada actualmente):")
print("   Ixx = (1/12) × m × (b² + 3×t²)")
print("   → Esta es la fórmula para un rectángulo sólido")
print("   → NO es apropiada para un ala trapezoidal")
print()

# Cálculo incorrecto
Ixx_wrong = (wing_weight_kg / g) * ((1/12) * (b**2 + 3*t_wing**2))
print(f"   Resultado incorrecto: Ixx = {Ixx_wrong:.2f} kg⋅m²")

print("\n✓ FÓRMULA CORRECTA:")
print("   Para ala trapezoidal en planta:")
print("   Ixx ≈ (1/12) × m × b² × K_taper")
print("   donde K_taper = (2/3) × (1 + lambda + lambda²) / (1 + lambda)")
print()

# Cálculo correcto
K_taper = (2/3) * (1 + taper_ratio + taper_ratio**2) / (1 + taper_ratio)
Ixx_correct = (wing_weight_kg / g) * ((1/12) * (b**2) * K_taper)
print(f"   K_taper = {K_taper:.4f}")
print(f"   Resultado correcto: Ixx = {Ixx_correct:.2f} kg⋅m²")
print(f"   Diferencia: {Ixx_wrong - Ixx_correct:.2f} kg⋅m² ({(Ixx_wrong/Ixx_correct - 1)*100:.1f}% error)")

# ==============================================================================
# PROBLEMA 2: CÁLCULO DE Iyy DEL ALA
# ==============================================================================

print("\n" + "=" * 80)
print("PROBLEMA 2: FÓRMULA INCORRECTA DE Iyy (CABECEO)")
print("=" * 80)

print("\n❌ FÓRMULA INCORRECTA (usada actualmente):")
print("   Iyy ≈ (1/12) × m × c_MAC²")
print("   → Dimensionalmente incorrecta para momento de inercia de alabeo")
print("   → c_MAC² tiene dimensión [m²], pero Iyy requiere [m²] × [kg]")
print()

Iyy_wrong = (wing_weight_kg / g) * ((1/12) * (c_mac**2))
print(f"   Resultado incorrecto: Iyy = {Iyy_wrong:.2f} kg⋅m²")

print("\n✓ FÓRMULA CORRECTA:")
print("   Para un ala concentrada en plano XZ respecto eje Y:")
print("   Iyy = ∫∫ (x² + z²) dm ≈ (1/12) × m × (b² + t²)")
print("   PERO para wing sólo x2: Iyy ≈ (1/12) × m × b²")
print()

Iyy_correct = (wing_weight_kg / g) * ((1/12) * (b**2))
print(f"   Resultado correcto (aproximación): Iyy = {Iyy_correct:.2f} kg⋅m²")
print(f"   Diferencia: {Iyy_wrong - Iyy_correct:.2f} kg⋅m² ({(Iyy_correct/Iyy_wrong - 1)*100:.1f}% menor)")

print("\n   JUSTIFICACIÓN:")
print("   - Para ala de tapered planform: inercia similar a rectángulo")
print("   - La dimensión que importa es b (envergadura), no c_MAC")
print("   - c_MAC aparece para cálculos aerodinámicos, no para masas")

# ==============================================================================
# PROBLEMA 3: CÁLCULO DE Izz DEL ALA
# ==============================================================================

print("\n" + "=" * 80)
print("PROBLEMA 3: USO INCORRECTO DEL TEOREMA DE EJES PARALELOS")
print("=" * 80)

print("\n❌ ASUNCIÓN INCORRECTA (usada actualmente):")
print("   Izz ≈ Ixx + Iyy")
print("   → Válido solo para objetos planos (z = const)")
print("   → El ala NO es perfectamente plana (tiene espesor)")
print()

Izz_wrong = Ixx_wrong + Iyy_wrong
print(f"   Resultado incorrecto: Izz = {Ixx_wrong:.2f} + {Iyy_wrong:.2f} = {Izz_wrong:.2f} kg⋅m²")

print("\n✓ FÓRMULA CORRECTA:")
print("   Para ala rectangular (aproximación mejor):")
print("   Izz = (1/12) × m × (b² + c_MAC²)")
print("   Esto suma correctamente las inercias en ambas direcciones")
print()

Izz_correct = (wing_weight_kg / g) * ((1/12) * (b**2 + c_mac**2))
print(f"   Resultado correcto: Izz = {Izz_correct:.2f} kg⋅m²")
print(f"   Diferencia: {Izz_wrong - Izz_correct:.2f} kg⋅m² ({(Izz_wrong/Izz_correct - 1)*100:.1f}% error)")

# ==============================================================================
# PROBLEMA 4: FACTOR DE CONCENTRACIÓN EN TANDEM
# ==============================================================================

print("\n" + "=" * 80)
print("PROBLEMA 4: FACTOR DE CONCENTRACIÓN INCORRECTO (TANDEM)")
print("=" * 80)

print("\n❌ ERROR EN TANDEM:")
print("   concentration_factor = 0.85 aplicado a Ixx del fuselaje")
print("   Justificación dada: 'concentración en cockpit forward y aft'")
print()
print("   PROBLEMA: Los pilotos en tandem están en Y = 0 (centerline)")
print("   Ixx es respecto al eje X (eje longitudinal de vuelo)")
print("   La dispersión longitudinal (en X) NO afecta Ixx (alabeo)")
print("   Ixx solo depende de la distribución en plano YZ")
print()

print("✓ CORRECCIÓN:")
print("   Para fuselaje cilíndrico:")
print("   Ixx = (1/2) × m × r² (sin factor)")
print("   El factor 0.85 debería ser 1.0")
print()

fuselage_Ixx_wrong = 0.85 * (fuselage_weight_kg / g) * ((1/2) * r_fuselage**2)
fuselage_Ixx_correct = (fuselage_weight_kg / g) * ((1/2) * r_fuselage**2)

print(f"   Ixx incorrecto (con factor 0.85): {fuselage_Ixx_wrong:.2f} kg⋅m²")
print(f"   Ixx correcto (sin factor): {fuselage_Ixx_correct:.2f} kg⋅m²")
print(f"   Error introducido: {fuselage_Ixx_wrong - fuselage_Ixx_correct:.2f} kg⋅m²")

# ==============================================================================
# PROBLEMA 5: FACTOR LATERAL EN SIDE-BY-SIDE
# ==============================================================================

print("\n" + "=" * 80)
print("PROBLEMA 5: FACTOR LATERAL APLICADO A Ixx (SIDE-BY-SIDE)")
print("=" * 80)

print("\n❌ ERROR EN SIDE-BY-SIDE:")
print("   lateral_distribution_factor = 1.15 aplicado a Ixx del fuselaje")
print("   Justificación: 'distribución lateral de masa (cockpit separado)'")
print()
print("   PROBLEMA: Ixx es respecto eje X (no es afectado por Y)")
print("   La separación lateral (Y = ±750 mm) afecta Izz, no Ixx")
print("   Ixx solo afecta rotación respecto eje X (roll/alabeo)")
print()

print("✓ CORRECCIÓN:")
print("   Ixx sigue siendo: Ixx = (1/2) × m × r²")
print("   El factor 1.15 debería aplicarse a Izz, no a Ixx")
print()
print("   Izz (con factor lateral) = (1/2) × m × r² × 1.15 + m × d_lateral²")
print("   donde d_lateral ≈ 0.75 m (mitad de separación)")
print()

fuselage_Ixx_sbs = (fuselage_weight_kg / g) * ((1/2) * r_fuselage**2)
# Izz sí debe incluir efecto lateral
d_lateral = 0.75
fuselage_Izz_sbs_correct = (fuselage_weight_kg / g) * ((1/2) * r_fuselage**2 + d_lateral**2)

print(f"   Ixx correcto (sin factor): {fuselage_Ixx_sbs:.2f} kg⋅m²")
print(f"   Izz correcto (con efecto lateral): {fuselage_Izz_sbs_correct:.2f} kg⋅m²")

# ==============================================================================
# RESUMEN DE CORRECCIONES
# ==============================================================================

print("\n" + "=" * 80)
print("TABLA COMPARATIVA: ANTES vs DESPUÉS")
print("=" * 80)

data_comparison = {
    'Parámetro': [
        'Wing Ixx',
        'Wing Iyy', 
        'Wing Izz',
        'Fuselage Ixx (Tandem)',
        'Fuselage Izz (Side-by-Side)'
    ],
    'Incorrecto': [
        f'{Ixx_wrong:.2f}',
        f'{Iyy_wrong:.2f}',
        f'{Izz_wrong:.2f}',
        f'{fuselage_Ixx_wrong:.2f}',
        'N/A'
    ],
    'Correcto': [
        f'{Ixx_correct:.2f}',
        f'{Iyy_correct:.2f}',
        f'{Izz_correct:.2f}',
        f'{fuselage_Ixx_correct:.2f}',
        f'{fuselage_Izz_sbs_correct:.2f}'
    ],
    'Error %': [
        f'{(Ixx_wrong/Ixx_correct - 1)*100:.1f}%',
        f'{(Iyy_wrong/Iyy_correct - 1)*100:.1f}%',
        f'{(Izz_wrong/Izz_correct - 1)*100:.1f}%',
        f'{(fuselage_Ixx_wrong/fuselage_Ixx_correct - 1)*100:.1f}%',
        f'-'
    ]
}

print(f"\n{'Parámetro':<30} {'Incorrecto':<15} {'Correcto':<15} {'Error %':<10}")
print("-" * 70)
for i, param in enumerate(data_comparison['Parámetro']):
    print(f"{param:<30} {data_comparison['Incorrecto'][i]:<15} {data_comparison['Correcto'][i]:<15} {data_comparison['Error %'][i]:<10}")

# ==============================================================================
# RECOMENDACIONES FINALES
# ==============================================================================

print("\n" + "=" * 80)
print("RECOMENDACIONES DE CORRECCIÓN")
print("=" * 80)

recommendations = """
1. IMMEDIATE ACTIONS:
   ✓ Agregar "# -*- coding: utf-8 -*-" al inicio de scripts
   ✓ Reemplazar caracteres griegos por ASCII en docstrings

2. FÓRMULAS A CORREGIR:

   WING (Ala):
   ────────────
   a) Ixx (Roll - Alabeo):
      ANTES: Ixx = (1/12) × m × (b² + 3×t²)
      DESPUÉS: Ixx = (1/12) × m × b² × (2/3) × (1+λ+λ²)/(1+λ)
   
   b) Iyy (Pitch - Cabeceo):
      ANTES: Iyy = (1/12) × m × c_MAC²
      DESPUÉS: Iyy = (1/12) × m × b²
   
   c) Izz (Yaw - Guiñada):
      ANTES: Izz = Ixx + Iyy
      DESPUÉS: Izz = (1/12) × m × (b² + c_MAC²)

   FUSELAGE (Fuselaje):
   ──────────────────
   d) Ixx (Roll - Alabeo):
      TANDEM: Ixx = (1/2) × m × r²  (remove 0.85 factor)
      SIDE-BY-SIDE: Ixx = (1/2) × m × r²  (same, remove 1.15 factor)
   
   e) Izz (Yaw - Guiñada):
      TANDEM: Izz = (1/2) × m × r² + (1/12) × m × L²
      SIDE-BY-SIDE: Izz = (1/2) × m × r² + (1/12) × m × L² + m × d_lateral²
                         = (1/2) × m × r² + (1/12) × m × L² + m × 0.75²

3. VALIDACIÓN:
   ✓ Comparar contra Roskam "Airplane Design: Part 3" (MOI tables)
   ✓ Verificar con datos de aeronaves similares (Cessna 172, Piper Cherokee)
   ✓ Hacer análisis de sensibilidad (±10% en parámetros)

4. DOCUMENTACIÓN:
   ✓ Citar fuentes de fórmulas (Raymer, Roskam, etc.)
   ✓ Agregar referencias a ecuaciones en la literatura
   ✓ Documentar asunciones claramente

5. TESTING:
   ✓ Crear script de validación cruzada (tandem vs side-by-side)
   ✓ Comparar resultados totales vs suma de componentes
   ✓ Verificar dimensionalidad de todas las fórmulas
"""

print(recommendations)

print("\n" + "=" * 80)
print("FIN DEL ANÁLISIS DE CORRECCIONES")
print("=" * 80)
