import requests
import datetime
import random
import string

from Perfil import Perfil
from Profesor import Profesor
from Estudiante import Estudiante
from Post import Post
from Comentario import Comentario
from Administrador import Administrador
class App(object):
    
    def __init__(self):
        self.lista_perfiles = []
        self.lista_post = []
        self.lista_likes = []
        self.departamentos = []
        self.carreras = []
        self.lista_administradores = [
            Administrador("Antonio1", "antonioguerra@correo.unimet.edu.ve")
        ]
        
    
    def see_api(self):
        link = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/08d4d2ce028692d71e9f8c32ea8c29ae24efe5b1/users.json"
        api = requests.get(link)
        datos = api.json()
        
        for i in datos: 
            lista_id = self.cambiar_id(i['following'],datos)
            if i["type"] == 'professor':
                profesor = Profesor(i['id'], i["firstName"], i["lastName"], i["email"], i["username"], i["type"], i["department"], lista_id )
                self.lista_perfiles.append(profesor)
                if not i["department"] in self.departamentos:
                    self.departamentos.append(i["department"])
               
                
            else:
                estudiante = Estudiante(i['id'], i["firstName"], i["lastName"], i["email"], i["username"], i["type"], i['major'], lista_id)
                self.lista_perfiles.append(estudiante)
                if not i['major'] in self.carreras:
                    self.carreras.append(i)
              
        link2 = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/main/posts.json"
        api2 = requests.get(link2)
        datos2 = api2.json()

        self.cambiar_id_post(datos2)
        for j in datos2: 
                
                post = Post(j["publisher"], j["type"], j["caption"], j["date"], j["tags"], j["multimedia"])
                self.lista_post.append(post)

        return datos, datos2
    

    def cambiar_id(self, id_list,datos):
        lista_id = []
        for i in id_list:
            for j in datos:
                if j['id'] == i:
                    lista_id.append(j['username'])
        return lista_id

    def cambiar_id_post(self, datos2):
        lista_id_post = []
        cont = 0
        for i in datos2:
            for j in self.lista_perfiles:
                if i["publisher"] == j.dni:
                    datos2[cont]["publisher"] =  j.username
            cont += 1   

        return lista_id_post   
    
    def asignar_post(self):
        cont = 0
        for i in self.lista_perfiles:
            for j in self.lista_post:
                if i.username == j.publicador:
                    self.lista_perfiles[cont].publicaciones.append(j)
            cont += 1  

    def start(self):
        self.see_api()
        self.asignar_post()
        user_login = self.login()
        self.menu(user_login)
        self.menu_administrador(user_login)

#--------------------------------------------------------------------------------------------------------------
# METODOS DE GESTION DEL PERFIL:

    def registro_perfil(self): 
        """
        Registro de nuevas personas

        No tiene parametros

        Retorna Nuevo perfil creado
        """
        print("""
----------------
|   Registro   |
----------------
\n--------------------------------\nIngrese los siguientes datos para completar el registro de su cuenta: \n -------------------------------- \n
              """)
        dni = ""
        for _ in range(16):
            dni += random.choice(string.ascii_uppercase + string.digits)
            if len(dni) == 4 or len(dni) == 9 or len(dni) == 14:
                dni += "-"
        nombre = input("Ingrese su nombre: ")
        while not nombre.isalpha():
            nombre = input("Error - 400 Bad Request- \nIngrese nuevamente su nombre: ")
        apellido = input("Ingrese su apellido: ")
        while not apellido.isalpha():
            apellido = input("Error - 400 Bad Request- \nIngrese nuevamente su apellido: ")
        correo = input("Ingrese su correo electronico: ") 
        while not correo.endswith("@correo.unimet.edu.ve"):
            correo = input("Error - 400 Bad Request- \nIngrese nuevamente su correo, pero asegurese que contenga @correo.unimet.edu.ve:\n")
        username = input("Ingrese el Username que quiere: ")
        tipo = input("Usted es: \n1. professor \n2. student: ")
        while not tipo.isnumeric() or not int(tipo) in range(1,3):
            tipo = input("Error - 400 Bad Request- \nIngrese nuevamente, solo un numero: ")
        if tipo == "1":
            departamento = input("Ingrese el departamento donde trabaja: ")
            seguidores = []
            new_profesor = Profesor(dni, nombre, apellido, correo, username,  tipo, departamento, seguidores)
            self.lista_perfiles.append(new_profesor)
            print(new_profesor.nombre, "-", "201 Created \n Bienvenido a Metrogram")
            return new_profesor
        else:
            carrera = input("Ingrese la carrera que esta cursando: ")
            seguidores = []
            new_estudiante = Estudiante(dni, nombre, apellido, correo, username,  tipo, carrera, seguidores)
            self.lista_perfiles.append(new_estudiante)
            print(new_estudiante.nombre, "-", "201 Created \n Bienvenido a Metrogram")
            return new_estudiante


    def cambiar_data(self, user_login): 
        """
        Cambiar los datos de mi mismo perfil

        Argumentos: user_login \ user que inicio seccion

        No retorna nada
        """
        cont = 0 
        for objeto in self.lista_perfiles:
            if objeto.username == user_login:
                break
            cont += 1
             
        opcion = input("""¿Que desea modificar de este perfil?:\n 
            1. Nombre
            2. Apellido
            3. Correo
            4. Username
            5. Carrera/Departamento
            ---> """)
        while not opcion.isnumeric() or int(opcion) and range(1,5):
            opcion = input("Error - 400 Bad Request - Ingrese nuevamente: ")
        if opcion == "1":
            nombre = input("Ingrese un nuevo nombre:\n ")
            self.lista_perfiles[cont] = nombre 
            print("201 Created")
        
        elif opcion == "2":
            apellido = input("Ingrese un nuevo apellido:\n ")
            self.lista_perfiles[cont] = apellido 
            print("201 Created")
        
        elif opcion == "3":
            correo = input("Ingrese un nuevo correo:\n ") #validar correo
            while not "@" in correo:
                correo = input("Error - 400 Bad Request- \nIngrese nuevamente su correo, pero asegurese que contenga @:\n")
            self.lista_perfiles[cont] = correo 
            print("201 Created")
        
        elif opcion == "4":
            username = input("Ingrese un nuevo username:\n ")
            self.lista_perfiles[cont] = username 
            print("201 Created")

        elif opcion == "5":
            if type(self.lista_perfiles[cont]) == Estudiante:
                carrera = input("Ingrese una nueva carrera:\n ")
                self.lista_perfiles[cont] = carrera 
                print("201 Created")
        
            else:
                departamento = input("Ingrese un nuevo departamento:\n ")
                self.lista_perfiles[cont] = departamento
                print("201 Created")


    def eliminar_perfil(self, user_login):
        """
        Elimina la cuenta (objeto) de la lista de perfiles

        Argumentos : user_login \ el user que inicio seccion

        No retorna nada
        """
        cont = 0 
        for objeto in self.lista_perfiles:
            if objeto.username == user_login:
              break
            cont += 1
        self.lista_perfiles.pop(cont)
        print("Se ha borrado exitosamente") 


    def buscar_user(self):
        """
        Aqui se busca por username y se selecciona el deseado

        Argumentos: no hay argumentos

        No retorna 
        """
        perfiles_iguales = []
        buscar = input("\nIngrese el username de la cuenta que desea buscar: \n")
        for i in self.lista_perfiles:
            if buscar in i.username:
                self.perfiles_iguales.append(i)
        cont = 1
        for i in perfiles_iguales:
            print(f"--- Resultados de la busquedad ---\n {cont} {i.username}")
        selec = input("\n Ingrese el numero de la cuenta que desea ingresar: \n--->")
        while not selec.isnumeric() or int(selec) or len(self.perfiles_iguales):
            selec = input("Error - 400 Bad Request - Ingrese nuevamente: ")
        print(self.perfiles_iguales[int(selec)-1].show_perfil())
        cont += 1

        for post in perfiles_iguales[int(selec)-1].publicaciones:
            print(post.multimedia["url"])
    
    def buscar_carrera_departamento(self):
        buscar = input("""\n Usted desea buscar por: \n
                       1. Carrera
                       2. Departamento
                       3. Retroceder
                       ---> """)
        while not buscar.isnumeric() or range(1,3):
            buscar = input("Error - 400 Bad Request - Ingrese nuevamente: ")
        for user in self.lista_perfiles:
            if buscar == "1":
                if user.tipo == "student" and buscar == user.carrera:
                    cont = 0
                    for estudiante in self.carreras: 
                        print(f"{cont} . {estudiante}")
                    print("--- Resultados de la busquedad ---")
                    carrera = input("\n Ingrese el numero de la cuenta que desea ingresar: \n--->")
                    while not carrera.isnumeric() or int(carrera) or carrera < len(self.carreras) and carrera > 0:
                        carrera = input("Error - 400 Bad Request - Ingrese nuevamente: ")
                    mostrar = self.carreras[int(carrera) - 1]
                    carrera_iguales = []
                    for i in self.lista_perfiles:
                        if i.carrera == mostrar:
                            carrera_iguales.append(i)
                    for i in carrera_iguales:
                        print(i.show_perfil())
                    cont += 1
                    post = self.carreras[int(carrera)-1].publicaciones
                    print(post.multimedia["url"])

            elif buscar == "2":
                if user.tipo == "professor" and buscar == user.departamento:
                    cont = 0
                    for profesor in self.departamento: # cambiar a enumerate
                        print(f"{cont} . {profesor}")
                    print("--- Resultados de la busquedad ---")
                    departamento = input("\n Ingrese el numero de la cuenta que desea ingresar: \n--->")
                    while not departamento.isnumeric() or int(departamento) or departamento < len(self.departamento) and departamento > 0:
                        departamento = input("Error - 400 Bad Request - Ingrese nuevamente: ")
                    mostrar = self.departamento[int(departamento) - 1]
                    departamento_iguales = []
                    for i in self.lista_perfiles:
                        if i.departamento == mostrar:
                            departamento_iguales.append(i)
                    for i in departamento_iguales:
                        print(i.show_perfil())
                    cont += 1
                    post = self.carreras[int(departamento)-1].publicaciones
                    print(post.multimedia["url"])

            else:
                break
    
#--------------------------------------------------------------------------------------------------------------------------------------------
#METODOS DE GESTION DE POST

    def mostrar_posts_usuario(self, user_login):
        posts_user_login = [post for post in self.lista_post if post.publicador == user_login]
        if posts_user_login:
            print(f"Posts de {user_login}:")
            for post in posts_user_login:
                print(f"Contenido: {post.show_post()}")
                print(post.multimedia["url"])
        else:
            print(f"No se encontraron posts")

    def montar_post(self, user_login):
        print("""
------------- Publicar un post ----------------
""")
        user = user_login
        tipo = input("1. Foto\n 2. Video\n ")
        descripcion = input("\nIngresa la descripcion del post: \n")
        fecha = self.set_date()
        hashtags = input("Coloque un hashtags #Ejemplo: \n\n")
        while not "#" in hashtags:
            hashtags = input("\nError 400 - Bad request \n Asegurece que tenga #: \n\n")
        multimedia = input("\nIngrese el URL, de su multimedia: \n")
        new_post = Post(user, tipo, descripcion, fecha, hashtags, multimedia)
        self.lista_post.append(new_post)
        print("200 Ok - Create\n\nPost - Creado con exito\n\n")
    
    def modificar_post(self, user_login):
        """
      
    Modifica la información de un post en la lista.

    Argumentos:
    user_login

    No retorna.
        """
        cont = 0 
        for post in self.lista_post:
            if post.publicador == user_login:
                break
            cont += 1
             
        opcion = input("""¿Que desea modificar de este perfil?:\n 
            1. Descripcion
            2. Hashtag
            ---> """)
        while not opcion.isnumeric() or int(opcion) and range(1,2):
            opcion = input("Error - 400 Bad Request - Ingrese nuevamente: ")

        if opcion == "1":
            descripcion = input("Ingrese un nuevo descripcion:\n ")
            self.lista_post[cont] = descripcion 
            print("201 Created")
        
        elif opcion == "2":
            hashtag = input("Ingrese un nuevo hashtag:\n ")
            self.lista_post[cont] = hashtag 
            print("201 Created")
        
    def set_date(self): 
        fechaActual= datetime.datetime.now()
        fechaFormato=datetime.datetime.strftime(fechaActual,"%d/%m/%Y")
        print(f"Fecha de publicacion: {fechaFormato}\n")
        return fechaFormato
    
    def eliminar_post(self, user_login):
        cont = 0 
        for objeto in self.lista_post:
            if objeto.username == user_login:
              break
            cont += 1
            print(f"{cont}.{objeto}")
            cuenta = input("Ingrese el numero del post que desea borrar: ")
            while cuenta.isnumeric() or int(cuenta) and range(len(self.lista_post)):
                cuenta = input("¡Error! Ingrese numeros unicamente: ")   
            cuenta = int(cuenta)
            self.lista_post.pop(cuenta)
            print("Se ha borrado exitosamente") 

    def buscar_hashtags(self):
        hashtags_iguales = []
        buscar = input("Ingrese el hashtags que desea buscar: \n--->")
        for hash in self.lista_post:
            if buscar in hash.hashtag:
                hashtags_iguales.append(hash)
        cont = 0
        for i in hashtags_iguales:
            print("--- Resultados de la busquedad ---")
            print(f"{cont}.{i}")
            hashtags = input("Ingrese el numero del hashtags que desea ingresar: ")
            while not hashtags.isnumeric() or int(hashtags) or hashtags < len(hashtags_iguales) and hashtags > 0:
                hashtags = input("Error - 400 Bad Request - Ingrese nuevamente: ")
            mostrar = hashtags_iguales[int(hashtags) - 1]
            for i in hashtags_iguales:
                if i.hashtags == mostrar:
                    print(i.show_post())
            cont += 1
            post = hashtags_iguales[int(hashtags)-1].publicaciones
            print(post.multimedia["url"])

    def buscar_user_post(self):
        """
        Aqui se busca por username y se selecciona el deseado

        Argumentos: no hay argumentos

        No retorna 
        """
        perfiles_iguales = []
        buscar = input("\nIngrese el username de la cuenta que desea buscar: \n")
        for i in self.lista_perfiles:
            if buscar in i.username:
                self.perfiles_iguales.append(i)
        cont = 1
        for i in perfiles_iguales:
            print(f"--- Resultados de la busquedad ---\n {cont} {i.username}")
        selec = input("\n Ingrese el numero de la cuenta que desea ingresar: \n--->")
        while not selec.isnumeric() or int(selec) or len(self.perfiles_iguales):
            selec = input("Error - 400 Bad Request - Ingrese nuevamente: ")
        print(self.perfiles_iguales[int(selec)-1].show_post())
        cont += 1
        for post in perfiles_iguales[int(selec)-1].publicaciones:
            print(post.multimedia["url"])
            
#-----------------------------------------------------------------------------------------------------------------------------------------
#METODOS DE USUARIO
#COMENTARIOS, LIKES, FOLLOW
    
    def comentar_post(self):
        perfiles_iguales = []
        buscar = input("\nIngrese el username de la cuenta que desea buscar, para comentar: \n")
        for i in self.lista_post:
            if buscar in i.publicador:
                self.perfiles_iguales.append(i)
        cont = 1
        for i in perfiles_iguales:
            print(f"--- Resultados de la busquedad ---\n {cont} {i.publicador}")
        selec = input("\n Ingrese el numero de la cuenta que desea ingresar: \n--->")
        while not selec.isnumeric() or int(selec) or len(self.perfiles_iguales):
            selec = input("Error - 400 Bad Request - Ingrese nuevamente: ")
        print(self.perfiles_iguales[int(selec)-1].show_post())
        cont += 1
      
        count = 0
        index = []
        for i in range(len(self.lista_post)):
            if self.lista_post.publicador == selec:
                index.append(i)
                print(f"{count}. {self.lista_post[i].show_post()}")
                count += 1
   
        for post in self.lista_post:
            print(f"{cont}.{post.show_post()}")
        cont += 1
        comentar = input("Ingrese el numero del post que desea comentar: ")
        while comentar.isnumeric() or int(comentar) and range(len(self.lista_post)):
            comentar = input("Error - 400 Bad Request - Ingrese nuevamente: ")  

        index_post = index[int(comentar)]
        self.lista_post[index_post].show_post() 
        user = selec
        post = comentar
        fecha = self.set_date()
        comentario = input("Ingrese el comentario: ")
        new_comentario = Comentario(comentario, user, post, fecha)
        self.comentarios.append(new_comentario)
    
    def eliminar_comentario(self):
        pass

    def follow(self):
        pass

    def dejar_seguir(self):
        pass

    def dar_like(self):
        pass

   

#-------------------------------------------------------------------------------------------------------------------------------
#ESTADISTICA

    def mayor_cantidad_post(self):
        max_publicaciones = []
        for post in self.lista_post:
            usuario = post.publicador
            encontrado = False
            for i in max_publicaciones:
                if i[0] == usuario:
                    i[1] += 1
                    encontrado = True
                    break
                if not encontrado:
                    max_publicaciones.append([usuario, 1])
        print("Usuarios con mayor cantidad de publicaciones:")
        for usuario, cantidad in sorted(max_publicaciones, key=lambda x: x[1], reverse=True):
            print(f"{usuario}: {cantidad} publicaciones")
    
    def max_carreras(self):
        max_carreras = []
        carreras = [perfil.carrera for perfil in self.lista_perfiles]

        for carrera in carreras:
            cantidad_publicaciones = sum(1 for post in self.lista_post if post.usuario in [perfil.usuario for perfil in self.lista_perfiles if perfil.carrera == carrera])
            max_carreras.append([carrera, cantidad_publicaciones])

        if max_carreras:
            carrera_max_publicaciones = max(max_carreras, key=lambda x: x[1])
            print(f"\nLa carrera con mayor cantidad de publicaciones es: {carrera_max_publicaciones[0]} con {carrera_max_publicaciones[1]} publicaciones")
        else:
            print("\nNo hay publicaciones para mostrar.")

    def info_moderacion_usuario(self):
        usuarios_bajados = []
        for post in self.lista_post:
            if post.tipo == "eliminado":
                usuario = post.publicador
                encontrado = False
                for usuario_info in usuarios_bajados:
                    if usuario_info[0] == usuario:
                        usuario_info[1] += 1
                        encontrado = True ####
                        break
                if not encontrado:
                    usuarios_bajados.append([usuario, 1])
        print("\nUsuarios con la mayor cantidad de posts tumbados:")
        for usuario, cantidad in sorted(usuarios_bajados, key=lambda x: x[1], reverse=True):
            print(f"{usuario}: {cantidad} posts tumbados")


    def info_hashtags_moderacion(self):
        hashtags_comentarios_inadecuados = []
        for post in self.lista_post:
            if post.tipo == "comentario inadecuado":
                hashtags = post.hashtag
                for hashtag in hashtags: ###
                    encontrado = False
                    for hashtag_info in hashtags_comentarios_inadecuados:
                        if hashtag_info[0] == hashtag:
                            hashtag_info[1] += 1
                            encontrado = True
                            break
                    if not encontrado:
                        hashtags_comentarios_inadecuados.append([hashtag, 1])
        print("\nHashtags con mayor cantidad de comentarios inadecuados:")
        for hashtag, cantidad in sorted(hashtags_comentarios_inadecuados, key=lambda x: x[1], reverse=True):
            print(f"{hashtag}: {cantidad} comentarios inadecuados")

    def info_usuario_eliminado(self):
        usuarios_eliminados = [post.publicador for post in self.lista_post if post.tipo == "eliminado_por_infraccion"]
        print("\nUsuarios eliminados por infracciones:")
        for usuario in usuarios_eliminados:
            print(usuario) 
#----------------------------------------------------------------------------------------------------------------------------------------------       
#METODOS DE ADMI
    
    def menu_administrador(self, user_login):
        while True:
            print("""
--------------------------------------------
|      M E T R O G R A M   A D M I         |
--------------------------------------------
            BIENVENIDO ANTONIO
                    \n""")

            option = input("""
                    1. Eliminar post
                    2. Eliminar comentario
                    3. Eliminar cuenta
                    4. Salir
                                    """)
            while not option.isnumeric() or int(option) not in range(1, 4):
                option = input("Error - 400 Bad Request- \nIngrese nuevamente, solo numero: ")
            if option == "1":
                self.eliminar_post_admi()
            elif option == "2":
                self.eliminar_comentario_admi()
            elif option == "3":
                self.eliminar_usuario_admi
            else:
                break

    def eliminar_post_admi(self):
        cont = 0 
        for post in self.lista_post:
            print(f"{cont}.{post.show_post()}")
        cont += 1
        post = input("Ingrese el numero del post que desea borrar: ")
        while post.isnumeric() or int(post) and range(len(self.lista_post)):
            cuenta = input("Error - 400 Bad Request- \nIngrese nuevamente, solo numero:")   
        self.lista_post.pop(cuenta)
        print("200 ok - Borrado") 

    def eliminar_comentario_admi(self):
        cont = 0 
        for post in self.lista_post:
            print(f"{cont}.{post.show_post()}")
        cont += 1
        post = input("Ingrese el numero del post en el que desea borrar un comentario: ")
        while post.isnumeric() or int(post) and range(len(self.lista_post)):
            cuenta = input("Error - 400 Bad Request- \nIngrese nuevamente, solo numero:")   
        
        comentario = int(cuenta)
        ver = self.lista_post[comentario]

        aux = 0
        for i in range(len(ver.comentarios)):
            print(f"{aux}.{ver.comentarios}")
        aux += 1

        eliminar = input("Ingrese el numero del comentario que quiere seleccinar para borrar /n:")
        while eliminar.isnumeric() or int(eliminar) and range(len(ver.comentarios)):
            eliminar = input("Error - 400 Bad Request- \nIngrese nuevamente, solo numero:")  
        ver.comentarios.pop(eliminar)
    
    def eliminar_usuario_admi(self):
        cont = 0
        for user in self.lista_perfiles:
            print(f"--- Resultados de la busquedad ---\n {cont}.{user}")
        cont +=1
        selec = input("\n Ingrese el numero de la cuenta que desea borrar: \n--->")
        while not selec.isnumeric() or int(selec) or len(self.lista_perfiles):
            selec = input("Error - 400 Bad Request - Ingrese nuevamente: ")
        self.lista_perfiles.pop(selec)
        print("200 ok - Borrado") 


#----------------------------------------------------------------------------------------------------------------------------------------------
#LOG IN 
#ADMINISTRADOR : Antonio1
#USUARIO : Hernan2
    def login(self):

        """
        Inicio del programa 

        Argumentos: Lista de perfiles

        Retorna usario 
        """
        while True:

            print("""

                ___________________________________________________________________
                
                |            B I E N V E N I D O   A   M E T R O G R A M           |
                ___________________________________________________________________ 
                                
                                    -------------------------
                                    | 1 - Iniciar seccion   |
                                    -------------------------
                                            
                                        ----------------
                                        | 2 - Registrar |
                                        ----------------
                
                                        ----------------
                                        | 3 - Salir    |
                                        ----------------

    """)

            option = input("Ingrese una opcion: ")
            while not option.isnumeric() or int(option) not in range(1, 4):
                option = input("\nError - 400 Bad Request- \nIngrese nuevamente, solo numeros: ")
            if option == "1":
                username = input("\nIngrese su username: \n---> ").lower()
                encontrado = False
                for i in self.lista_perfiles:
                    if i.username.lower() == username:
                        user_login = i.username
                        encontrado = True
                        return user_login
                
                if encontrado == False:
                    for i in self.lista_administradores:
                        if i.username.lower() == username:
                            user_login = i.username 
                            encontrado = True
                            self.menu_administrador()
                            return user_login
                
                        else:
                            print("\nError 404 - not found \nEl usario ingresado no ha sido encontrado, procederemos a registrarlo \n")
                            nuevo_registro = self.registro_perfil()
                            self.lista_perfiles.append(nuevo_registro)
                            user_login = nuevo_registro.username 
                            return user_login
                    
            elif option == "2":
                nuevo_registro = self.registro_perfil()
                self.lista_perfiles.append(nuevo_registro)
                user_login = nuevo_registro.username
                print("200 - Ok")
                return user_login
            
            else:
                print("""---Usted salio de Metrogram---
                                VUELVA PRONTO
                        """)
                break
    

#--------------------------------------------------------------------------------------------------------------------------------------------
    def menu(self, user_login):
        while True:
            print("""
            --------------------------------------------
            |             M E T R O G R A M            |
            --------------------------------------------
                    \n""")
            option = input("""
            1. Mi perfil
            2. Buscar
            3. Estadistica
            4. Interacciones
            5. Salir

                            """)
            while not option.isnumeric() or int(option) not in range(1, 6):
                option = input("Error - 400 Bad Request- \nIngrese nuevamente, solo numero: ")
            if option == "1":
                while True:
                    option = input("""
            1. Ver mis publicaciones 
            2. Editar Perfil
            3. Publicar un post
            4. Eliminar mi cuenta
            5. Retroceder

                    """)
                    while not option.isnumeric() or int(option) not in range(1, 6):
                        option = input("Error - 400 Bad Request- \nIngrese nuevamente, solo numero: ")
                    if option == "1":
                        self.mostrar_posts_usuario(user_login)
                        while True:
                            option = input("""
            1. Eliminar post
            2. Eliminar comentario
            3. Modificar informacion del post
            4. Retroceder
                            """)
                            while not option.isnumeric() or int(option) not in range(1, 5):
                                option = input("Error - 400 Bad Request- \nIngrese nuevamente, solo numero: ")
                            if option == "1":
                                self.eliminar_post()
                            elif option == "2":
                                self.eliminar_comentario()
                            elif option == "3":
                                self.modificar_post()
                            else:
                                break
                    
                    elif option == "2":
                        self.cambiar_data(user_login)

                    elif option == "3":
                        self.montar_post(user_login)

                    elif option == "4":
                        self.eliminar_perfil()
                    
                    else:
                        break                 

            elif option == "2":
                while True:
                    option = input("""
                                
        1. Buscar username
        2. Buscar carrera / departamento
        3. Buscar #Hashtags
        4. Buscar usuario desde un post
        5. Retroceder                       
                                
                        """)
                    while not option.isnumeric() or int(option) not in range(1, 7):
                        option = input("Error - 400 Bad Request- \nIngrese nuevamente, solo numero: ")
                    if option == "1":
                        self.buscar_user()
                    
                    elif option == "2":
                        self.buscar_carrera_departamento()


                    elif option == "3":
                        self.buscar_hashtags()


                    elif option == "4":
                        self.buscar_user_post()

                    else:
                        break

            elif option == "3":
                option = input("""
        1. Informes de publicaciones
        2. Informes de interaccion
        3. Informes de moderacion
        4. Graficos
        5. Retroceder
                                """)
                while not option.isnumeric() or int(option) not in range(1, 5):
                    option = input("Error - 400 Bad Request- \nIngrese nuevamente, solo numero: ")
                if option == "1":
                    while True:
                        option = input("""
        1. Informes de usuarios con mayor numero de publicaciones
        2. Informes de carreras con mayor numero de publicaciones
        3. Retroceder
        """) 
                        while not option.isnumeric() or int(option) not in range(1, 5):
                            option = input("Error - 400 Bad Request- \nIngrese nuevamente, solo numero: ")
                        if option == "1":
                            self.mayor_cantidad_post()
                        
                        elif option == "2":
                            self.max_carreras()
                        
                        else: 
                            break

                elif option == "2":
                    self.max_interadores()

                elif option == "3":
                    while True:
                        option = input("""
        1. Usuarios con la mayor cantidad de post tumbados
        2. Hashtags con mayor comentarios inadecuados.
        3. Usuarios eliminados por infracciones.
        4. Retroceder
        """) 
                        while not option.isnumeric() or int(option) not in range(1, 4):
                            option = input("Error - 400 Bad Request- \nIngrese nuevamente, solo numero: ")
                        if option == "1":
                            self.info_moderacion_usuario()
                        
                        elif option == "2":
                            self.info_hashtags_moderacion()
                        
                        elif option == "3":
                            self.info_usuario_eliminado

                        else: 
                            break
                elif option == "4":
                    pass

                else:
                    break

            elif option == "4":
                while True:
                    option = input("""
        1. Comentar Post
        2. Dar like
        3. Segruir
        4. Dejar de seguir
        5. Retroceder
                                    """) 
                    while not option.isnumeric() or int(option) not in range(1, 4):
                        option = input("Error - 400 Bad Request- \nIngrese nuevamente, solo numero: ")
                    if option == "1":
                        self.comentar_post()
                    
                    elif option == "2":
                        self.dar_like()
                    
                    elif option == "3":
                        self.follow()

                    elif option == "4":
                        self.dejar_seguir()
                    else: 
                        break
                
            else:
                break
                 

#------------------------------
        
            



    


        
    

        
    

        
    





        




    

        





    

        


    

        



    

        

    




        


    

        
    

        
    



        
    
