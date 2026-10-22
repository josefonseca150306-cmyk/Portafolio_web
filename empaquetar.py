import base64
import os
import re

carpeta = os.path.dirname(os.path.abspath(__file__))

# 1. Buscar y codificar el PDF del CV
pdf_path = None
for c in ["CV_JoseFonseca.pdf", "CV.pdf"]:
  ruta = os.path.join(carpeta, c)
  if os.path.exists(ruta):
    pdf_path = ruta
    break

if not pdf_path:
  for f in os.listdir(carpeta):
    if f.lower().endswith(".pdf") and "cv" in f.lower():
      pdf_path = os.path.join(carpeta, f)
      break

with open(pdf_path, "rb") as f:
  b64_pdf = base64.b64encode(f.read()).decode("utf-8")

# 2. Buscar y codificar la fotografía
foto_path = None
for c in ["perfil.jpg", "perfil.png", "perfil.jpeg", "foto.jpg", "foto.png"]:
  ruta = os.path.join(carpeta, c)
  if os.path.exists(ruta):
    foto_path = ruta
    break

if foto_path:
  ext = "png" if foto_path.endswith(".png") else "jpeg"
  with open(foto_path, "rb") as f:
    b64_foto = base64.b64encode(f.read()).decode("utf-8")
  foto_src = f"data:image/{ext};base64,{b64_foto}"
  print(f"Foto detectada y codificada: {os.path.basename(foto_path)}")
else:
  foto_src = "perfil.jpg"

# 3. Leer index.html y limpiar por completo el contenedor del avatar
html_path = os.path.join(carpeta, "index.html")
with open(html_path, "r", encoding="utf-8") as f:
  contenido = f.read()

# Reemplaza todo el interior de hero-avatar-wrapper sin dejar residuos de texto
clean_avatar = f"""<div class="hero-avatar-wrapper">
                    <img src="{foto_src}" 
                         alt="Fotografía profesional de José Antonio Fonseca" 
                         class="hero-avatar-img">
                </div>"""

contenido = re.sub(
    r'<div class="hero-avatar-wrapper">[\s\S]*?</div>', clean_avatar, contenido
)

# Reemplaza el PDF en memoria si es necesario
contenido = re.sub(
    r'const EMBEDDED_PDF_BASE64 = "[^"]*";',
    f'const EMBEDDED_PDF_BASE64 = "{b64_pdf}";',
    contenido,
)

with open(html_path, "w", encoding="utf-8") as f:
  f.write(contenido)

print("¡Listo! index.html corregido, centrado y sin caracteres residuales.")