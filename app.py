"""
Aplicación Streamlit para consultar precios de productos por código QR
"""

import streamlit as st
import time
from odoo_client import OdooClient, AppConfig
from barcode_scanner import BarcodeScanner


def main():
    """Función principal de la aplicación"""
    
    # Configurar página
    st.set_page_config(
        page_title="Puya Price Scanner",
        page_icon="📱",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # CSS personalizado
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 3rem;
        margin-bottom: 2rem;
    }
    .scan-button {
        text-align: center;
        margin: 2rem 0;
    }
    .product-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .price {
        font-size: 2.5rem;
        color: #28a745;
        font-weight: bold;
        text-align: center;
    }
    .stock {
        font-size: 2rem;
        color: #007bff;
        font-weight: bold;
        text-align: center;
    }
    .product-name {
        font-size: 1.5rem;
        color: #333;
        text-align: center;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Título principal
    st.markdown('<h1 class="main-header">📱 Puya Price Scanner</h1>', unsafe_allow_html=True)
    
    # Verificar credenciales de Odoo
    if not AppConfig.validate_odoo_credentials():
        st.error("❌ Configuración incompleta de Odoo. Verifica las credenciales en Streamlit Cloud.")
        st.stop()
    
    # Inicializar variables de sesión
    if 'scanner' not in st.session_state:
        st.session_state.scanner = BarcodeScanner()
    if 'scanning' not in st.session_state:
        st.session_state.scanning = False
    if 'product_info' not in st.session_state:
        st.session_state.product_info = None
    if 'last_barcode' not in st.session_state:
        st.session_state.last_barcode = None
    
    # Landing page
    if not st.session_state.scanning:
        show_landing_page()
    else:
        show_scanner_page()


def show_landing_page():
    """Muestra la página de inicio"""
    
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h2>🔍 Consulta precios de productos por código QR</h2>
        <p style="font-size: 1.2rem; color: #666;">
            Escanea cualquier código QR para obtener información del producto:
        </p>
        <ul style="text-align: left; display: inline-block; font-size: 1.1rem;">
            <li>💰 Precio de venta</li>
            <li>📦 Stock disponible</li>
            <li>📝 Nombre del producto</li>
        </ul>
        
        <div style="margin: 2rem 0; padding: 1rem; background-color: #f8f9fa; border-radius: 10px;">
            <h3>💡 Optimizado para códigos QR:</h3>
            <p><strong>📱 Códigos QR:</strong> Más fáciles de escanear con móviles</p>
            <p><strong>⚡ Escaneo automático:</strong> Sin necesidad de entrada manual</p>
            <p><strong>🔍 Detección inteligente:</strong> Funciona desde cualquier ángulo</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón central para iniciar escaneo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 INICIAR ESCANEO", type="primary", use_container_width=True):
            st.session_state.scanning = True
            st.rerun()
    
    # Mostrar información del último producto consultado
    if st.session_state.product_info:
        st.markdown("---")
        st.markdown("### 📋 Último producto consultado:")
        show_product_info(st.session_state.product_info)


def show_scanner_page():
    """Muestra la página del escáner"""
    
    st.markdown("""
    <div style="text-align: center; margin: 1rem 0;">
        <h2>📱 Escáner Automático de Códigos QR</h2>
        <p>Escanea automáticamente el código QR del producto</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón para volver
    if st.button("← Volver al inicio"):
        st.session_state.scanning = False
        st.session_state.scanner.reset_scanner()
        st.rerun()
    
    # Obtener código QR con escaneo automático
    barcode = st.session_state.scanner.scan_with_fallback()
    
    if barcode:
        # Verificar que no sea el mismo código
        if barcode != st.session_state.last_barcode:
            st.session_state.last_barcode = barcode
            
            # Consultar producto en Odoo
            with st.spinner("🔍 Consultando información del producto..."):
                product_info = get_product_info(barcode)
            
            if product_info:
                st.session_state.product_info = product_info
                show_product_info(product_info)
                
                # Botón para escanear otro producto
                if st.button("🔍 Escanear otro producto"):
                    st.session_state.last_barcode = None
                    st.session_state.scanner.reset_scanner()
                    st.rerun()
            else:
                st.error("❌ Producto no encontrado en la base de datos")
                
                # Botón para intentar de nuevo
                if st.button("🔄 Intentar con otro código"):
                    st.session_state.last_barcode = None
                    st.session_state.scanner.reset_scanner()
                    st.rerun()


def get_product_info(barcode: str):
    """Obtiene información del producto desde Odoo"""
    
    try:
        # Obtener credenciales
        credentials = AppConfig.get_odoo_credentials()
        
        # Crear cliente de Odoo
        client = OdooClient(
            url=credentials['url'],
            db=credentials['db'],
            username=credentials['username'],
            password=credentials['password']
        )
        
        # Consultar producto
        return client.get_product_by_barcode(barcode)
        
    except Exception as e:
        st.error(f"Error al consultar producto: {str(e)}")
        return None


def show_product_info(product_info):
    """Muestra la información del producto (solo precio y stock)"""
    
    st.markdown("""
    <div class="product-info">
    """, unsafe_allow_html=True)
    
    # Nombre del producto
    st.markdown(f'<p class="product-name">📝 {product_info["name"]}</p>', unsafe_allow_html=True)
    
    # Precio
    price = product_info.get('list_price', 0.0)
    st.markdown(f'<p class="price">💰 ${price:,.2f}</p>', unsafe_allow_html=True)
    
    # Stock disponible
    stock = product_info.get('immediately_usable_qty', 0)
    st.markdown(f'<p class="stock">📦 {stock:,.0f} unidades</p>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main() 