import pandas as pd
import numpy as np

# Configuración inicial
np.random.seed(42)  # Para reproducibilidad
num_apartamentos = 200
meses_historico = 36
meses_optimizado = 12

# Perfil de estacionalidad mensual (1 = Enero, 12 = Diciembre)
# Valores entre 0 (verano) y 1 (pleno invierno)
estacionalidad_base = np.array([1.0, 0.9, 0.7, 0.4, 0.1, 0.0, 0.0, 0.0, 0.1, 0.4, 0.8, 1.0])
consumo_promedio_invierno = 250

# Definimos invierno como los meses con estacionalidad alta (Ene, Feb, Mar, Nov, Dic)
es_invierno = estacionalidad_base >= 0.7

def generar_datos(num_meses, offset_mes, reduccion_base, prob_anomalia):
    datos = []
    
    for apt_id in range(1, num_apartamentos + 1):
        fila = {'ID_Apto': f'Apto_{apt_id:03d}'}
        
        for m in range(1, num_meses + 1):
            mes_absoluto = m + offset_mes
            mes_del_anio = (mes_absoluto - 1) % 12
            
            # Consumo base considerando estacionalidad y algo de ruido aleatorio (+/- 10%)
            factor_est = estacionalidad_base[mes_del_anio]
            consumo_base = consumo_promedio_invierno * factor_est * np.random.uniform(0.9, 1.1)
            
            # Reducción por eficiencia (tarjetas)
            consumo_base *= (1 - reduccion_base)
            
            # Aplicar anomalía de derroche
            if es_invierno[mes_del_anio] and np.random.rand() < prob_anomalia:
                # Pico entre 80% y 120% extra sobre el consumo promedio de invierno
                pico = consumo_promedio_invierno * np.random.uniform(0.8, 1.2)
                consumo_final = consumo_base + pico
            else:
                consumo_final = consumo_base
            
            # Limpiar datos: no puede haber negativos
            consumo_final = max(0, round(consumo_final, 2))
            
            fila[f'Mes_{mes_absoluto}'] = consumo_final
            
        datos.append(fila)
        
    return pd.DataFrame(datos)

# 1. Generar Histórico (36 meses)
# Reducción 0% y 30% de probabilidad de anomalía en meses de invierno
df_historico = generar_datos(
    num_meses=meses_historico, 
    offset_mes=0, 
    reduccion_base=0.0, 
    prob_anomalia=0.30
)

# 2. Generar Optimizado (12 meses posteriores)
# Reducción 0% (el ahorro viene del corte de anomalías) y 2.5% de probabilidad de anomalía residual
df_optimizado = generar_datos(
    num_meses=meses_optimizado, 
    offset_mes=meses_historico, 
    reduccion_base=0.0, 
    prob_anomalia=0.025
)

import os

# Obtener ruta absoluta del directorio del proyecto
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, 'data')
os.makedirs(data_dir, exist_ok=True)

# Exportar a CSV
path_historico = os.path.join(data_dir, 'consumo_historico.csv')
path_optimizado = os.path.join(data_dir, 'consumo_optimizado.csv')

df_historico.to_csv(path_historico, index=False)
df_optimizado.to_csv(path_optimizado, index=False)

print("Generación completada con éxito.")
print(f"-> 'data/consumo_historico.csv' ({df_historico.shape[0]} filas, {df_historico.shape[1]} columnas)")
print(f"-> 'data/consumo_optimizado.csv' ({df_optimizado.shape[0]} filas, {df_optimizado.shape[1]} columnas)")
