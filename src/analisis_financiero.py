import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Variables financieras fijas (ajustables)
precio_gasoil = 1.15  # € / litro
capex_por_apto = 60   # €
num_apartamentos = 200
capex_total = capex_por_apto * num_apartamentos

import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, 'data')
assets_dir = os.path.join(base_dir, 'assets')
os.makedirs(assets_dir, exist_ok=True)

# 2. Cargar datos
df_historico = pd.read_csv(os.path.join(data_dir, 'consumo_historico.csv'))
df_optimizado = pd.read_csv(os.path.join(data_dir, 'consumo_optimizado.csv'))

# Filtrar solo las columnas numéricas de los meses
cols_historico = [col for col in df_historico.columns if col.startswith('Mes_')]
cols_optimizado = [col for col in df_optimizado.columns if col.startswith('Mes_')]

# 3. Procesamiento y Métricas de Consumo
# Consumo total de los 36 meses históricos (3 años)
consumo_total_historico = df_historico[cols_historico].sum().sum()
consumo_anual_historico = consumo_total_historico / 3

# Consumo total del año optimizado (Mes 37 al 48)
consumo_anual_optimizado = df_optimizado[cols_optimizado].sum().sum()

# Reducción porcentual exacta
reduccion_porcentual = ((consumo_anual_historico - consumo_anual_optimizado) / consumo_anual_historico) * 100

# 4. Modelo Financiero
# Ahorro operativo anual (OPEX)
ahorro_anual_opex = (consumo_anual_historico - consumo_anual_optimizado) * precio_gasoil

# Retorno de la Inversión (ROI) anualizado
roi_anualizado = ((ahorro_anual_opex - capex_total) / capex_total) * 100

# Periodo de Recuperación (Payback) expresado en meses
payback_meses = (capex_total / ahorro_anual_opex) * 12

# Imprimir en consola una tabla resumen limpia
print("\n" + "=" * 55)
print(" RESUMEN FINANCIERO Y MÉTRICAS DE IMPACTO ".center(55))
print("=" * 55)
print(f"Consumo Promedio Anual Histórico : {consumo_anual_historico:,.2f} L")
print(f"Consumo Anual Optimizado         : {consumo_anual_optimizado:,.2f} L")
print(f"Reducción de Consumo             : {reduccion_porcentual:.2f} %")
print("-" * 55)
print(f"CAPEX Total                      : {capex_total:,.2f} €")
print(f"Ahorro Anual OPEX                : {ahorro_anual_opex:,.2f} €")
print(f"ROI Anualizado                   : {roi_anualizado:.2f} %")
print(f"Periodo de Payback               : {payback_meses:.1f} meses")
print("=" * 55 + "\n")

# 5. Visualización
# Obtener el consumo promedio por apartamento para cada mes
promedio_mensual_historico = df_historico[cols_historico].mean()
promedio_mensual_optimizado = df_optimizado[cols_optimizado].mean()

# Unir todas las series
promedio_total = pd.concat([promedio_mensual_historico, promedio_mensual_optimizado])
meses = np.arange(1, 49)

# Configurar estilo general
plt.style.use('default') # 'seaborn' ha sido deprecado en versiones recientes de pandas/matplotlib, usamos el default limpio
plt.figure(figsize=(14, 7))

# Trazar la evolución del consumo
plt.plot(meses, promedio_total.values, marker='o', linestyle='-', color='#2c3e50', linewidth=2, markersize=5)

# Añadir línea vertical en el mes 36
plt.axvline(x=36, color='#e74c3c', linestyle='--', linewidth=2.5, label='Implementación de Tarjetas')

# Títulos y etiquetas
plt.title('Evolución del Consumo Promedio Mensual de Gasoil por Apartamento', fontsize=16, pad=20, fontweight='bold', color='#34495e')
plt.xlabel('Meses (1 a 48)', fontsize=12, fontweight='bold')
plt.ylabel('Consumo de Gasoil (Litros)', fontsize=12, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.5)

# Ajuste de los ticks del eje X
plt.xticks(np.arange(0, 49, 4))
plt.legend(loc='upper right', fontsize=11, framealpha=0.9)

# Añadir cuadro de texto con métricas clave (annotation)
texto_metricas = (
    f"Ahorro: ~{reduccion_porcentual:.0f}% | "
    f"CAPEX: {int(capex_total/1000)}k€ | "
    f"ROI: {roi_anualizado:.0f}% | "
    f"Payback: {payback_meses:.1f} meses"
)

# Colocar la anotación (calculando una altura conveniente)
y_max = plt.ylim()[1]
plt.text(1, y_max * 0.90, texto_metricas, fontsize=12, fontweight='bold', color='#27ae60',
         bbox=dict(facecolor='white', edgecolor='#bdc3c7', alpha=0.95, boxstyle='round,pad=0.7'))

plt.tight_layout()

# Guardar en alta resolución
nombre_grafico = os.path.join(assets_dir, 'analisis_financiero_consumo.png')
plt.savefig(nombre_grafico, dpi=300)
print(f"Gráfico de alta resolución guardado en '{nombre_grafico}'")
