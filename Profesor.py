from Perfil import Perfil

class Profesor(Perfil):
    def __init__(self, dni, nombre, apellido, correo, username,  tipo, departamento, seguidores):
        super().__init__(dni, nombre, apellido, correo, username, "professor")
        self.tipo = tipo
        self.departamento = departamento
        self.seguidores = seguidores
        self.publicaciones = []

    def show_profesor(self):
        return f"""
        ID : {self.dni}
        NOMBRE : {self.nombre}
        APELLIDO : {self.apellido}
        CORREO: {self.correo}
        USUARIO : {self.username}
        TIPO : {self.tipo}
        DEPARTAMENTO : {self.carrera}
        SEGUIDORES : {self.seguidores}
        PUBLICACIONES : {self.publicaciones}
"""