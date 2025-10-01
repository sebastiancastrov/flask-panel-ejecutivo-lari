from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_super_segura'

# Usuarios permitidos
USUARIOS = {
    'EJIMENEZ': 'LARI2025',
    'ETAMAYO': 'LARI2025',
    'FPIMENTEL': 'LARI2025',
    'IFERRADA': 'LARI2025',
    'YNUÑEZ': 'LARI2025',
    'SCASTRO': 'LARI2025',
    'HGOMEZ': 'LARI2025',
    'FMORALES': 'LARI2025',
    'JFILLA': 'LARI2025'
}

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# Estructura de categorías, subcategorías y reportes
REPORTES = {
    'operaciones': {
        'SOC': [
            {'nombre': 'Antihurto', 'url': None},
            {'nombre': 'Empalmes', 'url': None},
            {'nombre': 'Medición', 'url': None},
            {'nombre': 'Corte y Reposición', 'url': None}
        ],
        'Servicios eléctricos': [
            {'nombre': 'Mantenimiento aéreo', 'url': None},
            {'nombre': 'Mantenimiento subterráneo', 'url': None},
            {'nombre': 'Poda', 'url': "https://app.powerbi.com/view?r=eyJrIjoiM2RhZTA5YmUtYzNmNS00MTIyLThjMDEtZDEyZWIzMzA5YzZkIiwidCI6ImM5ZDQ1YjZlLTIxY2EtNGY1MC05YWM2LWE4NWMzMzQzNTgzOCIsImMiOjR9"},
            {'nombre': 'Obras eléctricas', 'url': None}
        ],
        'Servicios de emergencias': [
            {'nombre': 'Servicios de emergencias', 'url': 'https://app.powerbi.com/view?r=eyJrIjoiMzk3MDJlODYtNWQwYy00YzgyLWI0NWQtMDVlNTAyMTk2YWNjIiwidCI6ImM5ZDQ1YjZlLTIxY2EtNGY1MC05YWM2LWE4NWMzMzQzNTgzOCIsImMiOjR9&pageName=ReportSection'}
        ],
        'Obras civiles': [
            {'nombre': 'Obras civiles', 'url': None}
        ]
    },
    'recursos_humanos': [
        {'nombre': 'Horas Extras', 'url': 'https://app.powerbi.com/view?r=eyJrIjoiODEyMDg2ZTYtMjc5ZC00YTBmLWFhZDYtY2IxYWIxNzg5ZWIyIiwidCI6ImM5ZDQ1YjZlLTIxY2EtNGY1MC05YWM2LWE4NWMzMzQzNTgzOCIsImMiOjR9&pageName=fdff25b40e362aacd30a'},
        {'nombre': 'Bonos', 'url': None},
        {'nombre': 'Compensados', 'url': None},
        {'nombre': 'Dotación', 'url': None},
        {'nombre': 'Ingresos - Egresos de personal', 'url': None},
        {'nombre': 'Amonestaciones', 'url': None}
    ],
    'prevencion_de_riesgos': [
        {'nombre': 'Inspecciones de seguridad', 'url': 'https://app.powerbi.com/view?r=eyJrIjoiZTk5NGQwYjUtMzFmNy00MTEzLWI1NWMtMmRiMzMzZDRlNWU4IiwidCI6ImM5ZDQ1YjZlLTIxY2EtNGY1MC05YWM2LWE4NWMzMzQzNTgzOCIsImMiOjR9'},
        {'nombre': 'Accidentes e incidentes', 'url': 'https://app.powerbi.com/view?r=eyJrIjoiNGE4NDJmZmQtYzYwYy00MTJjLThlNjgtYjhjODIwNjk5YzY2IiwidCI6ImM5ZDQ1YjZlLTIxY2EtNGY1MC05YWM2LWE4NWMzMzQzNTgzOCIsImMiOjR9'},
        {'nombre': 'Estado de documentos', 'url': 'https://app.powerbi.com/view?r=eyJrIjoiNzk2Nzk4ZTgtZmNhMC00MDNiLTg0MmEtN2YxYmUwNjU0MDAyIiwidCI6ImM5ZDQ1YjZlLTIxY2EtNGY1MC05YWM2LWE4NWMzMzQzNTgzOCIsImMiOjR9'}
    ],
    'cadena_de_suministro': [
        {'nombre': 'Flota', 'url': 'https://app.powerbi.com/view?r=eyJrIjoiOGJmYmQ1OGMtOTJjOC00NWM2LWJhMmEtYTI4OTE2YmJiNzQyIiwidCI6IjFhNWRmM2U0LTBiYzgtNDVhNi05MGM0LTZhYzkyOWMzNGRmOCJ9'},
        {'nombre': 'Movimiento de unidades (Km)', 'url': 'https://app.powerbi.com/view?r=eyJrIjoiM2VkNWU3OTYtMzA5NS00OGY0LWI5MzAtMDRlMTg4NjZiMmI0IiwidCI6IjFhNWRmM2U0LTBiYzgtNDVhNi05MGM0LTZhYzkyOWMzNGRmOCJ9'},
        {'nombre': 'Equipamientos y materiales dieléctricos certificados', 'url': 'https://app.powerbi.com/view?r=eyJrIjoiNTlhZTRmNDAtNjU3ZC00Njg2LTgzZmQtYjBiOTg3ZmQzOTQwIiwidCI6IjFhNWRmM2U0LTBiYzgtNDVhNi05MGM0LTZhYzkyOWMzNGRmOCJ9'},
        {'nombre': 'Exceso de velocidad', 'url': 'https://app.powerbi.com/view?r=eyJrIjoiMWVkNzEyY2QtZDRkZi00NmE4LWJiZjAtNjE3MDEzZDQzOTA3IiwidCI6IjFhNWRmM2U0LTBiYzgtNDVhNi05MGM0LTZhYzkyOWMzNGRmOCJ9'},
        {'nombre': 'Fuera de Horario', 'url': 'https://app.powerbi.com/view?r=eyJrIjoiMDMzOWZjM2UtMjgzNy00M2JjLTg0OWUtM2YzZmRiMjRkZmU5IiwidCI6IjFhNWRmM2U0LTBiYzgtNDVhNi05MGM0LTZhYzkyOWMzNGRmOCJ9'},
        {'nombre': 'GPS inactivo', 'url': 'https://app.powerbi.com/view?r=eyJrIjoiMzQzYmViOTUtYzM3Yi00MTEyLWE5MWYtNWM5OTU1MGI0OWI2IiwidCI6IjFhNWRmM2U0LTBiYzgtNDVhNi05MGM0LTZhYzkyOWMzNGRmOCJ9'},
        {'nombre': 'Combustible', 'url': 'https://app.powerbi.com/view?r=eyJrIjoiYmRiNDZiZDMtOGU5My00N2Q5LWFjZGItYzE3MmVhYmM1YzQ3IiwidCI6IjFhNWRmM2U0LTBiYzgtNDVhNi05MGM0LTZhYzkyOWMzNGRmOCJ9'}
    ],
    'oficina_tecnica': [
        {'nombre': 'Facturación', 'url': 'https://app.powerbi.com/view?r=eyJrIjoiOGRmODcwMTItOThkMi00ZDhlLWE4NTYtZmI3ZmQzMDBkZTBiIiwidCI6ImM5ZDQ1YjZlLTIxY2EtNGY1MC05YWM2LWE4NWMzMzQzNTgzOCIsImMiOjR9&pageName=1c559b81a2c1ecdec51e'},
        {'nombre': 'Consumo de materiales', 'url': 'https://app.powerbi.com/view?r=eyJrIjoiM2U4NWVjMjctNjMwMi00N2MzLTkzZjQtNDk4Nzk3NDgzODk3IiwidCI6ImM5ZDQ1YjZlLTIxY2EtNGY1MC05YWM2LWE4NWMzMzQzNTgzOCIsImMiOjR9'},
        {'nombre': 'Pendiente de Cobro Oficina Técnica', 'url': 'https://app.powerbi.com/view?r=eyJrIjoiMzZhNjY3MWEtNTVjZi00OTI1LTgxM2MtYTVmMjg3NjIyNzZhIiwidCI6ImM5ZDQ1YjZlLTIxY2EtNGY1MC05YWM2LWE4NWMzMzQzNTgzOCIsImMiOjR9'},
        {'nombre': 'E-Control', 'url': "https://app.powerbi.com/view?r=eyJrIjoiYWM5MGUzNDEtMzRlYS00MzNjLTgzODQtMWQwYWJmY2RiMmZjIiwidCI6IjZiMTY5NjM0LWZkY2EtNGM5Ny1hZDBmLWEyMjk0YzcxODdhNyIsImMiOjR9"},
        
        # 🔹 Nuevos reportes
        {'nombre': 'Control CRO', 'url': 'https://app.powerbi.com/view?r=eyJrIjoiM2U2NzExNjktODhlMi00NzM4LWJjOWUtMzliMzcyMzlhODIwIiwidCI6ImM5ZDQ1YjZlLTIxY2EtNGY1MC05YWM2LWE4NWMzMzQzNTgzOCIsImMiOjR9'},
        {'nombre': 'Control Solicitud List', 'url': 'https://app.powerbi.com/view?r=eyJrIjoiOGZlODAyYmMtMjUxZC00Yjc0LThiNjctYzA3MTE1YWRmMjk4IiwidCI6ImM5ZDQ1YjZlLTIxY2EtNGY1MC05YWM2LWE4NWMzMzQzNTgzOCIsImMiOjR9'}
    ]
}

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usuario = request.form['usuario'].upper()
        password = request.form['password']
        if usuario in USUARIOS and USUARIOS[usuario] == password:
            session['usuario'] = usuario
            return redirect(url_for('portada'))
        else:
            error = 'Usuario o contraseña incorrectos'
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/portada')
@login_required
def portada():
    return render_template('portada.html')

@app.route('/categoria/<categoria>')
@login_required
def categoria(categoria):
    data = REPORTES.get(categoria)
    return render_template('categoria.html', categoria=categoria, data=data)

@app.route('/subcategoria/<categoria>/<subcategoria>')
@login_required
def subcategoria(categoria, subcategoria):
    data = REPORTES[categoria][subcategoria]
    return render_template('subcategoria.html', categoria=categoria, subcategoria=subcategoria, data=data)

@app.route('/reporte')
@login_required
def reporte():
    url = request.args.get('url')
    volver_a = request.args.get('volver_a', url_for('portada'))
    return render_template('reporte.html', url=url, volver_a=volver_a)

if __name__ == '__main__':
    app.run(debug=True)
