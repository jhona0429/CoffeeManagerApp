from app.pedido import Pedido
from app.producto import Producto

def test_agregar_productos_a_pedido():
    pedido = Pedido("Ana Gomes")
    p1 = Producto("Jugo", 8.0)
    p2 = Producto("Tostada", 5.0)
    pedido.agregar_producto(p1)
    pedido.agregar_producto(p2)
    assert len(pedido.productos) == 2
