import pandas as pd
import os

# Configuración de rutas
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, 'data')

# 1. Variables financieras fijas
precio_gasoil = 1.15  # € / litro
capex_por_apto = 60   # €
num_apartamentos = 200
capex_total = capex_por_apto * num_apartamentos

# 2. Cargar histórico como base
try:
    df_historico = pd.read_csv(os.path.join(data_dir, 'consumo_historico.csv'))
    cols_historico = [col for col in df_historico.columns if col.startswith('Mes_')]
    consumo_total_historico = df_historico[cols_historico].sum().sum()
    consumo_anual_historico = consumo_total_historico / 3
except FileNotFoundError:
    print("Error: No se encontró 'consumo_historico.csv'. Ejecuta primero 'generar_datos_consumo.py'.")
    exit(1)

# 3. Definir escenarios de sensibilidad
escenarios = [
    ("Conservador", 0.15),
    ("Base", 0.20),
    ("Optimista", 0.25)
]

# 4. Calcular e imprimir métricas
print("\n" + "=" * 65)
print(" " * 18 + "ANÁLISIS DE SENSIBILIDAD")
print("=" * 65)
print(f"{'Escenario':<15} | {'Ahorro anual (€)':<18} | {'ROI (%)':<10} | {'Payback (meses)':<15}")
print("-" * 65)

resultados = []
for nombre, ahorro_pct in escenarios:
    litros_ahorrados = consumo_anual_historico * ahorro_pct
    ahorro_opex = litros_ahorrados * precio_gasoil
    roi = ((ahorro_opex - capex_total) / capex_total) * 100
    payback = (capex_total / ahorro_opex) * 12
    
    # Formateo de salida
    ahorro_str = f"~ {ahorro_opex:,.0f} €"
    roi_str = f"{roi:.0f}%"
    payback_str = f"{payback:.1f} meses"
    
    print(f"{nombre:<15} | {ahorro_str:<18} | {roi_str:<10} | {payback_str:<15}")
    resultados.append([nombre, ahorro_str, roi_str, payback_str])

print("=" * 65 + "\n")
