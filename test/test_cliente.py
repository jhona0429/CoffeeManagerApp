from app.cliente import Cliente

def test_crear_cliente():
    c = Cliente("Joan Pérez")
    assert c.nombre == "Joan Pérez"
