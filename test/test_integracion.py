from app.pedido import Pedido
from app.producto import Producto
from app.facturacion import calcular_factura

def test_flujo_completo():
    pedido = Pedido("Carlos Rojas")
    pedido.agregar_producto(Producto("Café", 10))
    pedido.agregar_producto(Producto("Tostada", 5))
    subtotal = pedido.calcular_total()
    factura = calcular_factura(subtotal)
    assert round(factura["total"], 2) == 16.95
