import os
import sys
from flask import Flask

# 🔹 DETECTAR EXECUTÁVEL
if getattr(sys, 'frozen', False):
    # PyInstaller executável
    base_path = sys._MEIPASS
else:
    # Modo normal
    base_path = os.path.abspath(os.path.dirname(__file__))

template_dir = os.path.join(base_path, "templates")
static_dir = os.path.join(base_path, "static")

FRONTEND = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir
)
FRONTEND.secret_key = os.getenv("segredo_flask")

# importa rotas
from FRONTEND.controllers import default
