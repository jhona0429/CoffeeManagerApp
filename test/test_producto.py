import pytest
from app.producto import Producto

def test_crear_producto_valido():
    p = Producto("Café", 10.5)
    assert p.nombre == "Café"
    assert p.precio == 10.5

def test_precio_invalido():
    with pytest.raises(ValueError):
        Producto("Café", -2)
