"""
Módulo para escanear códigos QR automáticamente usando OpenCV
Optimizado para Streamlit Cloud (sin dependencias problemáticas)
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
from typing import Optional


class BarcodeScanner:
    """Clase para manejar el escaneo automático de códigos QR"""
    
    def __init__(self):
        self.last_barcode = None
        
    @st.cache_data
    def decode_qr_code(_self, image):
        """
        Decodifica códigos QR desde una imagen usando OpenCV
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
            
            if qr_data and qr_data.strip():
                return qr_data.strip()
            
            return None
            
        except Exception as e:
            st.error(f"Error al decodificar QR: {str(e)}")
            return None
    
    def scan_barcode_auto(self) -> Optional[str]:
        """
        Escanea un código QR automáticamente usando la cámara
        
        Returns:
            str: Código QR escaneado o None si no se detecta
        """
        try:
            st.markdown("### 📱 Escáner Automático de Códigos QR")
            st.markdown("**Apunta la cámara hacia el código QR del producto**")
            
            # Información sobre códigos QR
            with st.expander("ℹ️ Información sobre códigos QR"):
                st.markdown("""
                **Códigos QR (Recomendados):**
                - ✅ Más fáciles de escanear con móviles
                - ✅ Se leen desde cualquier ángulo
                - ✅ Más tolerantes a errores
                - ✅ Mayor capacidad de datos
                - ✅ Mejor para aplicaciones móviles
                
                **Nota:** Esta aplicación está optimizada para códigos QR.
                Si tienes códigos de barras tradicionales, considera
                convertirlos a códigos QR para mejor compatibilidad.
                """)
            
            # Usar cámara de Streamlit
            camera_input = st.camera_input("📷 Escanea el código QR automáticamente")
            
            if camera_input is not None:
                # Convertir la imagen de la cámara
                image = Image.open(camera_input)
                
                # Intentar decodificar automáticamente
                with st.spinner("🔍 Detectando código QR..."):
                    decoded_data = self.decode_qr_code(image)
                
                if decoded_data:
                    # Verificar que no sea el mismo código
                    if decoded_data != self.last_barcode:
                        self.last_barcode = decoded_data
                        st.success(f"✅ Código QR detectado automáticamente: {decoded_data}")
                        return decoded_data
                    else:
                        st.info("🔄 Código ya escaneado, apunta hacia otro código QR")
                else:
                    st.warning("⚠️ No se pudo detectar ningún código QR. Asegúrate de que:")
                    st.markdown("""
                    - El código QR esté bien iluminado
                    - La cámara esté enfocada en el código
                    - El código QR no esté dañado o borroso
                    - El código QR sea legible y de buena calidad
                    """)
            
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
        st.markdown("### 📱 Escáner de Códigos QR")
        
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
            "🔢 Ingresa el código QR o código de barras:",
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