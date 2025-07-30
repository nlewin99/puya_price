"""
Aplicación Streamlit para consultar precios de productos por código de barras
"""

import streamlit as st
import time
from odoo_client import OdooClient, AppConfig
from barcode_scanner import BarcodeScanner
import cv2
import numpy as np


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
        font-size: 2rem;
        color: #28a745;
        font-weight: bold;
    }
    .stock {
        font-size: 1.5rem;
        color: #007bff;
        font-weight: bold;
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
        <h2>🔍 Escanea códigos de barras para consultar precios</h2>
        <p style="font-size: 1.2rem; color: #666;">
            Escanea cualquier código de barras para obtener información del producto:
        </p>
        <ul style="text-align: left; display: inline-block; font-size: 1.1rem;">
            <li>💰 Precio de venta</li>
            <li>📦 Stock disponible</li>
            <li>📝 Nombre del producto</li>
            <li>📋 SKU/Código interno</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón central para iniciar escaneo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 INICIAR ESCANEO", type="primary", use_container_width=True):
            st.session_state.scanning = True
            st.rerun()
    
    # Mostrar información del último producto escaneado
    if st.session_state.product_info:
        st.markdown("---")
        st.markdown("### 📋 Último producto consultado:")
        show_product_info(st.session_state.product_info)


def show_scanner_page():
    """Muestra la página del escáner"""
    
    st.markdown("""
    <div style="text-align: center; margin: 1rem 0;">
        <h2>📱 Escáner de Códigos de Barras</h2>
        <p>Apunta la cámara hacia el código de barras del producto</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón para volver
    if st.button("← Volver al inicio"):
        st.session_state.scanning = False
        st.session_state.scanner.stop_camera()
        st.rerun()
    
    # Iniciar cámara
    if not st.session_state.scanner.cap or not st.session_state.scanner.cap.isOpened():
        if not st.session_state.scanner.start_camera():
            st.error("No se pudo acceder a la cámara. Verifica los permisos.")
            return
    
    # Contenedor para la cámara
    camera_placeholder = st.empty()
    
    # Procesar frames de la cámara
    try:
        while True:
            frame = st.session_state.scanner.get_frame()
            if frame is not None:
                # Procesar frame para detectar códigos de barras
                barcode_data, processed_frame = st.session_state.scanner.process_frame_for_barcode(frame)
                
                # Mostrar frame procesado
                camera_placeholder.image(processed_frame, channels="RGB", use_column_width=True)
                
                # Si se detectó un código de barras
                if barcode_data and barcode_data != st.session_state.last_barcode:
                    st.session_state.last_barcode = barcode_data
                    
                    # Mostrar código detectado
                    st.success(f"✅ Código detectado: {barcode_data}")
                    
                    # Consultar producto en Odoo
                    with st.spinner("🔍 Consultando información del producto..."):
                        product_info = get_product_info(barcode_data)
                    
                    if product_info:
                        st.session_state.product_info = product_info
                        show_product_info(product_info)
                        
                        # Pausa para mostrar resultado
                        time.sleep(3)
                        
                        # Volver al inicio
                        st.session_state.scanning = False
                        st.session_state.scanner.stop_camera()
                        st.rerun()
                    else:
                        st.error("❌ Producto no encontrado en la base de datos")
                        time.sleep(2)
            
            time.sleep(0.1)  # Pequeña pausa para no saturar la CPU
            
    except Exception as e:
        st.error(f"Error en el escáner: {str(e)}")
    finally:
        st.session_state.scanner.stop_camera()


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
    """Muestra la información del producto"""
    
    st.markdown("""
    <div class="product-info">
    """, unsafe_allow_html=True)
    
    # Nombre del producto
    st.markdown(f"### 📝 {product_info['name']}")
    
    # Precio
    price = product_info.get('list_price', 0.0)
    st.markdown(f'<p class="price">💰 Precio: ${price:,.2f}</p>', unsafe_allow_html=True)
    
    # Stock disponible
    stock = product_info.get('immediately_usable_qty', 0)
    st.markdown(f'<p class="stock">📦 Stock disponible: {stock:,.0f} unidades</p>', unsafe_allow_html=True)
    
    # Información adicional
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**📋 SKU:** {product_info.get('default_code', 'N/A')}")
    
    with col2:
        st.markdown(f"**📊 Código de barras:** {product_info.get('barcode', 'N/A')}")
    
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main() 