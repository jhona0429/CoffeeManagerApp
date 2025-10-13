from app.facturacion import calcular_factura

def test_calculo_factura():
    factura = calcular_factura(100.0)
    assert round(factura["subtotal"], 2) == 100.0
    assert round(factura["iva"], 2) == 13.0
    assert round(factura["total"], 2) == 113.0
