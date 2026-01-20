from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Annotated
from decimal import Decimal

from app.database import fetch_all_productos, fetch_producto_by_id, insert_producto, update_producto, delete_producto


app = FastAPI(
    title="FerreApp API Ing María Chaparro",
    version="1.0.0",
    description="API REST desacoplada para gestión de productos de ferretería"
)


# ========================
# Modelos Pydantic
# ========================

class ProductoBase(BaseModel):
    """Modelo base con validaciones compartidas para Producto."""
    nombre: Annotated[str, Field(min_length=1, max_length=80)]
    descripcion: Optional[Annotated[str, Field(max_length=255)]] = None
    precio: float = Field(ge=0)
    stock: int = Field(ge=0)
    categoria: Annotated[str, Field(min_length=1, max_length=50)]
    codigo_sku: Annotated[str, Field(min_length=1, max_length=20)]
    activo: bool = True

    @field_validator('nombre', 'categoria')
    @classmethod
    def validar_nombre_categoria(cls, v: str) -> str:
        """Valida nombre y categoría."""
        if not v or not v.strip():
            raise ValueError('El campo no puede estar vacío')
        return v.strip()

    @field_validator('codigo_sku')
    @classmethod
    def validar_codigo_sku(cls, v: str) -> str:
        """Valida código SKU."""
        v = v.strip().upper()
        if not v:
            raise ValueError('El SKU no puede estar vacío')
        return v

    @field_validator('descripcion')
    @classmethod
    def validar_descripcion(cls, v: Optional[str]) -> Optional[str]:
        """Valida descripción."""
        if v is None or v.strip() == '':
            return None
        return v.strip()


class ProductoDB(BaseModel):
    """Modelo para lectura desde BD (sin validaciones estrictas para datos históricos)."""
    id_producto: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int
    categoria: str
    codigo_sku: str
    activo: bool


class ProductoCreate(ProductoBase):
    """Modelo para crear nuevo producto (sin ID)."""
    pass


class ProductoUpdate(ProductoBase):
    """Modelo para actualizar producto (sin ID)."""
    pass


class Producto(ProductoBase):
    """Modelo completo de Producto (con ID y validaciones)."""
    id_producto: int

@app.get("/ping")
def ping():
    """Endpoint de prueba."""
    return {"message": "pong"}