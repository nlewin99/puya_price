"""
Módulo simplificado para escanear códigos QR usando streamlit_qrcode_scanner
"""

import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner
from typing import Optional


class BarcodeScanner:
    """Clase simplificada para manejar el escaneo de códigos QR"""
    
    def __init__(self):
        self.last_barcode = None
        
    def scan_qr_code(self) -> Optional[str]:
        """
        Escanea un código QR automáticamente usando streamlit_qrcode_scanner
        
        Returns:
            str: Código QR escaneado o None si no se detecta
        """
        try:
            st.markdown("### 📱 Escáner de Códigos QR")
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
                """)
            
            # Usar streamlit_qrcode_scanner
            qr_code = qrcode_scanner(key='qrcode_scanner')
            
            if qr_code:
                # Verificar que no sea el mismo código
                if qr_code != self.last_barcode:
                    self.last_barcode = qr_code
                    st.success(f"✅ Código QR detectado: {qr_code}")
                    return qr_code
                else:
                    st.info("🔄 Código ya escaneado, apunta hacia otro código QR")
            
            return None
            
        except Exception as e:
            st.error(f"Error en el escáner: {str(e)}")
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
        qr_code = self.scan_qr_code()
        
        if qr_code:
            return qr_code
        
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