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
5. Facebook ofrecía un formato de 720p de 918 MB para un video de una hora. Se cambió la selección a SD, se agregó un límite de 200 MB y se bloquearon los envíos repetidos.
6. Algunos reels públicos pueden dejar de ser compatibles cuando Facebook cambia su página; la aplicación informa la limitación sin solicitar credenciales.
7. Durante las pruebas, otro contenedor llamado `mi-app-container` ya utilizaba el puerto 5000. Para no interrumpirlo, los contenedores del Caso 1 se comprobaron temporalmente con `-p 5001:5000`. En un equipo con el puerto libre se debe usar `-p 5000:5000`.

### Conclusión

El Caso 1 permite validar y procesar enlaces públicos compatibles sin detener el servidor cuando una URL falla. Para Facebook se prioriza el formato SD, se aplica un límite de 200 MB y se evita iniciar más de una descarga simultánea. La aplicación funciona localmente y en las tres imágenes Docker. El orden de capas, `.dockerignore` y la construcción multistage redujeron el tamaño final de 1.47 GB a 578 MB.

## Caso 2: miembros de mesa y generación de Excel

Aplicación web para registrar a las personas que, después de consultar su DNI en el portal oficial de ONPE, aparecen como miembros de mesa. Solo los resultados marcados como **Sí** se incorporan a la tabla y al archivo Excel.

La aplicación no automatiza el portal ni intenta superar CAPTCHA, autenticación o controles anti-bot. El usuario consulta un DNI propio o proporcionado con autorización en <https://consultaelectoral.onpe.gob.pe/inicio> y registra el resultado mostrado por ONPE.

### Tecnologías utilizadas

- Python 3.11
- Flask 3.1.2
- openpyxl 3.1.5
- HTML, CSS y JavaScript básico
- Docker Desktop

### Estructura

~~~text
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
~~~

### Funcionamiento y validaciones

1. Se abre el portal oficial mediante el botón **Abrir portal ONPE**.
2. El usuario consulta el DNI y verifica si aparece como miembro de mesa.
3. En la aplicación se ingresa el DNI y se selecciona **Sí** o **No**.
4. Si se selecciona **Sí**, son obligatorios ubicación o local, región, provincia, distrito y dirección.
5. Si se selecciona **No**, el DNI no se agrega a la lista ni al Excel.
6. La aplicación valida que el DNI tenga ocho dígitos y evita registros duplicados.
7. **Exportar Excel** genera el archivo exports/miembros_de_mesa.xlsx.

Los registros permanecen en memoria durante la ejecución. Al reiniciar la aplicación o el contenedor, la tabla comienza vacía.

### Instalación y ejecución local

Desde la raíz del repositorio:

~~~powershell
Set-Location .\caso2-onpe
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
~~~

Abrir <http://localhost:5000>. Para las pruebas de desarrollo se deben usar datos ficticios. Para la evidencia final se utiliza únicamente un DNI propio o proporcionado con autorización.

### Generación de Excel

El archivo contiene solamente personas confirmadas como miembros de mesa y utiliza los siguientes encabezados:

- DNI
- Miembro de mesa
- Ubicación
- Región
- Provincia
- Distrito
- Dirección del local de votación

~~~powershell
Get-ChildItem .\exports
~~~

La carpeta exports está ignorada para evitar publicar DNIs o archivos generados en GitHub.

### Dockerfile base

~~~powershell
docker build -t caso2-onpe:v1.0 .
docker run -d --name caso2-onpe-v1 -p 5000:5000 caso2-onpe:v1.0
docker ps
docker logs caso2-onpe-v1
~~~

### Dockerfile optimizado

Dockerfile.optimizado copia primero requirements.txt para reutilizar la capa de dependencias. .dockerignore excluye Git, entornos virtuales, exportaciones, cachés y archivos temporales.

~~~powershell
docker build -f Dockerfile.optimizado -t caso2-onpe:v1.1-optimizado .
docker run -d --name caso2-onpe-optimizado -p 5000:5000 caso2-onpe:v1.1-optimizado
~~~

### Dockerfile Multi-Stage

La primera etapa instala las dependencias en /opt/python. La etapa final usa Debian, instala Python y certificados, y copia las dependencias preparadas junto con el código.

~~~powershell
docker build -f Dockerfile.multistage -t caso2-onpe:v1.2-multistage .
docker run -d --name caso2-onpe-multistage -p 5000:5000 caso2-onpe:v1.2-multistage
~~~

### Comparación obtenida

~~~powershell
docker images caso2-onpe
~~~

| Imagen | Tamaño obtenido |
| --- | ---: |
| caso2-onpe:v1.0 | 226 MB |
| caso2-onpe:v1.1-optimizado | 210 MB |
| caso2-onpe:v1.2-multistage | 193 MB |

Los tamaños pueden variar ligeramente según Docker Desktop y las imágenes base.

### Comandos de comprobación

~~~powershell
docker ps
docker logs <nombre-contenedor>
docker images caso2-onpe
Invoke-WebRequest -Uri http://localhost:5000 -UseBasicParsing
git status
git log --oneline
~~~

Durante las pruebas de esta computadora se utilizó temporalmente -p 5002:5000 porque el puerto 5000 estaba ocupado.

### Evidencias

Las capturas reales deben guardarse en evidencias/caso2/. Deben mostrar la consulta permitida en ONPE, la confirmación de miembro de mesa, la lista de la aplicación, el Excel abierto, cada contenedor funcionando y la comparación de imágenes.

No se incluyen capturas ficticias. Tampoco se versiona el Excel que contiene DNIs.

### Observaciones

- ONPE requiere una consulta interactiva con JavaScript y puede aplicar controles anti-bot; por ello la verificación se realiza en su portal.
- La aplicación registra únicamente los resultados positivos.
- Si se intenta exportar sin miembros registrados, se muestra un mensaje de validación.
- Los archivos .xlsx y los entornos virtuales están excluidos de Git.

### Conclusión

El Caso 2 cumple el flujo solicitado: verificar en ONPE si una persona es miembro de mesa, almacenar solamente los resultados positivos con su ubicación y generar el Excel. Las versiones Docker base, optimizada y multistage permiten ejecutar la misma aplicación.
