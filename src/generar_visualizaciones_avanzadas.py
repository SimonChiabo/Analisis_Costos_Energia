import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Configuración de rutas
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, 'data')
assets_dir = os.path.join(base_dir, 'assets')
os.makedirs(assets_dir, exist_ok=True)

# Paleta corporativa
color_base = '#1A3636'  # Gris pizarra
color_opt = '#4A7C59'   # Verde salvia
text_color = '#4f4f4f'

def style_plot(ax):
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors=text_color, length=0)
    ax.xaxis.label.set_color(text_color)
    ax.yaxis.label.set_color(text_color)
    ax.grid(axis='y', linestyle='--', alpha=0.2, color=text_color)

# Cargar datos
df_historico = pd.read_csv(os.path.join(data_dir, 'consumo_historico.csv'))
df_optimizado = pd.read_csv(os.path.join(data_dir, 'consumo_optimizado.csv'))

cols_historico = [col for col in df_historico.columns if col.startswith('Mes_')]
cols_optimizado = [col for col in df_optimizado.columns if col.startswith('Mes_')]

# ==========================================
# 1. Gráfico de Cascada (Waterfall - Negocio)
# ==========================================
consumo_hist = df_historico[cols_historico].sum().sum() / 3
consumo_opt = df_optimizado[cols_optimizado].sum().sum()
ahorro = consumo_hist - consumo_opt

fig1, ax1 = plt.subplots(figsize=(8, 5))
fig1.patch.set_alpha(0.0)
ax1.patch.set_alpha(0.0)

labels = ['Histórico', 'Derroche Eliminado', 'Optimizado']
valores = [consumo_hist, -ahorro, consumo_opt]
starts = [0, consumo_opt, 0]
colores = [color_base, color_opt, color_base]

bars = ax1.bar(labels, [abs(v) for v in valores], bottom=starts, color=colores, width=0.5, alpha=0.9)

for i, bar in enumerate(bars):
    if i == 1:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_y() + bar.get_height()/2, 
                 f'-{int(ahorro/1000)}k L', ha='center', va='center', color='white', fontweight='bold')
    else:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_y() + bar.get_height() + 5000, 
                 f'{int(valores[i]/1000)}k L', ha='center', va='bottom', color=text_color, fontweight='bold')

ax1.set_ylabel('Consumo Total Anual (Litros)')
style_plot(ax1)
plt.tight_layout()
plt.savefig(os.path.join(assets_dir, "01_grafico_cascada.png"), transparent=True, dpi=300)
plt.close(fig1)

# ==========================================
# 2. Box Plot (Varianza - Analítica)
# ==========================================
meses_invierno_hist = [col for col in cols_historico if int(col.split('_')[1]) % 12 in [1, 2, 3, 11, 0]]
meses_invierno_opt = [col for col in cols_optimizado if int(col.split('_')[1]) % 12 in [1, 2, 3, 11, 0]]

datos_hist_invierno = df_historico[meses_invierno_hist].values.flatten()
datos_opt_invierno = df_optimizado[meses_invierno_opt].values.flatten()

fig2, ax2 = plt.subplots(figsize=(8, 5))
fig2.patch.set_alpha(0.0)
ax2.patch.set_alpha(0.0)

bplot = ax2.boxplot([datos_hist_invierno, datos_opt_invierno], patch_artist=True,
                    tick_labels=['Invierno\n(Histórico)', 'Invierno\n(Optimizado)'],
                    widths=0.4, medianprops=dict(color='white', linewidth=2))

for patch, color in zip(bplot['boxes'], [color_base, color_opt]):
    patch.set_facecolor(color)
    patch.set_alpha(0.8)
for element in ['whiskers', 'caps']:
    for line in bplot[element]:
        line.set_color(text_color)
for flier in bplot['fliers']:
    flier.set(marker='o', color=text_color, alpha=0.2, markersize=4)

ax2.set_ylabel('Consumo Mensual por Apto. (Litros)')
style_plot(ax2)
plt.tight_layout()
plt.savefig(os.path.join(assets_dir, "02_grafico_boxplot.png"), transparent=True, dpi=300)
plt.close(fig2)

# ==========================================
# 3. Densidad (Distribución - Analítica)
# ==========================================
fig3, ax3 = plt.subplots(figsize=(8, 5))
fig3.patch.set_alpha(0.0)
ax3.patch.set_alpha(0.0)

# Usamos ax3.hist con density=True para evitar depender de scipy
ax3.hist(datos_hist_invierno, bins=30, density=True, color=color_base, alpha=0.3, label='Histórico (Cola de derroche)')
ax3.hist(datos_opt_invierno, bins=30, density=True, color=color_opt, alpha=0.6, label='Optimizado (Controlado)')

ax3.set_xlim(0, max(datos_hist_invierno) * 1.1)
ax3.set_ylabel('Densidad / Frecuencia')
ax3.set_xlabel('Consumo Mensual por Apto. (Litros)')
ax3.legend(frameon=False, labelcolor=text_color)
style_plot(ax3)
# Ocultar y-ticks por ser densidad relativa
ax3.set_yticks([])
plt.tight_layout()
plt.savefig(os.path.join(assets_dir, "03_grafico_densidad.png"), transparent=True, dpi=300)
plt.close(fig3)

# ==========================================
# 4. Barras Apiladas (Macro - Negocio)
# ==========================================
fig4, ax4 = plt.subplots(figsize=(8, 5))
fig4.patch.set_alpha(0.0)
ax4.patch.set_alpha(0.0)

etiquetas = ['Año 1', 'Año 2', 'Año 3', 'Año 4\n(Optimizado)']
# Promedio base (estimado sin derroche) es similar al optimizado
base_anual = consumo_opt 
derroche_hist = consumo_hist - base_anual

bases = [base_anual, base_anual, base_anual, base_anual]
derroches = [derroche_hist, derroche_hist, derroche_hist, 0]

ax4.bar(etiquetas, bases, color=color_base, width=0.5, alpha=0.8, label='Consumo Estructural')
ax4.bar(etiquetas, derroches, bottom=bases, color=color_opt, width=0.5, alpha=0.9, label='Derroche (Potencial Ahorro)')

ax4.set_ylabel('Consumo Total Anual (Litros)')
ax4.legend(frameon=False, labelcolor=text_color, loc='upper right')
style_plot(ax4)

plt.tight_layout()
plt.savefig(os.path.join(assets_dir, "04_grafico_barras_apiladas.png"), transparent=True, dpi=300)
plt.close(fig4)

print("Visualizaciones avanzadas generadas en la carpeta assets.")
