# MyLinkedList.py

class Nodo:
    def __init__(self, info):
        self.info = info  # INFO: Dato guardado en el nodo
        self.liga = None  # LIGA: Puntero al siguiente nodo (NIL)


class ListaEnlazada:
    def __init__(self):
        self.inicio = None  # Apuntador P al inicio de la lista

    def longitud(self):
        cant = 0
        actual = self.inicio
        while actual:
            cant += 1
            actual = actual.liga
        return cant

    def obtener_nodo(self, pos):
        actual = self.inicio
        for _ in range(pos):
            if actual is None:
                return None
            actual = actual.liga
        return actual

    def insertar_inicio(self, valor):
        nuevo_nodo = Nodo(valor)
        nuevo_nodo.liga = self.inicio
        self.inicio = nuevo_nodo

    def insertar_final(self, valor):
        nuevo_nodo = Nodo(valor)
        if not self.inicio:
            self.inicio = nuevo_nodo
            return
        
        actual = self.inicio
        while actual.liga:
            actual = actual.liga
        actual.liga = nuevo_nodo

    def insertar_posicion(self, valor, pos):
        if pos <= 0:
            self.insertar_inicio(valor)
            return

        tamanio_actual = self.longitud()

        if pos > tamanio_actual:
            faltantes = pos - tamanio_actual
            for _ in range(faltantes):
                self.insertar_final(None)
            self.insertar_final(valor)
            return

        nuevo_nodo = Nodo(valor)
        actual = self.inicio
        for _ in range(pos - 1):
            actual = actual.liga
            
        nuevo_nodo.liga = actual.liga
        actual.liga = nuevo_nodo

    def sobrescribir_posicion(self, valor, pos):
        nodo = self.obtener_nodo(pos)
        if nodo:
            anterior = nodo.info
            nodo.info = valor
            return anterior
        return None

    def eliminar_posicion(self, pos):
        if not self.inicio or pos < 0 or pos >= self.longitud():
            return None

        if pos == 0:
            eliminado = self.inicio.info
            self.inicio = self.inicio.liga
            return eliminado

        anterior = self.obtener_nodo(pos - 1)
        actual = anterior.liga
        eliminado = actual.info
        anterior.liga = actual.liga
        return eliminado

    def eliminar_valor(self, valor):
        q = self.inicio
        t = None
        
        while q is not None:
            val_q = "" if q.info is None else str(q.info).strip().lower()
            val_target = str(valor).strip().lower()
            if val_q == val_target:
                break
            t = q
            q = q.liga

        if q is None:
            return False  # No encontrado

        if t is None:
            self.inicio = q.liga
        else:
            t.liga = q.liga
        return True

    def buscar_valor(self, valor):
        posiciones = []
        actual = self.inicio
        pos = 0
        target = str(valor).strip().lower()
        while actual:
            val_actual = "" if actual.info is None else str(actual.info).strip().lower()
            if val_actual == target:
                posiciones.append(pos)
            actual = actual.liga
            pos += 1
        return posiciones

    def obtener_elementos(self):
        elementos = []
        actual = self.inicio
        while actual:
            val_txt = "None" if actual.info is None else str(actual.info)
            elementos.append(val_txt)
            actual = actual.liga
        return elementos