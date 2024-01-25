import pandas as pd
import flet
from flet import *

       
## TODO:    POR AHORA HACE COINCIDENCIAS 1 A 1, FUTURO DE COINCIDENCIAS VARIAS? // FUNCIONES DE AGRUPACION
##          CONTROL DE TIPOS DE DATOS
##          REFACTORIZAR



def main(page: Page):

    page.padding = 0
#####################################################################################################################################################################
############################################################### METODOS Y VARIABLES GENERALES #######################################################################
#####################################################################################################################################################################


    listaEncodes = ["UTF-8", "UTF-16", "UTF-32", "ISO-8859-1", "ISO-8859", "Windows-1252", "ASCII", "MacRoman"]
    separadoresComunes = [dropdown.Option(text="'    \t'"), dropdown.Option(text=","), dropdown.Option(text=";"), dropdown.Option(text="' '"), dropdown.Option(text="|"),
        dropdown.Option(text=":"), dropdown.Option(text="_"), dropdown.Option(text="-"), dropdown.Option(text="/")] 
    
    global contadorDeArchivos
    contadorDeArchivos = 0

    def devolverValorSeparador(elemento):
        if elemento.value == "'    \t'":
            return "\t"
        elif elemento.value == ",":
            return ","
        elif elemento.value == ";":
            return ";"
        elif elemento.value == "' '":
            return " "
        elif elemento.value == "|":
            return "|"
        elif elemento.value == "_":
            return "_"
        elif elemento.value == ":":
            return ":"
        elif elemento.value == "/":
            return "/"
        elif elemento.value == "-":
            return "-"
        else:
            return None
        
    def devolverValorSeparador(elemento):
        if elemento.value == "Registros Coincidentes":
            return "inner"
        elif elemento.value == "Registros Disimiles":
            return "outer"
        else: 
            return "inner"
        
    def leerPrimerArchivo():
        global contadorDeArchivos
        if contadorDeArchivos < 2:
            contadorDeArchivos += 1
            actualizarBotonConciliarArchivos()
            actualizarBotonCargaArchivo(botonCargarPrimerArchivo)
            actualizarEstadoBoton(botonSeleccionarPrimerArchivo, True)
            actualizarEstadoBoton(botonBorrarPrimerArchivo, False)
            botonBorrarPrimerArchivo.disabled = False
        if extensionPrimerArchivoSeleccionado.value.upper() == ".CSV" or extensionPrimerArchivoSeleccionado.value.upper() == ".TXT":
            for i in listaEncodes:
                try:
                    df0 = pd.read_csv(primerArchivoSeleccionado.value, header=int(headerPrimerArchivo.value) if headerPrimerArchivo.value != '' else 0, skip_blank_lines=skipFilasVaciasPrimerArchivo.value, na_filter=quitarNaPrimerArchivo.value, sep=devolverValorSeparador(separadorPrimerArchivo), encoding=i)
                    if not columnaCamposPrimerArchivo.controls:
                        listarCamposPrimerArchivo(df0.columns)
                    return df0
                except:
                    pass
        if extensionPrimerArchivoSeleccionado.value.upper() == "XLSX":
            try:
                columnasEspecificadas = especificarColumnasPrimerArchivo.value.split(',') if especificarColumnasPrimerArchivo.value else None
                df0 = pd.read_excel(primerArchivoSeleccionado.value, header=int(headerPrimerArchivo.value) if headerPrimerArchivo.value != '' else 0, na_filter=quitarNaPrimerArchivo.value, usecols=columnasEspecificadas if columnasEspecificadas else None)
                if not columnaCamposPrimerArchivo.controls:
                    listarCamposPrimerArchivo(df0.columns)
                return df0
            except Exception as e:
                print(e)

    def leerSegundoArchivo():
        global contadorDeArchivos
        if contadorDeArchivos < 2:
            contadorDeArchivos += 1
            actualizarBotonConciliarArchivos()
            actualizarBotonCargaArchivo(botonCargarSegundoArchivo)
            actualizarEstadoBoton(botonSeleccionarSegundoArchivo, True)
            actualizarEstadoBoton(botonBorrarSegundoArchivo, False)
            botonBorrarSegundoArchivo.disabled = False
        if extensionSegundoArchivoSeleccionado.value.upper() == ".CSV" or extensionSegundoArchivoSeleccionado.value.upper() == ".TXT":
            for i in listaEncodes:
                try:
                    df1 = pd.read_csv(segundoArchivoSeleccionado.value, header=int(headerSegundoArchivo.value) if headerSegundoArchivo.value != '' else 0, na_filter=quitarNaSegundoArchivo.value, skip_blank_lines=skipFilasVaciasSegundoArchivo.value, sep=devolverValorSeparador(separadorSegundoArchivo), encoding=i)
                    if not columnaCamposSegundoArchivo.controls:
                        listarCamposSegundoArchivo(df1.columns)
                    return df1
                except:
                    pass
        if extensionSegundoArchivoSeleccionado.value.upper() == "XLSX":
            try:
                columnasEspecificadas = especificarColumnasSegundoArchivo.value.split(',') if especificarColumnasSegundoArchivo.value else None
                df1 = pd.read_excel(segundoArchivoSeleccionado.value, header=int(headerSegundoArchivo.value) if headerSegundoArchivo.value != '' else 0, na_filter=quitarNaSegundoArchivo.value,usecols=columnasEspecificadas if columnasEspecificadas else None)
                if not columnaCamposSegundoArchivo.controls:
                    listarCamposSegundoArchivo(df1.columns)
                return df1
            except Exception as e:
                print(e)

    def actualizarBotonConciliarArchivos():
        global contadorDeArchivos
        if contadorDeArchivos == 2:
            botonConciliarArchivos.disabled = False
        else: 
            botonConciliarArchivos.disabled = True
        botonConciliarArchivos.update()

    def actualizarBotonCargaArchivo(boton):
        boton.disabled = True
        boton.text = "Cargado"
        boton.bgcolor = "grey"
        boton.color = "white"
        boton.update()

    def actualizarEstadoBoton(boton, disabled):
        boton.disabled = disabled
        boton.update()

    def conciliarAchivos():
        try:
            botonGuardarConciliacion.disabled = False
            botonBorrarInputs.disabled = False
            botonConciliarArchivos.disabled = True
            botonConciliarArchivos.update()
            botonGuardarConciliacion.update()
            botonBorrarInputs.update()
            camposConciliarPrimerArchivo = []

            for i in range(1,len(columnaCamposPrimerArchivo.controls)):
                if columnaCamposPrimerArchivo.controls[i].controls[0].value == True:
                    camposConciliarPrimerArchivo.append(columnaCamposPrimerArchivo.controls[i].controls[1].value)

            camposConciliarSegundoArchivo = []
            for i in range(1,len(columnaCamposSegundoArchivo.controls)):
                if columnaCamposSegundoArchivo.controls[i].controls[0].value == True:
                    camposConciliarSegundoArchivo.append(columnaCamposSegundoArchivo.controls[i].controls[1].value)

            if dropTipoDeConciliacion.value == "Registros Disimiles":
                dfConciliado = pd.merge(leerPrimerArchivo(), leerSegundoArchivo(), left_on=camposConciliarPrimerArchivo, right_on=camposConciliarSegundoArchivo,how='outer', indicator=True)
                dfConciliado = dfConciliado[dfConciliado["_merge"].str.contains("_only")]
                dfConciliado = dfConciliado.drop(['_merge'], axis=1)
                return dfConciliado
            else:
                dfConciliado = pd.merge(leerPrimerArchivo(), leerSegundoArchivo(), left_on=camposConciliarPrimerArchivo, right_on=camposConciliarSegundoArchivo, how='inner')
                dfConciliado = dfConciliado.drop_duplicates().reset_index(drop=True)
                return dfConciliado
        except:
            AlertDialog(title="Error en Conciliacion", content=Text("No se pudieron conciliar los archivos"))

    botonConciliarArchivos = ElevatedButton(
        bgcolor="#ff9755",
        color= "#192543",
        disabled=True,
        text="Conciliar",
        on_click=lambda _: conciliarAchivos(),
    )

    dropTipoDeConciliacion = Dropdown(
        hint_text="Tipo de Conciliacion",
        border_color="#ff9755",
        options=[
            dropdown.Option("Registros Coincidentes"),
            dropdown.Option("Registros Disimiles"),
        ]
    )

    botonGuardarConciliacion = ElevatedButton(
        bgcolor="#ff9755",
        color= "#192543",
        disabled=True,
        text="Descargar",
        on_click=lambda _: ventanaGuardarConciliacion.save_file(allowed_extensions=["xlsx","csv"]),
    )

    def save_files(e:FilePickerResultEvent):
        direccionGuardado = e.path
        if direccionGuardado:
            try:
                conciliarAchivos().to_excel(direccionGuardado, index=False)
            except Exception as e:
                print(e)
        page.update()

    ventanaGuardarConciliacion = FilePicker(on_result=save_files)
    page.overlay.append(ventanaGuardarConciliacion)


    def borrarInputsCliente():
        borrarPrimerArchivo()
        borrarSegundoArchivo()
        botonGuardarConciliacion.disabled = True
        botonConciliarArchivos.disabled = True
        botonBorrarInputs.disabled = True
        botonBorrarInputs.update()
        botonGuardarConciliacion.update()
        botonConciliarArchivos.update()

    botonBorrarInputs = ElevatedButton(
        bgcolor="#ff9755",
        color= "#192543",
        disabled=True,
        text="Limpiar Datos",
        on_click= lambda _:borrarInputsCliente()
    )

#####################################################################################################################################################################
########################################################## METODOS Y VARIABLES PRIMER ARCHIVO #######################################################################
#####################################################################################################################################################################

    def pick_files_result_1(e: FilePickerResultEvent):
        primerArchivoSeleccionado.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else ""
        )
        extensionPrimerArchivoSeleccionado.value = primerArchivoSeleccionado.value[-4:]
        botonCargarPrimerArchivo.disabled = False
        botonCargarPrimerArchivo.bgcolor = "#ff9755"
        botonCargarPrimerArchivo.color = "#192543"
        primerArchivoSeleccionado.update()
        extensionPrimerArchivoSeleccionado.update()
        botonCargarPrimerArchivo.update()

    ventanaSeleccionArchivo_1 = FilePicker(on_result=pick_files_result_1)

    primerArchivoSeleccionado = TextField(width=500, height=40, border="underline", border_color="#ff9755")
    page.overlay.append(ventanaSeleccionArchivo_1)

    botonSeleccionarPrimerArchivo = ElevatedButton(
        bgcolor="#ff9755",
        color= "#192543",
        text='Seleccionar Archivo',
        on_click=lambda _: ventanaSeleccionArchivo_1.pick_files(allow_multiple=True),
    )

    extensionPrimerArchivoSeleccionado = Text(size=20)
    separadorPrimerArchivo = Dropdown(options=separadoresComunes, hint_text="Seleccione el seperador",border_color="#ff9755")
    headerPrimerArchivo = TextField(width=50, height=40, text_align="center", border_color="#ff9755")

    columnaIndicePrimerArchivo = TextField(width=50, height=40, text_align="center", border_color="#ff9755")
    quitarNaPrimerArchivo = Checkbox(check_color="#192543", active_color="#ff9755")
    skipFilasVaciasPrimerArchivo = Checkbox(check_color="#192543", active_color="#ff9755")
    especificarColumnasPrimerArchivo = TextField(width=350, height=40, text_align="center", border_color="#ff9755")

    botonCargarPrimerArchivo = ElevatedButton(
        bgcolor="#ff9755",
        color= "#192543",
        disabled = True,
        text="Cargar DF",
        on_click=lambda _: leerPrimerArchivo(),
    )
    def borrarPrimerArchivo():
        global contadorDeArchivos
        contadorDeArchivos -= 1

        primerArchivoSeleccionado.value = ""
        botonSeleccionarPrimerArchivo.disabled = False
        botonCargarPrimerArchivo.text = "Cargar DF"
        botonBorrarPrimerArchivo.disabled = True
        columnaCamposPrimerArchivo.controls.clear()
        extensionPrimerArchivoSeleccionado.value = ""
        separadorPrimerArchivo.value = ""

        primerArchivoSeleccionado.update()
        botonSeleccionarPrimerArchivo.update()
        botonCargarPrimerArchivo.update()
        botonBorrarPrimerArchivo.update()
        columnaCamposPrimerArchivo.update()
        extensionPrimerArchivoSeleccionado.update()
        separadorPrimerArchivo.update()

        actualizarBotonConciliarArchivos()

    botonBorrarPrimerArchivo = ElevatedButton(
        bgcolor="#ff9755",
        color= "#192543",
        disabled = True,
        text="Borrar Archivo",
        on_click=lambda _: borrarPrimerArchivo(),
    )

    columnaCamposPrimerArchivo = Column()
    
    def listarCamposPrimerArchivo(listaCampos):
        columnaCamposPrimerArchivo.controls.append(Row(controls=[Text("Campos del Primer Archivo")]))
        contador = 0
        for i in listaCampos:
            contador += 5
            columnaCamposPrimerArchivo.controls.append(Row(controls=[Checkbox(check_color="#192543", active_color="#ff9755"), Text(value=i)]))
        page.update()
#####################################################################################################################################################################
########################################################## METODOS Y VARIABLES SEGUNDO ARCHIVO ######################################################################
#####################################################################################################################################################################

    def pick_files_result_2(e: FilePickerResultEvent):
            segundoArchivoSeleccionado.value = (
                ", ".join(map(lambda f: f.path, e.files)) if e.files else ""
            )
            extensionSegundoArchivoSeleccionado.value = segundoArchivoSeleccionado.value[-4:]
            botonCargarSegundoArchivo.disabled = False
            botonCargarSegundoArchivo.bgcolor = "#ff9755"
            botonCargarSegundoArchivo.color = "#192543"
            segundoArchivoSeleccionado.update()
            extensionSegundoArchivoSeleccionado.update()
            botonCargarSegundoArchivo.update()

    ventanaSeleccionArchivo_2 = FilePicker(on_result=pick_files_result_2)

    segundoArchivoSeleccionado = TextField(width=500, height=40, border="underline", border_color="#ff9755")
    page.overlay.append(ventanaSeleccionArchivo_2)

    botonSeleccionarSegundoArchivo = ElevatedButton(
        bgcolor="#ff9755",
        color= "#192543",
        text='Seleccionar Archivo',
        on_click=lambda _: ventanaSeleccionArchivo_2.pick_files(allow_multiple=True),
    )

    extensionSegundoArchivoSeleccionado = Text(size=20)
    separadorSegundoArchivo = Dropdown(options=separadoresComunes, hint_text="Seleccione el separador",border_color="#ff9755")
    headerSegundoArchivo = TextField(width=50, height=40, text_align="center", border_color="#ff9755")

    columnaIndiceSegundoArchivo = TextField(width=50, height=40, text_align="center", border_color="#ff9755")
    quitarNaSegundoArchivo = Checkbox(check_color="#192543", active_color="#ff9755")
    skipFilasVaciasSegundoArchivo = Checkbox(check_color="#192543", active_color="#ff9755")
    especificarColumnasSegundoArchivo = TextField(width=350, height=40, text_align="center", border_color="#ff9755")

    botonCargarSegundoArchivo = ElevatedButton(
        bgcolor="#ff9755",
        color= "#192543",
        disabled = True,
        text="Cargar DF",
        on_click=lambda _: leerSegundoArchivo(),
    )

    def borrarSegundoArchivo():
        global contadorDeArchivos
        contadorDeArchivos -= 1
        
        segundoArchivoSeleccionado.value = ""
        botonSeleccionarSegundoArchivo.disabled = False
        botonCargarSegundoArchivo.text = "Cargar DF"
        botonBorrarSegundoArchivo.disabled = True
        columnaCamposSegundoArchivo.controls.clear()
        extensionSegundoArchivoSeleccionado.value = ""
        separadorSegundoArchivo.value = ""

        segundoArchivoSeleccionado.update()
        botonSeleccionarSegundoArchivo.update()
        botonCargarSegundoArchivo.update()
        botonBorrarSegundoArchivo.update()
        columnaCamposSegundoArchivo.update()
        extensionSegundoArchivoSeleccionado.update()
        separadorSegundoArchivo.update()

        actualizarBotonConciliarArchivos()

    botonBorrarSegundoArchivo = ElevatedButton(
        bgcolor="#ff9755",
        color= "#192543",
        disabled = True,
        text="Borrar Archivo",
        on_click=lambda _: borrarSegundoArchivo(),
    )

    columnaCamposSegundoArchivo = Column()

    def listarCamposSegundoArchivo(listaCampos):
        columnaCamposSegundoArchivo.controls.append(Row(controls=[Text("Campos del Segundo Archivo")]))
        for i in listaCampos:
            columnaCamposSegundoArchivo.controls.append(Row(controls=[Checkbox(check_color="#192543", active_color="#ff9755"), Text(value=i)]))
        page.update()
#####################################################################################################################################################################
########################################################## CARGA DE VARAIABLES A LA INTERFAZ ########################################################################
#####################################################################################################################################################################

    page.add(
        Container(
            expand=True,
            image_src='imagen_fondo.jpg',
            image_opacity=0.05,
            image_fit= ImageFit.COVER,
            padding= padding.all(30),
            gradient=LinearGradient(
                colors=[
                    "#192543",
                    "#27334f",
                    "#192543"
                ],
                begin=alignment.center_left,
                end=alignment.center_right
            ),
            content=Column(
                scroll=ScrollMode.ALWAYS,
                height=page.height,
                controls=[
                    Text("SECCION DEL PRIMER ARCHIVO", style=TextThemeStyle.HEADLINE_MEDIUM, color="lightblue"),
                    Row(
                        alignment = MainAxisAlignment.START,
                        controls=[
                            botonSeleccionarPrimerArchivo,
                            primerArchivoSeleccionado,
                            Text("Extension del archivo:"),
                            extensionPrimerArchivoSeleccionado,
                        ],
                    ),
                    Row(
                        alignment = MainAxisAlignment.START,
                        controls=[
                            Text("Delimitador:"),
                            separadorPrimerArchivo,
                            Text("Fila de Titulos:"),
                            headerPrimerArchivo,
                            Text("Columna Indice:"),
                            columnaIndicePrimerArchivo,
                            Text("Campos a Leer:"),
                            especificarColumnasPrimerArchivo,
                        ]
                    ),
                    Row(
                        alignment = MainAxisAlignment.START,
                        controls=[
                            Text("Eliminar valores N/A"),
                            quitarNaPrimerArchivo,
                            Text("Ignorar filas vacias"),
                            skipFilasVaciasPrimerArchivo,
                            botonCargarPrimerArchivo,
                            botonBorrarPrimerArchivo,
                        ]
                    ),
                    Divider(),
                    Text("SECCION DEL SEGUNDO ARCHIVO", style=TextThemeStyle.HEADLINE_MEDIUM, color="lightblue"),
                    Row(
                        controls=[
                            botonSeleccionarSegundoArchivo,
                            segundoArchivoSeleccionado,
                            Text("Extension del archivo:"),
                            extensionSegundoArchivoSeleccionado,
                        ],
                    ),
                    Row(
                        controls=[
                            Text("Delimitador:"),
                            separadorSegundoArchivo,
                            Text("Fila de Titulos:"),
                            headerSegundoArchivo,
                            Text("Columna Indice:"),
                            columnaIndiceSegundoArchivo,
                            Text("Campos a Leer:"),
                            especificarColumnasSegundoArchivo,
                        ]
                    ),
                    Row(
                        controls=[
                            Text("Eliminar valores N/A"),
                            quitarNaSegundoArchivo,
                            Text("Ignorar filas vacias"),
                            skipFilasVaciasSegundoArchivo,
                            botonCargarSegundoArchivo,
                            botonBorrarSegundoArchivo,
                        ]
                    ),
                    Divider(),
                    Text("ANALISIS DE RESULTADOS", style=TextThemeStyle.HEADLINE_MEDIUM, color="lightblue"),
                    Row(
                        controls=[
                            botonConciliarArchivos,
                            dropTipoDeConciliacion,
                            botonGuardarConciliacion,
                            botonBorrarInputs
                        ]
                    ),
                    Row(
                        vertical_alignment = CrossAxisAlignment.START,
                        controls=[
                            columnaCamposPrimerArchivo,
                            columnaCamposSegundoArchivo,

                        ]
                    )
                ]
            )
        )
    )


flet.app(target=main)