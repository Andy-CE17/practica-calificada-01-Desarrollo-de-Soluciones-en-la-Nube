from pathlib import Path
from urllib.parse import urlparse
from uuid import uuid4

import imageio_ffmpeg
from flask import Flask, render_template, request, send_from_directory
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


app = Flask(__name__)

CARPETA_DESCARGAS = Path(__file__).parent / "downloads"
CARPETA_DESCARGAS.mkdir(exist_ok=True)

PLATAFORMAS = {
    "youtube.com": "YouTube",
    "youtu.be": "YouTube",
    "instagram.com": "Instagram",
    "tiktok.com": "TikTok",
    "facebook.com": "Facebook",
    "fb.watch": "Facebook",
    "linkedin.com": "LinkedIn",
}


def obtener_plataforma(url):
    """Valida la URL y devuelve el nombre de la plataforma."""
    try:
        partes = urlparse(url)
        dominio = (partes.hostname or "").lower()
    except ValueError:
        return None

    if partes.scheme not in ("http", "https") or not dominio:
        return None

    for dominio_permitido, plataforma in PLATAFORMAS.items():
        if dominio == dominio_permitido or dominio.endswith(f".{dominio_permitido}"):
            return plataforma

    return None


def descargar_video(url):
    identificador = uuid4().hex[:8]
    opciones = {
        "format": "bv*[height<=720]+ba/b[height<=720]/b",
        "outtmpl": str(
            CARPETA_DESCARGAS / f"{identificador}-%(title).80s-%(id)s.%(ext)s"
        ),
        "merge_output_format": "mp4",
        "ffmpeg_location": imageio_ffmpeg.get_ffmpeg_exe(),
        "noplaylist": True,
        "restrictfilenames": True,
        "quiet": True,
        "no_warnings": True,
        "js_runtimes": {"node": {}},
        "socket_timeout": 30,
        "retries": 2,
    }

    with YoutubeDL(opciones) as descargador:
        informacion = descargador.extract_info(url, download=True)

    archivos_creados = [
        ruta
        for ruta in CARPETA_DESCARGAS.glob(f"{identificador}-*")
        if ruta.is_file() and ruta.suffix not in (".part", ".ytdl")
    ]

    if not archivos_creados:
        raise DownloadError("No se encontró el archivo descargado.")

    ruta_archivo = max(archivos_creados, key=lambda ruta: ruta.stat().st_mtime)
    return ruta_archivo.name, informacion.get("title", ruta_archivo.stem)


@app.route("/", methods=["GET", "POST"])
def inicio():
    mensaje_error = None
    mensaje_exito = None
    archivo = None
    url = ""

    if request.method == "POST":
        url = request.form.get("url", "").strip()

        if not url:
            mensaje_error = "Ingresa una URL para continuar."
        else:
            plataforma = obtener_plataforma(url)
            if not plataforma:
                mensaje_error = "Ingresa una URL válida de una plataforma compatible."
            else:
                try:
                    archivo, titulo = descargar_video(url)
                    mensaje_exito = f"Video procesado correctamente desde {plataforma}: {titulo}"
                except DownloadError as error:
                    app.logger.warning("Error al procesar la URL: %s", error)
                    mensaje_error = (
                        "No se pudo procesar el video. Verifica que el enlace sea público "
                        "y compatible."
                    )
                except Exception:
                    app.logger.exception("Error inesperado durante la descarga")
                    mensaje_error = "Ocurrió un error inesperado. Intenta nuevamente."

    return render_template(
        "index.html",
        url=url,
        mensaje_error=mensaje_error,
        mensaje_exito=mensaje_exito,
        archivo=archivo,
    )


@app.route("/descargas/<path:nombre_archivo>")
def obtener_archivo(nombre_archivo):
    return send_from_directory(CARPETA_DESCARGAS, nombre_archivo, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
