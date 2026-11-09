import os
import base64
import re

# Carpeta actual donde se encuentra este script
carpeta = os.path.dirname(os.path.abspath(__file__))

# 1. Detectar archivo HTML (busca T14FONSECA.html o index.html)
html_file = None
for nombre in ["T14FONSECA.html", "t14Fonseca.html", "index.html"]:
    ruta = os.path.join(carpeta, nombre)
    if os.path.exists(ruta):
        html_file = ruta
        break

if not html_file:
    print("❌ Error: No se encontró T14FONSECA.html ni index.html en la carpeta.")
    exit(1)

# 2. Detectar y codificar el CV en PDF
pdf_path = None
for nombre_pdf in ["CV_JoseFonseca.pdf", "CV_JoseAntonioFonseca.pdf", "CV.pdf"]:
    ruta_pdf = os.path.join(carpeta, nombre_pdf)
    if os.path.exists(ruta_pdf):
        pdf_path = ruta_pdf
        break

b64_pdf = ""
if pdf_path:
    with open(pdf_path, "rb") as f:
        b64_pdf = base64.b64encode(f.read()).decode("utf-8")
    print(f"✔ CV detectado y codificado en memoria: {os.path.basename(pdf_path)}")
else:
    print("⚠ Aviso: No se encontró el archivo PDF del CV en la carpeta.")

# 3. Detectar y codificar la foto de perfil en Base64
foto_src = None
for c in ["perfil.jpg", "perfil.png", "perfil.jpeg"]:
    ruta_foto = os.path.join(carpeta, c)
    if os.path.exists(ruta_foto):
        ext = "png" if c.endswith(".png") else "jpeg"
        with open(ruta_foto, "rb") as f:
            b64_foto = base64.b64encode(f.read()).decode("utf-8")
        foto_src = f"data:image/{ext};base64,{b64_foto}"
        print(f"✔ Foto detectada y codificada: {c}")
        break

# 4. Leer el archivo HTML
with open(html_file, "r", encoding="utf-8") as f:
    contenido = f.read()

# 5. Inyectar PDF en Base64 dentro de la variable de memoria
if b64_pdf:
    if "{B64_PDF_DATA}" in contenido:
        contenido = contenido.replace("{B64_PDF_DATA}", b64_pdf)
        print("✔ Variable {B64_PDF_DATA} reemplazada con el contenido del PDF.")
    elif "const EMBEDDED_PDF_BASE64 =" in contenido:
        contenido = re.sub(
            r'const EMBEDDED_PDF_BASE64\s*=\s*"[^"]*";',
            f'const EMBEDDED_PDF_BASE64 = "{b64_pdf}";',
            contenido
        )
        print("✔ Variable EMBEDDED_PDF_BASE64 actualizada con el PDF en Base64.")

# 6. Incrustar foto directamente sin tocar los aros HUD ni la animación
if foto_src:
    contenido = re.sub(r'src=["\']perfil\.(?:jpg|png|jpeg)["\']', f'src="{foto_src}"', contenido)
    print("✔ Foto incrustada directamente en el código HTML.")

# 7. Guardar el archivo HTML empaquetado
with open(html_file, "w", encoding="utf-8") as f:
    f.write(contenido)

print(f"\n🎉 ¡ÉXITO! Se empaquetó correctamente en: {os.path.basename(html_file)}")