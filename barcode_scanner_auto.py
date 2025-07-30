"""
Módulo para escanear códigos QR y de barras automáticamente usando OpenCV
Basado en: https://medium.com/analytics-vidhya/create-a-qr-code-decoder-web-application-using-opencv-and-streamlit-b0656146e2d1
"""

import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import io
from typing import Optional


class AutoBarcodeScanner:
    """Clase para manejar el escaneo automático de códigos QR y de barras"""
    
    def __init__(self):
        self.last_barcode = None
        
    @st.cache_data
    def decode_qr_barcode(_self, image):
        """
        Decodifica códigos QR y de barras desde una imagen
        Basado en el artículo de Medium sobre QR code decoder
        """
        try:
            # Convertir imagen PIL a array numpy
            if isinstance(image, Image.Image):
                image_array = np.array(image)
            else:
                image_array = image
            
            # Convertir a escala de grises si es necesario
            if len(image_array.shape) == 3:
                gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = image_array
            
            # Detectar códigos QR usando OpenCV
            qr_detector = cv2.QRCodeDetector()
            qr_data, bbox, _ = qr_detector.detectAndDecode(gray)
            
            if qr_data:
                return qr_data
            
            # Si no se detectó QR, intentar con códigos de barras usando pyzbar
            barcodes = decode(gray)
            for barcode in barcodes:
                barcode_data = barcode.data.decode('utf-8')
                if barcode_data:
                    return barcode_data
            
            return None
            
        except Exception as e:
            st.error(f"Error al decodificar: {str(e)}")
            return None
    
    def scan_barcode_auto(self) -> Optional[str]:
        """
        Escanea un código de barras o QR automáticamente usando la cámara
        
        Returns:
            str: Código escaneado o None si no se detecta
        """
        try:
            st.markdown("### 📱 Escáner Automático")
            st.markdown("**Apunta la cámara hacia el código QR o código de barras del producto**")
            
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
            
            # Usar cámara de Streamlit
            camera_input = st.camera_input("📷 Escanea el código automáticamente")
            
            if camera_input is not None:
                # Convertir la imagen de la cámara
                image = Image.open(camera_input)
                
                # Intentar decodificar automáticamente
                with st.spinner("🔍 Detectando código..."):
                    decoded_data = self.decode_qr_barcode(image)
                
                if decoded_data:
                    # Verificar que no sea el mismo código
                    if decoded_data != self.last_barcode:
                        self.last_barcode = decoded_data
                        st.success(f"✅ Código detectado automáticamente: {decoded_data}")
                        
                        # Determinar tipo de código (aproximado)
                        if len(decoded_data) > 20:
                            st.info("📱 Código QR detectado")
                        else:
                            st.info("📏 Código de barras detectado")
                        
                        return decoded_data
                    else:
                        st.info("🔄 Código ya escaneado, apunta hacia otro código")
                else:
                    st.warning("⚠️ No se pudo detectar ningún código. Intenta con mejor iluminación o un código más claro.")
            
            return None
            
        except Exception as e:
            st.error(f"Error en el escáner automático: {str(e)}")
            return None
    
    def scan_with_fallback(self) -> Optional[str]:
        """
        Escanea con fallback a entrada manual si el automático falla
        
        Returns:
            str: Código escaneado o ingresado manualmente
        """
        st.markdown("### 📱 Escáner de Códigos")
        
        # Opción 1: Escaneo automático
        st.markdown("#### 🔍 Escaneo Automático")
        barcode_auto = self.scan_barcode_auto()
        
        if barcode_auto:
            return barcode_auto
        
        # Opción 2: Entrada manual como fallback
        st.markdown("---")
        st.markdown("#### 📝 Entrada Manual")
        st.markdown("Si el escaneo automático no funciona, puedes ingresar el código manualmente:")
        
        barcode_manual = st.text_input(
            "🔢 Ingresa el código (QR o código de barras):",
            placeholder="Ej: 1234567890123",
            key="manual_barcode_input"
        )
        
        if st.button("🔍 Buscar Producto", type="primary"):
            if barcode_manual and barcode_manual.strip():
                return barcode_manual.strip()
            else:
                st.error("❌ Por favor ingresa un código válido")
        
        return None
    
    def reset_scanner(self):
        """Reinicia el escáner"""
        self.last_barcode = None 