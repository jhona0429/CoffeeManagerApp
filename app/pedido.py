from app.producto import Producto

class Pedido:
    def __init__(self, cliente: str):
        self.cliente = cliente
        self.productos: list[Producto] = []

    def agregar_producto(self, producto: Producto):
        self.productos.append(producto)

    def calcular_total(self) -> float:
        return sum(p.precio for p in self.productos)
