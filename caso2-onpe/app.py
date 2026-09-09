from pathlib import Path

from flask import Flask, redirect, render_template, request, send_file, url_for
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill


app = Flask(__name__)
registros = []

CARPETA_EXPORTACIONES = Path(__file__).parent / "exports"
CARPETA_EXPORTACIONES.mkdir(exist_ok=True)

CAMPOS_UBICACION = ["ubicacion", "region", "provincia", "distrito", "direccion"]
TODOS_LOS_CAMPOS = ["dni", "es_miembro", *CAMPOS_UBICACION]


def datos_vacios():
    return {campo: "" for campo in TODOS_LOS_CAMPOS}


def validar_registro(datos):
    if not datos["dni"].isdigit() or len(datos["dni"]) != 8:
        return "El DNI debe contener exactamente 8 dígitos."

    if datos["es_miembro"] not in ("si", "no"):
        return "Indica si el DNI corresponde a un miembro de mesa."

    if datos["es_miembro"] == "si" and any(
        not datos[campo] for campo in CAMPOS_UBICACION
    ):
        return "Completa la ubicación y la dirección del local de votación."

    return None


@app.route("/", methods=["GET", "POST"])
def inicio():
    mensaje_error = None
    mensaje_exito = None
    datos = datos_vacios()

    if request.method == "POST":
        datos = {
            campo: request.form.get(campo, "").strip()
            for campo in TODOS_LOS_CAMPOS
        }
        mensaje_error = validar_registro(datos)

        if not mensaje_error and datos["es_miembro"] == "si":
            dni_repetido = any(
                registro["dni"] == datos["dni"] for registro in registros
            )
            if dni_repetido:
                mensaje_error = "Este DNI ya está registrado en la lista."
            else:
                registros.append(datos.copy())
                mensaje_exito = "Miembro de mesa agregado correctamente."
                datos = datos_vacios()
        elif not mensaje_error:
            mensaje_exito = (
                "El DNI consultado no es miembro de mesa y no se agregó al Excel."
            )
            datos = datos_vacios()

    return render_template(
        "index.html",
        datos=datos,
        registros=registros,
        mensaje_error=mensaje_error,
        mensaje_exito=mensaje_exito,
    )


@app.post("/eliminar/<dni>")
def eliminar_registro(dni):
    for registro in registros:
        if registro["dni"] == dni:
            registros.remove(registro)
            break

    return redirect(url_for("inicio"))


@app.route("/exportar")
def exportar_excel():
    if not registros:
        return render_template(
            "index.html",
            datos=datos_vacios(),
            registros=registros,
            mensaje_error="Agrega al menos un miembro de mesa antes de exportar.",
            mensaje_exito=None,
        ), 400

    libro = Workbook()
    hoja = libro.active
    hoja.title = "Miembros de mesa"

    encabezados = [
        "DNI",
        "Miembro de mesa",
        "Ubicación",
        "Región",
        "Provincia",
        "Distrito",
        "Dirección del local de votación",
    ]
    hoja.append(encabezados)

    for registro in registros:
        hoja.append(
            [
                registro["dni"],
                "Sí",
                *[registro[campo] for campo in CAMPOS_UBICACION],
            ]
        )

    relleno = PatternFill("solid", fgColor="0F766E")
    for celda in hoja[1]:
        celda.font = Font(color="FFFFFF", bold=True)
        celda.fill = relleno
        celda.alignment = Alignment(horizontal="center")

    anchos = [14, 18, 24, 20, 20, 20, 42]
    for columna, ancho in zip("ABCDEFG", anchos):
        hoja.column_dimensions[columna].width = ancho

    ruta_archivo = CARPETA_EXPORTACIONES / "miembros_de_mesa.xlsx"
    libro.save(ruta_archivo)

    return send_file(
        ruta_archivo,
        as_attachment=True,
        download_name="miembros_de_mesa.xlsx",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
