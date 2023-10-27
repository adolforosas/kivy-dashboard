import pandas as pd
import matplotlib.pyplot as plt
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from io import StringIO
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivymd.uix.datatables import MDDataTable



#Window.size = (310, 540)
#Window.minimum_width, Window.minimum_height = Window.size

# define parameters for a request
token = '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'
owner = 'adolforosas'
repo = 'contratos'
path = 'contratos_medicos_total_smallV2.csv'

# send a request
#r = requests.get(
#    'https://api.github.com/repos/{owner}/{repo}/contents/{path}'.format(
#    owner=owner, repo=repo, path=path),
#    headers={
#        'accept': 'application/vnd.github.v3.raw',
#        'authorization': 'token {}'.format(token)
#            }
#    )

# convert string to StringIO object
#string_io_obj = StringIO(r.text)
#df = pd.read_csv(string_io_obj, sep=",")

file_last ='contratos_medicos_total_smallV2_conproductoV7.csv'
df = pd.read_csv(file_last)

df2023 = df[df['año'] == 2023]
# Load data to df
def hola():
    print('hola')

def calcula_resumen(periodo):
    df2023 = df[df['año'] == int(periodo)]
    print(periodo)
    print(type(periodo))
    resumen = []
    # Calcular las ventas totales para el año 2023
    ventas_totales_2023 = df2023['Importe del contrato'].sum()
    # Formatear el resultado con el signo de dólar y comas
    ventas_totales_2023_formateadas = "${:,.0f}".format(ventas_totales_2023)
    resumen.append(ventas_totales_2023_formateadas)
    # Calcular la suma total de contratos para el año 2023
    suma_total_contratos_2023 = df2023['Código del contrato'].count()
    resumen.append(str(suma_total_contratos_2023))
    suma_total_proveedores = df2023['Proveedor o contratista'].nunique()
    resumen.append(str(suma_total_proveedores))
    # Calcular la suma total de instituciones únicas en el año 2023
    total_instituciones = df2023['Siglas de la Institución'].nunique()
    resumen.append(str(total_instituciones))
    print(resumen)
    return resumen

def calcula_tabla(periodo):
    df2023 = df[df['año'] == int(periodo)]
    top_10_contratos = df2023.nlargest(10, 'Importe del contrato')
    tabla = GridLayout(cols=4, spacing=5, size_hint_y=None)
    tabla.bind(minimum_height=tabla.setter('height'))

    # Agrega encabezados a la tabla
    tabla.add_widget(Label(text='Número del procedimiento'))
    tabla.add_widget(Label(text='Proveedor'))
    tabla.add_widget(Label(text='Institución'))
    tabla.add_widget(Label(text='Importe'))
    # Agrega datos a la tabla

    #self.ids.tabla_contratos.clear_widgets()  # Borra cualquier tabla anterior
    #self.ids.tabla_contratos.add_widget(tabla)  # Agrega la nueva tabla

    print('ya termino la tabla?')

periodo = 2023
resumen = calcula_resumen(periodo=periodo)
calcula_tabla(periodo=periodo)




class Interface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.entrada1.text = "Total Contratado \n " + resumen[0]
        self.ids.entrada2.text = "Contratos \n " + resumen[1]
        self.ids.entrada3.text = "Empresas \n " + resumen[2]
        self.ids.entrada4.text = "Instituciones \n " + resumen[3]
        self.grafica_institucion()
        self.grafica_empresa()
        self.display_info()

        #tabla = GridLayout(cols=3, spacing=0, row_default_height=28,size_hint_y=None)
#
        #tabla.bind(minimum_height=tabla.setter('height'))
        #tabla.cols_minimum = {0: 30, 1: 300, 2: 60}
#
        ## Agrega encabezados a la tabla
        #tabla.add_widget(Label(text='Institución',font_size=16))
        #tabla.add_widget(Label(text='Proveedor',font_size=16))
        #tabla.add_widget(Label(text='Importe',font_size=16))
#
        #top_10_contratos = df2023.nlargest(10, 'Importe del contrato')
        #for index, row in top_10_contratos.iterrows():
#
        #    #print(row['Número del procedimiento'], row['Proveedor o contratista'], row['Siglas de la Institución'],
        #     #     row['Importe del contrato'])
        #    tabla.add_widget(Label(text=row['Siglas de la Institución'], font_size=12))
        #    tabla.add_widget(Label(text=row['Proveedor o contratista'],font_size=12))
#
        #    importe_millones = row['Importe del contrato'] / 1000000  # Convierte a millones
        #    importe_formateado = "${:,.2f} M".format(importe_millones)  # Formatea el monto
        #    tabla.add_widget(Label(text=importe_formateado, font_size=12))
#
#
        #self.ids.tabla_contratos.clear_widgets()  # Borra cualquier tabla anterior
        #self.ids.tabla_contratos.add_widget(tabla)  # Agrega la nueva tabla
#
    def actualizar_textos(self,periodo):
        print(periodo)
        print('actualiza textos al año 2022')

        self.resumen = calcula_resumen(periodo=periodo)
        self.tabla = calcula_tabla(periodo=periodo)
        self.ids.etiqueta2.text = str(periodo)
        #self.ids.etiqueta.text =f'Compras Gubernamentales \n Equipo Médico {periodo}'
        self.ids.entrada1.text = "Total Contratado \n " + self.resumen[0]
        self.ids.entrada2.text = "Contratos \n " + self.resumen[1]
        self.ids.entrada3.text = "Empresas \n " + self.resumen[2]
        self.ids.entrada4.text = "Instituciones \n " + self.resumen[3]
        self.grafica_institucion()
        self.grafica_empresa()
        self.display_info()
    def display_info(self):
        print("pass","Estoy probando la lógica")
        df2023 = df[df['año'] == int(self.ids.etiqueta2.text)]
        tabla = GridLayout(cols=3, spacing=15, row_default_height=28, size_hint_y=None)

        tabla.bind(minimum_height=tabla.setter('height'))
        tabla.cols_minimum = {0: 70, 1: 240, 2: 60}

        # Agrega encabezados a la tabla

        tabla.add_widget(Label(text='Institución', font_size=16, text_size=(80, None)))
        tabla.add_widget(Label(text='Proveedor', font_size=16, text_size=(240, None)))
        tabla.add_widget(Label(text='Importe', font_size=16, text_size=(60, None)))

        top_10_contratos = df2023.nlargest(10, 'Importe del contrato')
        for index, row in top_10_contratos.iterrows():
            # print(row['Número del procedimiento'], row['Proveedor o contratista'], row['Siglas de la Institución'],
            #     row['Importe del contrato'])
            label = Label(
                text=row['Siglas de la Institución'],
                font_size=14,
                halign='left',
                text_size=(60, None)  # Ajusta el ancho (200) y deja la altura como None
            )
            tabla.add_widget(label)
            #tabla.add_widget(Label(text=row['Siglas de la Institución'], font_size=12))
            #tabla.add_widget(Label(text=row['Proveedor o contratista'], font_size=12))
            label = Label(
                text=row['Proveedor o contratista'],
                font_size=14,
                halign='left',
                text_size=(240, None)  # Ajusta el ancho (200) y deja la altura como None
            )
            tabla.add_widget(label)

            #importe_millones = row['Importe del contrato'] / 1000000  # Convierte a millones
            #importe_formateado = "${:,.2f} M".format(importe_millones)  # Formatea el monto
            #tabla.add_widget(Label(text=importe_formateado, font_size=14))
            importe_millones = row['Importe del contrato'] / 1000000  # Convierte a millones
            importe_formateado = "${:,.2f} M".format(importe_millones)  # Formatea el monto
            label = Label(
                text=importe_formateado,
                font_size=14,
                halign='left',
                text_size=(80, None)  # Ajusta el ancho (200) y deja la altura como None
            )
            tabla.add_widget(label)

        self.ids.tabla_contratos.clear_widgets()  # Borra cualquier tabla anterior
        self.ids.tabla_contratos.add_widget(tabla)  # Agrega la nueva tabla

    def display_info2(self):
        df2023 = df[df['año'] == int(self.ids.etiqueta2.text)]

        data = []
        column_headers = ["Institución", "Proveedor", "Importe"]

        top_10_contratos = df2023.nlargest(10, 'Importe del contrato')
        for index, row in top_10_contratos.iterrows():
            importe_millones = row['Importe del contrato'] / 1000000
            importe_formateado = "${:,.2f} M".format(importe_millones)

            data.append([row['Siglas de la Institución'], row['Proveedor o contratista'], importe_formateado])

        table = MDDataTable(
            column_data=data,
            row_data=column_headers,
            pos_hint={'center_x': 0.5},
            size_hint=(0.9, 0.6),
            check=True,
            use_pagination=True,
            pagination_menu_pos="auto",
            elevation=2
        )

        table.open()

    def grafica_institucion(self):
        print(self.ids.etiqueta2.text, 'esto viene de la etiqueta2')
        print("seleccionaste institucion")
        df2023 = df[df['año'] == int(self.ids.etiqueta2.text)]
        # Agrupar los datos filtrados por Siglas de la Institución y sumar los importes de contrato
        total_monto_por_institucion = df2023.groupby('Siglas de la Institución')['Importe del contrato'].sum()
        # Ordenar los resultados en orden descendente y seleccionar las 10 primeras instituciones
        total_monto_por_institucion = total_monto_por_institucion / 1000000  # Dividir entre 1 millón
        top_10_instituciones = total_monto_por_institucion.sort_values(ascending=False).head(10)
        # Formatear los montos totales como cadenas de caracteres
        top_10_instituciones_formateadas = top_10_instituciones.apply("${:,.0f}".format)

        # Crea una figura de Matplotlib para la gráfica de instituciones
        fig_instituciones, ax_instituciones = plt.subplots(figsize=(4.5, 4,),facecolor='#192444',dpi=100)
        ax_instituciones.set_facecolor('#182243')

        # Crea la gráfica de barras utilizando los datos de top_10_instituciones
        bars = ax_instituciones.barh(top_10_instituciones.index[::-1], top_10_instituciones.values[::-1],
                                     color='#4974A5')

        # Agrega etiquetas de monto dentro de las barras sin la palabra "millones"
        for bar, valor in zip(bars, top_10_instituciones.values[::-1]):
            ax_instituciones.text(valor * 1.01, bar.get_y() + bar.get_height() / 2, "${:,.0f}".format(valor),
                                  va='center', color='white')

        ax_instituciones.set_yticklabels(['    ' + label for label in top_10_instituciones.index[::-1]])
        ax_instituciones.set_xlabel('Monto Total en millones de pesos', color='white')
        #ax_instituciones.set_ylabel('Institución', color='lightcyan')
        ax_instituciones.tick_params(axis='y', labelcolor='white')  # Cambiar el color de las etiquetas del eje y a lightcyan
        ax_instituciones.tick_params(axis='x', colors='white')
        plt.tick_params(labelbottom=False, bottom=False)

        title = ax_instituciones.set_title('Instituciones con mas compras',
                                   color='white')
        title.set_position([.5, .98])  # Ajusta las coordenadas [x, y]
        #plt.subplots_adjust(left=0.05, right=1, top=0.95, bottom=0.05)
        #plt.margins(0.20, 0.0)
        plt.tight_layout(pad=0.08)
        # Establece el límite inferior del eje x en cero
        #ax_instituciones.set_xlim(left=0)
        #ax_instituciones.grid(axis='x', linestyle='--', alpha=0.4, color='lightcyan')
        #ax_instituciones.xaxis.set_visible(False)
        #ax_instituciones.yaxis.set_visible(False)
        for spine in ['top', 'right', 'left', 'bottom']:
            ax_instituciones.spines[spine].set_visible(False)
        self.ids.grafica.clear_widgets()
        self.ids.grafica.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        #self.ids.grafica.add_widget(FigureCanvasKivyAgg(fig_instituciones))


    def grafica_empresa(self):
        print(self.ids.etiqueta2.text, 'esto viene de la etiqueta2')
        print("seleccionaste empresa")
        df2023 = df[df['año'] == int(self.ids.etiqueta2.text)]
        df2023['Proveedor o contratista'] = df2023['Proveedor o contratista'].str.title()
        print("seleccionaste empresa")
        # Agrupar los datos filtrados por proveedor o contratista y sumar los importes de contrato
        total_monto_por_empresa = df2023.groupby('Proveedor o contratista')['Importe del contrato'].sum()

        # Dividir los montos entre 1 millón
        total_monto_por_empresa = total_monto_por_empresa / 1000000  # Dividir entre 1 millón

        # Ordenar los resultados en orden descendente y seleccionar las 10 primeras empresas
        top_10_empresas = total_monto_por_empresa.sort_values(ascending=False).head(10)

        # Crear una figura de Matplotlib
        fig_empresas, ax = plt.subplots(figsize=(4.5, 4),facecolor='#192444',dpi=100)
        ax.set_facecolor('#182243')
        #ax.set_facecolor('#1f2c56')
        bars = ax.barh(top_10_empresas.index[::-1], top_10_empresas.values[::-1],
                       color='#ffa500')  # Revertir el orden #58E3F1'

        # Agregar etiquetas de monto dentro de las barras sin la palabra "millones"
        for bar, valor in zip(bars, top_10_empresas.values[::-1]):
            if valor >= 30:  # Mostrar el texto solo si el valor es mayor o igual a 300 millones
                ax.text(valor * 1.01, bar.get_y() + bar.get_height() / 2, "${:,.0f}".format(valor), va='center',
                        color='lightcyan')  # Cambiar el color a lightcyan

        ax.set_yticklabels(['    ' + label for label in top_10_empresas.index[::-1]])
        ax.set_xlabel('Monto Total en millones de pesos',
                      color='lightcyan')  # Cambiar el color del texto del eje x a lightcyan
        #ax.set_ylabel('Empresa', color='lightcyan')  # Cambiar el color del texto del eje y a lightcyan
        title= ax.set_title('Empresas con mas Ventas (Millones)',
                     color='lightcyan')  # Cambiar el color del título a lightcyan

        title.set_position([.5, .95])  # Ajusta las coordenadas [x, y]
        ax.tick_params(axis='y', labelcolor='darkblue')  # Cambiar el color de las etiquetas del eje y a lightcyan
        ax.tick_params(axis='x', colors='lightcyan')
        plt.tick_params(labelbottom=False, bottom=False)
        plt.yticks(rotation=0, ha='left')
        #plt.margins(0.20, 0.0)
        plt.tight_layout(pad=0.08)

        # Establecer el límite inferior del eje x en cero
        ax.set_xlim(left=0)
        ax.tick_params(axis='y', labelsize=8)  # Ajusta el tamaño (8 es un ejemplo)
        #plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

        # Eliminar el marco completo
        # ax.spines['top'].set_visible(True)
        # ax.spines['right'].set_visible(False)
        # ax.spines['bottom'].set_visible(False)
        # ax.spines['left'].set_visible(False)
        #ax.grid(axis='x', linestyle='--', alpha=0.4, color='lightcyan')
        for spine in ['top', 'right', 'left', 'bottom']:
            ax.spines[spine].set_visible(False)
        self.ids.grafica2.clear_widgets()
        self.ids.grafica2.add_widget(FigureCanvasKivyAgg(plt.gcf()))


class DashboardApp(App):
    def build(self):
        #self.graph_canvas = FigureCanvasKivyAgg(figure=self.figura_empresas, size_hint_y=1)

        return Interface()

    def hola(self):
        año =2022
        print(resumen,'prueb')
        print('hola')



if __name__ == '__main__':
    DashboardApp().run()


