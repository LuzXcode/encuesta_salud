from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resultado', methods=['POST'])
def resultado():
    datos = request.form.to_dict()

    # Guardar en CSV
    archivo = 'respuestas.csv'
    existe = os.path.isfile(archivo)
    with open(archivo, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=datos.keys())
        if not existe:
            writer.writeheader()
        writer.writerow(datos)

    # Analizar riesgos y protecciones
    riesgo = []
    try:
        horas = int(datos.get('horas_pantalla', 0))
        if horas > 5:
            riesgo.append("Exceso de tiempo frente a pantallas (>5h/día)")
    except:
        pass
    if datos.get('pantallas_comida') == 'sí':
        riesgo.append("Uso de pantallas durante las comidas")
    if datos.get('comparacion') == 'sí':
        riesgo.append("Comparación frecuente con otros en redes")
    if datos.get('ansiedad') == 'sí':
        riesgo.append("Ansiedad o tristeza después de redes")
    if datos.get('presion') == 'sí':
        riesgo.append("Presión por cumplir estereotipos")
    if datos.get('distraccion') == 'sí':
        riesgo.append("Distracción con el celular al comer")
    if datos.get('comer_rapido') == 'sí':
        riesgo.append("Comer rápido o en exceso")
    if datos.get('saltarse') == 'sí':
        riesgo.append("Saltarse comidas por redes/juegos")
    if datos.get('restriccion') == 'sí':
        riesgo.append("Restricciones alimentarias (dietas)")
    if datos.get('alimentacion') == 'deficiente':
        riesgo.append("Alimentación deficiente")
    if datos.get('valioso') == 'no':
        riesgo.append("Baja autoestima")
    if datos.get('satisfaccion', '').lower() in ['mala', 'pobre', 'insatisfecho']:
        riesgo.append("Insatisfacción corporal")
    if datos.get('percepcion', '').lower() in ['sobrepeso', 'delgado', 'obeso']:
        riesgo.append("Percepción corporal negativa")
    if datos.get('burlas') == 'sí':
        riesgo.append("Ha recibido burlas por su cuerpo")
    if datos.get('rechazo') == 'sí':
        riesgo.append("Se siente rechazado o excluido")
    if datos.get('evita_comer') == 'sí':
        riesgo.append("Evita comer en público")

    proteccion = []
    if datos.get('comunicacion') == 'sí':
        proteccion.append("Buena comunicación familiar durante comidas")
    if datos.get('actividad') == 'sí':
        proteccion.append("Actividad física regular")
    if datos.get('apoyo_familiar') == 'sí':
        proteccion.append("Recibe apoyo escolar/familiar")
    if datos.get('actividades_fuera') == 'sí':
        proteccion.append("Participa en actividades fuera de pantallas")

    return render_template('resultado.html',
                           nombre=datos.get('nombre'),
                           apellido=datos.get('apellido'),
                           genero=datos.get('genero'),
                           edad=datos.get('edad'),
                           alimentacion=datos.get('alimentacion'),
                           tension_sist=datos.get('tension_sist'),
                           tension_diast=datos.get('tension_diast'),
                           riesgo=riesgo,
                           proteccion=proteccion)

if __name__ == '__main__':
    # Para producción: host='0.0.0.0', debug=False
    app.run(host='0.0.0.0', port=5000, debug=True)
