from flask import request, abort
from functools import wraps

def validate_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'entrada' not in request.form or 'tipo' not in request.form:
            abort(400, description="Campos obrigatórios ausentes")
        
        tipo = request.form['tipo']
        if tipo not in ['musica', 'video']:
            abort(400, description="Tipo inválido")
            
        return f(*args, **kwargs)
    return decorated_function
