import pandas as pd
import flet
from flet import *


def main(page: Page):

#####################################################################################################################################################################
############################################################### METODOS Y VARIABLES GENERALES #######################################################################
#####################################################################################################################################################################


    listaEncodes = [dropdown.Option("UTF-8"), dropdown.Option("UTF-16"),dropdown.Option("UTF-32"),dropdown.Option("ISO-8859-1"),
        dropdown.Option("ISO-8859"),dropdown.Option("Windows-1252"),dropdown.Option("ASCII"),dropdown.Option("MacRoman")]
    
    camposConciliables = TextField(width=500, height=40)
    global contadorDeArchivos
    contadorDeArchivos = 0

    def leerPrimerArchivo():
        global contadorDeArchivos
        contadorDeArchivos += 1
        actualizarBotonConciliarArchivos()
        actualizarBotonCargaArchivo(botonCargarPrimerArchivo)
        actualizarEstadoBoton(botonSeleccionarPrimerArchivo, True)
        actualizarEstadoBoton(botonBorrarPrimerArchivo, False)
        botonBorrarPrimerArchivo.disabled = False
        if extensionPrimerArchivoSeleccionado.value == ".csv" or extensionPrimerArchivoSeleccionado.value == ".txt":
            df0 = pd.read_csv(primerArchivoSeleccionado.value, skip_blank_lines=skipFilasVaciasPrimerArchivo.value ,na_filter=quitarNaPrimerArchivo.value, sep=str(delimitadorPrimerArchivo.value) if delimitadorPrimerArchivo.value is not None else None, encoding=encodePrimerArchivo.value if encodePrimerArchivo.value is not None else None)
            return df0
        if extensionPrimerArchivoSeleccionado.value == "xlsx":
            columnasEspecificadas = especificarColumnasPrimerArchivo.value.split(',') if especificarColumnasPrimerArchivo.value else None
            df0 = pd.read_excel(primerArchivoSeleccionado.value, na_filter=quitarNaPrimerArchivo.value, usecols=columnasEspecificadas if columnasEspecificadas else None)
            return df0
        
    def leerSegundoArchivo():
        global contadorDeArchivos
        contadorDeArchivos += 1
        actualizarBotonConciliarArchivos()
        actualizarBotonCargaArchivo(botonCargarSegundoArchivo)
        actualizarEstadoBoton(botonSeleccionarSegundoArchivo, True)
        actualizarEstadoBoton(botonBorrarSegundoArchivo, False)
        botonBorrarSegundoArchivo.disabled = False
        if extensionSegundoArchivoSeleccionado.value == ".csv" or extensionSegundoArchivoSeleccionado.value == ".txt":
            df1 = pd.read_csv(segundoArchivoSeleccionado.value, na_filter=quitarNaSegundoArchivo.value, skip_blank_lines=skipFilasVaciasSegundoArchivo.value, sep=str(delimitadorSegundoArchivo.value) if delimitadorSegundoArchivo.value is not None else None, encoding=encodeSegundoArchivo.value if encodeSegundoArchivo.value is not None else None)
            return df1
        if extensionSegundoArchivoSeleccionado.value == "xlsx":
            columnasEspecificadas = especificarColumnasSegundoArchivo.value.split(',') if especificarColumnasSegundoArchivo.value else None
            df1 = pd.read_excel(segundoArchivoSeleccionado.value, na_filter=quitarNaSegundoArchivo.value,usecols=columnasEspecificadas if columnasEspecificadas else None)
            return df1

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
        campos_a_conciliar = camposConciliables.value.split(",")
        dfConciliado = pd.merge(leerPrimerArchivo(), leerSegundoArchivo(), on=campos_a_conciliar, how='inner')
        botonGuardarConciliacion.disabled = False
        botonGuardarConciliacion.update()
        return dfConciliado

    botonConciliarArchivos = ElevatedButton(
        disabled=True,
        text="Conciliar",
        on_click=lambda _: conciliarAchivos(),
    )
    botonGuardarConciliacion = ElevatedButton(
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

#####################################################################################################################################################################
########################################################## METODOS Y VARIABLES PRIMER ARCHIVO #######################################################################
#####################################################################################################################################################################

    def pick_files_result_1(e: FilePickerResultEvent):
        primerArchivoSeleccionado.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else ""
        )
        extensionPrimerArchivoSeleccionado.value = primerArchivoSeleccionado.value[-4:]
        botonCargarPrimerArchivo.disabled = False
        botonCargarPrimerArchivo.bgcolor = "#202429"
        botonCargarPrimerArchivo.color = "#95bff0"
        primerArchivoSeleccionado.update()
        extensionPrimerArchivoSeleccionado.update()
        botonCargarPrimerArchivo.update()

    ventanaSeleccionArchivo_1 = FilePicker(on_result=pick_files_result_1)

    primerArchivoSeleccionado = TextField(width=500, height=40)
    page.overlay.append(ventanaSeleccionArchivo_1)

    botonSeleccionarPrimerArchivo = ElevatedButton(
        text='Seleccionar Archivo',
        on_click=lambda _: ventanaSeleccionArchivo_1.pick_files(allow_multiple=True),
    )

    extensionPrimerArchivoSeleccionado = Text(size=20)
    delimitadorPrimerArchivo = TextField(width=50, height=40, text_align="center")
    encodePrimerArchivo = Dropdown(
        hint_text="Tipo de Encoding",
        height=50,
        text_size=12,
        options= listaEncodes
    )
    headerPrimerArchivo = TextField(width=50, height=40, text_align="center")

    columnaIndicePrimerArchivo = TextField(width=50, height=40, text_align="center")
    quitarNaPrimerArchivo = Checkbox()
    skipFilasVaciasPrimerArchivo = Checkbox()  # NO TIENE FUNCION TODAVIA
    especificarColumnasPrimerArchivo = TextField(width=350, height=40, text_align="center")

    botonCargarPrimerArchivo = ElevatedButton(
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

        primerArchivoSeleccionado.update()
        botonSeleccionarPrimerArchivo.update()
        botonCargarPrimerArchivo.update()
        botonBorrarPrimerArchivo.update()

        actualizarBotonConciliarArchivos()

    botonBorrarPrimerArchivo = ElevatedButton(
        disabled = True,
        text="Borrar Archivo",
        on_click=lambda _: borrarPrimerArchivo(),
    )


#####################################################################################################################################################################
########################################################## METODOS Y VARIABLES SEGUNDO ARCHIVO ######################################################################
#####################################################################################################################################################################

    def pick_files_result_2(e: FilePickerResultEvent):
            segundoArchivoSeleccionado.value = (
                ", ".join(map(lambda f: f.path, e.files)) if e.files else ""
            )
            extensionSegundoArchivoSeleccionado.value = segundoArchivoSeleccionado.value[-4:]
            botonCargarSegundoArchivo.disabled = False
            botonCargarSegundoArchivo.bgcolor = "#202429"
            botonCargarSegundoArchivo.color = "#95bff0"
            segundoArchivoSeleccionado.update()
            extensionSegundoArchivoSeleccionado.update()
            botonCargarSegundoArchivo.update()

    ventanaSeleccionArchivo_2 = FilePicker(on_result=pick_files_result_2)

    segundoArchivoSeleccionado = TextField(width=500, height=40)
    page.overlay.append(ventanaSeleccionArchivo_2)

    botonSeleccionarSegundoArchivo = ElevatedButton(
        text='Seleccionar Archivo',
        on_click=lambda _: ventanaSeleccionArchivo_2.pick_files(allow_multiple=True),
    )

    extensionSegundoArchivoSeleccionado = Text(size=20)
    delimitadorSegundoArchivo = TextField(width=50, height=40, text_align="center")
    encodeSegundoArchivo = Dropdown(
                    hint_text="Tipo de Encoding",
                    height=50,
                    text_size=12,
                    options= listaEncodes
                )
    headerSegundoArchivo = TextField(width=50, height=40, text_align="center")

    columnaIndiceSegundoArchivo = TextField(width=50, height=40, text_align="center")
    quitarNaSegundoArchivo = Checkbox()
    skipFilasVaciasSegundoArchivo = Checkbox()  # NO TIENE FUNCION TODAVIA
    especificarColumnasSegundoArchivo = TextField(width=350, height=40, text_align="center")

    botonCargarSegundoArchivo = ElevatedButton(
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

        segundoArchivoSeleccionado.update()
        botonSeleccionarSegundoArchivo.update()
        botonCargarSegundoArchivo.update()
        botonBorrarSegundoArchivo.update()

        actualizarBotonConciliarArchivos()

    botonBorrarSegundoArchivo = ElevatedButton(
        disabled = True,
        text="Borrar Archivo",
        on_click=lambda _: borrarSegundoArchivo(),
    )
#####################################################################################################################################################################
########################################################## CARGA DE VARAIABLES A LA INTERFAZ ########################################################################
#####################################################################################################################################################################

    page.add(
        Row(
            controls=[
                botonSeleccionarPrimerArchivo,
                primerArchivoSeleccionado,
                Text("Extension del archivo:"),
                extensionPrimerArchivoSeleccionado,
            ],
        ),
        Row(
            controls=[
                Text("Delimitador:"),
                delimitadorPrimerArchivo,
                encodePrimerArchivo,
                Text("Header:"),
                headerPrimerArchivo,
                Text("Columna Indice:"),
                columnaIndicePrimerArchivo,
                Text("Columnas:"),
                especificarColumnasPrimerArchivo,
            ]
        ),
        Row(
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
                delimitadorSegundoArchivo,
                encodeSegundoArchivo,
                Text("Header:"),
                headerSegundoArchivo,
                Text("Columna Indice:"),
                columnaIndiceSegundoArchivo,
                Text("Columnas:"),
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
        Row(
            controls=[
                Text("Campos a conciliar"),
                camposConciliables,
                botonConciliarArchivos,
                botonGuardarConciliacion
            ]
        )
    )


flet.app(target=main)