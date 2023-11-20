class Post:
    def __init__(self, publicador, tipo, descripcion, fecha, hashtag, multimedia):
        self.publicador = publicador
        self.tipo = tipo
        self.multimedia = multimedia
        self.descripcon = descripcion
        self.hashtag = hashtag
        self.fecha = fecha
        self.likes = []
        self.comentarios = []

        
    def show_post(self):
        return f"""
        USUARIO: {self.publicador}
        TIPO:   {self.tipo}
        DESCRIPCION: {self.descripcon}
        FECHA: {self.fecha}
        HASHTAGS: {self.hashtag}
        MULTIMEDIA: {self.multimedia}
        LIKES: {self.likes}
        COMENTARIOS: {self.comentarios}
    """