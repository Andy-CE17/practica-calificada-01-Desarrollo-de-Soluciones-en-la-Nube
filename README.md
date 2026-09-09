# Práctica Calificada 1

**Curso:** Desarrollo de Soluciones en la Nube — Tecsup  
**Repositorio:** https://github.com/Andy-CE17/practica-calificada-01-Desarrollo-de-Soluciones-en-la-Nube

Este repositorio contiene los dos casos de la Práctica Calificada 1. Actualmente se encuentra desarrollado y comprobado el Caso 1.

## Caso 1: descargador de videos

Aplicación web que recibe la URL de un video público, valida la plataforma y permite descargar el archivo procesado. Las plataformas consideradas son YouTube, Instagram, TikTok, Facebook y LinkedIn.

La aplicación no utiliza cookies, credenciales ni mecanismos para evitar autenticación, DRM o restricciones de las plataformas. Un enlace puede fallar si es privado, requiere una cuenta o dejó de ser compatible con `yt-dlp`.

### Tecnologías utilizadas

- Python 3.11
- Flask 3.1.2
- yt-dlp 2026.8.19
- imageio-ffmpeg 0.6.0
- HTML y CSS
- Node.js 22 para los desafíos JavaScript compatibles de yt-dlp
- Docker Desktop

### Estructura

```text
caso1-descargador/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── downloads/              # Ignorada por Git y Docker
├── .dockerignore
├── Dockerfile
├── Dockerfile.optimizado
└── Dockerfile.multistage
```

### Instalación local en Windows PowerShell

Desde la raíz del repositorio:

```powershell
Set-Location .\caso1-descargador
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
```

Si PowerShell no permite activar el entorno, se puede usar directamente su ejecutable:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Para procesar correctamente videos actuales de YouTube, el equipo debe tener Node.js 22 o superior disponible en `PATH`.

### Ejecución local

```powershell
.\.venv\Scripts\python.exe app.py
```

Abrir en el navegador:

```text
http://localhost:5000
```

Para detener la aplicación se utiliza `Ctrl+C` en la terminal.

### Dockerfile base

El Dockerfile base usa Node.js 22 sobre Debian, instala Python, copia todo el contexto y finalmente instala las dependencias. Esta versión muestra un funcionamiento válido, aunque incluye capas y archivos innecesarios.

```powershell
docker build -t caso1-descargador:v1.0 .
docker run -d --name caso1-descargador-v1 -p 5000:5000 caso1-descargador:v1.0
docker ps
docker logs caso1-descargador-v1
```

### Dockerfile optimizado

`Dockerfile.optimizado` instala paquetes del sistema sin recomendaciones, limpia la caché de `apt` y copia `requirements.txt` antes del código para reutilizar la capa de dependencias. `.dockerignore` excluye el entorno virtual, descargas, cachés, Git y archivos temporales.

```powershell
docker build -f Dockerfile.optimizado -t caso1-descargador:v1.1-optimizado .
docker run -d --name caso1-descargador-optimizado -p 5000:5000 caso1-descargador:v1.1-optimizado
```

### Dockerfile Multi-Stage

`Dockerfile.multistage` instala las librerías en una etapa de construcción. La etapa final recibe solamente las dependencias preparadas, Node.js, Python y el código de la aplicación; no conserva `pip` ni la etapa de construcción.

```powershell
docker build -f Dockerfile.multistage -t caso1-descargador:v1.2-multistage .
docker run -d --name caso1-descargador-multistage -p 5000:5000 caso1-descargador:v1.2-multistage
```

### Comparación obtenida

```powershell
docker images caso1-descargador
```

| Imagen | Tamaño obtenido |
| --- | ---: |
| `caso1-descargador:v1.0` | 1.47 GB |
| `caso1-descargador:v1.1-optimizado` | 613 MB |
| `caso1-descargador:v1.2-multistage` | 578 MB |

Los tamaños pueden variar ligeramente según la versión de las imágenes base y Docker Desktop.

### Comandos de comprobación

```powershell
docker ps
docker logs <nombre-contenedor>
docker images caso1-descargador
Invoke-WebRequest -Uri http://localhost:5000 -UseBasicParsing
git status
git log --oneline
```

### Evidencias

Las capturas del Caso 1 deben guardarse en la ruta relativa `evidencias/caso1/`. Se recomienda usar estos nombres:

- `01-flask-local.png`
- `02-interfaz.png`
- `03-descarga-valida.png`
- `04-validacion-error.png`
- `05-docker-base.png`
- `06-docker-optimizado.png`
- `07-comparacion-imagenes.png`
- `08-docker-multistage.png`

No se incluyen capturas ficticias. Los archivos deben agregarse después de tomarlas en la computadora donde se ejecutó la práctica.

### Problemas encontrados y solución

1. La versión solicitada inicialmente de yt-dlp no existía en PyPI. Se consultaron las versiones disponibles y se fijó `2026.8.19`.
2. YouTube requiere actualmente un runtime JavaScript y los scripts EJS de yt-dlp. Se utilizó Node.js 22 y `yt-dlp[default]`.
3. Algunos videos publican audio y video por separado. Se agregó `imageio-ffmpeg` para unir ambas pistas en un archivo reproducible.
4. La primera etapa final multistage utilizó `python3-minimal`, que no incluía el módulo estándar `uuid`. Se cambió a `python3` con `--no-install-recommends`.
5. Durante las pruebas, otro contenedor llamado `mi-app-container` ya utilizaba el puerto 5000. Para no interrumpirlo, los contenedores del Caso 1 se comprobaron temporalmente con `-p 5001:5000`. En un equipo con el puerto libre se debe usar `-p 5000:5000`.

### Conclusión

El Caso 1 permite validar y procesar enlaces públicos compatibles sin detener el servidor cuando una URL falla. La aplicación funciona localmente y en las tres imágenes Docker. El orden de capas, `.dockerignore` y la construcción multistage redujeron el tamaño final de 1.47 GB a 578 MB.

## Caso 2

Pendiente de desarrollo. No debe iniciarse hasta aprobar completamente el Caso 1.
