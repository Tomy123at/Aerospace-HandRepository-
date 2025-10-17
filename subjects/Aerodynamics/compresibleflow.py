import Tabla_ISA_module as isa

def mach_number(Vinf, altitude):
    if 'ft' in altitude:
        valor = float(altitude.replace('ft', '').strip())
        altitude = valor * 0.3048  # Conversión de pies a metros
        
    elif 'm' in altitude:
        altitude = float(altitude.replace('m', '').strip())
    else:
        print("Formato incorrecto. Usa 'm' para metros o 'ft' para pies.")
        return None, None  

    # Convertir Vinf a m/s si es necesario
    if 'm/s' in Vinf:
        Vinf = float(Vinf.replace('m/s', '').strip())  
   
    elif 'ft/s' in Vinf:
        valor = float(Vinf.replace('ft/s', '').strip())
        Vinf = valor * 0.3048  # Conversión de ft/s a m/s

    elif 'knots' in Vinf:
        valor = float(Vinf.replace('knots', '').strip())
        Vinf = valor * 0.514444  # Conversión de nudos a m/s

    elif 'mph' in Vinf:
        valor = float(Vinf.replace('mph', '').strip())
        Vinf = valor * 0.44704  # Conversión de mph a m/s

    else:
        print("Formato incorrecto. Usa 'm/s', 'ft/s', 'knots' o 'mph'.")
        return None, None
    
    T, p, rhoinf, avel = isa.Temp_Presion_Densidad(altitude)
    
    Mach_number = Vinf/avel

    return Mach_number, avel

Vinf = input("Ingrese la velocidad aerodinámica a la que vuela la aeronave (m/s, ft/s, knots, mph): ")
altitude = input("Ingrese la altitud a la que vuela la aeronave (m, ft): ")

Mach, avel = mach_number(Vinf,altitude)
print("M: ",round(Mach,3),"| a: ",round(avel,3),"m/s")