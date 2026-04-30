import matplotlib.pyplot as plt
import pandas as pd
import mplcyberpunk
import json
import os
from matplotlib.widgets import RadioButtons, Button, CheckButtons

def load_all_data():
    all_data = []
    for f_name in ["weather_cache.json", "manual_records.json"]:
        path = os.path.join("data", f_name)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                all_data.extend(json.load(f))
    df = pd.DataFrame(all_data)
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)
        df = df.sort_values('timestamp')
    return df

def run_dashboard():
    df = load_all_data()
    if df.empty: return

    # --- 1. ORDEN ALFABÉTICO CORRECTO (Ávila primero) ---
    # Ordenamos ignorando tildes para que la 'Á' no se vaya al final
    ciudades_base = sorted(df['city'].unique().tolist(), 
                          key=lambda x: x.replace('Á','A').replace('É','E').replace('Í','I').replace('Ó','O').replace('Ú','U'))
    ciudades_todas = [" [ MEDIA ESPAÑA ] "] + ciudades_base
    
    pag_actual = [0]
    items_por_pagina = 10
    ciudad_activa = [ciudades_todas[0]] 

    # --- 2. CONFIGURACIÓN DEL LIENZO ---
    plt.style.use("cyberpunk")
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='#21262d')
    # --- AJUSTE DE MÁRGENES PROFESIONAL ---
    # left: espacio para los checkboxes (aumentado)
    # right: espacio para el selector de ciudades
    # bottom: espacio para que la leyenda inferior no se corte
    # top: espacio para el título cyberpunk
    plt.subplots_adjust(left=0.12, right=0.75, top=0.88, bottom=0.20)

    VAR_MAP = {
        'Temperatura': {'col': 'temperature_c', 'color': '#08F7FE'},
        'Humedad':     {'col': 'humidity_pct',  'color': '#FE53BB'},
        'Viento':      {'col': 'wind_kph',      'color': '#F5D300'},
        'Lluvia':      {'col': 'rain_mm',       'color': '#00FF41'}
    }
    estado_vars = {k: True for k in VAR_MAP.keys()}

    def dibujar_escena(seleccion_ciudad):
        ax.clear()
        ax.set_facecolor('#1c1f23') 
        ax.grid(color='#444d56', linestyle=':', alpha=0.4)
        
        df_media_nac = df.groupby('timestamp').mean(numeric_only=True).reset_index().tail(15)
        data_city = df[df['city'] == seleccion_ciudad].tail(15)

        UNIDADES = {'Temperatura': '°C', 'Humedad': '%', 'Viento': 'km/h', 'Lluvia': 'mm'}

        # Lista para guardar solo los "dibujos" que queremos en la leyenda
        objetos_leyenda = []
        nombres_leyenda = []

        for v_name, visible in estado_vars.items():
            if visible:
                config = VAR_MAP[v_name]
                unidad = UNIDADES.get(v_name, "")
                
                # 1. Media Nacional (SIN label para que no ensucie)
                ax.plot(df_media_nac['timestamp'], df_media_nac[config['col']], 
                        color=config['color'], linestyle='--', linewidth=1, alpha=0.2)
                
                # 2. Ciudad o Selección Actual
                # Usamos una variable temporal 'linea' para capturar el objeto
                linea, = ax.plot([], []) # Creamos base para el color
                
                if not data_city.empty and seleccion_ciudad != " [ MEDIA ESPAÑA ] ":
                    linea, = ax.plot(data_city['timestamp'], data_city[config['col']], 
                                    color=config['color'], linewidth=3, marker='o')
                else:
                    # Si es Media España, usamos la línea punteada como referencia sólida
                    linea, = ax.plot(df_media_nac['timestamp'], df_media_nac[config['col']], 
                                    color=config['color'], linewidth=2)

                # GUARDAMOS SOLO ESTA LÍNEA PARA LA LEYENDA
                objetos_leyenda.append(linea)
                nombres_leyenda.append(f"{v_name} ({unidad})")

        try: mplcyberpunk.make_lines_glow(ax)
        except: pass

        # --- LEYENDA PURA Y PERSISTENTE ---
        if objetos_leyenda:
            leg = ax.legend(objetos_leyenda, nombres_leyenda,
                           loc='upper left', 
                           bbox_to_anchor=(0.01, 0.99),
                           frameon=True, 
                           facecolor='#0d1117', 
                           edgecolor='#444d56', 
                           fontsize=8)
            plt.setp(leg.get_texts(), color='#e6edf3')

        ax.set_title(f"MONITORIZACIÓN: {seleccion_ciudad.upper()}", color='white', pad=25, fontweight='bold')
        plt.setp(ax.get_xticklabels(), rotation=30, ha='right', color='#8b949e')
        fig.canvas.draw_idle()

    # --- 3. SELECTOR DE CIUDADES (SISTEMA DE SEGURIDAD) ---
    ax_menu = plt.axes([0.78, 0.25, 0.18, 0.65], facecolor='#21262d')
    selector_ref = [None]

    def actualizar_menu(inicio, fin):
        ax_menu.clear()
        opciones_pagina = ciudades_todas[inicio:fin]
        
        # 1. Buscamos si la ciudad activa está en esta página
        idx_visual = 0
        encontrada = False
        if ciudad_activa[0] in opciones_pagina:
            idx_visual = opciones_pagina.index(ciudad_activa[0])
            encontrada = True

        # 2. Creamos el selector. 
        # Si no se encuentra en la página, active=0 pondrá el punto arriba, 
        # pero el estilo del texto dirá la verdad.
        selector_ref[0] = RadioButtons(ax_menu, opciones_pagina, 
                                      active=idx_visual if encontrada else 0, 
                                      activecolor='#08F7FE')
        
        # 3. Estilo de etiquetas 100% compatible (Sin caracteres especiales)
        for i, lbl in enumerate(selector_ref[0].labels):
            if encontrada and i == idx_visual:
                # LA CIUDAD ESTÁ AQUÍ: Resaltado máximo
                lbl.set_color('#08F7FE') # Azul Ciano Cyberpunk
                lbl.set_fontweight('bold')
                lbl.set_text(f"  {opciones_pagina[i].upper()}") # Texto en Mayúsculas para destacar
            else:
                # NO ES LA CIUDAD O NO ESTÁ EN ESTA PÁGINA: Estilo apagado
                lbl.set_color('#444d56') # Gris oscuro
                lbl.set_fontweight('normal')
                lbl.set_text(f"  {opciones_pagina[i]}")

        def al_clicar(label):
            # Limpiamos el texto (por si acaso el upper() nos diera problemas al buscar en el DF)
            # Buscamos el nombre original comparando en minúsculas
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

    # --- 5. CHECKBOXES (Variables) MÁS GRANDES Y A LA IZQUIERDA ---
    # [x_inicio, y_inicio, ancho, alto] -> Ajustado para ser más alto y ancho
    # --- REPOSICIONAMIENTO DE CHECKBOXES ---
    # [distancia_izquierda, distancia_abajo, ancho, alto]
    ax_check = plt.axes([0.08, 0.05, 0.25, 0.10], facecolor='#21262d')
    check = CheckButtons(ax_check, list(VAR_MAP.keys()), [True]*4)
    
    # Estilo de las etiquetas de los Checkboxes
    for label in check.labels: 
        label.set_color('white')
        label.set_fontsize(11) # Más grandes como pediste
        label.set_fontweight('bold')

    def func_check(label):
        estado_vars[label] = not estado_vars[label]
        dibujar_escena(ciudad_activa[0])
    
    check.on_clicked(func_check)

    actualizar_menu(0, items_por_pagina)
    dibujar_escena(ciudad_activa[0])
    plt.show()

if __name__ == "__main__":
    run_dashboard()