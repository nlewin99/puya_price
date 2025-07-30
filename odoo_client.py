"""
Cliente para External API de Odoo v16
Maneja consultas de solo lectura usando la API externa oficial
"""

import xmlrpc.client
import pandas as pd
from typing import Optional, Dict
import streamlit as st


class OdooClient:
    """
    Cliente para interactuar con la External API de Odoo v16
    Solo permite operaciones de lectura
    """
    
    def __init__(self, url: str, db: str, username: str, password: str):
        """
        Inicializa el cliente de Odoo External API
        
        Args:
            url: URL base de Odoo
            db: Nombre de la base de datos
            username: Usuario de Odoo
            password: Contraseña de Odoo
        """
        self.url = url.rstrip('/')
        self.db = db
        self.username = username
        self.password = password
        self.uid = None
        self.models = None
        
    def authenticate(self) -> bool:
        """
        Autentica con la External API de Odoo
        
        Returns:
            bool: True si la autenticación fue exitosa
        """
        try:
            # Crear conexión XML-RPC
            common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            
            # Autenticar usando el método authenticate
            self.uid = common.authenticate(self.db, self.username, self.password, {})
            
            if self.uid:
                # Crear proxy para modelos
                self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
                return True
            else:
                st.error("Credenciales inválidas para Odoo")
                return False
                
        except Exception as e:
            st.error(f"Error de conexión con Odoo: {str(e)}")
            return False
    
    def get_product_by_barcode(self, barcode: str) -> Optional[Dict]:
        """
        Obtiene información de un producto por código de barras
        
        Args:
            barcode: Código de barras del producto
            
        Returns:
            Dict: Información del producto o None si no se encuentra
        """
        if not self.authenticate():
            return None
            
        try:
            # Buscar producto por código de barras
            product_ids = self.models.execute_kw(
                self.db, 
                self.uid, 
                self.password,
                'product.template', 
                'search',
                [[['barcode', '=', barcode], ['active', '=', True]]]
            )
            
            if product_ids:
                # Obtener información del producto incluyendo immediately_usable_qty
                products = self.models.execute_kw(
                    self.db, 
                    self.uid, 
                    self.password,
                    'product.template', 
                    'read',
                    [product_ids],
                    {
                        'fields': ['name', 'list_price', 'barcode', 'default_code', 'immediately_usable_qty']
                    }
                )
                
                if products:
                    product = products[0]
                    
                    return {
                        'name': product.get('name', ''),
                        'list_price': product.get('list_price', 0.0),
                        'barcode': product.get('barcode', ''),
                        'default_code': product.get('default_code', ''),
                        'immediately_usable_qty': product.get('immediately_usable_qty', 0.0)
                    }
            
            return None
                
        except Exception as e:
            st.error(f"Error al consultar producto: {str(e)}")
            return None


class AppConfig:
    """Configuración de la aplicación"""
    
    @staticmethod
    def get_odoo_credentials() -> Dict[str, Optional[str]]:
        """
        Obtiene credenciales de Odoo desde secrets de Streamlit Cloud
        
        Returns:
            Dict con credenciales de Odoo
        """
        return {
            'url': st.secrets.get("ODOO_URL"),
            'db': st.secrets.get("ODOO_DB"),
            'username': st.secrets.get("ODOO_USERNAME"),
            'password': st.secrets.get("ODOO_PASSWORD")
        }
    
    @staticmethod
    def validate_odoo_credentials() -> bool:
        """
        Valida que las credenciales de Odoo estén completas
        
        Returns:
            bool: True si las credenciales están completas
        """
        credentials = AppConfig.get_odoo_credentials()
        return all(credentials.values()) 