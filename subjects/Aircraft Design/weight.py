import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
import math

# Array global para almacenar nombres de fases de vuelo
flight_phases = []
# Array global para almacenar constantes de fases de vuelo
flight_constants = []

class FlightPhasesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Asignador de Fases de Vuelo")
        self.geometry("1000x700")
        self.total_phases = 0
        self._create_widgets()
        # Entry widget that will receive parameter values from the popup
        self.current_param_entry = None

    def _create_widgets(self):
        # Panel izquierdo para seleccionar constantes A y B
        left_frame = ttk.Frame(self, padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        # Datos de tabla: lista de (nombre, A, B)
        self.ab_table = [
            ("Homebuilts", 0.3411, 0.9519),
            ("Scaled Fighters", 0.5542, 0.8654),
            ("Composites", 0.8222, 0.8050),
            ("Single Engine Propeller", -0.1440, 1.1162),
            ("Twin Engine Propeller", 0.0966, 1.0298),
            ("Twin Engine Composites", 0.1130, 1.0403),
            ("Agricultural", -0.4398, 1.1946),
            ("Business Jets", 0.2678, 0.9979),
            ("Regional TBP", 0.3774, 0.9647),
            ("Transport Jets", 0.0833, 1.0383),
            ("Military Trainers Jets", 0.6632, 0.8640),
            ("Military Trainers Turboprops", -1.4041, 1.4660),
            ("Military Trainers Turboprops wout 2", 0.1677, 1.4660),
            ("Military Trainers Piston", 0.5627, 0.8761),
            ("Fighters Jets ext load", 0.5091, 0.9505),
            ("Fighters Jets clean", 0.1362, 1.0116),
            ("Fighters Turboprops ext load", 0.2705, 0.9830),
            ("Patrol/Bomb Jets", -0.2009, 1.1037),
            ("Patrol/Bomb Turboprops", -0.4179, 1.1446),
            ("Flying Boats", 0.1703, 1.0083),
            ("Supersonic Cruise", 0.4221, 0.9876)
        ]
        ttk.Label(left_frame, text="Selección A/B:").grid(column=0, row=0, sticky=tk.W)
        names = [row[0] for row in self.ab_table]
        self.ab_combo = ttk.Combobox(left_frame, values=names, state="readonly", width=30)
        self.ab_combo.grid(column=0, row=1, sticky=tk.W)
        self.ab_combo.bind("<<ComboboxSelected>>", self.on_ab_select)
        # Opción para usar tabla o personalizado
        self.ab_choice = tk.StringVar(value="tabla")
        ttk.Radiobutton(left_frame, text="Tabla", variable=self.ab_choice, value="tabla", command=self.on_ab_select).grid(column=0, row=2, sticky=tk.W)
        ttk.Radiobutton(left_frame, text="Personalizado", variable=self.ab_choice, value="custom", command=self.on_ab_select).grid(column=0, row=3, sticky=tk.W)
        ttk.Label(left_frame, text="A:").grid(column=0, row=4, sticky=tk.W)
        self.A_entry = ttk.Entry(left_frame, width=10)
        self.A_entry.grid(column=0, row=5, sticky=tk.W)
        ttk.Label(left_frame, text="B:").grid(column=0, row=6, sticky=tk.W)
        self.B_entry = ttk.Entry(left_frame, width=10)
        self.B_entry.grid(column=0, row=7, sticky=tk.W)
        # Entrada de valor D personalizado
        ttk.Label(left_frame, text="D:").grid(column=0, row=8, sticky=tk.W)
        self.D_entry = ttk.Entry(left_frame, width=10)
        self.D_entry.grid(column=0, row=9, sticky=tk.W)
        # Inicializar A/B valores según selección y propagar a WTO
        self.on_ab_select()
        self._propagate_AB_to_WTO()
        # Vincular D personalizado para propagar a WTO
        self.D_entry.bind("<FocusOut>", self._propagate_D_to_WTO)

        frame = ttk.Frame(self, padding=10)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Selector de tipo de aeronave
        ttk.Label(frame, text="Tipo de aeronave:").grid(column=0, row=0, sticky=tk.W)
        self.aircraft_type_var = tk.StringVar(value="propeller")
        prop_rb = ttk.Radiobutton(frame, text="Propeller", variable=self.aircraft_type_var, value="propeller")
        prop_rb.grid(column=1, row=0, sticky=tk.W)
        jet_rb = ttk.Radiobutton(frame, text="Jet", variable=self.aircraft_type_var, value="jet")
        jet_rb.grid(column=2, row=0, sticky=tk.W)

        # Bloque para inicializar número total de fases
        ttk.Label(frame, text="Total de fases de vuelo:").grid(column=0, row=1, sticky=tk.W)
        self.total_spin = ttk.Spinbox(frame, from_=1, to=100, width=5)
        self.total_spin.grid(column=1, row=1, sticky=tk.W)
        init_btn = ttk.Button(frame, text="Inicializar fases", command=self.init_phases)
        init_btn.grid(column=2, row=1, padx=5)

        # Selector de número de fase (deshabilitado hasta init)
        ttk.Label(frame, text="Número de fase:").grid(column=0, row=2, sticky=tk.W, pady=(10,0))
        self.phase_spin = ttk.Spinbox(frame, from_=1, to=1, width=5, state="disabled")
        self.phase_spin.grid(column=1, row=2, sticky=tk.W, pady=(10,0))

        # Entrada de nombre de fase (deshabilitada hasta init)
        ttk.Label(frame, text="Nombre de fase:").grid(column=0, row=3, sticky=tk.W, pady=(5,0))
        self.phase_name = ttk.Entry(frame, width=30, state="disabled")
        self.phase_name.grid(column=1, row=3, columnspan=2, sticky=tk.W, pady=(5,0))

        # Selección de tipo de constante
        ttk.Label(frame, text="Tipo de constante:").grid(column=0, row=4, sticky=tk.W, pady=(5,0))
        self.constant_type = ttk.Combobox(frame, values=["Personalizada", "Climb", "Cruise", "Loiter"], state="disabled", width=15)
        self.constant_type.current(0)
        self.constant_type.grid(column=1, row=4, sticky=tk.W, pady=(5,0))
        self.constant_type.bind("<<ComboboxSelected>>", self.on_constant_type_change)

        # Entrada de constante personalizada (deshabilitada hasta init)
        self.const_label = ttk.Label(frame, text="Constante de fase:")
        self.const_label.grid(column=0, row=5, sticky=tk.W, pady=(5,0))
        self.phase_constant = ttk.Entry(frame, width=15, state="disabled")
        self.phase_constant.grid(column=1, row=5, sticky=tk.W, pady=(5,0))
        # Botón de tabla de constantes (deshabilitado hasta modo personalizada)
        self.const_table_btn = ttk.Button(frame, text="Tabla 2.1", command=self.show_constant_table)
        self.const_table_btn.grid(column=2, row=5, sticky=tk.W, padx=(5,0))
        self.const_table_btn.grid_remove()

        # Frame para parámetros de cálculo
        self.param_frame = ttk.Frame(frame)
        self.param_frame.grid(column=1, row=5, columnspan=2, sticky=tk.W)
        self.param_frame.grid_remove()
        # Botón de tabla de parámetros (para Climb/Cruise/Loiter)
        self.param_table_btn = ttk.Button(frame, text="Tabla 2.2", command=self.show_param_table)
        # Desplazar un poco para que no colisione con Tabla 2.1
        self.param_table_btn.grid(column=3, row=5, sticky=tk.W, padx=(10,0))
        self.param_table_btn.grid_remove()
        # Ajuste de visibilidad inicial de constantes y tabla
        self.on_constant_type_change(None)

        # Botón para agregar fase (deshabilitado hasta init)
        self.add_btn = ttk.Button(frame, text="Asignar fase", command=self.add_phase, state="disabled")
        self.add_btn.grid(column=0, row=6, columnspan=3, pady=10)

        # Lista de fases
        ttk.Label(frame, text="Fases asignadas:").grid(column=0, row=7, sticky=tk.W, pady=(10,0))
        self.listbox = tk.Listbox(frame, height=8)
        self.listbox.grid(column=0, row=8, columnspan=3, sticky=tk.NSEW)
        frame.rowconfigure(8, weight=1)
        frame.columnconfigure(2, weight=1)
        # Botón para calcular fracción de combustible
        self.calc_btn = ttk.Button(frame, text="Calcular fracción combustible", command=self.compute_fuel_fraction, state="disabled")
        self.calc_btn.grid(column=0, row=9, columnspan=3, pady=(10,0))

        # Sección para calcular WTO
        ttk.Label(frame, text="-- Calcular WTO --").grid(column=0, row=10, sticky=tk.W, pady=(10,0))
        # A y B
        ttk.Label(frame, text="A:").grid(column=0, row=11, sticky=tk.W)
        self.WTO_A = ttk.Entry(frame, width=10)
        self.WTO_A.grid(column=1, row=11, sticky=tk.W)
        ttk.Label(frame, text="B:").grid(column=0, row=12, sticky=tk.W)
        self.WTO_B = ttk.Entry(frame, width=10)
        self.WTO_B.grid(column=1, row=12, sticky=tk.W)
        # Mff editable tras cálculo
        ttk.Label(frame, text="Mff:").grid(column=0, row=13, sticky=tk.W)
        self.WTO_Mff = ttk.Entry(frame, width=10)
        self.WTO_Mff.grid(column=1, row=13, sticky=tk.W)
        # Recalcular C cuando cambie Mff
        self.WTO_Mff.bind("<FocusOut>", self._calculate_C)
        # Mres y Mtfo
        ttk.Label(frame, text="Mres:").grid(column=0, row=14, sticky=tk.W)
        self.WTO_Mres = ttk.Entry(frame, width=10)
        self.WTO_Mres.grid(column=1, row=14, sticky=tk.W)
        # Valor por defecto de Mres (editable antes de calcular C)
        self.WTO_Mres.insert(0, "0.25")
        # Recalcular C cuando cambie Mres
        self.WTO_Mres.bind("<FocusOut>", self._calculate_C)
        ttk.Label(frame, text="Mtfo:").grid(column=0, row=15, sticky=tk.W)
        self.WTO_Mtfo = ttk.Entry(frame, width=10)
        self.WTO_Mtfo.grid(column=1, row=15, sticky=tk.W)
        # Valor por defecto de Mtfo (editable antes de calcular C)
        self.WTO_Mtfo.insert(0, "0.005")
        # Recalcular C cuando cambie Mtfo
        self.WTO_Mtfo.bind("<FocusOut>", self._calculate_C)
        # C editable (se actualizará tras calcular C pero permite corrección)
        ttk.Label(frame, text="C:").grid(column=0, row=16, sticky=tk.W)
        self.WTO_C = ttk.Entry(frame, width=10)
        self.WTO_C.grid(column=1, row=16, sticky=tk.W)
        # Botón para calcular C manualmente
        calcC_btn = ttk.Button(frame, text="Calcular C", command=self._calculate_C)
        calcC_btn.grid(column=2, row=16, sticky=tk.W, padx=(5,0))
        # D personalizado
        ttk.Label(frame, text="D:").grid(column=0, row=17, sticky=tk.W)
        self.WTO_D = ttk.Entry(frame, width=10)
        self.WTO_D.grid(column=1, row=17, sticky=tk.W)
        # Botón WTO
        self.WTO_btn = ttk.Button(frame, text="Calcular WTO", command=self.on_compute_WTO)
        self.WTO_btn.grid(column=0, row=18, columnspan=3, pady=(10,0))
        # Campo para mostrar resultado WTO
        ttk.Label(frame, text="WTO:").grid(column=0, row=19, sticky=tk.W, pady=(5,0))
        self.WTO_result = ttk.Entry(frame, width=15, state='readonly')
        self.WTO_result.grid(column=1, row=19, columnspan=2, sticky=tk.W, pady=(5,0))

    def init_phases(self):
        try:
            total = int(self.total_spin.get())
            if total < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Total de fases inválido")
            return

        global flight_phases, flight_constants
        flight_phases = [""] * total
        flight_constants = [0.0] * total
        self.total_phases = total

        # Configurar rango del spinbox de fases
        self.phase_spin.configure(to=total, state="normal")
        self.phase_name.configure(state="normal")
        self.constant_type.configure(state="readonly")
        self.phase_constant.configure(state="normal")
        self.add_btn.configure(state="normal")
        self.calc_btn.configure(state="normal")

        # Deshabilitar la inicialización
        self.total_spin.configure(state="disabled")


        self._refresh_list()

    def on_constant_type_change(self, event):
        sel = self.constant_type.get()
        # reset current parameter selection when changing constant type
        self.current_param_entry = None
        # Clear previous inputs
        for widget in self.param_frame.winfo_children():
            widget.destroy()
        self.phase_constant.delete(0, tk.END)
        # Show appropriate widgets
        if sel == "Personalizada":
            self.const_label.grid()
            self.phase_constant.grid()
            self.const_table_btn.grid()
            self.param_frame.grid_remove()
            self.param_table_btn.grid_remove()
        else:
            self.const_label.grid_remove()
            self.phase_constant.grid_remove()
            self.const_table_btn.grid_remove()
            # Determine params
            params = []
            if sel in ("Climb", "Loiter"):
                params = ["E_ltr", "V_ltr", "eta_p", "cp_ltr", "L/D"]
            elif sel == "Cruise":
                params = ["R_cr", "eta_p", "cp_cr", "L/D"]
            self.param_entries = {}
            for i, param in enumerate(params):
                ttk.Label(self.param_frame, text=f"{param}:").grid(column=0, row=i, sticky=tk.W)
                entry = ttk.Entry(self.param_frame, width=10)
                entry.grid(column=1, row=i, sticky=tk.W)
                # when focused, store this entry for popup insertion
                entry.bind("<FocusIn>", lambda e, widget=entry: setattr(self, 'current_param_entry', widget))
                self.param_entries[param] = entry
            self.param_frame.grid()
            # mostrar tabla de parámetros
            self.param_table_btn.grid()


    def add_phase(self):
        try:
            num = int(self.phase_spin.get())
        except ValueError:
            messagebox.showerror("Error", "Número de fase inválido")
            return

        name = self.phase_name.get().strip()
        if not name:
            messagebox.showerror("Error", "El nombre de la fase no puede estar vacío")
            return

        sel = self.constant_type.get()
        try:
            if sel == "Personalizada":
                constant = float(self.phase_constant.get())
            else:
                vals = {p: float(e.get()) for p, e in self.param_entries.items()}
                constant = calculate_phase_constant(sel, self.aircraft_type_var.get(), vals)
        except (ValueError, KeyError):
            messagebox.showerror("Error", "Faltan o son inválidos los parámetros de la constante")
            return

        # Redondear constante a 4 decimales
        constant = round(constant, 4)
        global flight_phases, flight_constants
        # Asignar en los arrays globales (índice num-1)
        flight_phases[num-1] = name
        flight_constants[num-1] = constant
        self._refresh_list()
        # Limpiar entradas
        self.phase_name.delete(0, tk.END)
        self.phase_constant.delete(0, tk.END)
        # Reset tipo de constante y parámetros
        self.constant_type.current(0)
        self.on_constant_type_change(None)
        # Avanzar al siguiente número de fase o deshabilitar si finalizado
        if num < self.total_phases:
            next_num = num + 1
            self.phase_spin.set(str(next_num))
        else:
            # Deshabilitar entradas al terminar
            self.phase_spin.configure(state="disabled")
            self.phase_name.configure(state="disabled")
            self.constant_type.configure(state="disabled")
            self.phase_constant.configure(state="disabled")
            self.add_btn.configure(state="disabled")

    def on_ab_select(self, event=None):
        """Actualiza entradas de A y B según tabla o modo personalizado."""
        if self.ab_choice.get() == 'tabla':
            idx = self.ab_combo.current()
            if idx >= 0:
                _, a_val, b_val = self.ab_table[idx]
                self.A_entry.config(state='normal')
                self.B_entry.config(state='normal')
                self.A_entry.delete(0, tk.END)
                self.B_entry.delete(0, tk.END)
                self.A_entry.insert(0, f"{a_val:.4f}")
                self.B_entry.insert(0, f"{b_val:.4f}")
                self.A_entry.config(state='readonly')
                self.B_entry.config(state='readonly')
        else:
            # Personalizado: habilitar y limpiar
            self.A_entry.config(state='normal')
            self.B_entry.config(state='normal')
            self.A_entry.delete(0, tk.END)
            self.B_entry.delete(0, tk.END)
        # Propagar a campos WTO
        self._propagate_AB_to_WTO()

    def compute_fuel_fraction(self):
        """
        Calcula la fracción total de combustible multiplicando las constantes de todas las fases.
        """
        if not flight_constants:
            messagebox.showerror("Error", "No hay fases inicializadas")
            return
        total_fraction = calculate_fuel_fraction(flight_constants)
        messagebox.showinfo("Fracción combustible", f"Fracción total de combustible: {total_fraction:.6f}")
        # Poblar entrada de Mff (editable para correcciones)
        if hasattr(self, 'WTO_Mff'):
            self.WTO_Mff.config(state='normal')
            self.WTO_Mff.delete(0, tk.END)
            self.WTO_Mff.insert(0, f"{total_fraction:.6f}")
            # Intentar calcular WTO automáticamente
            try:
                A = float(self.WTO_A.get())
                B = float(self.WTO_B.get())
                Mff = float(self.WTO_Mff.get())
                Mres = float(self.WTO_Mres.get())
                Mtfo = float(self.WTO_Mtfo.get())
                D = float(self.WTO_D.get())
                C, wto = calculate_WTO_model(A, B, Mff, Mres, Mtfo, D)
                # Mostrar C y WTO
                self.WTO_C.config(state='normal')
                self.WTO_C.delete(0, tk.END)
                self.WTO_C.insert(0, f"{C:.4f}")
                self.WTO_C.config(state='readonly')
                self.WTO_result.config(state='normal')
                self.WTO_result.delete(0, tk.END)
                self.WTO_result.insert(0, f"{wto:.6f}")
                self.WTO_result.config(state='readonly')
            except Exception:
                pass

    def _refresh_list(self):
        self.listbox.delete(0, tk.END)
        for idx, (name, constant) in enumerate(zip(flight_phases, flight_constants), start=1):
            name_display = name if name else "<sin asignar>"
            self.listbox.insert(tk.END, f"Fase {idx}: {name_display} (Mff: {constant})")


    def _calculate_C(self, event=None):
        """Calcula automáticamente C = 1 - (1+Mres)*(1-Mff) - Mtfo"""
        try:
            Mff = float(self.WTO_Mff.get())
            Mres = float(self.WTO_Mres.get())
            Mtfo = float(self.WTO_Mtfo.get())
            C = calculate_residual_C(Mff, Mres, Mtfo)
            self.WTO_C.config(state='normal')
            self.WTO_C.delete(0, tk.END)
            self.WTO_C.insert(0, f"{C:.4f}")
            self.WTO_C.config(state='readonly')
        except ValueError:
            pass

    def on_compute_WTO(self):
        try:
            A = float(self.WTO_A.get())
            B = float(self.WTO_B.get())
            Mff = float(self.WTO_Mff.get())
            Mres = float(self.WTO_Mres.get())
            Mtfo = float(self.WTO_Mtfo.get())
            D = float(self.WTO_D.get())
        except ValueError as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")
            return
        try:
            C, wto = calculate_WTO_model(A, B, Mff, Mres, Mtfo, D)
            # Mostrar C y WTO en sus campos
            self.WTO_C.config(state='normal')
            self.WTO_C.delete(0, tk.END)
            self.WTO_C.insert(0, f"{C:.4f}")
            self.WTO_C.config(state='readonly')
            self.WTO_result.config(state='normal')
            self.WTO_result.delete(0, tk.END)
            self.WTO_result.insert(0, f"{wto:.6f}")
            self.WTO_result.config(state='readonly')
        except Exception as e:
            messagebox.showerror("Error WTO", str(e))

    def _propagate_AB_to_WTO(self):
        """Copiar A y B de panel izquierdo a campos WTO."""
        if hasattr(self, 'WTO_A'):
            val_a = self.A_entry.get()
            val_b = self.B_entry.get()
            self.WTO_A.delete(0, tk.END)
            self.WTO_A.insert(0, val_a)
            self.WTO_B.delete(0, tk.END)
            self.WTO_B.insert(0, val_b)

    def _propagate_D_to_WTO(self, event=None):
        """Copiar D de panel izquierdo a campo WTO D."""
        if hasattr(self, 'WTO_D'):
            val_d = self.D_entry.get()
            self.WTO_D.delete(0, tk.END)
            self.WTO_D.insert(0, val_d)
    def show_constant_table(self):
        """Muestra una tabla emergente de constantes estándar para fases."""
        top = tk.Toplevel(self)
        top.title("Tabla de constantes de fase")
        ttk.Label(top, text="Selecciona un valor de la tabla:").pack(padx=10, pady=5)
        # Constantes por fase (número: [Warm-up, Taxi, Take-off, Climb, Descent, Landing])
        table = {
            1: ["0.998", "0.998", "0.998", "0.995", "0.995", "0.995"],
            2: ["0.995", "0.997", "0.998", "0.992", "0.993", "0.993"],
            3: ["0.992", "0.996", "0.996", "0.990", "0.992", "0.992"],
            4: ["0.996", "0.995", "0.996", "0.998", "0.999", "0.998"],
            5: ["0.990", "0.995", "0.995", "0.980", "0.990", "0.992"],
            6: ["0.990", "0.995", "0.995", "0.985", "0.985", "0.995"],
            7: ["0.990", "0.990", "0.995", "0.980", "0.990", "0.992"],
            8: ["0.990", "0.990", "0.990", "0.980", "0.990", "0.995"],
            9: ["0.990", "0.990", "0.990", "0.96-0.90", "0.990", "0.995"],
            10:["0.990", "0.990", "0.995", "0.980", "0.990", "0.992"],
            11:["0.992", "0.990", "0.996", "0.985", "0.990", "0.990"],
            12:["0.990", "0.995", "0.995", "0.92-0.87", "0.985", "0.992"]
        }
        # Mapa de fase a tipo de aeronave para lectura
        types = {
            1: "Homebuilt",
            2: "Single Engine",
            3: "Twin Engine",
            4: "Agricultural",
            5: "Business Jets",
            6: "Regional TBP's",
            7: "Transport Jets",
            8: "Military Trainers",
            9: "Fighters",
            10: "Mil. Patrol/Bomb/Transport",
            11: "Flying Boats/Amphibious/Float Airplanes",
            12: "Supersonic Cruise"
        }
        # Crear cuadrícula de botones clicables
        stages = ["Warm-up","Taxi","Take-off","Climb","Descent","Landing"]
        # Encabezados
        header = ttk.Frame(top)
        header.pack(padx=10)
        ttk.Label(header, text="Tipo de aeronave", width=20, anchor=tk.W).grid(row=0, column=0)
        for j, stage in enumerate(stages, start=1):
            ttk.Label(header, text=stage, width=12).grid(row=0, column=j)
        # Filas con botones
        body = ttk.Frame(top)
        body.pack(padx=10, pady=(0,10))
        def make_command(val):
            def cmd():
                sel = val
                if '-' in sel:
                    low, high = sel.split('-')
                    sel = f"{(float(low)+float(high))/2:.3f}"
                self.phase_constant.delete(0, tk.END)
                self.phase_constant.insert(0, sel)
            return cmd
        for i in range(1, 13):
            # Tipo de aeronave
            ttk.Label(body, text=types[i], width=20, anchor=tk.W).grid(row=i, column=0, pady=2)
            # Botones para cada etapa
            vals = table[i]
            for j, val in enumerate(vals, start=1):
                btn = ttk.Button(body, text=val, width=12, command=make_command(val))
                btn.grid(row=i, column=j, padx=2, pady=1)
    
    def show_param_table(self):
        """Muestra popup de tabla de parámetros para Climb/Cruise/Loiter"""
        sel = self.constant_type.get()
        # Prepare popup window
        top = tk.Toplevel(self)
        top.title(f"Tabla de parámetros 2.2 - {sel}")
        ttk.Label(top, text="Selecciona un valor para el parámetro seleccionado:").pack(padx=10, pady=5)
        # Common mapping phase to aircraft type
        types = {
            1: "Homebuilt",
            2: "Single Engine",
            3: "Twin Engine",
            4: "Agricultural",
            5: "Business Jets",
            6: "Regional TBP's",
            7: "Transport Jets",
            8: "Military Trainers",
            9: "Fighters",
            10: "Mil. Patrol/Bomb/Transport",
            11: "Flying Boats/Amphibious/Float Airplanes",
            12: "Supersonic Cruise"
        }
        # Parameter tables for Cruise and Loiter (lists: [L/D, c_j, c_p, η_p])
        table_cruise = {
            1: ["8-10", "", "0.6-0.7","0.7",],
            2: ["8-10", "", "0.5-0.7","0.8",],
            3: ["8-10", "", "0.5-0.7","0.82",],
            4: ["5-7", "", "0.5-0.7","0.82",],
            5: ["10-12", "0.5-0.9", "",],
            6: ["11-13", "", "0.4-0.6","0.85",],
            7: ["13-15", "0.5-0.9", "",],
            8: ["8-10", "0.5-1.0", "0.4-0.6","0.82",],
            9: ["4-7", "0.6-1.4", "0.5-0.7","0.82",],
            10: ["13-15", "0.5-0.9", "0.4-0.7","0.82",],
            11: ["10-12", "0.5-0.9", "0.5-0.7","0.82",],
            12: ["4-6", "0.7-1.5", "",]
        }
        table_loiter = {
            1: ["10-12", "", "0.5-0.7","0.6"],
            2: ["10-12", "", "0.5-0.7","0.7"],
            3: ["9-11", "", "0.5-0.7","0.72"],
            4: ["8-10","" , "0.5-0.7","0.72"],
            5: ["12-14", "0.4-0.6", "",""],
            6: ["14-16", "0.5-0.7", "0.5-0.7","0.77"],
            7: ["14-18", "0.4-0.6", "",""],
            8: ["10-14", "0.4-0.6", "0.5-0.7", "0.77"],
            9: ["6-9", "0.6-0.8", "0.5-0.7","0.77"],
            10: ["14-18", "0.4-0.6", "0.5-0.7","0.77"],
            11: ["13-15", "0.4-0.6", "0.5-0.7","0.77"],
            12: ["7-9", "0.6-0.8", "", ""]
        }
        # Select appropriate table and extend rows to include η_p
        raw_table = table_cruise if sel == "Cruise" else table_loiter
        table = {i: vals + [""] for i, vals in raw_table.items()}
        # Create header with η_p
        header = ttk.Frame(top)
        header.pack(padx=10)
        ttk.Label(header, text="Tipo de aeronave", width=20, anchor=tk.W).grid(row=0, column=0)
        for j, col in enumerate(["L/D", "c_j", "c_p", "η_p"], start=1):
            ttk.Label(header, text=col, width=12).grid(row=0, column=j)
        # Body with buttons
        body = ttk.Frame(top)
        body.pack(padx=10, pady=(0,10))
        def make_command(val):
            def cmd():
                if not hasattr(self, 'current_param_entry') or self.current_param_entry is None:
                    return
                sel_val = val
                if '-' in sel_val:
                    low, high = sel_val.split('-')
                    sel_val = f"{(float(low)+float(high))/2:.3f}"
                self.current_param_entry.delete(0, tk.END)
                self.current_param_entry.insert(0, sel_val)
                top.destroy()
            return cmd
        for i in range(1, 13):
            ttk.Label(body, text=types[i], width=20, anchor=tk.W).grid(row=i, column=0, pady=2)
            vals = table.get(i, ["", "", ""])
            for j, val in enumerate(vals, start=1):
                btn = ttk.Button(body, text=val, width=12, command=make_command(val))
                btn.grid(row=i, column=j, padx=2, pady=1)
    


# region Modelo de Cálculo
# Funciones de modelo separadas de la interfaz
def calculate_phase_constant(sel: str, aircraft_type: str, vals: dict, custom_constant: Optional[float] = None) -> float:
    if sel == "Personalizada":
        if custom_constant is None:
            raise ValueError("Constante personalizada no suministrada")
        return custom_constant
    if sel == "Climb":
        if aircraft_type == 'jet':
            return math.exp(-vals.get("E_cl", 0) / ((1/vals.get("cj_cl",1)) * vals.get("L/D",1)))
        else:
            return math.exp(-vals["E_ltr"] * vals["V_ltr"] / (375 * (vals["eta_p"]/vals["cp_ltr"]) * vals["L/D"]))
    elif sel == "Cruise":
        if aircraft_type == 'jet':
            return math.exp(-vals.get("R_cr",0) / ((vals.get("V_cr",1)/vals.get("cj_cr",1)) * vals.get("L/D",1)))
        else:
            return math.exp(-vals["R_cr"] / (375 * (vals["eta_p"]/vals["cp_cr"]) * vals["L/D"]))
    elif sel == "Loiter":
        if aircraft_type == 'jet':
            return math.exp(-vals.get("E_ltr",0) / ((1/vals.get("cj_ltr",1)) * vals.get("L/D",1)))
        else:
            return math.exp(-vals["E_ltr"] * vals["V_ltr"] / (375 * (vals["eta_p"]/vals["cp_ltr"]) * vals["L/D"]))
    else:
        raise ValueError(f"Tipo desconocido: {sel}")

def calculate_fuel_fraction(constants: list[float]) -> float:
     total = 1.0
     for c in constants:
         total *= c
     return total

def calculate_residual_C(Mff: float, Mres: float, Mtfo: float) -> float:
     return 1 - (1 + Mres) * (1 - Mff) - Mtfo

def calculate_WTO_model(A: float, B: float, Mff: float, Mres: float, Mtfo: float, D: float) -> tuple[float, float]:
    """Modelo que calcula primero C y luego WTO"""
    C = calculate_residual_C(Mff, Mres, Mtfo)
    wto = calcular_WTO(A, B, C, D)
    return C, wto

def calcular_WTO(A: float, B: float, c: float, D: float,
                  tol: float = 1e-8, max_iter: int = 100) -> float:
    x_min = D / c
    if c <= 0:
        raise ValueError("c debe ser positivo")
    if D < 0:
        raise ValueError("D debe ser no negativo")
    def f(x: float) -> float:
        return math.log10(x) - A - B * math.log10(c*x - D)
    x_low = x_min * (1 + 1e-6)
    f_low = f(x_low)
    x_high = x_low * 2.0
    for _ in range(100):
        f_high = f(x_high)
        if f_low * f_high < 0:
            break
        x_high *= 2.0
    else:
        raise RuntimeError("No se encontró intervalo con cambio de signo")
    for _ in range(max_iter):
        x_mid = 0.5 * (x_low + x_high)
        f_mid = f(x_mid)
        if abs(f_mid) < tol or (x_high - x_low) < tol:
            return x_mid
        if f_low * f_mid < 0:
            x_high = x_mid
        else:
            x_low = x_mid
            f_low = f_mid
    raise RuntimeError(f"No convergió en {max_iter} iteraciones")


if __name__ == "__main__":
    app = FlightPhasesApp()
    app.mainloop()