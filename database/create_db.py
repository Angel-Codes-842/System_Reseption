import sqlite3

# Conectar a la base de datos SQLite (o crearla si no existe)
conn = sqlite3.connect("database.db")

# Crear un objeto cursor usando la conexión
c = conn.cursor()

# Ejecutar el comando SQL para crear la tabla
try:
    c.execute(
        """CREATE TABLE recepcion (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            telefono TEXT,
            direccion TEXT,
            fecha DATE,
            tipo TEXT,
            accesorio TEXT,
            detalles TEXT,
            entregado INTEGER DEFAULT 0
        )"""
    )
    print("Tabla creada exitosamente.")
except sqlite3.OperationalError as e:
    print(f"Error al crear la tabla: {e}")

# Confirmar los cambios
conn.commit()

# Cerrar la conexión
conn.close()