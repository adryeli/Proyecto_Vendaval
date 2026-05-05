import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mplcyberpunk
import os
from matplotlib.widgets import RadioButtons, Button, CheckButtons
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# 1. IMPORTAMOS NUESTRO ADAPTADOR ESTRELLA
from backend.stats.data_adapter import get_combined_data, get_available_cities


def run_dashboard():
    print("""
    \033[96m
    ██╗   ██╗███████╗███╗   ██╗██████╗  █████╗ ██╗   ██╗ █████╗ ██╗     
    ██║   ██║██╔════╝████╗  ██║██╔══██╗██╔══██╗██║   ██║██╔══██╗██║     
    ██║   ██║█████╗  ██╔██╗ ██║██║  ██║███████║██║   ██║███████║██║     
    ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║  ██║██╔══██║╚██╗ ██╔╝██╔══██║██║     
     ╚████╔╝ ███████╗██║ ╚████║██████╔╝██║  ██║ ╚████╔╝ ██║  ██║███████╗
      ╚═══╝  ╚══════╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝
    [ BARLOVENTO DATA - SISTEMA DE MONITOREO CLIMÁTICO ]
    \033[0m
    """)

    # 2. CARGAMOS LOS DATOS USANDO EL ADAPTADOR
    df = get_combined_data()
    
    if df.empty: 
        print("\n\033[91m[!] No hay datos disponibles para mostrar en el Dashboard.\033[0m")
        return

    # Filtro de últimos 12 meses
    fecha_corte = pd.Timestamp.now() - pd.DateOffset(months=12)
    df = df[df['timestamp'] >= fecha_corte]

    if df.empty:
        print(f"\n\033[93m[!] No hay registros en los últimos 12 meses (desde {fecha_corte.strftime('%Y-%m-%d')}).\033[0m")
        return

    # 3. OBTENEMOS LAS CIUDADES
    ciudades_todas = get_available_cities()
    
    pag_actual = [0]
    items_por_pagina = 10
    ciudad_activa = [ciudades_todas[0]]

    # --- 2. CONFIGURACIÓN DEL LIENZO ---
    plt.style.use("cyberpunk")
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='#21262d')
    
    plt.subplots_adjust(left=0.12, right=0.75, top=0.88, bottom=0.20)

    VAR_MAP = {
        'Temperatura': {'col': 'temperature_c', 'color': '#08F7FE'},
        'Humedad':     {'col': 'humidity_pct',  'color': '#FE53BB'},
        'Viento':      {'col': 'wind_kph',      'color': '#F5D300'},
        'Lluvia':      {'col': 'rain_mm',       'color': '#00FF41'}
    }
    estado_vars = {k: True for k in VAR_MAP.keys()}

    def dibujar_escena(seleccion_ciudad):
        nonlocal range_start, range_end
        ax.clear()
        ax.set_facecolor('#1c1f23') 
        ax.grid(color='#444d56', linestyle=':', alpha=0.4)
        
        # Usamos directamente las fechas límite definidas por los botones
        fecha_inicio = pd.Timestamp(range_start)
        fecha_fin    = pd.Timestamp(range_end)
        df_filtrado = df[(df['timestamp'] >= fecha_inicio) & (df['timestamp'] <= fecha_fin)]
        
        # Datos de la ciudad seleccionada
        data_city = df_filtrado[df_filtrado['city'] == seleccion_ciudad]

        UNIDADES = {'Temperatura': '°C', 'Humedad': '%', 'Viento': 'km/h', 'Lluvia': 'mm'}
        objetos_leyenda = []
        nombres_leyenda = []

        for v_name, visible in estado_vars.items():
            if visible:
                config = VAR_MAP[v_name]
                unidad = UNIDADES.get(v_name, "")
                
                if not data_city.empty:
                    # Línea conectora
                    linea, = ax.plot(data_city['timestamp'], data_city[config['col']], 
                                    color=config['color'], 
                                    linestyle='-', linewidth=1.5, alpha=0.7)

                    # Puntos resaltados
                    ax.plot(data_city['timestamp'], data_city[config['col']], 
                            color=config['color'], 
                            marker='o', markersize=8, linestyle='None',
                            markeredgecolor='white', markeredgewidth=0.5,
                            alpha=1.0)

                    objetos_leyenda.append(linea)
                    nombres_leyenda.append(f"{v_name} ({unidad})")

        # Forzar los límites del eje X para que coincidan con el rango seleccionado
        ax.set_xlim([fecha_inicio, fecha_fin])

        try: mplcyberpunk.make_lines_glow(ax)
        except: pass

        if objetos_leyenda:
            leg = ax.legend(objetos_leyenda, nombres_leyenda,
                           loc='upper left', bbox_to_anchor=(0.01, 0.99),
                           frameon=True, facecolor='#0d1117', edgecolor='#444d56', fontsize=8)
            plt.setp(leg.get_texts(), color='#e6edf3')

        # Título con rango de fechas
        f_ini_str = fecha_inicio.strftime('%Y-%m-%d')
        f_fin_str = fecha_fin.strftime('%Y-%m-%d')
        
        # Logo
        try:
            logo_path = "cli/logo.png" 
            if os.path.exists(logo_path):
                img = mpimg.imread(logo_path)
                imagebox = OffsetImage(img, zoom=0.025) 
                ab = AnnotationBbox(imagebox, (0.85, 0.98), 
                                    xycoords='figure fraction',
                                    frameon=False, 
                                    box_alignment=(0, 1)) 
                fig.add_artist(ab)
        except:
            pass

        titulo = f"SISTEMA VENDAVAL: {seleccion_ciudad.upper()}\n[ {f_ini_str}  --->  {f_fin_str} ]"
        ax.set_title(titulo, color='white', pad=25, fontweight='bold', fontsize=13)
        plt.setp(ax.get_xticklabels(), rotation=30, ha='right', color='#8b949e')
        fig.canvas.draw_idle()

    # --- 3. SELECTOR DE CIUDADES ---
    ax_menu = plt.axes([0.78, 0.25, 0.18, 0.65], facecolor='#21262d')
    selector_ref = [None]

    def actualizar_menu(inicio, fin):
        ax_menu.clear()
        opciones_pagina = ciudades_todas[inicio:fin]
        
        idx_visual = 0
        encontrada = False
        if ciudad_activa[0] in opciones_pagina:
            idx_visual = opciones_pagina.index(ciudad_activa[0])
            encontrada = True

        selector_ref[0] = RadioButtons(ax_menu, opciones_pagina, 
                                      active=idx_visual if encontrada else 0, 
                                      activecolor='#08F7FE')
        
        for i, lbl in enumerate(selector_ref[0].labels):
            if encontrada and i == idx_visual:
                lbl.set_color('#08F7FE') 
                lbl.set_fontweight('bold')
                lbl.set_text(f"  {opciones_pagina[i].upper()}")
            else:
                lbl.set_color('#444d56') 
                lbl.set_fontweight('normal')
                lbl.set_text(f"  {opciones_pagina[i]}")

        def al_clicar(label):
            seleccionada = label.strip()
            for c in ciudades_todas:
                if c.strip().upper() == seleccionada.upper():
                    ciudad_activa[0] = c
                    break
            
            dibujar_escena(ciudad_activa[0])
            actualizar_menu(inicio, fin) 
            
        selector_ref[0].on_clicked(al_clicar)

    # --- 4. BOTONES DE NAVEGACIÓN ---
    ax_prev = plt.axes([0.78, 0.18, 0.08, 0.05])
    ax_next = plt.axes([0.88, 0.18, 0.08, 0.05])
    btn_prev = Button(ax_prev, '<<', color='#30363d', hovercolor='#484f58')
    btn_next = Button(ax_next, '>>', color='#30363d', hovercolor='#484f58')
    btn_prev.label.set_color('white'); btn_next.label.set_color('white')

    def cambiar_pag(event):
        direccion = 1 if event.inaxes == ax_next else -1
        nueva_pos = (pag_actual[0] + direccion) * items_por_pagina
        if 0 <= nueva_pos < len(ciudades_todas):
            pag_actual[0] += direccion
            actualizar_menu(nueva_pos, nueva_pos + items_por_pagina)
            plt.draw()

    btn_prev.on_clicked(cambiar_pag)
    btn_next.on_clicked(cambiar_pag)

    # --- 5. CHECKBOXES (Variables) ---
    ax_check = plt.axes([0, 0, 0.25, 0.10], facecolor='#21262d')
    check = CheckButtons(ax_check, list(VAR_MAP.keys()), [True]*4)
    
    for label in check.labels: 
        label.set_color('white')
        label.set_fontsize(11)
        label.set_fontweight('bold')

    def func_check(label):
        estado_vars[label] = not estado_vars[label]
        dibujar_escena(ciudad_activa[0])
    
    check.on_clicked(func_check)

    # --- 6. SELECTOR DE RANGO (BOTONERA HORIZONTAL) ---
    opciones_rango = ['Día', 'Semana', 'Mes', 'Año']
    rango_btns = []
    seleccion_rango = ["Año"]  # texto del botón activo

    def actualizar_estilo_rango():
        """Ilumina el botón seleccionado y apaga los demás"""
        for btn in rango_btns:
            if btn.label.get_text() == seleccion_rango[0]:
                btn.color = '#08F7FE'      # Cyan (Activo)
                btn.label.set_color('black')
            else:
                btn.color = '#21262d'      # Oscuro (Inactivo)
                btn.label.set_color('white')
        fig.canvas.draw_idle()
    
    # Inicialización coherente con "Año"
    ahora_inicial = pd.Timestamp.now().normalize()
    range_start = ahora_inicial.replace(month=1, day=1)
    range_end   = ahora_inicial.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
    range_end   = min(range_end, pd.Timestamp.now())

    # Creamos los 4 botones de rango temporal
    for i, nombre in enumerate(opciones_rango):
        ax_b = plt.axes([0.30 + (i * 0.11), 0.05, 0.10, 0.045])
        btn = Button(ax_b, nombre, color='#21262d', hovercolor='#30363d')
        btn.label.set_fontweight('bold')
        btn.label.set_fontsize(9)
        
        def crear_manejador(n=nombre):
            def manejar_clic(event):
                nonlocal range_start, range_end
                seleccion_rango[0] = n
                ahora = pd.Timestamp.now().normalize()  # fecha sin hora (00:00:00 de hoy)

                if n == 'Día':
                    # Solo hoy: desde medianoche hasta fin del día (horas futuras permitidas)
                    range_start = ahora
                    range_end   = ahora.replace(hour=23, minute=59, second=59, microsecond=999999)
                elif n == 'Semana':
                    range_start = ahora - pd.Timedelta(weeks=1)
                    range_end   = ahora
                elif n == 'Mes':
                    range_start = ahora.replace(day=1)
                    range_end   = (range_start + pd.DateOffset(months=1)) - pd.Timedelta(microseconds=1)
                else:  # Año
                    range_start = ahora.replace(month=1, day=1)
                    range_end   = ahora.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

                # Evitar fechas futuras en todos los casos excepto en 'Día'
                if n != 'Día':
                    range_end = min(range_end, pd.Timestamp.now())

                dibujar_escena(ciudad_activa[0])
                actualizar_estilo_rango()
                
            return manejar_clic

        btn.on_clicked(crear_manejador(nombre))
        rango_btns.append(btn)

    # Estilo inicial (sin botón activo, se iluminará el primer clic)
    actualizar_estilo_rango()

    # Dibujar la escena inicial
    actualizar_menu(0, items_por_pagina)
    dibujar_escena(ciudad_activa[0])
    plt.show()

if __name__ == "__main__":
    run_dashboard()