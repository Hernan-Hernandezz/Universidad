import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.models import Usuarios

# Ejecutar una sola vez: python hashear_passwords.py

from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"])

engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    usuarios = db.query(Usuarios).all()

    for usuario in usuarios:
        if not usuario.contrasena_hash.startswith("$2b$"):
            usuario.contrasena_hash = pwd_context.hash(usuario.contrasena_hash)
            print(f"✅ {usuario.correo} actualizado")
        else:
            print(f"⏭️ {usuario.correo} ya estaba hasheado")
    db.commit()
    print("\n✅ Todas las contraseñas fueron hasheadas correctamente")

except Exception as e:
    db.rollback()
    print(f"❌ Error: {e}")

finally:
    db.close()
