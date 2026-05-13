import tkinter as tk
from tkinter import messagebox

class ControlUniversalDFA:
    """
    Definición Formal del Autómata Finito Determinista (DFA)
    M = (Q, Sigma, delta, q0, F)
    """
    def __init__(self):
        # Q: Conjunto de estados
        self.estados = ['APAGADO', 'REPOSO', 'TV', 'AUDIO', 'CONFIG']
        
        # Sigma: Alfabeto de entrada (Botones)
        self.alfabeto = ['btn_power', 'btn_tv', 'btn_audio', 'btn_setup', 'btn_vol', 'btn_exit']
        
        # q0: Estado inicial
        self.estado_inicial = 'APAGADO'
        self.estado_actual = self.estado_inicial
        
        # F: Estados de aceptación
        self.estados_aceptacion = ['APAGADO']
        
        # delta: Función de transición
        self.transiciones = {
            'APAGADO': {
                'btn_power': 'REPOSO'
            },
            'REPOSO': {
                'btn_tv': 'TV',
                'btn_audio': 'AUDIO',
                'btn_setup': 'CONFIG',
                'btn_exit': 'APAGADO'
            },
            'TV': {
                'btn_audio': 'AUDIO',
                'btn_setup': 'CONFIG',
                'btn_vol': 'TV',
                'btn_exit': 'APAGADO'
            },
            'AUDIO': {
                'btn_tv': 'TV',
                'btn_setup': 'CONFIG',
                'btn_vol': 'AUDIO',
                'btn_exit': 'APAGADO'
            },
            'CONFIG': {
                'btn_tv': 'TV',
                'btn_audio': 'AUDIO',
                'btn_vol': 'CONFIG',
                'btn_exit': 'APAGADO'
            }
        }
        
        # Historial (Cinta de la máquina)
        self.cinta_entrada = []

    def procesar_simbolo(self, simbolo):
        """Aplica la función de transición delta(q, a) = q' """
        if simbolo in self.transiciones.get(self.estado_actual, {}):
            estado_anterior = self.estado_actual
            self.estado_actual = self.transiciones[self.estado_actual][simbolo]
            self.cinta_entrada.append(simbolo)
            
            return f"δ({estado_anterior}, {simbolo}) = {self.estado_actual}"
        else:
            self.cinta_entrada.append(f"[{simbolo}: IGNORADO]")
            return f"δ({self.estado_actual}, {simbolo}) = {self.estado_actual} (Ignorado)"

    def reiniciar(self):
        self.estado_actual = self.estado_inicial
        self.cinta_entrada.clear()


class InterfazProyectoFinal:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Final: Modelado de Control Universal con DFA")
        self.root.geometry("800x550")
        self.root.configure(bg="#1e1e2e")
        
        self.dfa = ControlUniversalDFA()
        
        # Título Principal
        lbl_titulo = tk.Label(
            root,
            text="TEORÍA DE LA COMPUTACIÓN - AUTÓMATA FINITO DETERMINISTA", 
            font=("Courier", 14, "bold"),
            bg="#1e1e2e",
            fg="#a6e3a1",
            pady=10
        )
        lbl_titulo.pack()

        # ================= PANEL IZQUIERDO: EL CONTROL =================
        panel_izq = tk.Frame(root, bg="#313244", bd=2, relief="groove")
        panel_izq.pack(side="left", fill="y", padx=20, pady=10)
        
        tk.Label(
            panel_izq,
            text="CONTROL FÍSICO",
            font=("Arial", 12, "bold"),
            bg="#313244",
            fg="#f38ba8"
        ).pack(pady=10)
        
        # Pantallita del control
        self.pantalla_control = tk.Label(
            panel_izq,
            text=self.dfa.estado_actual, 
            font=("Consolas", 18, "bold"),
            bg="#11111b",
            fg="#89b4fa",
            width=15,
            height=2
        )
        self.pantalla_control.pack(pady=10, padx=20)
        
        # Botones del control
        botones = [
            ("Encendido", "btn_power", "#a6e3a1"),
            ("Modo TV", "btn_tv", "#89b4fa"),
            ("Modo AUDIO", "btn_audio", "#cba6f7"),
            ("Modo SETUP", "btn_setup", "#f9e2af"),
            ("Subir Volumen", "btn_vol", "#fab387"),
            ("Exit", "btn_exit", "#f38ba8")
        ]
        
        for texto, simbolo, color in botones:
            btn = tk.Button(
                panel_izq,
                text=texto,
                font=("Arial", 10, "bold"),
                bg=color,
                fg="#11111b",
                width=18,
                command=lambda s=simbolo: self.accionar_boton(s)
            )
            btn.pack(pady=5)

        # ================= PANEL DERECHO: MONITOR MATEMÁTICO =================
        panel_der = tk.Frame(root, bg="#1e1e2e")
        panel_der.pack(side="right", fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(
            panel_der,
            text="MONITOR TEÓRICO DEL AUTÓMATA",
            font=("Arial", 12, "bold"),
            bg="#1e1e2e",
            fg="#f38ba8"
        ).pack(anchor="w")
        
        # Consola de transiciones
        tk.Label(
            panel_der,
            text="Función de Transición Ejecutada:",
            font=("Arial", 10, "italic"),
            bg="#1e1e2e",
            fg="#cdd6f4"
        ).pack(anchor="w", pady=(10, 0))

        self.consola_teoria = tk.Text(
            panel_der,
            height=8,
            bg="#11111b",
            fg="#a6e3a1",
            font=("Consolas", 11),
            state="disabled"
        )
        self.consola_teoria.pack(fill="x", pady=5)
        
        # Cinta de entrada
        tk.Label(
            panel_der,
            text="Cinta de Entrada (Palabra w):",
            font=("Arial", 10, "italic"),
            bg="#1e1e2e",
            fg="#cdd6f4"
        ).pack(anchor="w", pady=(10, 0))

        self.consola_cinta = tk.Text(
            panel_der,
            height=6,
            bg="#11111b",
            fg="#cba6f7",
            font=("Consolas", 11),
            state="disabled"
        )
        self.consola_cinta.pack(fill="x", pady=5)
        
        # Botones de control de la simulación
        frame_simulacion = tk.Frame(panel_der, bg="#1e1e2e")
        frame_simulacion.pack(fill="x", pady=20)
        
        tk.Button(
            frame_simulacion,
            text="Imprimir Quíntupla (M)",
            font=("Arial", 10, "bold"),
            bg="#fab387",
            fg="#11111b",
            command=self.mostrar_quintupla
        ).pack(side="left", padx=5)
                  
        tk.Button(
            frame_simulacion,
            text="Resetear Máquina",
            font=("Arial", 10, "bold"),
            bg="#f38ba8",
            fg="#11111b",
            command=self.resetear
        ).pack(side="right", padx=5)

        self.actualizar_pantallas("Máquina inicializada en q0.")

    def accionar_boton(self, simbolo):
        resultado_transicion = self.dfa.procesar_simbolo(simbolo)
        self.actualizar_pantallas(resultado_transicion)

    def actualizar_pantallas(self, log_transicion):
        self.pantalla_control.config(text=self.dfa.estado_actual)
        
        self.consola_teoria.config(state="normal")
        self.consola_teoria.insert("end", log_transicion + "\n")
        self.consola_teoria.see("end")
        self.consola_teoria.config(state="disabled")
        
        self.consola_cinta.config(state="normal")
        self.consola_cinta.delete(1.0, "end")
        cinta_texto = " -> ".join(self.dfa.cinta_entrada)
        self.consola_cinta.insert("end", f"w = {cinta_texto}")
        self.consola_cinta.config(state="disabled")

    def mostrar_quintupla(self):
        quintupla = f"""Definición Formal M = (Q, Σ, δ, q0, F)
        
Q = {self.dfa.estados}
Σ = {self.dfa.alfabeto}
q0 = {self.dfa.estado_inicial}
F = {self.dfa.estados_aceptacion}

El botón Encendido permite pasar del estado APAGADO
al estado REPOSO.

El botón Exit funciona como apagado seguro, ya que desde
REPOSO, TV, AUDIO o CONFIG regresa al estado APAGADO."""
        
        messagebox.showinfo("Definición Matemática", quintupla)

    def resetear(self):
        if messagebox.askyesno("Reset", "¿Vaciar la cinta y regresar al estado inicial?"):
            self.dfa.reiniciar()
            self.consola_teoria.config(state="normal")
            self.consola_teoria.delete(1.0, "end")
            self.consola_teoria.config(state="disabled")
            self.actualizar_pantallas("Máquina reiniciada a q0.")


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazProyectoFinal(root)
    root.mainloop()