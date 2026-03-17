"""
API Configuration Module

Configuración centralizada para metadatos, tags, y configuraciones avanzadas de la API.
Este módulo separa la configuración de la lógica de routing.

Author: Backend Team
Version: 1.0.0
"""

from typing import Dict, List, Any
from fastapi.openapi.models import Tag


class APIMetadata:
    """Metadatos y configuración para la documentación de la API"""
    
    # === INFORMACIÓN GENERAL ===
    TITLE = "Producto Backend API"
    DESCRIPTION = """
    ## API Backend para Producto
    
    Esta API proporciona endpoints para la gestión completa del sistema, incluyendo:
    
    ### 🔐 Autenticación
    - Registro y login de usuarios
    - Autenticación OAuth2 con JWT
    - Gestión de tokens y sesiones
    
    ### 👥 Gestión de Usuarios
    - **Públicos**: Registro, recuperación de contraseña
    - **Protegidos**: Perfil, actualización de datos, cambio de contraseña
    
    ### 📊 Funcionalidades Core
    - **Grupos**: Gestión de grupos y membresías
    - **Paquetes**: Administración de paquetes del sistema
    - **Formularios**: Creación y gestión de formularios dinámicos
    - **Pandas**: Procesamiento y análisis de datos
    
    ### 🔒 Seguridad
    - Autenticación OAuth2 con Bearer tokens
    - Validación de permisos por endpoint
    - Rate limiting y protección CORS
    
    ### 📚 Documentación
    - Swagger UI disponible en `/docs`
    - ReDoc disponible en `/redoc`
    - OpenAPI 3.0 schema en `/openapi.json`
    """
    
    VERSION = "1.0.0"
    CONTACT = {
        "name": "Backend Team",
        "email": "backend@producto.com",
        "url": "https://producto.com/contact"
    }
    
    LICENSE_INFO = {
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }


class APITags:
    """Configuración de tags para la documentación automática"""
    
    @staticmethod
    def get_tags_metadata() -> List[Tag]:
        """
        Retorna la configuración completa de tags para OpenAPI.
        
        Returns:
            List[Tag]: Lista de tags con descripciones detalladas
        """
        return [
            {
                "name": "Authentication",
                "description": "🔐 **Endpoints de autenticación y autorización**\n\n"
                             "Gestión de login, registro, tokens JWT y OAuth2. "
                             "Incluye endpoints para obtener y refrescar tokens de acceso.",
                "externalDocs": {
                    "description": "Documentación OAuth2",
                    "url": "https://oauth.net/2/"
                }
            },
            {
                "name": "Users - Public",
                "description": "👥 **Endpoints públicos de usuarios**\n\n"
                             "Operaciones que no requieren autenticación: "
                             "registro de nuevos usuarios, recuperación de contraseña, "
                             "verificación de email.",
            },
            {
                "name": "Users - Protected", 
                "description": "🔒 **Endpoints protegidos de usuarios**\n\n"
                             "Operaciones que requieren autenticación: "
                             "obtener perfil, actualizar información personal, "
                             "cambiar contraseña, gestión de preferencias.",
            },
            {
                "name": "Groups",
                "description": "👥 **Gestión de grupos**\n\n"
                             "Creación, modificación y administración de grupos. "
                             "Gestión de membresías, roles y permisos dentro de grupos.",
            },
            {
                "name": "Packages",
                "description": "📦 **Administración de paquetes**\n\n"
                             "Gestión del sistema de paquetes: "
                             "instalación, actualización, configuración y dependencias.",
            },
            {
                "name": "Forms",
                "description": "📝 **Formularios dinámicos**\n\n"
                             "Creación y gestión de formularios configurables. "
                             "Validación de datos, campos personalizados y procesamiento.",
            },
            {
                "name": "Pandas",
                "description": "📊 **Procesamiento de datos**\n\n"
                             "Análisis y manipulación de datos usando Pandas. "
                             "Operaciones de ETL, estadísticas y exportación de resultados.",
            },
            {
                "name": "OAuth 2.0 (Legacy)",
                "description": "⚠️ **Endpoints legacy de OAuth2**\n\n"
                             "Endpoints mantenidos para compatibilidad con versiones anteriores. "
                             "Se recomienda usar los nuevos endpoints de Authentication.",
            }
        ]


class APIResponses:
    """Respuestas HTTP estándar para la documentación"""
    
    # Respuestas comunes para endpoints públicos
    PUBLIC_RESPONSES = {
        400: {
            "description": "Bad Request - Datos de entrada inválidos",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid input data",
                        "errors": ["Field 'email' is required"]
                    }
                }
            }
        },
        422: {
            "description": "Validation Error - Error de validación",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "email"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        },
        500: {
            "description": "Internal Server Error - Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Internal server error occurred"
                    }
                }
            }
        }
    }
    
    # Respuestas adicionales para endpoints protegidos
    PROTECTED_RESPONSES = {
        **PUBLIC_RESPONSES,
        401: {
            "description": "Unauthorized - Token de autenticación requerido",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated"
                    }
                }
            }
        },
        403: {
            "description": "Forbidden - Permisos insuficientes",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Insufficient permissions"
                    }
                }
            }
        },
        404: {
            "description": "Not Found - Recurso no encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Resource not found"
                    }
                }
            }
        }
    }


class APIVersioning:
    """Configuración para versionado de API"""
    
    # Versiones soportadas
    CURRENT_VERSION = "v1"
    SUPPORTED_VERSIONS = ["v1"]
    DEPRECATED_VERSIONS = []
    
    # Prefijos de URL
    V1_PREFIX = "/api/v1"
    V2_PREFIX = "/api/v2"  # Para futuras versiones
    
    # Configuración legacy
    LEGACY_OAUTH_PREFIX = "/oauth2/v2.0"
    
    @staticmethod
    def get_version_info() -> Dict[str, Any]:
        """
        Retorna información sobre las versiones de la API.
        
        Returns:
            Dict[str, Any]: Información de versionado
        """
        return {
            "current": APIVersioning.CURRENT_VERSION,
            "supported": APIVersioning.SUPPORTED_VERSIONS,
            "deprecated": APIVersioning.DEPRECATED_VERSIONS,
            "endpoints": {
                "v1": APIVersioning.V1_PREFIX,
                "legacy_oauth": APIVersioning.LEGACY_OAUTH_PREFIX
            }
        }


# === EXPORTS ===
__all__ = [
    "APIMetadata",
    "APITags", 
    "APIResponses",
    "APIVersioning"
]