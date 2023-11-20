from Perfil import Perfil

class Estudiante(Perfil):
    def __init__(self, dni, nombre, apellido, correo, username,  tipo, carrera, seguidores):
        super().__init__(dni, nombre, apellido, correo, username, "student")
        self.tipo = tipo
        self.carrera = carrera
        self.seguidores = seguidores
        self.publicaciones = []

    def show_estudiante(self):
        return f"""
        ID : {self.dni}
        NOMBRE : {self.nombre}
        APELLIDO : {self.apellido}
        CORREO: {self.correo}
        USUARIO : {self.username}
        TIPO : {self.tipo}
        CARRERA : {self.carrera}
        SEGUIDORES : {self.seguidores}
        PUBLICACIONES : {self.publicaciones}
"""