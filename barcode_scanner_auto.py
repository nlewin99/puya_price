"""
Módulo para escanear códigos de barras automáticamente usando streamlit-barcode-scanner
"""

import streamlit as st
from streamlit_barcode_scanner import barcode_scanner
from typing import Optional


class AutoBarcodeScanner:
    """Clase para manejar el escaneo automático de códigos de barras"""
    
    def __init__(self):
        self.last_barcode = None
        
    def scan_barcode_auto(self) -> Optional[str]:
        """
        Escanea un código de barras automáticamente usando la cámara
        
        Returns:
            str: Código de barras escaneado o None si no se detecta
        """
        try:
            st.markdown("### 📱 Escáner Automático de Códigos de Barras")
            st.markdown("**Apunta la cámara hacia el código de barras del producto**")
            
            # Usar streamlit-barcode-scanner para escaneo automático
            barcode = barcode_scanner(
                key="barcode_scanner",
                help_text="Apunta la cámara hacia el código de barras"
            )
            
            if barcode:
                # Verificar que no sea el mismo código
                if barcode != self.last_barcode:
                    self.last_barcode = barcode
                    st.success(f"✅ Código detectado: {barcode}")
                    return barcode
                else:
                    st.info("🔄 Código ya escaneado, apunta hacia otro código de barras")
            
            return None
            
        except Exception as e:
            st.error(f"Error en el escáner automático: {str(e)}")
            return None
    
    def scan_with_fallback(self) -> Optional[str]:
        """
        Escanea con fallback a entrada manual si el automático falla
        
        Returns:
            str: Código de barras escaneado o ingresado manualmente
        """
        st.markdown("### 📱 Escáner de Códigos de Barras")
        
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
            "🔢 Ingresa el código de barras:",
            placeholder="Ej: 1234567890123",
            key="manual_barcode_input"
        )
        
        if st.button("🔍 Buscar Producto", type="primary"):
            if barcode_manual and barcode_manual.strip():
                return barcode_manual.strip()
            else:
                st.error("❌ Por favor ingresa un código de barras válido")
        
        return None
    
    def reset_scanner(self):
        """Reinicia el escáner"""
        self.last_barcode = None 