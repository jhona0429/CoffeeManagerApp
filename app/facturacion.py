def calcular_factura(subtotal: float, iva_rate: float = 0.13) -> dict:
    iva = subtotal * iva_rate
    total = subtotal + iva
    return {"subtotal": subtotal, "iva": iva, "total": total}
