"""
Módulo simplificado para escanear códigos de barras usando Streamlit
Compatible con Streamlit Cloud (sin dependencias externas problemáticas)
"""

import streamlit as st
from typing import Optional
import time


class SimpleBarcodeScanner:
    """Clase simplificada para manejar el escaneo de códigos de barras"""
    
    def __init__(self):
        self.last_barcode = None
        
    def scan_barcode(self) -> Optional[str]:
        """
        Escanea un código de barras usando la cámara de Streamlit
        
        Returns:
            str: Código de barras escaneado o None si no se detecta
        """
        try:
            # Usar la función de cámara de Streamlit
            camera_input = st.camera_input("Escanea el código de barras")
            
            if camera_input is not None:
                # Por ahora, pedir al usuario que ingrese el código manualmente
                # ya que el procesamiento de imagen requiere OpenCV
                st.info("📝 Por favor, ingresa el código de barras manualmente:")
                barcode = st.text_input("Código de barras:", key="barcode_input")
                
                if barcode and barcode.strip():
                    return barcode.strip()
            
            return None
            
        except Exception as e:
            st.error(f"Error al escanear código de barras: {str(e)}")
            return None
    
    def get_barcode_input(self) -> Optional[str]:
        """
        Obtiene el código de barras mediante entrada manual con cámara de referencia
        
        Returns:
            str: Código de barras ingresado o None
        """
        st.markdown("### 📱 Escáner de Códigos QR y de Barras")
        st.markdown("""
        **Instrucciones:**
        1. Toma una foto del código QR o código de barras con la cámara
        2. Ingresa el código manualmente en el campo de abajo
        3. Haz clic en 'Buscar Producto'
        """)
        
        # Información sobre tipos de códigos
        with st.expander("ℹ️ Tipos de códigos soportados"):
            st.markdown("""
            **Códigos QR (Recomendados):**
            - ✅ Más fáciles de escanear con móviles
            - ✅ Se leen desde cualquier ángulo
            - ✅ Más tolerantes a errores
            
            **Códigos de Barras:**
            - 📏 Más compactos
            - 🔍 Requieren alineación precisa
            - 📱 Funcionan mejor en buena iluminación
            """)
        
        # Cámara para referencia visual
        camera_input = st.camera_input("📷 Toma una foto del código QR o código de barras")
        
        if camera_input:
            st.success("✅ Foto capturada")
            st.info("Ahora ingresa el código manualmente en el campo de abajo")
        
        # Campo de entrada manual
        barcode = st.text_input(
            "🔢 Ingresa el código (QR o código de barras):",
            placeholder="Ej: 1234567890123",
            key="manual_barcode_input"
        )
        
        if st.button("🔍 Buscar Producto", type="primary"):
            if barcode and barcode.strip():
                return barcode.strip()
            else:
                st.error("❌ Por favor ingresa un código válido")
        
        return None
    
    def show_camera_preview(self):
        """Muestra la vista previa de la cámara"""
        st.markdown("### 📷 Vista de Cámara")
        camera_input = st.camera_input("Apunta la cámara hacia el código QR o código de barras")
        
        if camera_input:
            st.success("✅ Foto capturada")
            st.info("Ahora ingresa el código manualmente en el campo de abajo")
        
        return camera_input is not None
    
    def reset_scanner(self):
        """Reinicia el escáner"""
        self.last_barcode = None 