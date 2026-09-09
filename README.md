# Práctica Calificada 1

**Curso:** Desarrollo de Soluciones en la Nube — Tecsup  
**Repositorio:** <https://github.com/Andy-CE17/practica-calificada-01-Desarrollo-de-Soluciones-en-la-Nube>

Proyecto compuesto por dos aplicaciones web desarrolladas con Python, Flask y Docker.

## Estructura

~~~text
practica-calificada-01/
├── caso1-descargador/
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   ├── static/
│   ├── Dockerfile
│   ├── Dockerfile.optimizado
│   └── Dockerfile.multistage
├── caso2-onpe/
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   ├── static/
│   ├── Dockerfile
│   ├── Dockerfile.optimizado
│   └── Dockerfile.multistage
└── evidencias/
    ├── caso1/
    └── caso2/
~~~

## Requisitos

- Python 3.11
- Docker Desktop
- Node.js 22 para el Caso 1

## Caso 1: descargador de videos

Permite procesar enlaces públicos de YouTube, Instagram, TikTok, Facebook y LinkedIn. Valida la URL, controla errores y genera un enlace para guardar el video.

Para Facebook utiliza calidad SD, un límite de 200 MB y una sola descarga simultánea. No utiliza cookies, credenciales ni métodos para evitar restricciones de las plataformas.

### Ejecución local

~~~powershell
Set-Location .\caso1-descargador
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
~~~

Abrir <http://localhost:5000>.

### Docker

~~~powershell
docker build -t caso1-descargador:v1.0 .
docker build -f Dockerfile.optimizado -t caso1-descargador:v1.1-optimizado .
docker build -f Dockerfile.multistage -t caso1-descargador:v1.2-multistage .
docker run -d --name caso1-descargador -p 5000:5000 caso1-descargador:v1.2-multistage
~~~

| Imagen | Tamaño comprobado |
| --- | ---: |
| caso1-descargador:v1.0 | 1.47 GB |
| caso1-descargador:v1.1-optimizado | 613 MB |
| caso1-descargador:v1.2-multistage | 578 MB |

## Caso 2: miembros de mesa

Permite registrar los resultados obtenidos en el portal oficial de ONPE:

<https://consultaelectoral.onpe.gob.pe/inicio>

El usuario indica si el DNI consultado corresponde a un miembro de mesa. Solo los resultados positivos se agregan a la tabla y al Excel.

Datos registrados:

- DNI
- Ubicación o local
- Región
- Provincia
- Distrito
- Dirección del local de votación

La aplicación valida los campos, evita DNIs duplicados y permite eliminar registros antes de exportar el archivo miembros_de_mesa.xlsx.

### Ejecución local

~~~powershell
Set-Location .\caso2-onpe
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
~~~

Abrir <http://localhost:5000>.

### Docker

~~~powershell
docker build -t caso2-onpe:v1.0 .
docker build -f Dockerfile.optimizado -t caso2-onpe:v1.1-optimizado .
docker build -f Dockerfile.multistage -t caso2-onpe:v1.2-multistage .
docker run -d --name caso2-onpe -p 5000:5000 caso2-onpe:v1.2-multistage
~~~

| Imagen | Tamaño comprobado |
| --- | ---: |
| caso2-onpe:v1.0 | 226 MB |
| caso2-onpe:v1.1-optimizado | 210 MB |
| caso2-onpe:v1.2-multistage | 193 MB |

## Evidencias

### Caso 1

- [Página principal](evidencias/caso1/01-pagina-principal.png)
- [Descarga desde YouTube](evidencias/caso1/02-youtube.png)
- [Descarga desde TikTok](evidencias/caso1/03-tiktok.png)
- [Descarga desde Facebook](evidencias/caso1/04-facebook.png)

### Caso 2

- [Interfaz principal](evidencias/caso2/01-interfaz-principal.png)
- [Validación de resultado no miembro](evidencias/caso2/03-resultado-no-miembro.png)

Los videos descargados, archivos Excel, entornos virtuales y evidencias con datos privados están excluidos de Git.

