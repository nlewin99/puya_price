"""
Módulo para escanear códigos de barras y QR automáticamente usando streamlit-barcode-scanner
"""

import streamlit as st
from streamlit_barcode_scanner import barcode_scanner
from typing import Optional


class AutoBarcodeScanner:
    """Clase para manejar el escaneo automático de códigos de barras y QR"""
    
    def __init__(self):
        self.last_barcode = None
        
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
            
            # Usar streamlit-barcode-scanner para escaneo automático
            barcode = barcode_scanner(
                key="barcode_scanner",
                help_text="Apunta la cámara hacia el código QR o código de barras"
            )
            
            if barcode:
                # Verificar que no sea el mismo código
                if barcode != self.last_barcode:
                    self.last_barcode = barcode
                    st.success(f"✅ Código detectado: {barcode}")
                    
                    # Determinar tipo de código (aproximado)
                    if len(barcode) > 20:
                        st.info("📱 Código QR detectado")
                    else:
                        st.info("📏 Código de barras detectado")
                    
                    return barcode
                else:
                    st.info("🔄 Código ya escaneado, apunta hacia otro código")
            
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