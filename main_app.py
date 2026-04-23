import os
import io
import threading
import contextlib
import tkinter as tk
from tkinter import ttk, scrolledtext


# from config import RUTA_PROYECTO

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Agg renderiza en memoria (sin ventanas propias).
# Debe configurarse ANTES de importar pyplot o cualquier módulo del proyecto.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib._pylab_helpers as _gcf_helpers
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import pandas as pd
pd.set_option('display.max_columns', None)   # pandas nunca oculta columnas
pd.set_option('display.width', None)         # pandas nunca parte filas
pd.set_option('display.max_colwidth', None)  # pandas nunca trunca valores

import leer_datos
import analisis_neuropatia_diabetica
import analisis_estres
import analisis_dinafamiliar
import regrelogi_diabetes_v2
import regrelogi_estres
import regrelogi_dinafami


# ── Paleta ───────────────────────────────────────────────────────────────
C_FONDO      = "#f0f4f8"
C_PANEL_IZQ  = "#dce8f5"
C_ENCABEZADO = "#00482B"
C_TEXTO_ENC  = "#ffffff"
C_VERDE      = "#2e7d32"
C_AZUL       = "#1565c0"
C_NARANJA    = "#e65100"
C_CONSOLA_BG = "#1e1e2e"
C_CONSOLA_FG = "#cdd6f4"
C_ESTADO_BG  = "#bbdefb"
C_ESTADO_FG  = "#0d47a1"

class AppRelopen(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("RELOPEN v2 — Modelo de Regresión Lógica · Pronóstico de la Vejez")
        self.geometry("1100x720")
        self.minsize(850, 550)
        self.configure(bg=C_FONDO)
        self._ocupado = False
        self._figuras_antes: set = set()
        self._canvases = []          # referencias a FigureCanvasTkAgg activos
        self._construir_ui()

    # ── UI ────────────────────────────────────────────────────────────────

    def _construir_ui(self):
        # Encabezado
        enc = tk.Frame(self, bg=C_ENCABEZADO, pady=10)
        enc.pack(fill=tk.X)
        tk.Label(enc, text="RELOPEN v2", font=("Arial", 22, "bold"),
                 fg=C_TEXTO_ENC, bg=C_ENCABEZADO).pack()
        tk.Label(enc, text="Modelo de Regresión Logística — Pronóstico de la Vejez",
                 font=("Arial", 11), fg="#bbdefb", bg=C_ENCABEZADO).pack()

        # Cuerpo: panel izquierdo + panel derecho
        cuerpo = tk.Frame(self, bg=C_FONDO)
        cuerpo.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        self._panel_izquierdo(cuerpo)
        self._panel_derecho(cuerpo)

        # Barra de estado
        self.estado_var = tk.StringVar(value="Listo  |  Seleccione una opción")
        tk.Label(self, textvariable=self.estado_var, font=("Arial", 9),
                 bg=C_ESTADO_BG, fg=C_ESTADO_FG, anchor=tk.W,
                 padx=12, pady=3).pack(fill=tk.X, side=tk.BOTTOM)

    def _panel_izquierdo(self, padre):
        panel = tk.Frame(padre, bg=C_PANEL_IZQ, width=265, padx=10, pady=10)
        panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        panel.pack_propagate(False)

        tk.Label(panel, text="Opciones", font=("Arial", 11, "bold"),
                 bg=C_PANEL_IZQ, fg=C_ENCABEZADO).pack(pady=(0, 8))

        self._seccion(panel, "DATOS")
        self._btn(panel, "1 · Cargar y Preprocesar Datos",  self.opcion_1, C_VERDE)

        self._seccion(panel, "ANÁLISIS")
        self._btn(panel, "2 · Neuropatía Diabética",        self.opcion_2, C_AZUL)
        self._btn(panel, "3 · Estrés",                      self.opcion_3, C_AZUL)
        self._btn(panel, "4 · Dinámica Familiar",           self.opcion_4, C_AZUL)

        self._seccion(panel, "REGRESIÓN LOGÍSTICA")
        self._btn(panel, "5 · Neuropatía Diabética",        self.opcion_5, C_NARANJA)
        self._btn(panel, "6 · Estrés",                      self.opcion_6, C_NARANJA)
        self._btn(panel, "7 · Dinámica Familiar",           self.opcion_7, C_NARANJA)

        ttk.Separator(panel).pack(fill=tk.X, pady=10)
        tk.Button(panel, text="Limpiar consola y gráficas",
                  command=self._limpiar_todo,
                  bg="#546e7a", fg="white", font=("Arial", 9),
                  relief=tk.FLAT, cursor="hand2", pady=5).pack(fill=tk.X)

    def _seccion(self, p, label):
        f = tk.Frame(p, bg=C_PANEL_IZQ)
        f.pack(fill=tk.X, pady=(8, 2))
        tk.Label(f, text=label, font=("Arial", 8, "bold"),
                 bg=C_PANEL_IZQ, fg="#78909c").pack(anchor=tk.W)
        ttk.Separator(f).pack(fill=tk.X)

    def _btn(self, p, texto, cmd, color):
        tk.Button(p, text=texto, command=cmd, bg=color, fg="white",
                  font=("Arial", 9, "bold"), relief=tk.FLAT, cursor="hand2",
                  wraplength=225, justify=tk.LEFT, anchor=tk.W,
                  padx=10, pady=7, activebackground=color
                  ).pack(fill=tk.X, pady=2)

    def _panel_derecho(self, padre):
        panel = tk.Frame(padre, bg=C_FONDO)
        panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # PanedWindow vertical: consola arriba, gráficas abajo
        pw = tk.PanedWindow(panel, orient=tk.VERTICAL, bg=C_FONDO,
                            sashrelief=tk.RAISED, sashwidth=5)
        pw.pack(fill=tk.BOTH, expand=True)

        # ── Consola ──────────────────────────────────────────────────────
        marco_consola = tk.Frame(pw, bg=C_FONDO)
        tk.Label(marco_consola, text="Consola / Resultados",
                 font=("Arial", 10, "bold"), bg=C_FONDO,
                 fg=C_ENCABEZADO).pack(anchor=tk.W, pady=(0, 3))
        self.consola = scrolledtext.ScrolledText(
            marco_consola, wrap=tk.WORD, font=("Consolas", 10),
            bg=C_CONSOLA_BG, fg=C_CONSOLA_FG, insertbackground="white",
            state=tk.DISABLED, padx=8, pady=6,
        )
        self.consola.pack(fill=tk.BOTH, expand=True)
        F = ("Consolas", 10)
        FB = ("Consolas", 10, "bold")
        self.consola.tag_config("titulo",    foreground="#89b4fa", font=FB)
        self.consola.tag_config("ok",        foreground="#a6e3a1", font=FB)
        self.consola.tag_config("error",     foreground="#f38ba8", font=FB)
        self.consola.tag_config("aviso",     foreground="#fab387")
        self.consola.tag_config("sep",       foreground="#45475a", font=F)
        self.consola.tag_config("seccion",   foreground="#cba6f7", font=FB)
        self.consola.tag_config("subheader", foreground="#89dceb", font=("Consolas", 10, "bold"))
        self.consola.tag_config("clave",     foreground="#89dceb", font=F)
        self.consola.tag_config("numero",    foreground="#a6e3a1", font=FB)
        self.consola.tag_config("variable",  foreground="#f9e2af", font=F)
        self.consola.tag_config("matriz",    foreground="#fab387", font=F)
        self.consola.tag_config("estado",    foreground="#6c7086", font=F)
        self.consola.tag_config("t_borde",   foreground="#45475a", font=("Consolas", 9))
        self.consola.tag_config("t_cabeza",  foreground="#cdd6f4", font=("Consolas", 9, "bold"),
                                background="#313244")
        self.consola.tag_config("t_par",     foreground="#cdd6f4", font=("Consolas", 9),
                                background="#1e1e2e")
        self.consola.tag_config("t_impar",   foreground="#a6adc8", font=("Consolas", 9),
                                background="#181825")
        self.consola.tag_config("t_nota",    foreground="#6c7086", font=("Consolas", 9))
        self.consola.tag_config("normal",    foreground="#cdd6f4", font=F)
        pw.add(marco_consola, minsize=120)

        # ── Gráficas ──────────────────────────────────────────────────────
        marco_graficas = tk.Frame(pw, bg=C_FONDO)
        tk.Label(marco_graficas, text="Gráficas",
                 font=("Arial", 10, "bold"), bg=C_FONDO,
                 fg=C_ENCABEZADO).pack(anchor=tk.W, pady=(4, 3))

        # Canvas con scroll horizontal + vertical para las figuras
        wrapper = tk.Frame(marco_graficas, bg=C_FONDO)
        wrapper.pack(fill=tk.BOTH, expand=True)

        self._scroll_canvas = tk.Canvas(wrapper, bg=C_FONDO,
                                        highlightthickness=0)
        sb_y = ttk.Scrollbar(wrapper, orient=tk.VERTICAL,
                              command=self._scroll_canvas.yview)
        sb_x = ttk.Scrollbar(wrapper, orient=tk.HORIZONTAL,
                              command=self._scroll_canvas.xview)
        self._scroll_canvas.configure(yscrollcommand=sb_y.set,
                                      xscrollcommand=sb_x.set)

        sb_y.pack(side=tk.RIGHT,  fill=tk.Y)
        sb_x.pack(side=tk.BOTTOM, fill=tk.X)
        self._scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._figuras_frame = tk.Frame(self._scroll_canvas, bg=C_FONDO)
        self._figuras_win = self._scroll_canvas.create_window(
            (0, 0), window=self._figuras_frame, anchor="nw"
        )
        self._figuras_frame.bind("<Configure>", self._actualizar_scroll)
        self._scroll_canvas.bind("<Configure>", self._ajustar_ancho_interior)

        # Scroll con rueda del ratón
        self._scroll_canvas.bind_all("<MouseWheel>",
            lambda e: self._scroll_canvas.yview_scroll(
                int(-1 * (e.delta / 120)), "units"))

        pw.add(marco_graficas, minsize=150)
        pw.paneconfig(marco_consola,   height=220)
        pw.paneconfig(marco_graficas,  height=380)

    def _actualizar_scroll(self, _event=None):
        self._scroll_canvas.configure(
            scrollregion=self._scroll_canvas.bbox("all"))

    def _ajustar_ancho_interior(self, event):
        self._scroll_canvas.itemconfig(self._figuras_win, width=event.width)

    # ── Escritura en consola ──────────────────────────────────────────────

    def _log(self, texto, tag="normal"):
        self.consola.config(state=tk.NORMAL)
        self.consola.insert(tk.END, texto, tag)
        self.consola.see(tk.END)
        self.consola.config(state=tk.DISABLED)

    def _log_titulo(self, nombre):
        self.consola.config(state=tk.NORMAL)
        self.consola.insert(tk.END, "\n", "normal")
        self.consola.insert(tk.END, f"  ▌ {nombre}\n", "titulo")
        self.consola.insert(tk.END, "  " + "─" * 50 + "\n", "sep")
        self.consola.see(tk.END)
        self.consola.config(state=tk.DISABLED)

    # ── Renderizador de tabla pandas ─────────────────────────────────────

    def _renderizar_tabla(self, header_line, data_lines, *_):
        ANCHO_MAX = 82   # ancho máximo de cada bloque (chars)
        import re

        def split_line(line):
            return [p for p in re.split(r'  +', line.strip()) if p]

        cols = split_line(header_line)
        if not cols:
            return

        # Parsear filas (descarta índice numérico inicial)
        rows = []
        for line in data_lines:
            parts = split_line(line)
            if parts and re.fullmatch(r'\d+', parts[0]):
                parts = parts[1:]
            rows.append(parts)

        # Ancho real de cada columna: lo que necesite su contenido
        widths = []
        for i, c in enumerate(cols):
            max_val = max(
                (len(str(r[i])) for r in rows if i < len(r)),
                default=0,
            )
            widths.append(max(len(c), max_val))

        # ── Dividir columnas en chunks que caben en ANCHO_MAX ────────
        chunks: list[list[int]] = []
        bloque: list[int] = []
        w_acum = 1  # borde izquierdo │
        for i, w in enumerate(widths):
            col_w = w + 3  # │ valor │
            if bloque and w_acum + col_w > ANCHO_MAX:
                chunks.append(bloque)
                bloque  = [i]
                w_acum  = 1 + col_w
            else:
                bloque.append(i)
                w_acum += col_w
        if bloque:
            chunks.append(bloque)

        # ── Funciones de dibujo ──────────────────────────────────────
        def borde(izq, mid, der, ws):
            seg = mid.join("─" * (w + 2) for w in ws)
            self._log(f"  {izq}{seg}{der}\n", "t_borde")

        def fila(celdas, tag, indices, ws):
            partes = []
            for i, w in zip(indices, ws):
                val = str(celdas[i]) if i < len(celdas) else ""
                partes.append(f" {val:<{w}} ")
            self._log("  │" + "│".join(partes) + "│\n", tag)

        # ── Renderizar cada chunk ────────────────────────────────────
        for k, indices in enumerate(chunks):
            ws = [widths[i] for i in indices]
            if len(chunks) > 1:
                rango = f"cols {indices[0]+1}–{indices[-1]+1} / {len(cols)}"
                self._log(f"  ╌╌ {rango} ╌╌\n", "t_nota")
            borde("┌", "┬", "┐", ws)
            fila(cols, "t_cabeza", indices, ws)
            borde("├", "┼", "┤", ws)
            for idx, row in enumerate(rows):
                fila(row, "t_par" if idx % 2 == 0 else "t_impar", indices, ws)
            borde("└", "┴", "┘", ws)
            if k < len(chunks) - 1:
                self._log("\n", "normal")

    # ── Formateador de salida de consola ─────────────────────────────────

    def _log_formateado(self, texto):
        import re
        lineas = texto.splitlines()

        # -- Acumulador de bloque tabla --
        tabla_header = None
        tabla_data   = []
        tabla_total  = 0

        def flush_tabla():
            nonlocal tabla_header, tabla_data, tabla_total
            if tabla_header is not None:
                self._renderizar_tabla(tabla_header, tabla_data, tabla_total)
                self._log("\n", "normal")
                tabla_header = None
                tabla_data   = []
                tabla_total  = 0

        i = 0
        while i < len(lineas):
            linea   = lineas[i]
            stripped = linea.strip()

            # ── ¿Es fila de datos de tabla? ──────────────────────────
            if re.match(r'^\s*\d+\s+\S', linea):
                if tabla_header is None:
                    # La línea anterior era el header; buscamos hacia atrás
                    # (ya la procesamos como normal, nada que hacer aquí
                    #  porque el look-ahead la captó)
                    pass
                tabla_data.append(linea)
                i += 1
                continue

            # ── ¿Es posible header de tabla? (look-ahead) ────────────
            if (stripped and
                    not re.match(r'^\s*\d+', linea) and
                    not re.fullmatch(r'[*\-\.]{8,}', stripped)):
                next_i = i + 1
                while next_i < len(lineas) and not lineas[next_i].strip():
                    next_i += 1
                if next_i < len(lineas) and re.match(r'^\s*\d+\s+\S', lineas[next_i]):
                    flush_tabla()
                    # Cuenta columnas reales en este header
                    partes = [p for p in re.split(r'  +', stripped) if p]
                    tabla_total  = len(partes)
                    tabla_header = linea
                    i += 1
                    continue

            # ── Fin de bloque tabla ───────────────────────────────────
            flush_tabla()

            # ── Separadores visuales ──────────────────────────────────
            if re.fullmatch(r'\*{8,}', stripped):
                self._log("  " + "━" * 46 + "\n", "sep")
                i += 1; continue
            if re.fullmatch(r'-{8,}', stripped):
                self._log("  " + "┄" * 46 + "\n", "sep")
                i += 1; continue
            if re.fullmatch(r'\.{8,}', stripped):
                self._log("  " + "·" * 46 + "\n", "sep")
                i += 1; continue

            # ── Línea vacía ───────────────────────────────────────────
            if not stripped:
                self._log("\n", "normal")
                i += 1; continue

            # ── Mensajes de estado internos ───────────────────────────
            if len(linea) - len(linea.lstrip()) > 12 and stripped.endswith("..."):
                self._log(f"  ⏳ {stripped.rstrip('.')}…\n", "estado")
                i += 1; continue

            # ── Marcadores internos irrelevantes ──────────────────────
            if stripped in ("Fin Crear",):
                i += 1; continue

            # ── Conteo: "Cantidad Total..  163" ──────────────────────
            m = re.match(r'^((?:Cantidad|Diferencia)\s+\w+\.+)\s+([\d-]+)$', stripped)
            if m:
                self._log(f"  {m.group(1):<26}", "clave")
                self._log(f"{m.group(2):>6}\n", "numero")
                i += 1; continue

            # ── Suma: "Suma X -> 12345" ───────────────────────────────
            m = re.match(r'^(Suma\s+.+?)\s*->\s*([\d.]+)$', stripped)
            if m:
                self._log(f"  {m.group(1)}: ", "clave")
                self._log(f"{m.group(2)}\n", "numero")
                i += 1; continue

            # ── Variable con coef/OR: "  - NOMBRE  :  0.1234" ────────
            m = re.match(r'^\s*-\s+(\w+)\s*:\s*([-\d.]+)\s*$', linea)
            if m:
                self._log(f"    • {m.group(1):<22}", "variable")
                self._log(f"{float(m.group(2)):>10.4f}\n", "numero")
                i += 1; continue

            # ── Variable sola: "  - NOMBRE" ──────────────────────────
            m = re.match(r'^\s*-\s+(\w+)\s*$', linea)
            if m:
                self._log(f"    • {m.group(1)}\n", "variable")
                i += 1; continue

            # ── Intercepto ────────────────────────────────────────────
            m = re.match(r'(Intercepto\s*\([^)]+\))\s*:\s*([-\d.]+)', stripped)
            if m:
                self._log(f"    {m.group(1)}: ", "clave")
                self._log(f"{float(m.group(2)):.4f}\n", "numero")
                i += 1; continue

            # ── Métricas numeradas: "1. AUC: 0.7234" ─────────────────
            m = re.match(r'^(\d+\.\s+.+?):\s*([\d.]+)\s*$', stripped)
            if m:
                self._log(f"\n  {m.group(1)}: ", "subheader")
                self._log(f"{m.group(2)}\n", "numero")
                i += 1; continue

            # ── Matriz de confusión ───────────────────────────────────
            if re.search(r'\bTN\b|\bFP\b|\bFN\b|\bTP\b', stripped):
                self._log(f"  {stripped}\n", "matriz")
                i += 1; continue

            # ── Títulos en MAYÚSCULAS ─────────────────────────────────
            if stripped.isupper() and len(stripped) > 4 and not re.search(r'[|\[\]{}]', stripped):
                self._log(f"\n  ◆ {stripped}\n", "seccion")
                i += 1; continue

            # ── Sub-encabezados (terminan en ":") ────────────────────
            if stripped.endswith(":") and len(stripped) < 45 and not stripped.startswith("-"):
                self._log(f"\n  {stripped}\n", "subheader")
                i += 1; continue

            # ── Aclaraciones ──────────────────────────────────────────
            if stripped.startswith("- ") and len(stripped) < 80:
                self._log(f"    {stripped}\n", "estado")
                i += 1; continue

            # ── Normal ────────────────────────────────────────────────
            self._log(f"  {linea}\n", "normal")
            i += 1

        flush_tabla()  # por si el texto termina con tabla

    def _limpiar_todo(self):
        # Consola
        self.consola.config(state=tk.NORMAL)
        self.consola.delete("1.0", tk.END)
        self.consola.config(state=tk.DISABLED)
        # Gráficas embebidas
        for w in self._figuras_frame.winfo_children():
            w.destroy()
        self._canvases.clear()
        _gcf_helpers.Gcf.figs.clear()

    # ── Ejecución en hilo ─────────────────────────────────────────────────

    def _ejecutar(self, funcion, nombre):
        if self._ocupado:
            self._log("\n[!] Espere a que termine el análisis actual.\n", "aviso")
            return

        self._ocupado = True
        # Limpia las gráficas anteriores (marco y canvas)
        for w in self._figuras_frame.winfo_children():
            w.destroy()
        self._canvases.clear()
        _gcf_helpers.Gcf.figs.clear()

        self._figuras_antes = set(plt.get_fignums())
        self.estado_var.set(f"Ejecutando: {nombre}…")
        self._log_titulo(nombre)

        # Intercepta plt.show para que no intente abrir ventanas
        _show_original = plt.show
        def _noop(*_): pass
        plt.show = _noop

        def hilo():
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    funcion()
                salida = buf.getvalue()
                if salida:
                    self.after(0, self._log_formateado, salida)
                self.after(0, self._finalizar_ok, nombre, _show_original)
            except Exception as exc:
                salida = buf.getvalue()
                if salida:
                    self.after(0, self._log_formateado, salida)
                self.after(0, self._finalizar_error, str(exc), _show_original)

        threading.Thread(target=hilo, daemon=True).start()

    def _finalizar_ok(self, nombre, show_orig):
        plt.show = show_orig
        self._ocupado = False
        self.estado_var.set(f"✓ Completado: {nombre}")
        self._log(f"\n✓ Análisis completado.\n", "ok")
        self._incrustar_figuras()

    def _finalizar_error(self, mensaje, show_orig):
        plt.show = show_orig
        self._ocupado = False
        self.estado_var.set("Error durante la ejecución")
        self._log(f"\n[ERROR] {mensaje}\n", "error")

    def _incrustar_figuras(self):
        nuevas = set(plt.get_fignums()) - self._figuras_antes
        if not nuevas:
            self._log("(Sin gráficas generadas)\n", "aviso")
            return

        self._log(f"[Gráficas] Mostrando {len(nuevas)} figura(s) a continuación.\n", "ok")

        for num in sorted(nuevas):
            fig = plt.figure(num)
            # Marco contenedor para cada figura
            marco = tk.Frame(self._figuras_frame, bg="#e8edf5",
                             relief=tk.GROOVE, bd=1)
            marco.pack(fill=tk.X, padx=6, pady=6)

            canvas = FigureCanvasTkAgg(fig, master=marco)
            canvas.draw()
            widget = canvas.get_tk_widget()
            widget.pack(fill=tk.BOTH, expand=True)
            self._canvases.append(canvas)

        # Desplaza hacia las gráficas
        self.after(100, lambda: self._scroll_canvas.yview_moveto(0))

    # ── Opciones ──────────────────────────────────────────────────────────

    def opcion_1(self):
        def func():
            df = leer_datos.leer_csv()
            df_trabajo = leer_datos.crear_df_trabajo(df)
            # df = leer_datos.leer_csv(RUTA_PROYECTO)
            print(f"Datos cargados correctamente.")
            print(f"Filas: {len(df):,}   Columnas: {len(df.columns)}")
            print()
            print(df.head(5).to_string())
        self._ejecutar(func, "1 · Cargar y Preprocesar Datos")

    def opcion_2(self):
        def func():
            df_largo = analisis_neuropatia_diabetica.crea_df_neuropatia()
            analisis_neuropatia_diabetica.graf_boxplot_neuropatia(df_largo)
        self._ejecutar(func, "2 · Análisis Neuropatía Diabética")

    def opcion_3(self):
        def func():
            df_largo = analisis_estres.crea_df()
            analisis_estres.graf_boxplot(df_largo)
        self._ejecutar(func, "3 · Análisis Estrés")

    def opcion_4(self):
        def func():
            df_largo = analisis_dinafamiliar.crea_df()
            analisis_dinafamiliar.graf_boxplot(df_largo)
        self._ejecutar(func, "4 · Análisis Dinámica Familiar")

    def opcion_5(self):
        def func():
            regrelogi_diabetes_v2.calculo_regrelogis_diabetes()
            regrelogi_diabetes_v2.grafica_regrelogis_diabetes()
        self._ejecutar(func, "5 · Regresión Logística Neuropatía Diabética")

    def opcion_6(self):
        def func():
            regrelogi_estres.calculo_regrelogis_estres()
            regrelogi_estres.grafica_regrelogis_estres()
        self._ejecutar(func, "6 · Regresión Logística Estrés")

    def opcion_7(self):
        def func():
            regrelogi_dinafami.calculo_regrelogis_dinafamiliar()
            regrelogi_dinafami.grafica_regrelogis_dinafamiliar()
        self._ejecutar(func, "7 · Regresión Logística Dinámica Familiar")


if __name__ == "__main__":
    app = AppRelopen()
    app.mainloop()
