import mysql.connector
from app.producto import Producto
from app.pedido import Pedido
from app.facturacion import calcular_factura

def get_connection():
    return mysql.connector.connect(
        host="mysql-jhonatan.alwaysdata.net",
        user="jhonatan_admin",
        password="Mynameisjhonax",
        database="jhonatan_coffe"
    )

# --- Clientes ---
def insertar_cliente(nombre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO clientes (nombre) VALUES (%s)", (nombre,))
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

def obtener_clientes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM clientes")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return [r[0] for r in resultados]

# --- Productos ---
def insertar_producto(nombre, precio):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO productos (nombre, precio) VALUES (%s, %s)", (nombre, precio))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_producto_id(nombre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM productos WHERE nombre = %s", (nombre,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def obtener_productos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, precio FROM productos")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return {nombre: precio for nombre, precio in resultados}

# --- Pedidos ---
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

def obtener_pedidos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, c.nombre, pr.nombre, pr.precio
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        JOIN detalle_pedido dp ON dp.pedido_id = p.id
        JOIN productos pr ON dp.producto_id = pr.id
        ORDER BY p.id ASC
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    pedidos_dict = {}
    for pedido_id, cliente, producto, precio in resultados:
        if pedido_id not in pedidos_dict:
            pedidos_dict[pedido_id] = {
                "cliente": cliente,
                "productos": []
            }
        pedidos_dict[pedido_id]["productos"].append(Producto(producto, precio))

    pedidos = []
    for datos in pedidos_dict.values():
        pedido = Pedido(datos["cliente"])
        for p in datos["productos"]:
            pedido.agregar_producto(p)
        subtotal = float(pedido.calcular_total())
        factura = calcular_factura(subtotal)
        pedidos.append({
            "cliente": datos["cliente"],
            "pedido": pedido,
            "factura": factura
        })

    return pedidos
