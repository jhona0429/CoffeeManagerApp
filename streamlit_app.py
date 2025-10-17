import streamlit as st
from app.cliente import Cliente
from app.producto import Producto
from app.pedido import Pedido
from app.facturacion import calcular_factura
import base64
from app.db import insertar_cliente, insertar_producto, crear_pedido, obtener_clientes, obtener_productos

# --- Fondo con imagen ---
def set_background(image_file: str):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
    }}
    th, td {{
        border: 1px solid #ffbe5f;
        padding: 8px;
        text-align: left;
        color: white;
    }}
    th {{
        background-color: #a05638;
    }}
    tr:nth-child(even) {{
        background-color: rgba(255, 255, 255, 0.05);
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("fondocoffe6.jpg")

# --- Inicialización de estado ---
if "clientes" not in st.session_state:
    st.session_state.clientes = obtener_clientes()

if "productos" not in st.session_state:
    st.session_state.productos = obtener_productos()

if "vista" not in st.session_state:
    st.session_state.vista = "principal"

if "pedidos" not in st.session_state:
    from app.db import obtener_pedidos
    st.session_state.pedidos = obtener_pedidos()


# --- Estilos personalizados ---
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #23140b !important;
    }
    .stApp {
        background-color: transparent;
    }
    html, body, [class*="css"] {
        color: white !important;
    }
    .titulo {
        position: relative;
        top: -35px;
        left: -250px;
        color: white;
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .seccion {
        background-color: rgba(0, 0, 0, 0.85);
        padding: 10px;
        border-radius: 8px;
        color: white;
        font-size: 22px;
        margin-top: 20px;
    }
    .texto {
        color: white;
        font-size: 18px;
    }
    .tarjeta {
        background-color: rgba(0, 0, 0, 0.85);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-top: 20px;
        border: 1px solid #ffbe5f;
    }
    .alerta-verde {
        background-color: #4CAF50;
        padding: 10px;
        border-radius: 8px;
        color: white;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }
    button {
        background-color: #a05638 !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
    }
    input, textarea, select {
        background-color: #000000 !important;
        color: white !important;
        border: 1px solid #db824a !important;
    }
    .stMultiSelect, .stSelectbox {
        background-color: #000000 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar: Navegación ---
st.sidebar.header("📋 Menú")

if st.sidebar.button("🧾 Realizar Pedido"):
    st.session_state.vista = "principal"
    st.session_state.factura = None
    st.session_state.productos_pedido = []

if st.sidebar.button("👥 Listar Clientes"):
    st.session_state.vista = "listar_clientes"

if st.sidebar.button("📦 Listar Productos"):
    st.session_state.vista = "listar_productos"

if st.sidebar.button("➕ Registrar Cliente"):
    st.session_state.vista = "registrar_cliente"

if st.sidebar.button("➕ Registrar Producto"):
    st.session_state.vista = "registrar_producto"

if st.sidebar.button("📋 Listar Pedidos"):
    st.session_state.vista = "listar_pedidos"

# --- Vistas dinámicas ---
if st.session_state.vista == "listar_clientes":
    st.markdown("<div class='titulo'>👥 Clientes Registrados</div>", unsafe_allow_html=True)
    tabla = "<table><tr><th>#</th><th>Nombre</th></tr>"
    for i, c in enumerate(st.session_state.clientes, 1):
        tabla += f"<tr><td>{i}</td><td>{c}</td></tr>"
    tabla += "</table>"
    st.markdown(tabla, unsafe_allow_html=True)
    if st.button("🔙 Volver"):
        st.session_state.vista = "principal"

elif st.session_state.vista == "listar_productos":
    st.markdown("<div class='titulo'>📦 Productos Registrados</div>", unsafe_allow_html=True)
    tabla = "<table><tr><th>Producto</th><th>Precio (Bs)</th></tr>"
    for nombre, precio in st.session_state.productos.items():
        tabla += f"<tr><td>{nombre}</td><td>{precio:.2f}</td></tr>"
    tabla += "</table>"
    st.markdown(tabla, unsafe_allow_html=True)
    if st.button("🔙 Volver"):
        st.session_state.vista = "principal"

elif st.session_state.vista == "registrar_cliente":
    st.markdown("<div class='titulo'>➕ Registrar Cliente</div>", unsafe_allow_html=True)
    nuevo_cliente = st.text_input("Nombre del nuevo cliente")
    if st.button("Agregar cliente"):
        if nuevo_cliente and nuevo_cliente not in st.session_state.clientes:
            st.session_state.clientes.append(nuevo_cliente)
            insertar_cliente(nuevo_cliente)
            st.markdown("<div class='alerta-verde'>✅ Cliente agregado correctamente</div>", unsafe_allow_html=True)
        else:
            st.warning("Nombre inválido o ya registrado.")
    if st.button("🔙 Volver"):
        st.session_state.vista = "principal"

elif st.session_state.vista == "registrar_producto":
    st.markdown("<div class='titulo'>➕ Registrar Producto</div>", unsafe_allow_html=True)
    nombre_producto = st.text_input("Nombre del producto")
    precio_producto = st.number_input("Precio del producto", min_value=0.01, step=0.01)
    if st.button("Agregar producto"):
        if nombre_producto and precio_producto > 0:
            st.session_state.productos[nombre_producto] = precio_producto
            insertar_producto(nombre_producto, precio_producto)
            st.markdown("<div class='alerta-verde'>✅ Producto agregado correctamente</div>", unsafe_allow_html=True)
        else:
            st.warning("Completa ambos campos correctamente.")
    if st.button("🔙 Volver"):
        st.session_state.vista = "principal"

elif st.session_state.vista == "listar_pedidos":
    st.markdown("<div class='titulo'>📋 Pedidos Realizados</div>", unsafe_allow_html=True)
    if not st.session_state.pedidos:
        st.markdown("<div class='texto'>No hay pedidos registrados aún.</div>", unsafe_allow_html=True)
    else:
        for i, registro in enumerate(st.session_state.pedidos, 1):
            pedido = registro["pedido"]
            factura = registro["factura"]
            tabla = f"""
            <div class='tarjeta'>
                <div class='texto'><strong>🧑‍💼 Pedido #{i}</strong></div>
                <div class='texto'><strong>Cliente:</strong> {pedido.cliente}</div>
                <table>
                    <tr><th>Producto</th><th>Precio (Bs)</th></tr>
            """
            for producto in pedido.productos:
                tabla += f"<tr><td>{producto.nombre}</td><td>{producto.precio:.2f}</td></tr>"
            tabla += f"""
                </table>
                <div class='texto'><strong>Subtotal:</strong> {factura['subtotal']:.2f} Bs</div>
                <div class='texto'><strong>IVA:</strong> {factura['iva']:.2f} Bs</div>
                <div class='texto'><strong>Total:</strong> {factura['total']:.2f} Bs</div>
            </div>
            """
        st.markdown(tabla, unsafe_allow_html=True)

    if st.button("🔙 Volver"):
        st.session_state.vista = "principal"

elif st.session_state.vista == "principal":
    st.markdown("<div class='titulo'>☕ CoffeeManager</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.markdown("<div class='seccion'>🧑‍💼 Selección de Cliente</div>", unsafe_allow_html=True)
        cliente_seleccionado = st.selectbox(
            "Selecciona un cliente:",
            options=[""] + st.session_state.clientes,
            index=0,
            placeholder="Ingresa el nombre del cliente"
        )

        st.markdown("<div class='seccion'>🛒 Selección de Productos</div>", unsafe_allow_html=True)
        productos_seleccionados = st.multiselect(
            "Productos:",
            options=list(st.session_state.productos.keys()),
            placeholder="Selecciona productos para el pedido"
        )

        if st.button("💰 Realizar Pedido"):
            if cliente_seleccionado and productos_seleccionados:
                pedido = Pedido(cliente_seleccionado)
                for nombre in productos_seleccionados:
                    producto = Producto(nombre, st.session_state.productos[nombre])
                    pedido.agregar_producto(producto)

                subtotal = float(pedido.calcular_total())
                factura = calcular_factura(subtotal)


                st.session_state.factura = factura
                st.session_state.productos_pedido = productos_seleccionados

                crear_pedido(cliente_seleccionado, [(p.nombre, p.precio) for p in pedido.productos])

                st.session_state.pedidos.append({
                    "cliente": cliente_seleccionado,
                    "pedido": pedido,
                    "factura": factura
                })

                st.markdown(
                    """
                    <div style='background-color:#4CAF50; padding:10px; border-radius:8px;
                    color:white; font-weight:bold; text-align:center; margin-top:20px;'>
                        ✅ Pedido realizado correctamente
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.warning("Selecciona un cliente y al menos un producto.")

    with col2:
        if "factura" in st.session_state and st.session_state.factura is not None:
            factura = st.session_state.factura
            resumen_html = "<div class='tarjeta'>"
            resumen_html += "<div class='texto'><strong>🧾 Resumen del Pedido</strong></div>"

            for nombre in st.session_state.productos_pedido:
                precio = st.session_state.productos[nombre]
                resumen_html += f"<div class='texto'>• {nombre}: {precio:.2f} Bs</div>"

            resumen_html += (
                f"<div class='texto'><strong>Subtotal:</strong> {factura['subtotal']:.2f} Bs</div>"
            )
            resumen_html += (
                f"<div class='texto'><strong>IVA (13%):</strong> {factura['iva']:.2f} Bs</div>"
            )
            resumen_html += (
                f"<div class='texto'><strong>Total:</strong> {factura['total']:.2f} Bs</div>"
            )
            resumen_html += "</div>"

            st.markdown(resumen_html, unsafe_allow_html=True)
        else:
            st.markdown(
                """
                <div class='tarjeta'>
                    <div class='texto'><strong>🧾 Resumen del Pedido</strong></div>
                    <div class='texto'>Calcula el total para ver el resumen.</div>
                </div>
                """,
                unsafe_allow_html=True
            )
