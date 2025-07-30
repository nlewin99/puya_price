"""
Módulo para escanear códigos de barras usando la cámara
"""

import cv2
import numpy as np
from pyzbar.pyzbar import decode
import streamlit as st
from typing import Optional, Tuple
import time


class BarcodeScanner:
    """Clase para manejar el escaneo de códigos de barras"""
    
    def __init__(self):
        self.cap = None
        
    def start_camera(self) -> bool:
        """
        Inicia la cámara
        
        Returns:
            bool: True si la cámara se inició correctamente
        """
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                st.error("No se pudo acceder a la cámara")
                return False
            return True
        except Exception as e:
            st.error(f"Error al iniciar la cámara: {str(e)}")
            return False
    
    def stop_camera(self):
        """Detiene la cámara"""
        if self.cap:
            self.cap.release()
    
    def scan_barcode(self) -> Optional[str]:
        """
        Escanea un código de barras desde la cámara
        
        Returns:
            str: Código de barras escaneado o None si no se detecta
        """
        if not self.cap or not self.cap.isOpened():
            return None
            
        try:
            ret, frame = self.cap.read()
            if not ret:
                return None
            
            # Convertir frame a escala de grises
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detectar códigos de barras
            barcodes = decode(gray)
            
            for barcode in barcodes:
                # Extraer datos del código de barras
                barcode_data = barcode.data.decode('utf-8')
                barcode_type = barcode.type
                
                # Dibujar rectángulo alrededor del código de barras
                points = np.array([barcode.polygon], np.int32)
                points = points.reshape((-1, 1, 2))
                cv2.polylines(frame, [points], True, (0, 255, 0), 2)
                
                # Mostrar información del código de barras
                cv2.putText(frame, f"{barcode_type}: {barcode_data}", 
                           (barcode.rect.left, barcode.rect.top - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                return barcode_data
            
            return None
            
        except Exception as e:
            st.error(f"Error al escanear código de barras: {str(e)}")
            return None
    
    def get_frame(self) -> Optional[np.ndarray]:
        """
        Obtiene un frame de la cámara
        
        Returns:
            np.ndarray: Frame de la cámara o None si hay error
        """
        if not self.cap or not self.cap.isOpened():
            return None
            
        try:
            ret, frame = self.cap.read()
            if ret:
                # Convertir BGR a RGB para Streamlit
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                return frame_rgb
            return None
        except Exception as e:
            st.error(f"Error al obtener frame: {str(e)}")
            return None
    
    def process_frame_for_barcode(self, frame: np.ndarray) -> Tuple[Optional[str], np.ndarray]:
        """
        Procesa un frame para detectar códigos de barras
        
        Args:
            frame: Frame de la cámara
            
        Returns:
            Tuple: (código de barras detectado, frame procesado)
        """
        try:
            # Convertir a escala de grises
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            
            # Detectar códigos de barras
            barcodes = decode(gray)
            
            processed_frame = frame.copy()
            
            for barcode in barcodes:
                # Extraer datos del código de barras
                barcode_data = barcode.data.decode('utf-8')
                barcode_type = barcode.type
                
                # Dibujar rectángulo alrededor del código de barras
                points = np.array([barcode.polygon], np.int32)
                points = points.reshape((-1, 1, 2))
                cv2.polylines(processed_frame, [points], True, (0, 255, 0), 3)
                
                # Mostrar información del código de barras
                cv2.putText(processed_frame, f"{barcode_type}: {barcode_data}", 
                           (barcode.rect.left, barcode.rect.top - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                return barcode_data, processed_frame
            
            return None, processed_frame
            
        except Exception as e:
            st.error(f"Error al procesar frame: {str(e)}")
            return None, frame 