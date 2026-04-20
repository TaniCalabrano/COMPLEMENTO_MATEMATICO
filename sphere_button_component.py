"""
sphere_button_component.py

Usa declare_component() con un directorio local que contiene index.html.
Esto permite comunicación bidireccional real via Streamlit.setComponentValue().

IMPORTANTE: La carpeta 'sphere_component/' debe estar en el mismo directorio
que este archivo (junto a app.py).
"""
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# Path al directorio con el index.html de la esfera
_COMPONENT_DIR = Path(__file__).parent / "sphere_component"

# Declarar el componente apuntando al directorio local
_sphere_func = components.declare_component(
    "sphere_button",
    path=str(_COMPONENT_DIR),
)


def mostrar_boton_esfera() -> bool:
    """
    Muestra la esfera giratoria clickeable.
    Retorna True cuando el usuario hace clic.

    Requiere que exista la carpeta 'sphere_component/index.html'
    en el mismo directorio que este archivo.
    """
    _, col, _ = st.columns([1, 1, 1])
    with col:
        val = _sphere_func(key="sphere_btn_main", default=0)

    # Retorna True si el componente envió el valor 1 (clic)
    return val == 1
