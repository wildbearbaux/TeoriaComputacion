import tkinter as tk
from tkinter import messagebox
import math

class ControlUniversalDFA:
    """Motor DFA Definitivo: Rutas largas, exactas y con topologías complejas"""
    def __init__(self, config):
        self.marca = config['nombre']
        self.estados = config['Q']
        self.estado_inicial = config['q0']
        self.estados_aceptacion = config['F']
        
        self.alfabeto = [
            'btn_setup', 'btn_power', 'btn_menu', 'btn_source',
            'btn_1', 'btn_2', 'btn_3', 'btn_ok',
            'btn_vol_up', 'btn_vol_down', 'btn_ch_up', 'btn_ch_down',
            'btn_mute', 'btn_audio', 'btn_image', 'btn_exit'
        ]
        
        self.estado_actual = self.estado_inicial
        self.cinta_entrada = []
        
        # Iniciar todo hacia el Estado Pozo (qE)
        self.transiciones = {estado: {btn: 'qE' for btn in self.alfabeto} for estado in self.estados}
        if 'qE' not in self.transiciones:
            self.transiciones['qE'] = {btn: 'qE' for btn in self.alfabeto}

        # Aplicar transiciones formales (Rutas exactas, sin "basura")
        for (q_origen, simbolo, q_destino) in config['delta']:
            self.transiciones[q_origen][simbolo] = q_destino

        # Regla de hardware: EXIT siempre reinicia
        for estado in self.estados:
            self.transiciones[estado]['btn_exit'] = 'q0' 
        for btn in self.alfabeto:
            if btn != 'btn_exit':
                self.transiciones['qE'][btn] = 'qE' 

        # Los Estados de Aceptación hacen un ciclo libre con cualquier botón (uso normal)
        for qF in self.estados_aceptacion:
            for btn in self.alfabeto:
                if btn not in ['btn_exit', 'btn_setup']:
                    self.transiciones[qF][btn] = qF
            self.transiciones[qF]['btn_setup'] = 'qE'

    def procesar_simbolo(self, simbolo):
        est_anterior = self.estado_actual
        self.estado_actual = self.transiciones[est_anterior][simbolo]
        self.cinta_entrada.append(simbolo)
        
        log = f"δ({est_anterior}, {simbolo}) = {self.estado_actual}"
        if est_anterior == self.estado_actual and self.estado_actual not in ['q0', 'qE'] and self.estado_actual not in self.estados_aceptacion:
             log += " [¡Lazo Recursivo Ejecutado!]"
             
        return est_anterior, self.estado_actual, log

    def es_estado_aceptacion(self):
        return self.estado_actual in self.estados_aceptacion

    def reiniciar(self):
        self.estado_actual = self.estado_inicial
        self.cinta_entrada.clear()


class InterfazProyectoFinal:
    def __init__(self, root):
        self.root = root
        self.root.title("Teoría de la Computación - Proyecto Final DFA")
        self.root.geometry("1150x800")
        self.root.configure(bg="#1e1e2e")
        
        # =====================================================================
        # DICCIONARIO: TOPOLOGÍAS COMPLEJAS CON RUTAS ALARGADAS
        # =====================================================================
        self.configuraciones_tv = [
            {
                'nombre': "SAMSUNG",
                'color': '#89b4fa',
                'Q': ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'qE'],
                'q0': 'q0', 'F': ['q9'],
                'coords': {
                    'q0':(60,150), 'q1':(140,150), 'q2':(220,150), 'q3':(300,150), 'q4':(380,150),
                    'q5':(460,150), 'q6':(540,150), 'q7':(620,150), 'q8':(620,250), 'q9':(540,250), 'qE':(140,250)
                },
                'delta': [
                    ('q0', 'btn_setup', 'q1'), ('q1', 'btn_1', 'q2'), ('q2', 'btn_2', 'q3'), ('q3', 'btn_3', 'q4'),
                    ('q4', 'btn_mute', 'q4'), # LAZO RECURSIVO
                    ('q4', 'btn_ok', 'q5'), ('q5', 'btn_vol_up', 'q6'), ('q6', 'btn_vol_down', 'q7'), 
                    ('q7', 'btn_source', 'q8'), ('q8', 'btn_power', 'q9')
                ]
            },
            {
                'nombre': "LG",
                'color': '#f38ba8',
                'Q': ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'qF1', 'qF2', 'qE'],
                'q0': 'q0', 'F': ['qF1', 'qF2'],
                'coords': {
                    'q0':(60,150), 'q1':(160,150), 'q2':(260,150), 'q3':(360,150), 
                    'q4':(460,150), 'q5':(560,150), 'q6':(660,150), 
                    'qF1':(660,60),  # Éxito 1
                    'qF2':(660,240), # Éxito 2
                    'qE':(260,250)
                },
                'delta': [
                    ('q0', 'btn_power', 'q1'), ('q1', 'btn_setup', 'q2'), ('q2', 'btn_1', 'q3'), 
                    ('q3', 'btn_2', 'q4'), ('q4', 'btn_3', 'q5'), ('q5', 'btn_ok', 'q6'),
                    ('q6', 'btn_audio', 'qF1'), # BIFURCACIÓN FINAL A
                    ('q6', 'btn_image', 'qF2')  # BIFURCACIÓN FINAL B
                ]
            },
            {
                'nombre': "SONY",
                'color': '#cba6f7',
                'Q': ['q0', 'q1', 'q2', 'q3', 'q4a', 'q4b', 'q5', 'q6', 'q7', 'q8', 'q9', 'qE'],
                'q0': 'q0', 'F': ['q9'],
                'coords': {
                    'q0':(60,150), 'q1':(140,150), 'q2':(220,150), 'q3':(300,150), 
                    'q4a':(400,80),  # Rama Arriba
                    'q4b':(400,220), # Rama Abajo
                    'q5':(500,150),  # Fusión
                    'q6':(580,150), 'q7':(580,250), 'q8':(480,250), 'q9':(380,250), 'qE':(220,250)
                },
                'delta': [
                    ('q0', 'btn_menu', 'q1'), ('q1', 'btn_source', 'q2'), ('q2', 'btn_1', 'q3'),
                    ('q3', 'btn_vol_up', 'q4a'),   # SEPARA ARRIBA
                    ('q3', 'btn_vol_down', 'q4b'), # SEPARA ABAJO
                    ('q4a', 'btn_ok', 'q5'),       # UNE
                    ('q4b', 'btn_ok', 'q5'),       # UNE
                    ('q5', 'btn_ch_up', 'q6'), ('q6', 'btn_2', 'q7'), ('q7', 'btn_3', 'q8'), ('q8', 'btn_power', 'q9')
                ]
            },
            {
                'nombre': "HISENSE",
                'color': '#fab387',
                'Q': ['q0', 'q1', 'q2', 'q3', 'q4', 'q5a', 'q5b', 'q6', 'qF1', 'qF2', 'qE'],
                'q0': 'q0', 'F': ['qF1', 'qF2'],
                'coords': {
                    'q0':(60,150), 'q1':(140,150), 'q2':(220,150), 'q3':(300,150), 'q4':(380,150),
                    'q5a':(480,80), 'q5b':(480,220), 
                    'q6':(580,150), 
                    'qF1':(680,80), 'qF2':(680,220), 'qE':(220,250)
                },
                'delta': [
                    ('q0', 'btn_source', 'q1'), ('q1', 'btn_mute', 'q2'), ('q2', 'btn_audio', 'q3'), ('q3', 'btn_image', 'q4'),
                    ('q4', 'btn_ch_up', 'q4'),    # LAZO
                    ('q4', 'btn_menu', 'q5a'),    # BIFURCA
                    ('q4', 'btn_setup', 'q5b'),   # BIFURCA
                    ('q5a', 'btn_1', 'q6'),       # FUSIONA
                    ('q5b', 'btn_2', 'q6'),       # FUSIONA
                    ('q6', 'btn_power', 'qF1'),   # ÉXITO 1
                    ('q6', 'btn_ok', 'qF2')       # ÉXITO 2
                ]
            }
        ]
        
        self.dfa = None
        self.nodos_descubiertos = set()
        self.aristas_descubiertas = set()
        self.lazos_descubiertos = set() 

        self.frame_menu = tk.Frame(root, bg="#1e1e2e")
        self.frame_simulador = tk.Frame(root, bg="#1e1e2e")
        
        self.construir_menu()
        self.construir_simulador()
        self.mostrar_menu()

    def construir_menu(self):
        tk.Label(self.frame_menu, text="CATÁLOGO DE TOPOLOGÍAS DFA (RUTAS LARGAS)", font=("Courier", 22, "bold"), bg="#1e1e2e", fg="#a6e3a1").pack(pady=40)
        for config in self.configuraciones_tv:
            tk.Button(self.frame_menu, text=f"Cargar Matriz: {config['nombre']}", font=("Arial", 14, "bold"), bg=config['color'], fg="#11111b", width=45, pady=10,
                      command=lambda c=config: self.iniciar_simulacion(c)).pack(pady=10)

    def iniciar_simulacion(self, config):
        self.dfa = ControlUniversalDFA(config)
        self.coords_activas = config['coords']
        self.frame_menu.pack_forget()
        self.frame_simulador.pack(fill="both", expand=True)
        f_str = ", ".join(self.dfa.estados_aceptacion)
        self.lbl_titulo_sim.config(text=f"MÁQUINA: {self.dfa.marca} | ACEPTACIÓN: {f_str}")
        self.limpiar_sistema_completo()

    def mostrar_menu(self):
        self.frame_simulador.pack_forget()
        self.frame_menu.pack(fill="both", expand=True)

    def construir_simulador(self):
        self.lbl_titulo_sim = tk.Label(self.frame_simulador, text="", font=("Courier", 14, "bold"), bg="#1e1e2e", fg="#a6e3a1", pady=10)
        self.lbl_titulo_sim.pack()

        panel_izq = tk.Frame(self.frame_simulador, bg="#313244", bd=2, relief="groove")
        panel_izq.pack(side="left", fill="y", padx=10, pady=10)
        
        self.pantalla_control = tk.Label(panel_izq, text="", font=("Consolas", 18, "bold"), bg="#11111b", fg="#a6e3a1", width=12, height=2)
        self.pantalla_control.pack(pady=10, padx=10)
        
        botones = [
            ("SETUP", "btn_setup", "#f9e2af"), ("POWER", "btn_power", "#f38ba8"), ("MENU", "btn_menu", "#89b4fa"), ("SOURCE", "btn_source", "#cba6f7"),
            ("1", "btn_1", "#bac2de"), ("2", "btn_2", "#bac2de"), ("3", "btn_3", "#bac2de"), ("OK", "btn_ok", "#a6e3a1"),
            ("Vol +", "btn_vol_up", "#94e2d5"), ("Vol -", "btn_vol_down", "#94e2d5"), ("Ch +", "btn_ch_up", "#74c7ec"), ("Ch -", "btn_ch_down", "#74c7ec"),
            ("Mute", "btn_mute", "#fab387"), ("Audio", "btn_audio", "#f5c2e7"), ("Imagen", "btn_image", "#b4befe"), ("EXIT", "btn_exit", "#eba0ac")
        ]
        
        frame_grid = tk.Frame(panel_izq, bg="#313244")
        frame_grid.pack(pady=5)
        for i, (texto, simbolo, color) in enumerate(botones):
            btn = tk.Button(frame_grid, text=texto, font=("Arial", 9, "bold"), bg=color, fg="#11111b",
                            width=8, height=2, command=lambda s=simbolo: self.accionar_boton(s))
            btn.grid(row=i//4, column=i%4, padx=3, pady=3)

        tk.Button(panel_izq, text="⚠ RESET DEL HARDWARE ⚠", font=("Arial", 11, "bold"), bg="#e74c3c", fg="white", width=35,
                  command=self.boton_reset_hardware).pack(pady=20)
        tk.Button(panel_izq, text="← Volver al Menú", font=("Arial", 10, "bold"), bg="#585b70", fg="white",
                  command=self.mostrar_menu).pack(side="bottom", pady=20)

        panel_der = tk.Frame(self.frame_simulador, bg="#1e1e2e")
        panel_der.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(panel_der, width=720, height=400, bg="#11111b", highlightthickness=1, highlightbackground="#45475a")
        self.canvas.pack(fill="x", pady=5)
        self.nodos_ui = {}

        tk.Label(panel_der, text="Cinta de Entrada (w):", font=("Arial", 10, "italic"), bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w")
        self.consola_cinta = tk.Text(panel_der, height=3, bg="#11111b", fg="#cba6f7", font=("Consolas", 11), state="disabled")
        self.consola_cinta.pack(fill="x", pady=5)
        
        tk.Label(panel_der, text="Traza de Transición δ(q, a):", font=("Arial", 10, "italic"), bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w")
        self.consola_teoria = tk.Text(panel_der, height=8, bg="#11111b", fg="#a6e3a1", font=("Consolas", 11), state="disabled")
        self.consola_teoria.pack(fill="x", pady=5)

    def dibujar_self_loop(self, x_coords, y_coords, color):
        cx, cy = x_coords, y_coords
        radio, offset = 25, 5
        x1, y1 = cx - 15, cy - radio + offset
        x2, y2 = cx + 15, cy - radio + offset
        cp_y = cy - radio - 20 
        self.canvas.create_arc(x1-5, cp_y, x2+5, y2+15, start=40, extent=100, outline=color, width=2, style=tk.ARC)
        arrow_x1, arrow_y1 = x2 - 2, y2
        self.canvas.create_line(arrow_x1, arrow_y1-5, x2, arrow_y1+2, fill=color, width=2)
        self.canvas.create_line(arrow_x1+5, arrow_y1-2, x2, arrow_y1+2, fill=color, width=2)

    def dibujar_grafo_dinamico(self):
        self.canvas.delete("all")
        coords = self.coords_activas

        for estado in self.lazos_descubiertos:
            if estado in coords and estado != 'qE':
                cx, cy = coords[estado]
                color_loop = "#cba6f7" if estado in self.dfa.estados_aceptacion else "#a6e3a1"
                self.dibujar_self_loop(cx, cy, color_loop)

        for (origen, destino) in self.aristas_descubiertas:
            if origen not in coords or destino not in coords: continue
            x1, y1 = coords[origen]
            x2, y2 = coords[destino]
            
            color_linea = "#a6e3a1"
            if destino == 'qE': color_linea = "#f38ba8"
            if destino == 'q0' and origen != 'q0': color_linea = "#89b4fa"
            if origen == destino: continue 
            
            angulo = math.atan2(y2 - y1, x2 - x1)
            r = 28
            startX = x1 + r * math.cos(angulo)
            startY = y1 + r * math.sin(angulo)
            endX = x2 - r * math.cos(angulo)
            endY = y2 - r * math.sin(angulo)
            
            self.canvas.create_line(startX, startY, endX, endY, fill=color_linea, dash=(4,2), width=2, arrow=tk.LAST)

        r = 25
        self.nodos_ui.clear()
        for estado in self.nodos_descubiertos:
            if estado not in coords: continue
            x, y = coords[estado]
            
            if estado == 'q0' or estado in self.dfa.estados_aceptacion:
                 self.canvas.create_oval(x-r-5, y-r-5, x+r+5, y+r+5, outline="#a6e3a1" if estado=='q0' else "#cba6f7", width=2)
            
            nodo_id = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="#313244", outline="#cdd6f4", width=2)
            self.nodos_ui[estado] = nodo_id
            self.canvas.create_text(x, y, text=estado, font=("Courier", 10, "bold"), fill="#ffffff")
            
            if estado == 'qE': self.canvas.create_text(x, y+38, text="POZO", font=("Arial", 8, "bold"), fill="#f38ba8")
            if estado in self.dfa.estados_aceptacion: self.canvas.create_text(x, y+40, text="ÉXITO", font=("Arial", 8, "bold"), fill="#cba6f7")

    def accionar_boton(self, simbolo):
        est_anterior, est_nuevo, log_trans = self.dfa.procesar_simbolo(simbolo)
        
        if est_anterior == est_nuevo and est_nuevo not in ['qE', 'q0']:
            self.lazos_descubiertos.add(est_nuevo)
        else:
            self.nodos_descubiertos.add(est_nuevo)
            self.aristas_descubiertas.add((est_anterior, est_nuevo))
            
        self.actualizar_pantallas(log_trans)

    def boton_reset_hardware(self):
        if messagebox.askyesno("⚠ Reset", "¿Borrar la memoria de la máquina?"):
            self.limpiar_sistema_completo()

    def limpiar_sistema_completo(self):
        self.dfa.reiniciar()
        self.nodos_descubiertos = {'q0'}
        self.aristas_descubiertas = set()
        self.lazos_descubiertos = set() 
        
        for consola in [self.consola_teoria, self.consola_cinta]:
            consola.config(state="normal")
            consola.delete(1.0, "end")
            consola.config(state="disabled")
        
        self.actualizar_pantallas("Sistema iniciado en q0.", inicio=True)

    def actualizar_pantallas(self, log_transicion, inicio=False):
        self.pantalla_control.config(text=self.dfa.estado_actual)
        self.dibujar_grafo_dinamico()
        
        if self.dfa.estado_actual in self.nodos_ui:
            nodo_actual_id = self.nodos_ui[self.dfa.estado_actual]
            color_activo = "#a6e3a1"
            if self.dfa.estado_actual == 'qE': color_activo = "#f38ba8"
            elif self.dfa.estado_actual in self.dfa.estados_aceptacion: color_activo = "#cba6f7"
            self.canvas.itemconfig(nodo_actual_id, fill=color_activo)

        if not inicio:
            self.consola_teoria.config(state="normal")
            self.consola_teoria.insert("1.0", log_transicion + "\n")
            self.consola_teoria.config(state="disabled")
            
            self.consola_cinta.config(state="normal")
            self.consola_cinta.delete(1.0, "end")
            cinta_texto = " -> ".join(self.dfa.cinta_entrada[-9:])
            self.consola_cinta.insert("end", f"...{cinta_texto}")
            self.consola_cinta.config(state="disabled")
            
            if self.dfa.es_estado_aceptacion() and log_transicion.find("Lazo") == -1:
                # AQUÍ ESTÁ EL MENSAJE QUE PEDISTE
                messagebox.showinfo("¡VINCULACIÓN COMPLETA!", "La televisión se ha vinculado con éxito.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazProyectoFinal(root)
    root.mainloop()
