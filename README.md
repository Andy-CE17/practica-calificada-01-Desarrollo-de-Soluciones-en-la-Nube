# Práctica Calificada 1

**Curso:** Desarrollo de Soluciones en la Nube — Tecsup  
**Repositorio:** https://github.com/Andy-CE17/practica-calificada-01-Desarrollo-de-Soluciones-en-la-Nube

Este repositorio contiene los dos casos de la Práctica Calificada 1. Los dos casos están desarrollados y comprobados localmente y mediante Docker.

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

Las capturas reales del Caso 1 deben guardarse en `evidencias/caso1/`. Deben mostrar la aplicación local, una descarga válida, una validación o error controlado, cada contenedor funcionando y la comparación de las tres imágenes.

No se incluyen capturas ficticias. Los archivos deben agregarse después de tomarlas en la computadora donde se ejecutó la práctica.

### Problemas encontrados y solución

1. La versión solicitada inicialmente de yt-dlp no existía en PyPI. Se consultaron las versiones disponibles y se fijó `2026.8.19`.
2. YouTube requiere actualmente un runtime JavaScript y los scripts EJS de yt-dlp. Se utilizó Node.js 22 y `yt-dlp[default]`.
3. Algunos videos publican audio y video por separado. Se agregó `imageio-ffmpeg` para unir ambas pistas en un archivo reproducible.
4. La primera etapa final multistage utilizó `python3-minimal`, que no incluía el módulo estándar `uuid`. Se cambió a `python3` con `--no-install-recommends`.
5. Durante las pruebas, otro contenedor llamado `mi-app-container` ya utilizaba el puerto 5000. Para no interrumpirlo, los contenedores del Caso 1 se comprobaron temporalmente con `-p 5001:5000`. En un equipo con el puerto libre se debe usar `-p 5000:5000`.

### Conclusión

El Caso 1 permite validar y procesar enlaces públicos compatibles sin detener el servidor cuando una URL falla. La aplicación funciona localmente y en las tres imágenes Docker. El orden de capas, `.dockerignore` y la construcción multistage redujeron el tamaño final de 1.47 GB a 578 MB.

## Caso 2: registro electoral y generación de Excel

Aplicación web para registrar manualmente los resultados de una consulta electoral permitida y exportarlos a Excel. El formulario administra DNI, ubicación, región, provincia, distrito y dirección del local de votación.

La aplicación no automatiza consultas en el portal de ONPE ni intenta superar CAPTCHA, autenticación o controles anti-bot. Los datos de prueba deben ser ficticios. La URL de referencia indicada por la guía es <https://consultaelectoral.onpe.gob.pe/inicio>.

### Tecnologías utilizadas

- Python 3.11
- Flask 3.1.2
- openpyxl 3.1.5
- HTML y CSS
- Docker Desktop

### Estructura

```text
caso2-onpe/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── exports/                # Los archivos XLSX están ignorados por Git
├── .dockerignore
├── Dockerfile
├── Dockerfile.optimizado
└── Dockerfile.multistage
```

### Funcionamiento y validaciones

1. El usuario realiza la consulta permitida y copia manualmente el resultado.
2. Completa todos los campos del formulario.
3. El backend comprueba que ningún campo esté vacío y que el DNI tenga exactamente ocho dígitos.
4. Los resultados válidos se muestran en una tabla.
5. El botón **Exportar Excel** genera `exports/resultados_electorales.xlsx`.

Los registros se mantienen en memoria mientras la aplicación está activa. Al reiniciar el proceso o el contenedor, la tabla comienza vacía.

### Instalación y ejecución local

Desde la raíz del repositorio:

```powershell
Set-Location .\caso2-onpe
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Abrir <http://localhost:5000>. Para comprobar la validación se puede enviar el formulario vacío o utilizar un DNI que no tenga ocho dígitos.

### Generación de Excel

Después de agregar al menos un registro, seleccionar **Exportar Excel**. El archivo contiene los encabezados DNI, Ubicación, Región, Provincia, Distrito y Dirección del local de votación.

```powershell
Get-ChildItem .\exports
```

La carpeta `exports` está ignorada para evitar versionar información electoral o archivos generados.

### Dockerfile base

```powershell
docker build -t caso2-onpe:v1.0 .
docker run -d --name caso2-onpe-v1 -p 5000:5000 caso2-onpe:v1.0
docker ps
docker logs caso2-onpe-v1
```

### Dockerfile optimizado

`Dockerfile.optimizado` copia primero `requirements.txt` para reutilizar la capa de dependencias. `.dockerignore` evita enviar Git, entornos virtuales, exportaciones, cachés y archivos temporales al contexto de construcción.

```powershell
docker build -f Dockerfile.optimizado -t caso2-onpe:v1.1-optimizado .
docker run -d --name caso2-onpe-optimizado -p 5000:5000 caso2-onpe:v1.1-optimizado
```

### Dockerfile Multi-Stage

La primera etapa instala las dependencias en `/opt/python`. La etapa final usa Debian, instala únicamente Python y certificados, y copia las dependencias preparadas junto con el código.

```powershell
docker build -f Dockerfile.multistage -t caso2-onpe:v1.2-multistage .
docker run -d --name caso2-onpe-multistage -p 5000:5000 caso2-onpe:v1.2-multistage
```

### Comparación obtenida

```powershell
docker images caso2-onpe
```

| Imagen | Tamaño obtenido |
| --- | ---: |
| `caso2-onpe:v1.0` | 273 MB |
| `caso2-onpe:v1.1-optimizado` | 210 MB |
| `caso2-onpe:v1.2-multistage` | 193 MB |

Los tamaños pueden variar ligeramente según Docker Desktop y las imágenes base.

### Comandos de comprobación

```powershell
docker ps
docker logs <nombre-contenedor>
docker images caso2-onpe
Invoke-WebRequest -Uri http://localhost:5000 -UseBasicParsing
git status
git log --oneline
```

Durante las pruebas de esta computadora se utilizó temporalmente `-p 5002:5000` porque el puerto 5000 estaba ocupado por otro contenedor.

### Evidencias

Las capturas reales deben guardarse en `evidencias/caso2/`. Se recomienda incluir la ejecución local, el formulario con datos ficticios, el Excel abierto, cada contenedor funcionando y la comparación de las tres imágenes.

No se incluyen capturas ficticias. Los archivos deben agregarse después de tomarlas en la computadora donde se ejecutó la práctica.

### Observaciones y solución de problemas

- Si el portal presenta CAPTCHA o controles anti-bot, la consulta se realiza manualmente y el resultado se ingresa en esta aplicación.
- Si el puerto 5000 está ocupado, se puede utilizar `-p 5002:5000` y abrir <http://localhost:5002>.
- Si se intenta exportar sin registros, la aplicación muestra un mensaje y no genera un archivo vacío.
- Los archivos `.xlsx` generados y los entornos virtuales están excluidos de Git.

### Conclusión

El Caso 2 permite organizar resultados ingresados manualmente, validarlos y exportarlos a un Excel con encabezados claros. Las tres variantes Docker funcionan y la construcción multistage redujo la imagen de 273 MB a 193 MB.
