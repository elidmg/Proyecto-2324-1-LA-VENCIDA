class Comentario:
    def __init__(self, comentario, user, post, fecha):
        self.comentario = comentario
        self.user =  user
        self.post =  post
        self.fecha = fecha

    def show_comentario(self):
        return f"""
    COMENTARIO: {self.comentario}
    USER: {self.user}
    POST: {self.post}
    FECHA: {self.fecha}

"""
        