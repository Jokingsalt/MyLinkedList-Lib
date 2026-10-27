# main.py
import tkinter as tk
from tkinter import messagebox

# IMPORTAMOS NUESTRA PROPIA BIBLIOTECA
from MyLinkedList import ListaEnlazada


class AppListaEnlazada:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor Completo de Lista Simplemente Ligada")
        self.root.geometry("680x540")
        self.root.resizable(False, False)
        
        # Instanciamos la clase que viene de nuestra biblioteca MyLinkedList
        self.lista = ListaEnlazada()
        self.posiciones_resaltadas = []

        # Frame de Entrada
        frame_input = tk.Frame(root, padx=10, pady=10)
        frame_input.pack()

        tk.Label(frame_input, text="Valor (INFO):", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_valor = tk.Entry(frame_input, font=("Arial", 10))
        self.entry_valor.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Posición (Índice 0, 1...):", font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_pos = tk.Entry(frame_input, font=("Arial", 10))
        self.entry_pos.grid(row=1, column=1, padx=5, pady=5)

        # Frame de Botones
        frame_botones = tk.Frame(root, pady=5)
        frame_botones.pack()

        btn_inicio = tk.Button(frame_botones, text="Insertar Inicio", bg="#4CAF50", fg="white", font=("Arial", 9, "bold"), command=self.agregar_inicio)
        btn_inicio.grid(row=0, column=0, padx=4, pady=3)

        btn_final = tk.Button(frame_botones, text="Insertar Final", bg="#2196F3", fg="white", font=("Arial", 9, "bold"), command=self.agregar_final)
        btn_final.grid(row=0, column=1, padx=4, pady=3)

        btn_pos = tk.Button(frame_botones, text="Insertar Posición", bg="#FF9800", fg="white", font=("Arial", 9, "bold"), command=self.agregar_posicion)
        btn_pos.grid(row=0, column=2, padx=4, pady=3)

        btn_sobrescribir = tk.Button(frame_botones, text="Sobrescribir Pos", bg="#009688", fg="white", font=("Arial", 9, "bold"), command=self.sobrescribir_posicion)
        btn_sobrescribir.grid(row=0, column=3, padx=4, pady=3)

        btn_buscar = tk.Button(frame_botones, text="Buscar Valor", bg="#9C27B0", fg="white", font=("Arial", 9, "bold"), command=self.buscar)
        btn_buscar.grid(row=1, column=0, padx=4, pady=3)

        btn_del_pos = tk.Button(frame_botones, text="Eliminar por Posición", bg="#F44336", fg="white", font=("Arial", 9, "bold"), command=self.eliminar_posicion)
        btn_del_pos.grid(row=1, column=1, padx=4, pady=3)

        btn_del_val = tk.Button(frame_botones, text="Eliminar por Valor", bg="#E91E63", fg="white", font=("Arial", 9, "bold"), command=self.eliminar_valor)
        btn_del_val.grid(row=1, column=2, padx=4, pady=3)

        btn_limpiar = tk.Button(frame_botones, text="Limpiar Resaltado", bg="#795548", fg="white", font=("Arial", 9, "bold"), command=self.limpiar_resaltado)
        btn_limpiar.grid(row=1, column=3, padx=4, pady=3)

        # Área de Visualización
        tk.Label(root, text="Representación Gráfica:", font=("Arial", 11, "bold")).pack(pady=(10, 5))
        
        frame_canvas = tk.Frame(root)
        frame_canvas.pack(padx=10, pady=5, fill="x")

        self.canvas = tk.Canvas(frame_canvas, bg="#F0F0F0", width=640, height=200, relief="sunken", bd=2)
        scrollbar = tk.Scrollbar(frame_canvas, orient="horizontal", command=self.canvas.xview)
        
        self.canvas.configure(xscrollcommand=scrollbar.set)
        self.canvas.pack(fill="x", expand=True)
        scrollbar.pack(fill="x")

        self.actualizar_vista()

    def obtener_valor(self):
        val = self.entry_valor.get().strip()
        if not val:
            messagebox.showwarning("Advertencia", "Por favor ingresa un valor en el campo INFO.")
            return None
        return val

    def obtener_posicion(self):
        pos_str = self.entry_pos.get().strip()
        if not pos_str.isdigit():
            messagebox.showwarning("Advertencia", "Ingresa una posición numérica entera (>= 0).")
            return None
        return int(pos_str)

    def agregar_inicio(self):
        val = self.obtener_valor()
        if val:
            self.lista.insertar_inicio(val)
            self.entry_valor.delete(0, tk.END)
            self.limpiar_resaltado()

    def agregar_final(self):
        val = self.obtener_valor()
        if val:
            self.lista.insertar_final(val)
            self.entry_valor.delete(0, tk.END)
            self.limpiar_resaltado()

    def agregar_posicion(self):
        val = self.obtener_valor()
        pos = self.obtener_posicion()
        if val is not None and pos is not None:
            n = self.lista.longitud()
            if pos < n:
                nodo_actual = self.lista.obtener_nodo(pos)
                if nodo_actual and nodo_actual.info is not None:
                    resp = messagebox.askyesno("Confirmación", f"La posición {pos} ya contiene '{nodo_actual.info}'.\n¿Deseas sobrescribir el valor en lugar de desplazar?")
                    if resp:
                        self.lista.sobrescribir_posicion(val, pos)
                        self.limpiar_campos()
                        self.limpiar_resaltado()
                        return

            self.lista.insertar_posicion(val, pos)
            self.limpiar_campos()
            self.limpiar_resaltado()

    def sobrescribir_posicion(self):
        val = self.obtener_valor()
        pos = self.obtener_posicion()
        if val is not None and pos is not None:
            if pos >= self.lista.longitud():
                messagebox.showerror("Error", f"La posición {pos} no existe en la lista.")
                return
            ant = self.lista.sobrescribir_posicion(val, pos)
            messagebox.showinfo("Éxito", f"Se reemplazó '{ant}' por '{val}' en la posición {pos}.")
            self.limpiar_campos()
            self.limpiar_resaltado()

    def eliminar_posicion(self):
        pos = self.obtener_posicion()
        if pos is not None:
            eliminado = self.lista.eliminar_posicion(pos)
            if eliminado is not None:
                messagebox.showinfo("Éxito", f"Se eliminó '{eliminado}' de la posición {pos}.")
                self.entry_pos.delete(0, tk.END)
                self.limpiar_resaltado()
            else:
                messagebox.showerror("Error", f"La posición {pos} está fuera de rango.")

    def eliminar_valor(self):
        val = self.obtener_valor()
        if val:
            encontrado = self.lista.eliminar_valor(val)
            if encontrado:
                messagebox.showinfo("Éxito", f"Se eliminó la primera aparición de '{val}'.")
                self.entry_valor.delete(0, tk.END)
                self.limpiar_resaltado()
            else:
                messagebox.showinfo("Resultado", f"'{val}' no fue encontrado en la lista.")

    def buscar(self):
        val = self.obtener_valor()
        if val:
            posiciones = self.lista.buscar_valor(val)
            if posiciones:
                self.posiciones_resaltadas = posiciones
                pos_txt = ", ".join(str(p) for p in posiciones)
                messagebox.showinfo("Encontrado", f"'{val}' se encuentra en la(s) posición(es): {pos_txt}")
                self.actualizar_vista()
            else:
                self.posiciones_resaltadas = []
                messagebox.showinfo("Resultado", f"'{val}' no está en la lista.")
                self.actualizar_vista()

    def limpiar_campos(self):
        self.entry_valor.delete(0, tk.END)
        self.entry_pos.delete(0, tk.END)

    def limpiar_resaltado(self):
        self.posiciones_resaltadas = []
        self.actualizar_vista()

    def actualizar_vista(self):
        self.canvas.delete("all")
        elementos = self.lista.obtener_elementos()
        
        if not elementos:
            self.canvas.create_text(320, 100, text="P -> NIL (Lista Vacía)", font=("Arial", 12, "italic"), fill="gray")
            self.canvas.config(scrollregion=(0, 0, 640, 200))
            return

        x, y = 40, 80
        ancho_nodo, alto_nodo = 75, 40

        self.canvas.create_text(x, y - 25, text="P", font=("Arial", 11, "bold"), fill="red")
        self.canvas.create_line(x, y - 15, x, y - 2, arrow=tk.LAST, fill="red", width=2)

        for i, val in enumerate(elementos):
            if i in self.posiciones_resaltadas:
                color_fondo = "#FFF59D"
            elif val == "None":
                color_fondo = "#FFCDD2"
            else:
                color_fondo = "#E0F7FA"

            self.canvas.create_rectangle(x, y, x + ancho_nodo, y + alto_nodo, fill=color_fondo, outline="black", width=2)
            self.canvas.create_line(x + 50, y, x + 50, y + alto_nodo, fill="black", width=1)
            
            self.canvas.create_text(x + 25, y - 10, text=f"[{i}]", font=("Arial", 8, "bold"), fill="#555")
            self.canvas.create_text(x + 25, y + 20, text=val, font=("Arial", 9, "bold"))

            if i < len(elementos) - 1:
                self.canvas.create_line(x + 62, y + 20, x + ancho_nodo + 30, y + 20, arrow=tk.LAST, fill="blue", width=2)
                x += ancho_nodo + 30
            else:
                self.canvas.create_line(x + 62, y + 20, x + ancho_nodo + 15, y + 20, arrow=tk.LAST, fill="blue", width=2)
                self.canvas.create_text(x + ancho_nodo + 35, y + 20, text="NIL", font=("Arial", 10, "bold"), fill="gray")
                x += ancho_nodo + 60

        self.canvas.config(scrollregion=(0, 0, max(640, x + 20), 200))


if __name__ == "__main__":
    root = tk.Tk()
    app = AppListaEnlazada(root)
    root.mainloop()