from tkinter import ttk
from tkinter import *
import sqlite3


# En este caso no se externaliza con otro fichero models.py las clases y objetos porque hay poco codigo
# ( y no es un proyecto que crecerá)
class Producto:
    db = "database/productos.db"

    def __init__(self, root):  # le agregamos la interfaz grafica a la clase producto que es quien inicializa la misma.
        self.ventana = root  # En esta variable se configura desde dentro de la clase la ventana grafica. Siempre tiene que estar vinculada a la clase prncipal
        self.ventana.title("APP Gestor de Productos")
        self.ventana.resizable(1, 1)  # sirve para redimensionar la ventana. 0,0 es cuando no se puede redimensionar.
        self.ventana.wm_iconbitmap("recursos/M6_P2_icon2.ico")  # Es un comando para Windows para ponerle icono a la ventana de la App.


        # Creación del contenedor Frame principal
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto", font=('Arial Black', 16, 'bold'), relief="groove", bg="#2F4F4F", fg="#DCDCDC")
        frame.grid(row=0, column=0,columnspan=3, sticky="nsew")#columnspan sirve para decirle cuantas columnas quiero que tenga el frame.
        # pady es la separacion entre columnas del frame.
        #Imagen de logo APP # no lo pude acomodar a la derecha del Frame principal sin que afectara espacios en los campos de input.
        #self.imagen_gestor = PhotoImage(file="recursos/Imagen Original.png")
        #self.imagen_gestor2 = Label(frame, image=self.imagen_gestor).grid(row=0, column=1, pady=1)


        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=("Arial", 13),bg="#2F4F4F", fg="#DCDCDC")
        self.etiqueta_nombre.grid(row=1, column=0, sticky="e", padx=10, pady=3)

        # Entry Nombre
        self.nombre = Entry(frame, font=("Arial", 13))
        self.nombre.focus()  # Es para que el cursor se situe dentro del cajon se texto. A eso se le llama foco.
        self.nombre.grid(row=1, column=1, sticky="w", padx=10, pady=3)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ", font=("Arial", 13), bg="#2F4F4F", fg="#DCDCDC")
        self.etiqueta_precio.grid(row=2, column=0, sticky="e", padx=10, pady=3)
        # Entry Precio
        self.precio = Entry(frame, font=('"Arial"', 13))
        self.precio.grid(row=2, column=1, sticky="w", padx=10, pady=3)

        #Label Stock
        self.etiqueta_cantidad = Label(frame, text="Cantidad: ", font=('"Arial"', 13), bg="#2F4F4F", fg="#DCDCDC")
        self.etiqueta_cantidad.grid(row=3, column=0, sticky="e", padx=10, pady=3)
        #Entry Stock
        self.cantidad = Entry(frame, font=('"Arial"', 13))
        self.cantidad.grid(row=3, column=1, sticky="w", padx=10, pady=3)

        # Label Categoria
        self.etiqueta_categoria = Label(frame, text="Categoria: ", font=("Arial", 13), bg="#2F4F4F", fg="#DCDCDC")
        self.etiqueta_categoria.grid(row=4, column=0, sticky="e", padx=10, pady=3)
        # Select Categoria  >> Esta opcion no será obligatorio introducirla.
        self.categoria = ttk.Combobox(frame, font=("Arial", 13), width=18, style="mystyle.TCombobox")
        self.categoria["values"] = ("Sin seleccionar","Libreria", "Tecnología", "Otros")
        self.categoria.current(0)
        self.categoria.grid(row=4, column=1, sticky="w", padx=10, pady=3)

        # Boton de Añadir Producto
        s = ttk.Style()
        s.map("my.TButton",
                  foreground=[('pressed', 'blue'), ('active', 'black')],
                  background=[('pressed', '!disabled', 'white'), ('active', 'yellow')]
                  )
        s.configure('my.TButton', font=("Arial", 12, 'bold'), foreground="#2F4F4F", background="#DCDCDC", relief="flat")
        self.boton_aniadir = ttk.Button(frame, text="GUARDAR PRODUCTO", command=self.add_producto, style="my.TButton") #OJO add.producto es un metodo pero aqui en Command va sin parentesis.!!
        self.boton_aniadir.grid(row=5, columnspan=4, sticky=W + E,padx=5, pady=2) # Queremos que ocupe el ancho de dos columnas que son los label y Entry de nombre y precio.
        #columnspan hace que se ubique en las dos columnas sticky usa las referencias de brujula para rellenar espacios del frame con el elemento.


        # Tabla Productos (El listado que se ve en la parte del medio de la APP con los productos creados)
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.map("mystyle.Treeview", background=[('selected', '#2F4F4F')])
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=("Arial", 11), background="#DCDCDC") # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading", font=("TkHeadingFont", 13, "bold"), relief="flat", foreground="#696969") # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nsew'})])# Eliminamos los bordes

        # Estructura de la tabla
        self.tabla = ttk.Treeview(frame, height=18, columns=[f"#{n}" for n in range(1, 4)], style="mystyle.Treeview") #se le aplica estilo a la tabla de tkinter
        self.tabla.grid(row=7, column=0, columnspan=3, padx=5, pady=2, sticky="nsew")
        self.tabla.heading("#0", text="   Nombre", anchor="w") #se inicializa la cabecera Nombre - No pude alinear a margen izq el contenido.
        self.tabla.heading("#1", text="Precio", anchor="w") #se inicializa la cabecera Precio
        self.tabla.heading("#2", text="Cantidad", anchor="w")  #se inicializa la cabecera Cantidad
        self.tabla.heading("#3", text="Categoría", anchor="w")  # se inicializa la cabecera Cantidad
        self.tabla_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tabla.yview)
        self.tabla_scrollbar.grid(row=7, column=3, sticky="ns", pady=2)
        self.tabla.configure(yscrollcommand=self.tabla_scrollbar.set)

        # Mensaje informativo para el usuario
        self.mensaje = Label(frame, text="", fg="red", bg="#2F4F4F", font=("Arial", 10, "bold"))  # fg letras en color bg fondo de color
        self.mensaje.grid(row=8, column=0, columnspan=2, sticky="we")

        # Botones de Eliminar y Editar
        s = ttk.Style()
        s.configure("my.TButton", font=("Arial", 12,"bold"), foreground="#2F4F4F")
        self.boton_eliminar = ttk.Button(frame, text="ELIMINAR", command=self.del_producto, style="my.TButton")
        self.boton_eliminar.grid(row=9, column=0, columnspan=1, sticky="nsew", pady=10, padx=130) #, padx=150, pady=15
        self.boton_editar = ttk.Button(frame, text='EDITAR', command=self.edit_producto, style='my.TButton')
        self.boton_editar.grid(row=9, column=1, columnspan=1, sticky="nsew", pady=10, padx=130) #padx=200, pady=15,

        self.ventana.columnconfigure(0, weight=1)
        self.ventana.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=3)
        frame.columnconfigure(1, weight=3)
        frame.columnconfigure(3, weight=0)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(3, weight=1)
        frame.rowconfigure(4, weight=1)
        frame.rowconfigure(5, weight=1)
        frame.rowconfigure(6, weight=1)
        frame.rowconfigure(7, weight=3)
        frame.rowconfigure(8, weight=1)
        frame.rowconfigure(9, weight=1)

        self.get_productos()

    def db_consulta(self, consulta, parametros =()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self): # Ejecuta el listado que se ve en pantalla de los productos guardados.
        # Lo primero, al iniciar la app, vamos a limpiar la tabla por si hubiera datos residuales o antiguos
        registros_tabla = self.tabla.get_children() # Obtener todos los datos de la tabla
        for fila in registros_tabla:
            self.tabla.delete(fila)

        # Consulta SQL
        query = "SELECT * FROM producto ORDER BY nombre DESC" #DESC significa orden descendente como ASC orden ascendente.
        registros = self.db_consulta(query)

        # Escribir los datos en pantalla
        for fila in registros:
            print(fila)
            self.tabla.insert("", 0, text=fila[1], values=(fila[2], fila[3],fila[4])) # el primer espacio "" es porque no hereda de otra tabla.


    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    def validacion_cantidad(self):
        cantidad_introducido_por_usuario = self.cantidad.get()
        return len(cantidad_introducido_por_usuario) != 0

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_cantidad():
            query = "INSERT INTO producto VALUES(NULL, ?, ?, ?, ?)" # el NULL es para que no haya error con id autoincrementado Primary Key. dos ?por nombre precio
            parametros = (self.nombre.get(), self.precio.get(), self.cantidad.get(), self.categoria.get())
            self.db_consulta(query, parametros)
            print("Datos guardados")
            self.mensaje["text"],self.mensaje["fg"] = "Producto '{}' añadido con éxito".format(self.nombre.get()),"#90EE90" # Label ubicado entre el boton y la tabla
            self.nombre.delete(0,END)  # Borrar el campo nombre del formulario
            self.precio.delete(0, END) # Borrar el campo precio del formulario
            self.cantidad.delete(0, END) # Borrar el campo cantidad del formulario
            self.categoria.delete(0,END) # Borrar el campo categoria del formulario
            #print(self.nombre.get())
            #print(self.precio.get())
            #print(self.cantidad.get())
            #print(self.categoria.get())
        #Validaciones si lo que hacemos en los cajones se valida bien.
        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_cantidad() == False:
            print("El precio y la cantidad son obligatorios")
            self.mensaje["text"], self.mensaje["fg"] = "El precio y la cantidad son obligatorios","red"
        elif self.validacion_nombre() == False and self.validacion_precio() and self.validacion_cantidad():
            print("El nombre es obligatorio")
            self.mensaje["text"], self.mensaje["fg"] = "El nombre es obligatorio","red"
        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_cantidad():
            print("El precio es obligatorio")
            self.mensaje["text"], self.mensaje["fg"] = "El precio es obligatorio","red"
        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_cantidad() == False:
            print("La cantidad es obligatoria")
            self.mensaje["text"], self.mensaje["fg"] = "La cantidad es obligatoria", "red"
        elif self.validacion_nombre() == False and self.validacion_precio() == False and self.validacion_cantidad():
            print("El nombre y el precio son obligatorios")
            self.mensaje["text"], self.mensaje["fg"] = "El nombre y el precio son obligatorios", "red"
        elif self.validacion_nombre() == False and self.validacion_cantidad() == False and self.validacion_precio():
            print("El nombre y la cantidad son obligatorios")
            self.mensaje["text"], self.mensaje["fg"] = "El nombre y la cantidad son obligatorios", "red"
        else:
            print("El nombre, el precio y la cantidad son obligatorios")
            self.mensaje["text"], self.mensaje["fg"] = "El nombre y el precio son obligatorios", "red"
        self.get_productos() # Cuando se finalice la insercion de datos volvemos a invocar a este metodo
        # para actualizar el contenido y ver los cambios

    def del_producto(self):
        # Debug #
        print(self.tabla.item(self.tabla.selection())) #
        #print(self.tabla.item(self.tabla.selection())['text'])
        #print(self.tabla.item(self.tabla.selection())['values'])
        #print(self.tabla.item(self.tabla.selection())['values'][0])
        self.mensaje['text'] = '' #Mensaje inicialmente vacio
        #Comprobacion de que se seleccione un producto para poder eliminarlo
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'], self.mensaje["fg"] = 'Por favor, seleccione un producto', "red"
            return

        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM producto WHERE nombre = ?' # Consulta SQL
        self.db_consulta(query, (nombre,)) # Ejecutar la consulta
        self.mensaje['text'], self.mensaje["fg"] = "Producto '{}' eliminado con éxito".format(nombre), "green"
        self.get_productos() # Actualizar la tabla de productos

    def edit_producto(self):
        self.mensaje['text'] = '' # Mensaje inicialmente vacio
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'], self.mensaje["fg"] = 'Por favor, seleccione un producto', "red"
            return
        nombre = self.tabla.item(self.tabla.selection())['text']
        old_precio = self.tabla.item(self.tabla.selection())['values'][0] #El precio se encuentra dentro de una lista
        old_cantidad = self.tabla.item(self.tabla.selection())['values'][1] #El cantidad se encuentra dentro de una lista
        old_categoria = self.tabla.item(self.tabla.selection())['values'][2]
        self.ventana_editar = Toplevel() # Crear una ventana por delante de la principal
        self.ventana_editar.title = "Editar Producto" # Titulo de la ventana
        self.ventana_editar.resizable(1, 1) # Activar la redimension de la ventana. Para desactivarla: (0,0)
        self.ventana_editar.wm_iconbitmap("recursos/M6_P2_icon2.ico") # Icono de la ventana
        titulo = Label(self.ventana_editar, text='Edición de Productos', font=('Arial Black', 16, 'bold'))
        titulo.grid(column=0, row=0)

        # Creacion del contenedor Frame de la ventana de Editar Producto
        frame_ep = LabelFrame(self.ventana_editar,
                              text="Editar el siguiente Producto", font=('Arial', 16, 'bold'), bg="#2F4F4F", fg="#DCDCDC")  # frame_ep: Frame Editar Producto
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_antiguo = Label(frame_ep, text="Nombre actual: ",
                                             font=('Arial', 13), bg="#2F4F4F", fg="#DCDCDC")
        # Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre_antiguo.grid(row=2, column=0, sticky="e")  # Posicionamiento a traves de grid

        # Entry Nombre antiguo (texto que no se podra modificar)
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre),
                                          state='readonly', font=('Arial', 13), fg="#2F4F4F")
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ", font=('Arial', 13), bg="#2F4F4F", fg="#DCDCDC")
        self.etiqueta_nombre_nuevo.grid(row=3, column=0, sticky="e")

        # Entry Nombre nuevo (texto que si se podra modificar)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Arial', 13))
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()  # Para que el foco del raton vaya a este Entry al inicio

        # Label Precio antiguo
        self.etiqueta_precio_antiguo = Label(frame_ep, text="Precio actual: ", font=('Arial', 13), bg="#2F4F4F", fg="#DCDCDC")  # Etiqueta de texto ubicada en el frame
        self.etiqueta_precio_antiguo.grid(row=4, column=0, sticky="e")  # Posicionamiento a traves de grid

        # Entry Precio antiguo (texto que no se podra modificar)
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),
                                          state='readonly', font=('Arial', 13), fg="#2F4F4F")
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=('Arial', 13), bg="#2F4F4F", fg="#DCDCDC")
        self.etiqueta_precio_nuevo.grid(row=5, column=0, sticky="e")

        # Entry Precio nuevo (texto que si se podra modificar)
        self.input_precio_nuevo = Entry(frame_ep, font=('Arial', 13))
        self.input_precio_nuevo.grid(row=5, column=1)

        # Label Cantidad antiguo
        self.etiqueta_cantidad_antigua = Label(frame_ep, text="Cantidad actual: ", font=('Arial', 13), bg="#2F4F4F", fg="#DCDCDC")
        # Etiqueta de texto ubicada en el frame
        self.etiqueta_cantidad_antigua.grid(row=6, column=0, sticky="e")  # Posicionamiento a traves de grid

        # Entry Cantidad antiguo (texto que no se podra modificar)
        self.input_cantidad_antigua = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_cantidad),
                                            state='readonly', font=('Arial', 13), fg="#2F4F4F")
        self.input_cantidad_antigua.grid(row=6, column=1)

        # Label Cantidad nueva
        self.etiqueta_cantidad_nueva = Label(frame_ep, text="Cantidad nueva: ", font=('Arial', 13), bg="#2F4F4F", fg="#DCDCDC")
        self.etiqueta_cantidad_nueva.grid(row=7, column=0, sticky="e")

        # Entry Cantidad nueva (texto que si se podra modificar)
        self.input_cantidad_nueva = Entry(frame_ep, font=('Arial', 13))
        self.input_cantidad_nueva.grid(row=7, column=1)

        # Label Categoria Antigua
        self.etiqueta_categoria_antigua = Label(frame_ep, text="Categoría actual: ", font=('Arial', 13), bg="#2F4F4F", fg="#DCDCDC")
        # Etiqueta de texto ubicada en el frame
        self.etiqueta_categoria_antigua.grid(row=8, column=0, sticky="e")  # Posicionamiento a traves de grid

        # Entry Categoria Antigua (texto que no se podra modificar)
        self.input_categoria_antigua = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_categoria),
                                          state='readonly', font=('Arial', 13), fg="#2F4F4F")
        self.input_categoria_antigua.grid(row=8, column=1)

        # Label Categoria nueva
        self.etiqueta_categoria_nueva = Label(frame_ep, text="Categoría nueva: ", font=('Arial', 13), bg="#2F4F4F", fg="#DCDCDC")
        self.etiqueta_categoria_nueva.grid(row=9, column=0, sticky="e")

        # Entry Categoria Nueva (texto que si se podra modificar)
        self.input_categoria_nueva = Entry(frame_ep, font=('Arial', 13))
        self.input_categoria_nueva.grid(row=9, column=1)

        # Boton Actualizar Producto
        s = ttk.Style()
        s.configure("my.TButton", font=("Arial", 12,"bold"), foreground="#2F4F4F")
        self.boton_actualizar = ttk.Button(frame_ep, text="ACTUALIZAR PRODUCTO", style='my.TButton', command=lambda:
        self.actualizar_productos(self.input_nombre_nuevo.get(), self.input_nombre_antiguo.get(),
                                  self.input_precio_nuevo.get(), self.input_precio_antiguo.get(),
                                  self.input_cantidad_nueva.get(), self.input_cantidad_antigua.get(),
                                  self.input_categoria_nueva.get(), self.input_categoria_antigua.get()))
        self.boton_actualizar.grid(row=10, columnspan=2, sticky=W + E, pady=5)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio, nueva_cantidad
                             , antigua_cantidad, nueva_categoria, antigua_categoria):
        global parametros
        #control por consola de los datos que entran
        #print(nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio, nueva_cantidad,
        # antigua_cantidad, nueva_categoria, antigua_categoria)
        producto_modificado = False
        query = 'UPDATE producto SET nombre =?, precio =?, cantidad =?, categoria= ? WHERE nombre =? ' \
                'AND precio =? AND cantidad =? AND categoria =?'
        if nuevo_nombre != '' and nuevo_precio != '' and nueva_cantidad != '' and nueva_categoria != '':
            # Si el usuario escribe nuevo nombre, nuevo precio y cantidad se cambian todos
            parametros = (nuevo_nombre, nuevo_precio, nueva_cantidad, nueva_categoria, antiguo_nombre, antiguo_precio,
                          antigua_cantidad, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_cantidad != '' and nueva_categoria != '':
            # Si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
            parametros = (antiguo_nombre, nuevo_precio, nueva_cantidad, nueva_categoria, antiguo_nombre, antiguo_precio,
                          antigua_cantidad, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_cantidad != '' and nueva_categoria != '':
            # Si el usuario deja vacio el nuevo nombre y el nuevo precio  se mantiene el nombre y precio anterior
            parametros = (antiguo_nombre, antiguo_precio, nueva_cantidad, nueva_categoria, antiguo_nombre, antiguo_precio,
                          antigua_cantidad, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_cantidad == '' and nueva_categoria != '':
            # Si el usuario deja vacio el nuevo nombre, el nuevo precio y la nueva cantidad se mantienen los valores anteriores.
            parametros = (antiguo_nombre, antiguo_precio, antigua_cantidad, nueva_categoria, antiguo_nombre,
                          antiguo_precio, antigua_cantidad, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_cantidad == '' and nueva_categoria != '':
            # Si el usuario deja vacio el nuevo nombre y la nueva cantidad se mantienen los valores anteriores.
            parametros = (antiguo_nombre, nuevo_precio, antigua_cantidad, nueva_categoria, antiguo_nombre,
                          antiguo_precio, antigua_cantidad, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_cantidad == '' and nueva_categoria == '':
            # Si el usuario deja vacio el nuevo nombre y la nueva categoria se mantienen los valores anteriores.
            parametros = (antiguo_nombre, nuevo_precio, antigua_cantidad, antigua_categoria, antiguo_nombre,
                          antiguo_precio, antigua_cantidad, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_cantidad != '' and nueva_categoria == '':
            # Si el usuario deja vacio el nuevo nombre y la nueva categoria se mantienen los valores anteriores.
            parametros = (antiguo_nombre, antiguo_precio, nueva_cantidad, antigua_categoria, antiguo_nombre,
                          antiguo_precio, antigua_cantidad, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_cantidad != '' and nueva_categoria == '':
            # Si el usuario deja vacio el nuevo nombre y la nueva categoria se mantienen los valores anteriores.
            parametros = (antiguo_nombre, nuevo_precio, nueva_cantidad, antigua_categoria, antiguo_nombre,
                          antiguo_precio, antigua_cantidad, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_cantidad != '' and nueva_categoria != '':
            # Si el usuario deja vacio el nuevo precio, se mantiene el pecio anterior
            parametros = (nuevo_nombre, antiguo_precio, nueva_cantidad, nueva_categoria, antiguo_nombre,
                          antiguo_precio, antigua_cantidad, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_cantidad == '' and nueva_categoria != '':
            # Si el usuario deja vacio el nuevo precio y cantidad, se mantienen ambos valores anteriores
            parametros = (nuevo_nombre, antiguo_precio, antigua_cantidad, nueva_categoria, antiguo_nombre,
                          antiguo_precio, antigua_cantidad, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_cantidad == '' and nueva_categoria == '':
            # Si el usuario deja vacio el nuevo precio, cantidad y categoria, se mantienen los valores anteriores
            parametros = (nuevo_nombre, antiguo_precio, antigua_cantidad,  antigua_categoria, antiguo_nombre,
                          antiguo_precio, antigua_cantidad, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_cantidad != '' and nueva_categoria != '':
            # Si el usuario deja vacio el nombre y nuevo precio  se mantienen los valores anteriores.
            parametros = (antiguo_nombre, antiguo_precio, nueva_cantidad, nueva_categoria, antiguo_nombre,
                          antiguo_precio, antigua_cantidad, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_cantidad == '' and nueva_categoria != '':
            # Si el usuario deja vacio la nueva cantidad se mantiene valor anterior.
            parametros = (nuevo_nombre, nuevo_precio,  antigua_cantidad, nueva_categoria, antiguo_nombre,
                          antiguo_precio, antigua_cantidad, antigua_categoria)
            producto_modificado = True

        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_cantidad != '' and nueva_categoria == "":
            # Si el usuario deja vacio la nueva categoria, se mantiene el valor anterior.
            parametros = (nuevo_nombre, nuevo_precio, nueva_cantidad, antigua_categoria, antiguo_nombre, antiguo_precio,
                          antigua_cantidad, antigua_categoria)
            producto_modificado = True

        if producto_modificado:
            self.db_consulta(query, parametros) # Ejecutar la consulta
            self.ventana_editar.destroy() # Cerrar la ventana de edicion de productos
            self.mensaje['text'], self.mensaje["fg"] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre),"green" # Mostrar mensaje para el usuario
            self.get_productos() # Actualizar la tabla de productos
        else:
            self.ventana_editar.destroy() # Cerrar la ventana de edicion de productos
            self.mensaje['text'], self.mensaje["fg"] = 'El producto {} NO ha sido actualizado'.format(antiguo_nombre), "red" # Mostrar mensaje para el usuario


if __name__ == "__main__":
    root = Tk()  # se inicializa la ventana gráfica de la APP, la variable es normal se recomienda ese nombre
    # TK es el constructor de la ventana grafica.
    app = Producto(root)  # Crear un objeto de la clase producto y pasarle la interfaz grafica.
    root.mainloop()  # Tiene que quedar creado hasta que el usuario cierre la APP. La instancia queda viva.
