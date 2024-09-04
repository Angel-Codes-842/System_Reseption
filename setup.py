from cx_Freeze import setup, Executable

setup(
    name="mi_aplicacion",
    version="0.1",
    description="Mi aplicación Flask",
    executables=[Executable("app.py")],  
    options={
        'build_exe': {
            'include_files': ['database.db', 'templates/'],  
        }
    }
)