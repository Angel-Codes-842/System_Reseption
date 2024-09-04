from flask import Flask, render_template, request, redirect, url_for, Response
import sqlite3
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ruta para el formulario de entrada
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/historial', methods=['GET'])
def historial():
    query = request.args.get('query')
    conn = get_db_connection()
    if query:
        records = conn.execute(
            'SELECT * FROM recepcion WHERE nombre LIKE ? OR tipo LIKE ?',
            ('%' + query + '%', '%' + query + '%')
        ).fetchall()
    else:
        records = conn.execute('SELECT * FROM recepcion').fetchall()
    conn.close()
    return render_template('historial.html', records=records)



# Ruta para manejar la recepción del formulario
@app.route('/submit', methods=['POST'])
def submit():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    fecha = request.form['fecha']
    tipo = request.form['tipo']
    accesorio = request.form['accesorio']
    detalles = request.form['detalles']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO recepcion (nombre, telefono, direccion, fecha, tipo, accesorio, detalles) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (nombre, telefono, direccion, fecha, tipo, accesorio, detalles)
    )
    conn.commit()
    record_id = cursor.lastrowid  # Obtiene el ID del último registro insertado
    conn.close()

    # Redirigir a la generación del PDF
    return redirect(url_for('generate_pdf', record_id=record_id))

# Ruta para generar el PDF
@app.route('/generate_pdf/<int:record_id>')
def generate_pdf(record_id):
    conn = get_db_connection()
    record = conn.execute('SELECT * FROM recepcion WHERE id = ?', (record_id,)).fetchone()
    conn.close()

    if record is None:
        return "Registro no encontrado", 404

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    p.drawString(150,780, "ALLNET")
    p.drawString(100,770,"--------------------------------")
    p.drawString(100, 750, f"Nombre: {record['nombre']}")
    p.drawString(100, 730, f"Teléfono: {record['telefono']}")
    p.drawString(100, 710, f"Dirección: {record['direccion']}")
    p.drawString(100, 690, f"Fecha: {record['fecha']}")
    p.drawString(100, 670, f"Tipo: {record['tipo']}")
    p.drawString(100, 650, f"Accesorio: {record['accesorio']}")
    p.drawString(100, 630, f"Condicion o Problema: {record['detalles']}")
    p.drawString(100,590,"COSTO:______________________________")
    p.drawString(100, 560, "NÚMERO PARA CONTACTO: 0975 122 715 - 0975 122 714")
    p.drawString(100, 540, "LINEA BAJA: 0786 233230")

    p.showPage()
    p.save()

    buffer.seek(0)
    return Response(buffer, mimetype='application/pdf', headers={'Content-Disposition': f'attachment; filename=record_{record_id}.pdf'})

if __name__ == '__main__':
    app.run(debug=True)
