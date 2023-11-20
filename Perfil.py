class Perfil:
    def __init__(self, dni, nombre, apellido, correo, username, tipo):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.username = username
        self.tipo = tipo
        self.publicaciones = []
        
    def show_perfil(self):
        return f"""
    ID : {self.dni}
    NOMBRE : {self.nombre}
    APELLIDO : {self.apellido}
    CORREO: {self.correo}
    USUARIO : {self.username}
    TIPO : {self.tipo}
"""