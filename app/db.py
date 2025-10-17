import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="mysql-jhonatan.alwaysdata.net",
        user="jhonatan_admin",  # cambia si usas otro usuario
        password="Mynameisjhonax",
        database="jhonatan_cofee"
    )

def insertar_cliente(nombre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO clientes (nombre) VALUES (%s)", (nombre,))
    conn.commit()
    cursor.close()
    conn.close()

def insertar_producto(nombre, precio):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO productos (nombre, precio) VALUES (%s, %s)", (nombre, precio))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_cliente_id(nombre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM clientes WHERE nombre = %s", (nombre,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def obtener_producto_id(nombre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM productos WHERE nombre = %s", (nombre,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def crear_pedido(cliente_nombre, productos):
    cliente_id = obtener_cliente_id(cliente_nombre)
    if cliente_id is None:
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pedidos (cliente_id) VALUES (%s)", (cliente_id,))
    pedido_id = cursor.lastrowid

    for nombre, precio in productos:
        producto_id = obtener_producto_id(nombre)
        if producto_id:
            cursor.execute(
                "INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, subtotal) VALUES (%s, %s, %s, %s)",
                (pedido_id, producto_id, 1, precio)
            )

    conn.commit()
    cursor.close()
    conn.close()
