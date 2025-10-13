class Producto:
    """Representa un producto con nombre y precio."""

    def __init__(self, nombre: str, precio: float):
        """
        Inicializa un producto.

        Args:
            nombre (str): Nombre del producto.
            precio (float): Precio del producto. Debe ser positivo.

        Raises:
            ValueError: Si el precio es menor o igual a cero.
        """
        if precio <= 0:
            raise ValueError("El precio debe ser positivo")
        self.nombre = nombre
        self.precio = precio
