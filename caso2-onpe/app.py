from flask import Flask, render_template, request


app = Flask(__name__)
registros = []

CAMPOS = ["dni", "ubicacion", "region", "provincia", "distrito", "direccion"]


def validar_registro(datos):
    if any(not datos[campo] for campo in CAMPOS):
        return "Completa todos los campos."

    if not datos["dni"].isdigit() or len(datos["dni"]) != 8:
        return "El DNI debe contener exactamente 8 dígitos."

    return None


@app.route("/", methods=["GET", "POST"])
def inicio():
    mensaje_error = None
    mensaje_exito = None
    datos = {campo: "" for campo in CAMPOS}

    if request.method == "POST":
        datos = {
            campo: request.form.get(campo, "").strip()
            for campo in CAMPOS
        }
        mensaje_error = validar_registro(datos)

        if not mensaje_error:
            registros.append(datos.copy())
            mensaje_exito = "Resultado electoral registrado correctamente."
            datos = {campo: "" for campo in CAMPOS}

    return render_template(
        "index.html",
        datos=datos,
        registros=registros,
        mensaje_error=mensaje_error,
        mensaje_exito=mensaje_exito,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
