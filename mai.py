import streamlit as st
import pandas as pd
import re
import plotly.graph_objects as go


import streamlit as st

st.set_page_config(page_title="App con Múltiples Páginas", layout="wide")

# Ruta o URL del logo
logo_path = "ucol_logo.PNG"  # Si es local, usa el nombre del archivo
#st.image("ucol_logo.PNG", width=150)  # Ajusta el ancho según necesites
#st.image(logo_path, use_container_width=True)
    
# Crear un contenedor con tres columnas y colocar la imagen en el centro
col1, col2, col3 = st.columns([1, 2, 1])  # La columna central es más ancha

with col2:  # Colocar la imagen en la columna central
    st.image(logo_path, width=400)  # Ajusta el tamaño según necesites



# Crear menú de navegación
pagina = st.selectbox("Selecciona una página", ["Inicio", "Análisis por base", "Análisis por autor", "Equipo de trabajo"])

# Mostrar contenido según la página seleccionada
if pagina == "Inicio":
    st.title("Inicio")
    st.write("Bienvenido a la aplicación de Streamlit.")


###############################################################################################################################
elif pagina == "Análisis por base":
    
#    @st.cache_data

    import streamlit as st
    import pandas as pd

    # 📌 Título de la aplicación
    st.title("Análisis temático de los autores de publicaciones científicas de la Universidad de Colima")

    st.markdown("""
    En esta sección se analizan algunos aspectos claves de los autores de la Universidad de Colima que han participado en publicaciones indizadas en la base de datos de Scopus. Algunos de estos aspectos son: los autores mas prolificos de la Universidad de Colima, la evolución temporal de estos autores, la distribución de autores de acuerdo a su productividad y un clasificador en el que el usuario puede comparar su productividad con la de los autores de la base. 
    """)
    st.markdown("""
    **Para poder visualizar el análisis de publicaciones, por favor cargue la base de datos de publicaciones de Scopus.**
    """)
    
    # 📂 **Subir archivo CSV**
    uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])

    if uploaded_file is not None:
        # Cargar el archivo en un DataFrame

        
        df = pd.read_csv(uploaded_file, encoding='utf-8')

        # ✅ Mostrar mensaje de éxito
        st.success("✅ Archivo cargado correctamente.")

        # 📊 **Mostrar las primeras filas**
        #st.subheader("📋 Vista previa de los datos")
        st.markdown("""
        Estas son las **primeras cinco filas** del archivo con la lista de publicaciones en las que se han involucrado profesores de la Universidad de Colima. En su estado actual, cada fila corresponde a un artículo diferente.
        """)
        
        st.write(df.head())
        with st.expander("**Datos del archivo**"):
            st.write(f"**Número de filas:** {df.shape[0]}")
            st.write(f"**Número de columnas:** {df.shape[1]}")
            st.write("**Lista de columnas:**")
            st.write(df.columns.tolist())  # Mostrar los nombres de las columnas como una lista

            
        # 📂 **Descargar el archivo procesado**
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV", csv_data, "datos_procesados.csv", "text/csv")


        import re

        # 📌 **Función para procesar los datos**
        def process_author_data(df):
            df.columns = df.columns.str.strip().str.replace(" ", "_")  # Reemplazar espacios en nombres de columnas

            # Verificar que las columnas necesarias están en el DataFrame
            if "Author_full_names" not in df.columns or "Author(s)_ID" not in df.columns:
                st.error("❌ No se encontraron las columnas 'Author full names' o 'Author(s) ID'.")
                return None

            # Crear diccionarios para asignar nombres a los IDs de autores
            author_id_map = {}
            author_name_map = {}

            for row in df.dropna(subset=["Author_full_names"]).itertuples(index=False):
                author_entries = str(getattr(row, "Author_full_names")).split(";")
                for entry in author_entries:
                    match = re.match(r"(.*) \((\d+)\)", entry.strip())  # Extraer nombre completo e ID
                    if match:
                        full_name, author_id = match.groups()
                        author_id_map[author_id] = full_name
                        author_name_map[author_id] = full_name.split(",")[0]  # Solo apellido y primera inicial

            # Expandir filas con múltiples IDs separados por ';'
            df = df.assign(**{"Author(s)_ID": df["Author(s)_ID"].astype(str).str.split(";")}).explode("Author(s)_ID")
            df["Author(s)_ID"] = df["Author(s)_ID"].str.strip()

            # Asignar nombres basados en los IDs de autor
            df["Author_full_names"] = df["Author(s)_ID"].map(author_id_map).fillna("Unknown Author")
            df["Authors"] = df["Author(s)_ID"].map(author_name_map).fillna("Unknown Author")

            return df

        df_processed = process_author_data(df)

        if df_processed is not None:
            #st.success("✅ Datos procesados correctamente.")
            st.write(" ")
            # 📋 **Vista previa**
            #st.subheader("📋 Vista previa de los datos procesados")
            #st.markdown("""
            #Como primer paso, se procesa la base de datos para crear un registro por autor de cada artículo producido. De esta manera, cada fila corresponde a una ocasión en la que un investigador participa en un artículo.
            #""")

            #st.write(df_processed.head())

            #with st.expander("Datos del archivo"):
            #    st.write(f"**Número de filas:** {df_processed.shape[0]}")
            #    st.write(f"**Número de columnas:** {df_processed.shape[1]}")
            #    st.write("**Lista de columnas:**")
            #    st.write(df_processed.columns.tolist())  # Mostrar los nombres de las columnas como una lista

            # 📂 **Descargar el archivo procesado**
            #csv_data = df_processed.to_csv(index=False).encode("utf-8")
            #st.download_button("📥 Descargar datos procesados", csv_data, "processed_author_data.csv", "text/csv")

        from collections import Counter
        import streamlit as st
        import pandas as pd
        import re
        from collections import Counter

#st.title("📊 Procesamiento de Datos de Autores")

# 📂 **Subir archivo CSV**
#uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])


        # 📌 **Funciones para procesamiento y análisis de datos**
        def process_author_data(df):
            df.columns = df.columns.str.strip().str.replace(" ", "_")
        
            if "Author_full_names" not in df.columns or "Author(s)_ID" not in df.columns:
                st.error("❌ No se encontraron las columnas 'Author full names' o 'Author(s) ID'.")
                return None

            author_id_map = {}
            author_name_map = {}

            for row in df.dropna(subset=["Author_full_names"]).itertuples(index=False):
                author_entries = str(getattr(row, "Author_full_names")).split(";")
                for entry in author_entries:
                    match = re.match(r"(.*) \((\d+)\)", entry.strip())
                    if match:
                        full_name, author_id = match.groups()
                        author_id_map[author_id] = full_name
                        author_name_map[author_id] = full_name.split(",")[0]

            df = df.assign(**{"Author(s)_ID": df["Author(s)_ID"].astype(str).str.split(";")}).explode("Author(s)_ID")
            df["Author(s)_ID"] = df["Author(s)_ID"].str.strip()

            df["Author_full_names"] = df["Author(s)_ID"].map(author_id_map).fillna("Unknown Author")
            df["Authors"] = df["Author(s)_ID"].map(author_name_map).fillna("Unknown Author")
        
            return df
    
        df_processed = process_author_data(df)

        if df_processed is not None:
            st.write(" ")
        
            # 📋 **Vista previa**
            #st.subheader("📋 Vista previa de los datos procesados")
            #st.write(df_processed.head())

            # 📊 **Análisis de Editoriales y Publicaciones**
            st.subheader("Autores mas prolíficos")

            def count_unique_publishers(publishers):
                if isinstance(publishers, float) and pd.isna(publishers):
                    return 0
                return len(set(str(publishers).split(";")))

            def sorted_frequent_publishers(publishers):
                if isinstance(publishers, float) and pd.isna(publishers):
                    return ""
                publisher_list = str(publishers).split(";")
                counter = Counter(publisher_list)
                sorted_publishers = sorted(counter.items(), key=lambda x: x[1], reverse=True)
                return "; ".join(f"{pub} ({count})" for pub, count in sorted_publishers)

            def format_year_counts(years):
                if isinstance(years, float) and pd.isna(years):
                    return ""
                year_list = str(years).split(";")
                counter = Counter(year_list)
                sorted_years = sorted(counter.items(), key=lambda x: int(x[0]))
                return "; ".join(f"{year} ({count})" for year, count in sorted_years)

            df_grouped = df_processed.groupby("Author(s)_ID").agg({
                "Cited_by": "sum",
                "Title": "count",
                "Source_title": lambda x: len(x.unique()),
                "Funding_Details": lambda x: x.notna().sum(),
                "Year": lambda x: format_year_counts(";".join(map(str, x))),
                **{col: lambda x: "; ".join(map(str, x.unique())) for col in df_processed.columns if col not in ["Cited_by", "Title", "Source_title", "Funding_Details", "Year", "Author(s)_ID"]}
            }).reset_index()

            df_grouped = df_grouped.rename(columns={"Title": "Publications", "Source_title": "Journals", "Funding_Details": "Funded_publications"})
            df_grouped["Not_funded_publications"] = df_grouped["Publications"] - df_grouped["Funded_publications"]

            if "Publisher" in df_processed.columns:
                df_grouped["Publisher_Count"] = df_grouped["Publisher"].apply(count_unique_publishers)
                df_grouped["Most_frequent_publisher"] = df_grouped["Publisher"].apply(sorted_frequent_publishers)

            columns_to_drop = ["DOI", "Volume", "Issue", "Art._No.", "Page_start", "Page_end", "Page_count", "Link", "ISBN", "CODEN", "Funding_Texts", "ISSN", "Open_Access", "Publisher"]
            df_grouped = df_grouped.drop(columns=columns_to_drop, errors="ignore")

            st.markdown("""
                Después del procesamiento, se agrupa la información a nivel de autor ("Author(s)_ID") y se generan estadísticas:
                - "Normalized_Author_Name": Nombre del autor, escrito en minúsculas y sin caracteres especiales.
                - "Cited_by": Suma de citas recibidas.
                - "Publications": Conteo de artículos por autor.
                - "Journals": Número de fuentes únicas en las que ha publicado.
                - "Funded_publications": Cantidad de artículos con financiamiento.
                - "Not_funded_publications": Publicaciones sin financiamiento (Publications - Funded_publications).
                - "Year": Años en los que el autor publicó (los números entre paréntesis representan el número de publicaciones por año).
                - "Authors_ID": ID de scopus del autor o autora.
                - "Publisher_Count" y "Most_frequent_publisher": Cantidad y ranking de editoriales (si la columna "Publisher" está en el DataFrame).
            """)
            #st.dataframe(df_grouped)
            # Definir el orden prioritario
            priority_columns = [
                "Author(s)_ID",
                "Authors",
                "Author_full_names",
                "Publications",
                "Year",
                "Cited_by",
                "Funded_publications",
                "Not_funded_publications",
                "Correspondence_Address"
            ]

            # Obtener las demás columnas sin alterar su orden original
            remaining_columns = [col for col in df_grouped.columns if col not in priority_columns]

            # Reordenar el DataFrame con las columnas prioritarias primero
            df_grouped = df_grouped[priority_columns + remaining_columns]

            # Mostrar las primeras filas para verificar
            #st.write(df_grouped.head())


            
            #with st.expander("Datos del archivo"):
            #    st.write(f"**Número de filas:** {df_grouped.shape[0]}")
            #    st.write(f"**Número de columnas:** {df_grouped.shape[1]}")
            #    st.write("**Lista de columnas:**")
            #    st.write(df_grouped.columns.tolist())  # Mostrar los nombres de las columnas como una lista



            
            #csv_data = df_grouped.to_csv(index=False).encode("utf-8")
            #st.download_button("📥 Descargar datos agrupados", csv_data, "unified_author_data.csv", "text/csv")

#####################################################

        # Filtrar filas donde la columna "Correspondence_Address" contenga variantes de "Universidad de Colima"
        keywords = ["Colima", "UCOL", "COLIMA", "UdeC", "ucol"]
        df_ucol = df_grouped[df_grouped["Correspondence_Address"].str.contains('|'.join(keywords), case=False, na=False)]

        #df_ucol
        # Guardar el resultado en un nuevo archivo CSV
        #df_ucol.to_csv("author_data_colima.csv", index=False)

        # Filtrar filas donde la columna "Correspondence_Address" contenga variantes de "Universidad de Colima"
        keywords = ["@ucol"]
        df_ucol_dir = df_ucol[df_ucol["Correspondence_Address"].str.contains('|'.join(keywords), case=False, na=False)]

        #df_ucol_dir
        # Guardar el resultado en un nuevo archivo CSV
        #df_ucol_dir.to_csv("author_data_colima_dir.csv", index=False)

        # Filtrar las filas que NO contienen las palabras clave en la columna 'Correspondence_Address'
        keywords = ["Colima", "UCOL", "COLIMA", "UdeC", "ucol"]
        df_not_ucol = df_grouped[~df_grouped["Correspondence_Address"].str.contains('|'.join(keywords), case=False, na=False)]

        # Guardar el resultado en un nuevo archivo CSV
        #df_not_ucol.to_csv("author_data_not_colima.csv", index=False)
        #df_not_ucol

#########################################################################
#########################################################################
        import unicodedata

        # Lista de autores a eliminar
        authors_to_remove = ["crossa,", "murillo zamora, efren", "guzman esquivel,", "martinez fierro,"]

        # Función mejorada para normalizar nombres y eliminar iniciales, espacios extra y puntos finales
        def normalize_name_v2(name):
            if pd.isna(name):
                return ""
            name = name.lower().strip()  # Convertir a minúsculas y quitar espacios extra
            name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')  # Eliminar acentos
            name = re.sub(r'[-_]', ' ', name)  # Reemplazar guiones y guiones bajos por espacios
            name = re.sub(r'\s+', ' ', name)  # Reemplazar múltiples espacios por un solo espacio
            name = re.sub(r'\b([A-Z])\b', '', name, flags=re.IGNORECASE)  # Eliminar iniciales de segundo nombre
            name = re.sub(r'\.$', '', name)  # Eliminar puntos al final del nombre
            name = name.strip()  # Quitar espacios extra resultantes
            return name

        # Aplicar la normalización mejorada a los nombres de autores
        df_ucol_dir["Normalized_Author_Name"] = df_ucol_dir["Author_full_names"].apply(normalize_name_v2)
        # Eliminar los autores no deseados antes de la agrupación
        df_ucol_dir = df_ucol_dir[~df_ucol_dir["Normalized_Author_Name"].isin(authors_to_remove)]


        # Función para sumar correctamente las publicaciones por año
        def sum_year_counts(year_entries):
            year_count = Counter()
            for entry in year_entries.dropna():
                matches = re.findall(r'(\d{4})\s*\((\d+)\)', entry)
                for year, count in matches:
                    year_count[year] += int(count)
            sorted_years = sorted(year_count.items(), key=lambda x: int(x[0]))
            return "; ".join(f"{year} ({count})" for year, count in sorted_years)

        # Agrupar por el nombre normalizado para fusionar datos de autores con el mismo nombre
        df_ucol = df_ucol_dir.groupby("Normalized_Author_Name").agg({
            "Cited_by": "sum",
            "Publications": "sum",
            "Journals": "sum",
            "Funded_publications": "sum",
            "Not_funded_publications": "sum",
            "Year": lambda x: sum_year_counts(x),  # Sumar correctamente los valores entre paréntesis
            **{col: lambda x: "; ".join(map(str, x.unique())) for col in df_ucol_dir.columns if col not in [
                "Cited_by", "Publications", "Journals", "Funded_publications", "Not_funded_publications", "Year", "Normalized_Author_Name"]}
        }).reset_index()

        # Crear un diccionario para rastrear qué filas se fusionan
        merge_log = {}
        for name in df_ucol["Normalized_Author_Name"].unique():
            merged_ids = df_ucol_dir[df_ucol_dir["Normalized_Author_Name"] == name]["Author(s)_ID"].unique()
            if len(merged_ids) > 1:  # Solo registrar si hubo más de una fusión
                merge_log[name] = list(merged_ids)

        # Convertir el log en un DataFrame para visualizar las fusiones
        df_merge_ucol_log = pd.DataFrame(list(merge_log.items()), columns=["Normalized_Author_Name", "Merged_Author_IDs"])



        st.write(df_ucol.head())
         
        with st.expander("Datos del archivo"):
            st.write(f"**Número de filas:** {df_ucol.shape[0]}")
            st.write(f"**Número de columnas:** {df_ucol.shape[1]}")
            st.write("**Lista de columnas:**")
            st.write(df_ucol.columns.tolist())  # Mostrar los nombres de las columnas como una lista
            
        csv_data = df_ucol.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar datos ucol", csv_data, "unified_ucol_author_data.csv", "text/csv")

##########################################################################

        # Recargar librerías
        import pandas as pd
        import plotly.express as px

        # Asegurar que la columna Year es de tipo string y separar los valores correctamente
        df_ucol["Year"] = df_ucol["Year"].astype(str)

        # Expandir la columna Year para contar las publicaciones por año por autor
        df_expanded = df_ucol.assign(Year=df_ucol["Year"].str.split(";")).explode("Year")

        # Extraer solo el año numérico y la cantidad de publicaciones en ese año
        df_expanded[["Year", "Publications"]] = df_expanded["Year"].str.extract(r'(\d{4})\s*\((\d+)\)')

        # Convertir los valores a tipo numérico
        df_expanded["Year"] = pd.to_numeric(df_expanded["Year"], errors='coerce')
        df_expanded["Publications"] = pd.to_numeric(df_expanded["Publications"], errors='coerce')
        df_expanded = df_expanded.dropna(subset=["Year", "Publications"])  # Eliminar filas con valores no válidos

        # Ordenar cronológicamente los años
        df_expanded = df_expanded.sort_values(by=["Year", "Normalized_Author_Name"])

        # Filtrar el DataFrame eliminando a los autores no deseados
        authors_to_remove = ["crossa,", "murillo zamora, efren", "guzman esquivel,", "martinez fierro,"]
        df_expanded_filtered = df_expanded[~df_expanded["Normalized_Author_Name"].isin(authors_to_remove)]

        # Identificar los 30 autores con más publicaciones totales después del filtrado
        top_authors_filtered = df_expanded_filtered.groupby("Normalized_Author_Name")["Publications"].sum().nlargest(30).index

        # Filtrar solo los datos de los 30 autores principales
        df_top30_filtered = df_expanded_filtered[df_expanded_filtered["Normalized_Author_Name"].isin(top_authors_filtered)].copy()

        # Obtener el primer y último año en la lista
        year_min = df_top30_filtered["Year"].min()
        year_max = df_top30_filtered["Year"].max()

        # Crear una columna de publicaciones acumuladas
        df_top30_filtered["Cumulative_Publications"] = 0

        # Diccionario para rastrear la acumulación de publicaciones por autor    
        author_cumulative_filtered = {author: 0 for author in top_authors_filtered}

        # Lista para almacenar los frames de la animación
        frames_filtered = []

        # Iterar año por año y actualizar el número acumulado de publicaciones
        for year in range(year_min, year_max + 1):
            # Obtener las publicaciones de los autores en el año actual
            df_year = df_top30_filtered[df_top30_filtered["Year"] == year].copy()

            # Actualizar los valores acumulados para cada autor en el año actual
            for author in top_authors_filtered:
                if author in df_year["Normalized_Author_Name"].values:
                    # Sumar publicaciones de este año
                    publications_this_year = df_year[df_year["Normalized_Author_Name"] == author]["Publications"].sum()
                    author_cumulative_filtered[author] += publications_this_year

            # Crear un DataFrame con los valores actualizados
            df_snapshot = pd.DataFrame({
                "Normalized_Author_Name": list(author_cumulative_filtered.keys()),
                "Cumulative_Publications": list(author_cumulative_filtered.values()),
                "Year": year
            })

            # Filtrar los 30 autores con más publicaciones acumuladas hasta el momento
            df_snapshot = df_snapshot.sort_values(by=["Cumulative_Publications", "Normalized_Author_Name"], ascending=[False, True]).head(30)

            # Agregar el snapshot a la lista de frames
            frames_filtered.append(df_snapshot)

        # Unir los datos en un solo DataFrame para la animación
        df_final_filtered = pd.concat(frames_filtered)

        # Determinar el valor máximo de publicaciones acumuladas en cada año
        df_max_values_filtered = df_final_filtered.groupby("Year")["Cumulative_Publications"].max().reset_index()
        df_max_values_filtered["Cumulative_Publications"] = df_max_values_filtered["Cumulative_Publications"] * 1.1  # Añadir margen del 10%

        # Agregar el Author(s)_ID al DataFrame antes de generar la gráfica
        df_final_filtered = df_final_filtered.merge(df_ucol[["Normalized_Author_Name", "Author(s)_ID"]], on="Normalized_Author_Name", how="left")

        # Obtener el último año de la animación
        last_year = df_final_filtered["Year"].max()

        # Extraer el orden final de los autores basado en el último año
        final_order = df_final_filtered[df_final_filtered["Year"] == last_year].sort_values(
            by="Cumulative_Publications", ascending=False
        )["Normalized_Author_Name"].tolist()

        # Crear la gráfica de barras animada con acumulación, orden final fijo y Author(s)_ID en hover
        fig_filtered = px.bar(
            df_final_filtered,
            x="Cumulative_Publications",
            y="Normalized_Author_Name",
            color="Normalized_Author_Name",
            animation_frame="Year",
            orientation="h",
            title="Evolución de Publicaciones Acumuladas - Top 30 Autores",
            labels={"Cumulative_Publications": "Número Acumulado de Publicaciones", "Normalized_Author_Name": "Autores"},
            hover_data={"Author(s)_ID": True},  # Agregar el ID del autor en el hover
            template="plotly_white"
        )

        # Aplicar el orden inverso en el eje Y para que los autores con más publicaciones estén abajo
        fig_filtered.update_layout(
            xaxis=dict(range=[0, df_max_values_filtered["Cumulative_Publications"].max()]),
            height=1000,  # Aumentar la altura para evitar que los nombres se aplasten
            yaxis=dict(categoryorder="array", categoryarray=final_order[::-1])  # Invertir el orden de los autores
        )



        
        # Mostrar la gráfica interactiva con la corrección en hover
        #st.plotly_chart(fig_filtered)


###########################################################################################

        import streamlit as st
        import pandas as pd
        import re
        import unicodedata
        from collections import Counter
        import plotly.express as px
        import matplotlib.pyplot as plt
        #import moviepy.editor as mpy
        import streamlit as st
        import pandas as pd
        import re
        import unicodedata
        from collections import Counter
        import plotly.express as px
        import matplotlib.pyplot as plt
        import os
        import numpy as np

        import streamlit as st
        import pandas as pd
        import plotly.express as px
        import numpy as np

        import streamlit as st
        import pandas as pd
        import plotly.express as px
        import numpy as np

        st.title("📊 Procesamiento y Análisis de Publicaciones Acumuladas")

        # Lista de autores a eliminar
        authors_to_remove = ["crossa,", "murillo zamora, efren", "guzman esquivel,", "martinez fierro,"]
        df_final_filtered = df_final_filtered[~df_final_filtered["Normalized_Author_Name"].isin(authors_to_remove)]

        # Obtener los años en orden
        years_sorted = sorted(df_final_filtered["Year"].unique())
        year_min = min(years_sorted)
        year_max = max(years_sorted)

        # Calcular publicaciones por año para cada autor
        df_final_filtered["Yearly_Publications"] = df_final_filtered.groupby(["Normalized_Author_Name", "Year"])["Cumulative_Publications"].diff().fillna(df_final_filtered["Cumulative_Publications"])
    
        # Crear la gráfica de barras animada con estratificación por año
        fig = px.bar(
            df_final_filtered,
            x="Yearly_Publications",
            y="Normalized_Author_Name",
            color="Normalized_Author_Name",
            animation_frame="Year",
            orientation="h",
            title="Evolución de Publicaciones Acumuladas - Top 30 Autores",
            labels={"Yearly_Publications": "Publicaciones en el Año", "Normalized_Author_Name": "Autores"},
            template="plotly_white"
        )


        for frame in fig.frames:
            year = frame.name
            frame.data += (go.Scatter(
                x=[df_final_filtered["Yearly_Publications"].max() * 1.05], 
                y=[df_final_filtered["Normalized_Author_Name"].min()],
                mode="lines",
                line=dict(color="black", width=2),
                name=f"Año {year}"
            ),)


        # Ajustar layout para la animación
        fig.update_layout(
            xaxis=dict(range=[0, df_final_filtered["Yearly_Publications"].max() * 1.1]),
            height=1000,
            yaxis=dict(categoryorder="total ascending"),
            updatemenus=[
                {
                    "buttons": [
                        {
                            "args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}],
                            "label": "Play",
                            "method": "animate"
                        },
                        {
                            "args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}],
                            "label": "Pause",
                            "method": "animate"
                        }
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 10},
                    "showactive": False,
                    "type": "buttons",
                    "x": 0.1,
                    "xanchor": "right",
                    "y": 1.15,
                    "yanchor": "top"
                }
            ]
        )

        st.plotly_chart(fig)


#####################################################################################3
        df_final_filtered
        import streamlit as st
        import pandas as pd
        import plotly.graph_objects as go
        import numpy as np
        import scipy.stats as stats

        st.title("📊 Correlación entre Número de Artículos y Número de Citas")

        # Convertir a valores numéricos (por si hay valores en string)
        df_ucol["Cited_by"] = pd.to_numeric(df_ucol["Cited_by"], errors='coerce')
        df_ucol["Publications"] = pd.to_numeric(df_ucol["Publications"], errors='coerce')

        # Eliminar valores NaN si existen
        df_correlation = df_ucol[["Cited_by", "Publications", "Author(s)_ID", "Normalized_Author_Name"]].dropna()

        # Calcular la correlación de Pearson
        correlation_coefficient, p_value = stats.pearsonr(df_correlation["Cited_by"], df_correlation["Publications"])

        # Ajustar una línea de tendencia (regresión lineal)
        slope, intercept = np.polyfit(df_correlation["Publications"], df_correlation["Cited_by"], 1)
        x_line = np.linspace(df_correlation["Publications"].min(), df_correlation["Publications"].max(), 100)
        y_line = slope * x_line + intercept

        # Crear la gráfica de dispersión con información adicional en el tooltip
        fig_corr = go.Figure()

        # Agregar los puntos de dispersión con el ID y nombre del autor en el hover
        fig_corr.add_trace(go.Scatter(
            x=df_correlation["Publications"],
            y=df_correlation["Cited_by"],
            mode="markers",
            marker=dict(color="blue", opacity=0.5, size=6),
            text=df_correlation["Normalized_Author_Name"] + "<br>ID: " + df_correlation["Author(s)_ID"].astype(str),
            hoverinfo="text+x+y",
            name="Datos"
        ))

        # Agregar la línea de tendencia
        fig_corr.add_trace(go.Scatter(
            x=x_line,
            y=y_line,
            mode="lines",
            line=dict(color="red", width=2),
            name="Línea de tendencia"
        ))

        # Configurar el diseño
        fig_corr.update_layout(
            title=f"Correlación entre Número de Artículos y Número de Citas<br>Coeficiente de Pearson: {correlation_coefficient:.2f}, p-valor: {p_value:.3f}",
            xaxis_title="Número Total de Artículos",
            yaxis_title="Número Total de Citas",
            template="plotly_white"
        )    

        # Mostrar la gráfica interactiva
        st.plotly_chart(fig_corr)
#############################################################################################33

        import streamlit as st
        import pandas as pd
        import plotly.express as px
        import numpy as np

        st.title("📊 Scatter Heatmap: Antigüedad vs. Publicaciones (Citas como color)")

        # Convertir a valores numéricos
        df_ucol["Cited_by"] = pd.to_numeric(df_ucol["Cited_by"], errors='coerce')
        df_ucol["Publications"] = pd.to_numeric(df_ucol["Publications"], errors='coerce')

        # Convertir Year a string y extraer el primer año de publicación
        df_ucol["Year"] = df_ucol["Year"].astype(str)
        df_ucol["First_Year"] = pd.to_numeric(df_ucol["Year"].str.extract(r'(\d{4})')[0], errors='coerce')

        # Calcular la antigüedad (años desde la primera publicación hasta 2025)
        df_ucol["Seniority"] = 2025 - df_ucol["First_Year"]

        # Filtrar valores válidos
        df_heatmap = df_ucol[["Seniority", "Publications", "Cited_by", "Author(s)_ID", "Normalized_Author_Name"]].dropna()

        # Ajustar el tamaño de los puntos al cuádruple
        df_heatmap["Size_Metric"] = df_heatmap["Cited_by"] * 10

        # Crear el scatter heatmap con el tamaño ajustado
        fig_heatmap = px.scatter(
            df_heatmap,
            x="Seniority",
            y="Publications",
            size="Size_Metric",  # Tamaño de los puntos escalado
            color="Cited_by",  # Color de los puntos según el número de citas
            labels={
                "Seniority": "Antigüedad (Años desde Primera Publicación)",
                "Publications": "Número Total de Publicaciones",
                "Cited_by": "Número de Citas",
                "Size_Metric": "Citas (Escalado)"
            },
            title="Scatter Heatmap: Antigüedad vs. Publicaciones (Citas como color)",
            hover_data={"Author(s)_ID": True, "Normalized_Author_Name": True, "Cited_by": True},
            color_continuous_scale="Viridis",
            template="plotly_white"
        )

        # Mostrar la gráfica interactiva    
        st.plotly_chart(fig_heatmap)


    #####################################################################################################3

        import streamlit as st
        import pandas as pd
        import plotly.graph_objects as go
        import numpy as np

        st.title("📊 Distribución de Publicaciones y Citas por Antigüedad")

        #     Convertir a valores numéricos
        df_ucol["Cited_by"] = pd.to_numeric(df_ucol["Cited_by"], errors='coerce')
        df_ucol["Publications"] = pd.to_numeric(df_ucol["Publications"], errors='coerce')

        # Convertir Year a string y extraer el primer año de publicación
        df_ucol["Year"] = df_ucol["Year"].astype(str)
        df_ucol["First_Year"] = pd.to_numeric(df_ucol["Year"].str.extract(r'(\d{4})')[0], errors='coerce')

        # Calcular la antigüedad (años desde la primera publicación hasta 2025)
        df_ucol["Seniority"] = 2025 - df_ucol["First_Year"]

        # Agrupar antigüedad en intervalos de 5 años
        df_ucol["Seniority_Group"] = (df_ucol["Seniority"] // 5) * 5

        # Calcular los valores del cuartil 75 (Q3) para definir el filtro
        q3_cited = df_ucol["Cited_by"].quantile(0.75)
        q3_publications = df_ucol["Publications"].quantile(0.75)

        df_ucol["Cited_Above_Q3"] = df_ucol["Cited_by"] > q3_cited
        df_ucol["Publications_Above_Q3"] = df_ucol["Publications"] > q3_publications

        # Crear la figura para citas
        fig_cites = go.Figure()
        fig_cites.add_trace(go.Box(
            x=df_ucol["Seniority_Group"],
            y=df_ucol["Cited_by"],
            boxpoints=False,
            notched=True,
            marker=dict(color="lightblue"),
            name="Número de Citas"
        ))
        fig_cites.add_trace(go.Scatter(
            x=df_ucol["Seniority_Group"],
            y=df_ucol["Cited_by"],
            mode="markers",
            marker=dict(size=8, opacity=0.8, color="darkblue"),
            name="Todos los Autores",
            text=df_ucol["Normalized_Author_Name"] + "<br>ID: " + df_ucol["Author(s)_ID"],
            hoverinfo="text+y"
        ))

        # Crear la figura para publicaciones
        fig_publications = go.Figure()
        fig_publications.add_trace(go.Box(
            x=df_ucol["Seniority_Group"],
            y=df_ucol["Publications"],
            boxpoints=False,
            notched=True,
            marker=dict(color="lightgreen"),
            name="Número de Publicaciones"
        ))
        fig_publications.add_trace(go.Scatter(
            x=df_ucol["Seniority_Group"],
            y=df_ucol["Publications"],
            mode="markers",
            marker=dict(size=8, opacity=0.8, color="darkgreen"),
            name="Todos los Autores",
            text=df_ucol["Normalized_Author_Name"] + "<br>ID: " + df_ucol["Author(s)_ID"],
            hoverinfo="text+y"
        ))

        st.subheader("Distribución del Número Total de Citas por Antigüedad")
        st.plotly_chart(fig_cites)

        st.subheader("Distribución del Número Total de Publicaciones por Antigüedad")
        st.plotly_chart(fig_publications)

    
###############################################################################################################

        import streamlit as st
        import pandas as pd
        import plotly.express as px
        import plotly.graph_objects as go
        import numpy as np
        from sklearn.preprocessing import StandardScaler
        from sklearn.cluster import AgglomerativeClustering
        from sklearn.manifold import TSNE

        st.title("📊 Clustering Jerárquico de Autores en Función de su Producción Académica")

        # Convertir a valores numéricos
        df_ucol["Cited_by"] = pd.to_numeric(df_ucol["Cited_by"], errors='coerce')
        df_ucol["Publications"] = pd.to_numeric(df_ucol["Publications"], errors='coerce')
        df_ucol["Funded_publications"] = pd.to_numeric(df_ucol["Funded_publications"], errors='coerce')

        # Crear la variable Funding Ratio
        df_ucol["Funding_Ratio"] = df_ucol["Funded_publications"] / df_ucol["Publications"]
        df_ucol["Funding_Ratio"] = df_ucol["Funding_Ratio"].fillna(0)

        # Convertir Year a string y extraer el primer año de publicación
        df_ucol["Year"] = df_ucol["Year"].astype(str)
        df_ucol["First_Year"] = pd.to_numeric(df_ucol["Year"].str.extract(r'(\d{4})')[0], errors='coerce')

        # Calcular la antigüedad (años desde la primera publicación hasta 2025)
        df_ucol["Seniority"] = 2025 - df_ucol["First_Year"]

        # Filtrar valores válidos
        df_valid = df_ucol.dropna(subset=["Publications", "Cited_by", "Seniority", "Funding_Ratio"])[
            ["Publications", "Cited_by", "Seniority", "Funding_Ratio"]
        ]

        # Estandarizar los datos
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_valid)

        # Aplicar Hierarchical Clustering (Agglomerative Clustering)
        num_clusters = 5
        agg_clustering = AgglomerativeClustering(n_clusters=num_clusters, linkage="ward")
        df_ucol.loc[df_valid.index, "Cluster"] = agg_clustering.fit_predict(df_scaled)

        # Aplicar t-SNE para reducir dimensiones
        tsne = TSNE(n_components=2, random_state=42)
        df_ucol.loc[df_valid.index, ["TSNE1", "TSNE2"]] = tsne.fit_transform(df_scaled)

        # Crear la gráfica de dispersión con t-SNE y curvas de nivel
        fig_clusters = px.scatter(
            df_ucol,
            x="TSNE1",
            y="TSNE2",
            color=df_ucol["Cluster"].astype(str),
            title="Visualización t-SNE de Clusters con Cuatro Variables (Hierarchical Clustering)",
            labels={"TSNE1": "Componente t-SNE 1", "TSNE2": "Componente t-SNE 2", "Cluster": "Cluster"},
            hover_data={
                "Author(s)_ID": True,
                "Normalized_Author_Name": True,
                "Seniority": True,
                "Funding_Ratio": True
            },
            template="plotly_white"
        )

        # Agregar curvas de nivel    
        fig_clusters.add_trace(go.Histogram2dContour(
            x=df_ucol["TSNE1"],
            y=df_ucol["TSNE2"],
            colorscale="blues",
            showscale=False
        ))

        st.plotly_chart(fig_clusters)


        # Filtrar los autores que están en el cluster 1.0
        df_cluster_0 = df_ucol[df_ucol["Cluster"] == 0.0]
        # Omitir las columnas "Correspondence_Address" y "Year" en el DataFrame df_cluster_1
        columns_to_exclude = ["Correspondence_Address", "Year", "Most_frequent_publisher"]
        df_cluster_0 = df_cluster_0.drop(columns=[col for col in columns_to_exclude if col in df_cluster_0.columns])
        df_cluster_0

        # Filtrar los autores que están en el cluster 1.0
        df_cluster_1 = df_ucol[df_ucol["Cluster"] == 1.0]
        # Omitir las columnas "Correspondence_Address" y "Year" en el DataFrame df_cluster_1
        columns_to_exclude = ["Correspondence_Address", "Year", "Most_frequent_publisher"]
        df_cluster_1 = df_cluster_1.drop(columns=[col for col in columns_to_exclude if col in df_cluster_1.columns])
        df_cluster_1

        # Filtrar los autores que están en el cluster 1.0
        df_cluster_2 = df_ucol[df_ucol["Cluster"] == 2.0]
        # Omitir las columnas "Correspondence_Address" y "Year" en el DataFrame df_cluster_1
        columns_to_exclude = ["Correspondence_Address", "Year", "Most_frequent_publisher"]
        df_cluster_2 = df_cluster_2.drop(columns=[col for col in columns_to_exclude if col in df_cluster_2.columns])
        df_cluster_2

        # Filtrar los autores que están en el cluster 1.0
        df_cluster_3 = df_ucol[df_ucol["Cluster"] == 3.0]
        # Omitir las columnas "Correspondence_Address" y "Year" en el DataFrame df_cluster_1
        columns_to_exclude = ["Correspondence_Address", "Year", "Most_frequent_publisher"]
        df_cluster_3 = df_cluster_3.drop(columns=[col for col in columns_to_exclude if col in df_cluster_3.columns])
        df_cluster_3

        # Filtrar los autores que están en el cluster 1.0
        df_cluster_4 = df_ucol[df_ucol["Cluster"] == 4.0]
        # Omitir las columnas "Correspondence_Address" y "Year" en el DataFrame df_cluster_1
        columns_to_exclude = ["Correspondence_Address", "Year", "Most_frequent_publisher"]
        df_cluster_4 = df_cluster_4.drop(columns=[col for col in columns_to_exclude if col in df_cluster_4.columns])
        df_cluster_4


        # Contar la cantidad de registros en cada cluster
        cluster_counts = df_ucol["Cluster"].value_counts().sort_index()

        # Calcular el porcentaje de cada cluster respecto al total
        total_count = len(df_ucol)
        cluster_percentages = (cluster_counts / total_count) * 100

        # Crear etiquetas con el total de autores por cluster
        labels = [f"Cluster {i} ({count} autores)" for i, count in cluster_counts.items()]

        # Crear gráfico de pastel con leyenda de total de autores
        fig_pie = go.Figure(data=[
            go.Pie(labels=labels, values=cluster_percentages, textinfo='label+percent', hole=0.4)
        ])
        fig_pie.update_layout(title_text=f"Distribución de Clusters en df_ucol\nTotal de autores: {total_count}")

        st.plotly_chart(fig_pie)


    ##################################################################################3

        import streamlit as st
        import pandas as pd
        import plotly.express as px
        import plotly.graph_objects as go
        import numpy as np
        from sklearn.preprocessing import StandardScaler
        from sklearn.cluster import AgglomerativeClustering
        from sklearn.manifold import TSNE
        import plotly.colors as pc

        st.title("📊 Clustering Jerárquico de Autores en Función de su Producción Académica")

        # Convertir a valores numéricos
        df_ucol["Cited_by"] = pd.to_numeric(df_ucol["Cited_by"], errors='coerce')
        df_ucol["Publications"] = pd.to_numeric(df_ucol["Publications"], errors='coerce')
        df_ucol["Funded_publications"] = pd.to_numeric(df_ucol["Funded_publications"], errors='coerce')
        df_ucol["Seniority"] = pd.to_numeric(df_ucol["Seniority"], errors='coerce')

        # Crear la variable Funding Ratio
        df_ucol["Funding_Ratio"] = df_ucol["Funded_publications"] / df_ucol["Publications"]
        df_ucol["Funding_Ratio"] = df_ucol["Funding_Ratio"].fillna(0)

        # Eliminar índices duplicados si existen
        df_ucol = df_ucol.drop_duplicates()

        # Filtrar solo las columnas necesarias para el análisis    
        df_boxplot = df_ucol[["Cluster", "Publications", "Cited_by", "Seniority", "Funding_Ratio"]].copy()

        # Convertir "Cluster" a tipo categórico
        df_boxplot["Cluster"] = df_boxplot["Cluster"].astype(str)
    
        # Definir colores de los clusters extraídos de la visualización t-SNE
        cluster_colors = pc.qualitative.Plotly[:len(df_boxplot["Cluster"].unique())]
        color_mapping = {str(cluster): color for cluster, color in zip(df_boxplot["Cluster"].unique(), cluster_colors)}

        # Crear los diagramas de caja con los colores de los clusters
        fig1 = px.box(df_boxplot, x="Cluster", y="Publications", color="Cluster",
              title="Número de Publicaciones por Cluster",
              labels={"Cluster": "Cluster", "Publications": "Número de Publicaciones"},
              notched=True, template="plotly_white",
              color_discrete_map=color_mapping)

        fig2 = px.box(df_boxplot, x="Cluster", y="Cited_by", color="Cluster",
              title="Número de Citas por Cluster",
              labels={"Cluster": "Cluster", "Cited_by": "Número de Citas"},
              notched=True, template="plotly_white",
              color_discrete_map=color_mapping)

        fig3 = px.box(df_boxplot, x="Cluster", y="Funding_Ratio", color="Cluster",
              title="Cociente de Publicaciones Financiadas por Cluster",
              labels={"Cluster": "Cluster", "Funding_Ratio": "Proporción de Publicaciones Financiadas"},
              notched=True, template="plotly_white",
              color_discrete_map=color_mapping)

        fig4 = px.box(df_boxplot, x="Cluster", y="Seniority", color="Cluster",
              title="Antigüedad por Cluster",
              labels={"Cluster": "Cluster", "Seniority": "Años desde la Primera Publicación"},
              notched=True, template="plotly_white",
              color_discrete_map=color_mapping)

        # Mostrar las gráficas en Streamlit
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
        st.plotly_chart(fig3)
        st.plotly_chart(fig4)

    #####################################################################################333

        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import plotly.express as px
        from sklearn.model_selection import train_test_split
        from sklearn.tree import DecisionTreeClassifier, plot_tree
        from sklearn.metrics import classification_report, confusion_matrix
        import seaborn as sns

        
        # 🏆 **Árbol de Decisión para Predicción de Clusters**
        st.header("🌳 Árbol de Decisión para Predicción de Clusters")

        # Filtrar datos válidos
        df_valid = df_ucol.dropna(subset=["Funding_Ratio", "Publications", "Cited_by", "Seniority", "Cluster"])

        # Definir variables predictoras y objetivo
        X = df_valid[["Funding_Ratio", "Publications", "Cited_by", "Seniority"]]

        # Crear un diccionario para asignar los clusters originales a etiquetas ordenadas
        cluster_mapping = {cluster: idx for idx, cluster in enumerate(sorted(df_valid["Cluster"].unique()))}
        reverse_mapping = {v: k for k, v in cluster_mapping.items()}  # Para revertir la codificación

        # Reemplazar los valores originales por los índices ordenados
        y = df_valid["Cluster"].map(cluster_mapping).astype(int)

        # Dividir en conjunto de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Entrenar el modelo de Árbol de Decisión
        clf = DecisionTreeClassifier(random_state=42, max_depth=4)
        clf.fit(X_train, y_train)

        # Evaluar el modelo
        y_pred = clf.predict(X_test)

        # Reconvertir las predicciones y etiquetas originales a los valores reales de cluster
        y_test_original = y_test.map(reverse_mapping)
        y_pred_original = pd.Series(y_pred).map(reverse_mapping)

        # Matriz de confusión
        st.subheader("📌 Matriz de Confusión")
        st.write(pd.DataFrame(confusion_matrix(y_test_original, y_pred_original),
                      index=[f"Actual {reverse_mapping[c]}" for c in sorted(y.unique())],
                      columns=[f"Predicho {reverse_mapping[c]}" for c in sorted(y.unique())]))

        # Reporte de Clasificación
        st.subheader("📌 Reporte de Clasificación")
        st.text(classification_report(y_test_original, y_pred_original))

        # Importancia de las Variables
        st.subheader("📌 Importancia de las Variables en el Modelo")
        importances = pd.Series(clf.feature_importances_, index=X.columns)
        fig_importance = px.bar(importances, x=importances.index, y=importances.values,
                        labels={"x": "Variables", "y": "Importancia Relativa"},
                        title="Importancia de las Variables en el Árbol de Decisión",
                        template="plotly_white")
        st.plotly_chart(fig_importance)

        # Visualización del Árbol de Decisión
        st.subheader("📌 Visualización del Árbol de Decisión")
        fig, ax = plt.subplots(figsize=(30, 15))
        plot_tree(clf, feature_names=X.columns, class_names=[str(reverse_mapping[c]) for c in sorted(y.unique())],
                  filled=True, fontsize=8, ax=ax)
        st.pyplot(fig)



        import streamlit as st
        import pandas as pd
        import plotly.express as px
        import plotly.graph_objects as go
        import numpy as np
        from sklearn.preprocessing import StandardScaler
        from sklearn.cluster import AgglomerativeClustering
        from sklearn.manifold import TSNE
        import plotly.colors as pc
        from sklearn.model_selection import train_test_split
        from sklearn.tree import DecisionTreeClassifier, plot_tree
        from sklearn.metrics import classification_report, confusion_matrix
        import seaborn as sns
        import matplotlib.pyplot as plt

        st.title("📊 Clustering Jerárquico y Árbol de Decisión de Autores en Función de su Producción Académica")

        # Convertir a valores numéricos
        df_ucol["Cited_by"] = pd.to_numeric(df_ucol["Cited_by"], errors='coerce')
        df_ucol["Publications"] = pd.to_numeric(df_ucol["Publications"], errors='coerce')
        df_ucol["Funded_publications"] = pd.to_numeric(df_ucol["Funded_publications"], errors='coerce')
        df_ucol["Seniority"] = pd.to_numeric(df_ucol["Seniority"], errors='coerce')

        # Crear la variable Funding Ratio
        df_ucol["Funding_Ratio"] = df_ucol["Funded_publications"] / df_ucol["Publications"]
        df_ucol["Funding_Ratio"] = df_ucol["Funding_Ratio"].fillna(0)

        # Filtrar datos válidos
        df_valid = df_ucol.dropna(subset=["Funding_Ratio", "Publications", "Cited_by", "Seniority", "Cluster"])

        # Definir variables predictoras y objetivo
        X = df_valid[["Funding_Ratio", "Publications", "Cited_by", "Seniority"]]

        # Crear un diccionario para asignar los clusters originales a etiquetas ordenadas
        cluster_mapping = {cluster: idx for idx, cluster in enumerate(sorted(df_valid["Cluster"].unique()))}
        reverse_mapping = {v: k for k, v in cluster_mapping.items()}  # Para revertir la codificación

        # Reemplazar los valores originales por los índices ordenados    
        y = df_valid["Cluster"].map(cluster_mapping).astype(int)

        # Entrenar el modelo de Árbol de Decisión
        clf = DecisionTreeClassifier(random_state=42, max_depth=4)
        clf.fit(X, y)

        # 📌 **Formulario Inteligente para Asignación de Cluster**
        st.header("📝 Predicción de Cluster Basado en Estadísticas de Autor")

        funding_ratio = st.number_input("Proporción de Publicaciones Financiadas", min_value=0.0, max_value=1.0, step=0.01)
        publications = st.number_input("Número de Publicaciones", min_value=0, step=1)
        cited_by = st.number_input("Número de Citas", min_value=0, step=1)
        seniority = st.number_input("Antigüedad (Años desde Primera Publicación)", min_value=0, max_value=100, step=1)

        if st.button("📌 Asignar Cluster"):
            user_data = np.array([[funding_ratio, publications, cited_by, seniority]])
            predicted_cluster_idx = clf.predict(user_data)[0]
            #predicted_cluster = str(reverse_mapping[predicted_cluster_idx])  # 🔹 Convertir a string para evitar errores en el diccionario
            predicted_cluster = str(int(reverse_mapping[predicted_cluster_idx]))  # 🔹 Convertimos primero a entero y luego a string

            st.success(f"🎯 Has sido asignado al Cluster {predicted_cluster}")
        
            # Explicación basada en el perfil de publicaciones
            cluster_explanations = {
                "0": "Autores con baja producción y pocas citas, posiblemente en inicio de carrera. "
                     "Suelen tener una antigüedad variable, pero con baja producción en publicaciones y un impacto limitado en citas. "
                     "El financiamiento es bajo o moderado. Estos autores pueden estar comenzando su trayectoria o no enfocarse completamente en la investigación.",

                "1": "Autores con una trayectoria consolidada, con muchas publicaciones y alta citación. "
                     "Son investigadores de alto impacto, con un gran número de publicaciones y citas. "
                     "Suelen tener una antigüedad alta en la academia (> 9.5 años) y financiamiento moderado o alto. "
                     "Frecuentemente tienen colaboraciones internacionales y publican en revistas de alto impacto.",

                "2": "Autores con producción moderada y algunas citas, con crecimiento académico estable. "
                     "Estos investigadores tienen una producción media en publicaciones y citas. "
                     "Suelen contar con financiamiento moderado y más de 9.5 años de antigüedad en la academia. "
                     "Es un perfil típico de académicos en consolidación o en áreas emergentes con un crecimiento estable en citas.",

                "3": "Autores en inicio de carrera con baja producción. "
                     "Tienen pocos años en la academia (≤ 9.5 años), pocas publicaciones y bajo impacto en citas. "
                     "El financiamiento es bajo o nulo, y su producción aún no ha crecido significativamente. "
                     "Pueden ser investigadores jóvenes, profesores con menor enfoque en investigación o estudiantes de doctorado.",

                "4": "Autores con producción alta y financiamiento significativo. "
                     "Son líderes en investigación con múltiples proyectos financiados. "
                     "Tienen una producción establecida en revistas de alto impacto y acceso a financiamiento significativo. "
                     "Suelen tener una antigüedad alta, con equipos de trabajo consolidados y un alto impacto en citas."
            }

    
            st.info(cluster_explanations.get(predicted_cluster, "Descripción no disponible."))

        ##############################################################################

        # 📌 **Comparación Tabular del Usuario con Cluster y Base Completa**
        st.subheader("📋 Comparación con el Cluster y la Base Completa")

        # 📌 **Comparación Visual Mejorada con Dos Arreglos de Gráficos**
        st.header("📊 Comparación del Usuario con su Cluster y la Base Completa")

        # 📌 **Filtrar Datos del Cluster y Crear DataFrame del Usuario**
        df_cluster = df_valid[df_valid["Cluster"] == int(predicted_cluster)]

        df_user = pd.DataFrame({
            "Métrica": ["Publications", "Cited_by", "Seniority", "Funding_Ratio"],
            "Valor": [publications, cited_by, seniority, funding_ratio]
        })


        
        # 📌 **Calcular Estadísticas**
        comparison_data = {
            "Métrica": ["Publicaciones", "Citas", "Antigüedad", "Ratio de Financiamiento"],
            "Valor del Usuario": [publications, cited_by, seniority, funding_ratio],
    
            # 📌 **Estadísticas del Cluster**
            "Cluster - Media": [
                df_cluster["Publications"].mean(), df_cluster["Cited_by"].mean(),
                df_cluster["Seniority"].mean(), df_cluster["Funding_Ratio"].mean()
            ],
            "Cluster - Q1 (P25)": [
                df_cluster["Publications"].quantile(0.25), df_cluster["Cited_by"].quantile(0.25),
                df_cluster["Seniority"].quantile(0.25), df_cluster["Funding_Ratio"].quantile(0.25)
            ],
            "Cluster - Q3 (P75)": [
                df_cluster["Publications"].quantile(0.75), df_cluster["Cited_by"].quantile(0.75),
                df_cluster["Seniority"].quantile(0.75), df_cluster["Funding_Ratio"].quantile(0.75)
            ],

            # 📌 **Estadísticas de la Base Completa**
            "Base - Media": [
                df_valid["Publications"].mean(), df_valid["Cited_by"].mean(),
                df_valid["Seniority"].mean(), df_valid["Funding_Ratio"].mean()
            ],
            "Base - Q1 (P25)": [
                df_valid["Publications"].quantile(0.25), df_valid["Cited_by"].quantile(0.25),
                df_valid["Seniority"].quantile(0.25), df_valid["Funding_Ratio"].quantile(0.25)
            ],
            "Base - Q3 (P75)": [
                df_valid["Publications"].quantile(0.75), df_valid["Cited_by"].quantile(0.75),
                df_valid["Seniority"].quantile(0.75), df_valid["Funding_Ratio"].quantile(0.75)
            ]
        }

        # 📌 **Convertir a DataFrame**
        df_comparison = pd.DataFrame(comparison_data)

        # 📌 **Mostrar la Tabla en Streamlit**
        st.dataframe(df_comparison.style.format({
            "Valor del Usuario": "{:.2f}",
            "Cluster - Media": "{:.2f}", "Cluster - Q1 (P25)": "{:.2f}", "Cluster - Q3 (P75)": "{:.2f}",
            "Base - Media": "{:.2f}", "Base - Q1 (P25)": "{:.2f}", "Base - Q3 (P75)": "{:.2f}"
        }))



#############################################################################################################


        # 📌 **Definir Función para Graficar Comparaciones**
        def plot_comparison(metric, title, y_label):
            fig_cluster = px.box(df_cluster, y=metric, points="all", 
                         title=f"{title} en el Cluster {predicted_cluster}",
                         labels={metric: y_label},
                         template="plotly_white")
    
            fig_cluster.add_trace(go.Scatter(
                x=["Usuario"], y=[df_user[df_user["Métrica"] == metric]["Valor"].values[0]], 
                mode="markers+text", text="📍", textposition="top center",
                marker=dict(color="red", size=12),
                name="Usuario"
            ))
    
            fig_base = px.box(df_valid, y=metric, points="all", 
                      title=f"{title} en Toda la Base",
                      labels={metric: y_label},
                      template="plotly_white")
    
            fig_base.add_trace(go.Scatter(
                x=["Usuario"], y=[df_user[df_user["Métrica"] == metric]["Valor"].values[0]], 
                mode="markers+text", text="📍", textposition="top center",
                marker=dict(color="red", size=12),
                name="Usuario"
            ))
    
            return fig_cluster, fig_base

        # 📌 **Comparaciones por Métrica**
        fig_pub_cluster, fig_pub_base = plot_comparison("Publications", "Número de Publicaciones", "Publicaciones")
        fig_cite_cluster, fig_cite_base = plot_comparison("Cited_by", "Número de Citas", "Citas")
        fig_sen_cluster, fig_sen_base = plot_comparison("Seniority", "Antigüedad", "Años desde la Primera Publicación")
        fig_fund_cluster, fig_fund_base = plot_comparison("Funding_Ratio", "Proporción de Publicaciones Financiadas", "Ratio de Financiamiento")

        # 📌 **Mostrar Gráficos**
        st.subheader(f"📊 Comparación con Autores del Cluster {predicted_cluster}")
        st.plotly_chart(fig_pub_cluster)
        st.plotly_chart(fig_cite_cluster)
        st.plotly_chart(fig_sen_cluster)
        st.plotly_chart(fig_fund_cluster)

        st.subheader("📊 Comparación con Toda la Base de Datos")
        st.plotly_chart(fig_pub_base)    
        st.plotly_chart(fig_cite_base)
        st.plotly_chart(fig_sen_base)
        st.plotly_chart(fig_fund_base)










    
    else:
        st.info("📂 **Sube un archivo CSV para comenzar**")











    



##############################################################################################################################3
elif pagina == "Análisis por autor":
    # Sección Markdown explicativa
    st.markdown("""
    ## Análisis de Datos por Autor

    El siguiente código muestra algunos datos por autor. Al correrlo:

    1. **Ingrese el apellido del autor**. Se desplegarán todos los autores que compartan apellido. En muchos casos, se mostrará más de un nombre por ID debido a que en ocasiones el nombre con el que se firma el artículo varía.
    2. **Ingrese el ID del autor** para ver los datos asociados a ese ID.

    El tipo de información que se desplegará será:
    - **Autores asociados con el ID**
    - **Total de citas asociadas**
    - **Total de artículos en los que participa el ID**
    - **Año más antiguo de publicación**
    - **Año más reciente de publicación**

    Además, se generarán las siguientes gráficas:
    - **Total de publicaciones vs. tiempo**
    - **Total de citas vs. tiempo**
    - **Gráfico de barras con las principales editoriales en las que publica el autor**
    """)



    import streamlit as st
    import pandas as pd
    import re
    import matplotlib.pyplot as plt

    @st.cache_data
    def load_data(file):
        df = pd.read_csv(file, encoding='utf-8')
        return df


    # Función para obtener autores por apellido
    @st.cache_data
    def get_author_options(df, author_last_name):
        if "Authors" not in df.columns or "Author(s) ID" not in df.columns:
            st.error("No se encontraron las columnas necesarias en el archivo.")
            return {}

        author_dict = {}
        for _, row in df.dropna(subset=["Authors", "Author(s) ID"]).iterrows():
            authors = row["Authors"].split(";")
            ids = str(row["Author(s) ID"]).split(";")
            for author, author_id in zip(authors, ids):
                author = author.strip()
                if author_last_name.lower() in author.lower():
                    author_dict.setdefault(author_id.strip(), []).append(author)

        return author_dict

    # Función para obtener nombres de autores por ID
    @st.cache_data
    def get_authors_by_id(df, selected_id):
        if "Authors" not in df.columns or "Author(s) ID" not in df.columns:
            st.error("No se encontraron las columnas necesarias en el archivo.")
            return []

        matching_authors = set()
        for _, row in df.dropna(subset=["Authors", "Author(s) ID"]).iterrows():
            authors = row["Authors"].split(";")
            ids = str(row["Author(s) ID"]).split(";")
            for author, author_id in zip(authors, ids):
                if author_id.strip() == selected_id:
                    matching_authors.add(author.strip())

        return list(matching_authors)

    # Función para obtener estadísticas del autor
    @st.cache_data
    def get_author_stats(df, selected_id):
        if "Author(s) ID" not in df.columns:
            st.error("No se encontraron las columnas necesarias en el archivo.")
            return {}

        df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
    
        total_citations = df_filtered["Cited by"].fillna(0).astype(int).sum() if "Cited by" in df.columns else 0
        total_articles = df_filtered.shape[0]
    
        min_year, max_year, year_counts = None, None, None
        if "Year" in df.columns:
            years = df_filtered["Year"].dropna().astype(int)
            if not years.empty:
                min_year, max_year = years.min(), years.max()
                year_counts = years.value_counts().sort_index()

        publisher_info = pd.DataFrame()
        if "Publisher" in df.columns and "Cited by" in df.columns:
            publisher_info = df_filtered.groupby("Publisher").agg(
                num_articles=("Title", "count"),
                total_citations=("Cited by", "sum")
            ).reset_index()

        return {
            "total_citations": total_citations,
            "total_articles": total_articles,
            "min_year": min_year,
            "max_year": max_year,
            "year_counts": year_counts,
            "publisher_info": publisher_info
        }

    # Función para graficar las publicaciones por año
    def plot_publications(year_counts, selected_id):
        if year_counts is None or year_counts.empty:
            st.warning("No se encontraron años de publicación para este autor.")
            return
    
        fig, ax = plt.subplots(figsize=(10, 5))
        year_counts.plot(kind='bar', color='blue', ax=ax)
        ax.set_xlabel("Año de publicación")
        ax.set_ylabel("Numero de publicaciones")
        ax.set_title(f"Publicaciones por año - ID {selected_id}")
        ax.set_xticklabels(year_counts.index, rotation=45)
        st.pyplot(fig)

    #@st.cache_data
    uploaded_file = st.file_uploader("Suba un archivo CSV", type=["csv"])
    file_path = "scopusUdeC con financiamiento 17 feb-2.csv"
    # Función para cargar y almacenar el DataFrame en caché
    #@st.cache_data
    #def load_data(file):
    #    return pd.read_csv(file, encoding='utf-8')


    #def get_total_citations(file_path, selected_id):
    #    #df = pd.read_csv(file_path, encoding='utf-8')
    #    df = load_data(uploaded_file) 
    #    if "Author(s) ID" not in df.columns or "Cited by" not in df.columns:
    #        print("No se encontraron las columnas necesarias en el archivo.")
    #        return 0

    #    df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
    #    total_citations = df_filtered["Cited by"].fillna(0).astype(int).sum()

    #    return total_citations

    def get_total_citations(df, selected_id):
        """Calcula el total de citas asociadas a un ID de autor en el DataFrame."""
        if "Author(s) ID" not in df.columns or "Cited by" not in df.columns:
            st.error("❌ No se encontraron las columnas necesarias en el archivo.")
            return 0

        df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
        total_citations = df_filtered["Cited by"].fillna(0).astype(int).sum()

        return total_citations

    
    #def get_total_articles(file_path, selected_id):
    #    df = pd.read_csv(file_path, encoding='utf-8')
    #    if "Author(s) ID" not in df.columns:
    #        print("No se encontraron las columnas necesarias en el archivo.")
    #        return 0

   #     df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
   #     total_articles = df_filtered.shape[0]

   #     return total_articles

    def get_total_articles(df, selected_id):
        """Calcula el total de artículos en los que participa un ID de autor."""
        if "Author(s) ID" not in df.columns:
            st.error("❌ No se encontró la columna 'Author(s) ID' en el archivo.")
            return 0

        df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
        total_articles = df_filtered.shape[0]

        return total_articles



    #def get_publication_years(file_path, selected_id):
    #    df = pd.read_csv(file_path, encoding='utf-8')
    #    if "Author(s) ID" not in df.columns or "Year" not in df.columns:
    #        print("No se encontraron las columnas necesarias en el archivo.")
    #        return None, None, None, None

    #    df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
    #    years = df_filtered["Year"].dropna().astype(int)
    #    if years.empty:
    #        return None, None, None, None

    #    min_year = years.min()
    #    max_year = years.max()
    #    year_counts = years.value_counts().sort_index()

    #    # Total de citas por año
    #    citations_per_year = df_filtered.groupby("Year")["Cited by"].sum().fillna(0).astype(int)

    #    return min_year, max_year, year_counts, citations_per_year

    def get_publication_years(df, selected_id):
        """Obtiene el rango de años de publicación y el número de publicaciones/citas por año de un autor."""
        df = load_data(uploaded_file)
        if "Author(s) ID" not in df.columns or "Year" not in df.columns:
            st.error("❌ No se encontraron las columnas necesarias en el archivo.")
            return None, None, None, None

        df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
        years = df_filtered["Year"].dropna().astype(int)

        if years.empty:
            return None, None, None, None

        min_year = years.min()
        max_year = years.max()
        year_counts = years.value_counts().sort_index()

        # Total de citas por año
        if "Cited by" in df_filtered.columns:
            citations_per_year = df_filtered.groupby("Year")["Cited by"].sum().fillna(0).astype(int)
        else:
            citations_per_year = None

        return min_year, max_year, year_counts, citations_per_year


#    def get_publisher_info(file_path, selected_id):
#        df = pd.read_csv(file_path, encoding='utf-8')
#        if "Author(s) ID" not in df.columns or "Publisher" not in df.columns or "Cited by" not in df.columns:
#            print("No se encontraron las columnas necesarias en el archivo.")
#            return None

#        df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
#        publisher_stats = df_filtered.groupby("Publisher").agg(
#            num_articles=("Title", "count"),
#            total_citations=("Cited by", "sum")
#        ).reset_index()

#        return publisher_stats

    def get_publisher_info(df, selected_id):
        """Obtiene información sobre las editoriales donde ha publicado un autor."""
        required_columns = ["Author(s) ID", "Publisher", "Cited by", "Title"]

        # Verificar que todas las columnas necesarias existen
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"❌ No se encontraron las columnas necesarias en el archivo: {', '.join(missing_columns)}")
            return None

        # Filtrar los artículos en los que ha participado el autor
        df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]

        # Agrupar por editorial y calcular número de artículos y citas
        publisher_stats = df_filtered.groupby("Publisher").agg(
            num_articles=("Title", "count"),
            total_citations=("Cited by", "sum")
        ).reset_index()

        return publisher_stats

    def get_top_cited_articles(df, selected_id, top_n=10):
        """
        Obtiene los artículos más citados de un autor, incluyendo título, número de citas, año y editorial.

        Parámetros:
        - df: DataFrame con los datos de publicaciones.
        - selected_id: ID del autor.
        - top_n: Número de artículos a mostrar (por defecto, 10).

        Retorna:
        - DataFrame con los artículos más citados del autor.
        """

        required_columns = ["Author(s) ID", "Title", "Cited by", "Year", "Source title", "Publisher"]

        # Verificar que todas las columnas necesarias existen
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"❌ No se encontraron las columnas necesarias en el archivo: {', '.join(missing_columns)}")
            return None

        # Filtrar los artículos en los que ha participado el autor
        df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]

        # Asegurar que "Cited by" y "Year" sean valores numéricos
        df_filtered["Cited by"] = pd.to_numeric(df_filtered["Cited by"], errors="coerce").fillna(0).astype(int)
        #df_filtered["Year"] = pd.to_numeric(df_filtered["Year"], errors="coerce")
        df_filtered["Year"] = pd.to_numeric(df_filtered["Year"], errors="coerce").fillna(0).astype(int)

        # Seleccionar las columnas necesarias
        top_articles = df_filtered[["Title", "Cited by", "Year", "Source title", "Publisher"]]

        # Ordenar por número de citas en orden descendente
        top_articles = top_articles.sort_values(by="Cited by", ascending=False).head(top_n)

        return top_articles




    def plot_publications(year_counts, selected_id):
        if year_counts is not None and not year_counts.empty:
            fig, ax = plt.subplots(figsize=(10, 5))
            year_counts.plot(kind='bar', color='blue', ax=ax)
            ax.set_xlabel("Año de publicación")
            ax.set_ylabel("Número de publicaciones")
            ax.set_title(f"Publicaciones por año - ID {selected_id}")
            ax.set_xticklabels(year_counts.index, rotation=45)
            st.pyplot(fig)

    def plot_citations_per_year(citations_per_year, selected_id):
        if citations_per_year is not None and not citations_per_year.empty:
            fig, ax = plt.subplots(figsize=(10, 5))
            citations_per_year.plot(kind='bar', color='red', ax=ax)
            ax.set_xlabel("Año")
            ax.set_ylabel("Total de citas")
            ax.set_title(f"Citas por año - ID {selected_id}")
            ax.set_xticklabels(citations_per_year.index, rotation=45)
            st.pyplot(fig)

    def plot_publisher_info(publisher_info, selected_id):
        if publisher_info is not None and not publisher_info.empty:
            publisher_info = publisher_info.sort_values(by="num_articles", ascending=False).head(10)

            fig, ax1 = plt.subplots(figsize=(12, 6))  # Ajustar tamaño para mejor visibilidad en Streamlit

            # Barras para número de artículos
            bars = ax1.bar(publisher_info["Publisher"], publisher_info["num_articles"], label="Número de artículos", alpha=0.7)
            ax1.set_xlabel("Editorial")
            ax1.set_ylabel("Número de artículos", color="blue")
            ax1.tick_params(axis="y", labelcolor="blue")

            # Línea para número de citas
            ax2 = ax1.twinx()
            ax2.plot(publisher_info["Publisher"], publisher_info["total_citations"], marker="o", linestyle="dashed", color="red", label="Total de citas")
            ax2.set_ylabel("Total de citas", color="red")
            ax2.tick_params(axis="y", labelcolor="red")

            plt.title(f"Principales editoriales donde publica ID {selected_id}")

            # Rotar etiquetas en el eje X
            ax1.set_xticklabels(publisher_info["Publisher"], rotation=45, ha="right", fontsize=10)

            # Ajustar margen inferior
            plt.tight_layout()

            # Mostrar gráfico en Streamlit
            st.pyplot(fig)


    

    #if uploaded_file:
    df = load_data(uploaded_file)

    # Input para apellido del autor
    author_last_name = st.text_input("Ingresa el apellido del autor")

    if author_last_name:
        available_authors = get_author_options(df, author_last_name)

        if available_authors:
            st.write("Autores encontrados:")
            author_options = {f"ID: {id_} - Nombres: {', '.join(authors)}": id_ for id_, authors in available_authors.items()}
            selected_id = st.selectbox("Seleccione el ID del autor:", list(author_options.keys()))

            if selected_id:
                selected_id = author_options[selected_id]  # Extrae el ID real
                matching_authors = get_authors_by_id(df, selected_id)

                if matching_authors:
                    st.write(f"Autores con ID {selected_id}: {', '.join(matching_authors)}")

                    author_stats = get_author_stats(df, selected_id)
                    st.write(f"**Total de citas asociadas:** {author_stats['total_citations']}")
                    st.write(f"**Total de artículos en los que participa:** {author_stats['total_articles']}")
                    
                    if author_stats['min_year'] and author_stats['max_year']:
                        st.write(f"**Año más antiguo de publicación:** {author_stats['min_year']}")
                        st.write(f"**Año más reciente de publicación:** {author_stats['max_year']}")
                        #plot_publications(author_stats['year_counts'], selected_id)

                    if not author_stats['publisher_info'].empty:
                        st.write("**Editoriales en las que ha publicado este ID:**")
                        st.dataframe(author_stats['publisher_info'])
                    
                    
                    print(f"Autores con ID {selected_id}: {', '.join(matching_authors)}")

                    #total_citations = get_total_citations(file_path, selected_id)
                    total_citations = get_total_citations(df, selected_id)
                    print(f"Total de citas asociadas a ID {selected_id}: {total_citations}")

                    #total_articles = get_total_articles(file_path, selected_id)
                    total_articles = get_total_articles(df, selected_id)
                    print(f"Total de artículos en los que participa ID {selected_id}: {total_articles}")

                    min_year, max_year, year_counts, citations_per_year = get_publication_years(file_path, selected_id)
                    if min_year and max_year:
                        print(f"Año más antiguo de publicación: {min_year}")
                        print(f"Año más reciente de publicación: {max_year}")
                        plot_publications(year_counts, selected_id)
                        plot_citations_per_year(citations_per_year, selected_id)
                    else:
                        print("No se encontraron años de publicación para este autor.")

                    top_articles = get_top_cited_articles(df, selected_id, top_n=10)

                    if top_articles is not None and not top_articles.empty:
                        #st.table(top_articles)
                        top_articles["Year"] = top_articles["Year"].astype(str)  # Convertir a string para evitar comas
                        #top_articles["Year"] = top_articles["Year"].astype(int)  # Forzar tipo entero sin formato
                        st.dataframe(top_articles)

                    else:
                        st.warning("⚠️ No se encontraron artículos con citas registradas para este autor.")
                    publisher_info = get_publisher_info(df, selected_id)
                    if publisher_info is not None and not publisher_info.empty:
                        print("Editoriales en las que ha publicado este ID:")
                        #display(publisher_info)
                        plot_publisher_info(publisher_info, selected_id)                  
                    else:
                        st.warning("No se encontraron editoriales para este autor.")
            else:
                st.warning("No se encontraron autores con ese ID.")
        else:
            st.warning("No se encontraron coincidencias para ese apellido.")

    #def get_author_options(file_path, author_last_name):
    #    df = pd.read_csv(file_path, encoding='utf-8')
    #    if "Authors" not in df.columns or "Author(s) ID" not in df.columns:
    #        print("No se encontraron las columnas necesarias en el archivo.")
    #        return {}

    #    author_dict = {}
    #    for _, row in df.dropna(subset=["Authors", "Author(s) ID"]).iterrows():
    #        authors = row["Authors"].split(";")
    #        ids = str(row["Author(s) ID"]).split(";")
    #        for author, author_id in zip(authors, ids):
    #            author = author.strip()
    #            if author_last_name.lower() in author.lower():
    #                author_dict.setdefault(author_id.strip(), []).append(author)

    #    return author_dict

    #def get_authors_by_id(file_path, selected_id):
    #    df = pd.read_csv(file_path, encoding='utf-8')
    #    if "Authors" not in df.columns or "Author(s) ID" not in df.columns:
    #        print("No se encontraron las columnas necesarias en el archivo.")
    #        return []

    #    matching_authors = set()
    #    for _, row in df.dropna(subset=["Authors", "Author(s) ID"]).iterrows():
    #        authors = row["Authors"].split(";")
    #        ids = str(row["Author(s) ID"]).split(";")
    #        for author, author_id in zip(authors, ids):
    #            if author_id.strip() == selected_id:
    #                matching_authors.add(author.strip())

    #    return list(matching_authors)

    #def get_total_citations(file_path, selected_id):
    #    df = pd.read_csv(file_path, encoding='utf-8')
    #    if "Author(s) ID" not in df.columns or "Cited by" not in df.columns:
    #        print("No se encontraron las columnas necesarias en el archivo.")
    #        return 0#

    #    df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
    #    total_citations = df_filtered["Cited by"].fillna(0).astype(int).sum()

    #    return total_citations

    #def get_total_articles(file_path, selected_id):
    #    df = pd.read_csv(file_path, encoding='utf-8')
    #    if "Author(s) ID" not in df.columns:
    #        print("No se encontraron las columnas necesarias en el archivo.")
    #        return 0

    #    df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
    #    total_articles = df_filtered.shape[0]

    #    return total_articles

    #def get_publication_years(file_path, selected_id):
    #    df = pd.read_csv(file_path, encoding='utf-8')
    #    if "Author(s) ID" not in df.columns or "Year" not in df.columns:
    #        print("No se encontraron las columnas necesarias en el archivo.")
    #        return None, None, None, None

    #    df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
    #    years = df_filtered["Year"].dropna().astype(int)
    #    if years.empty:
    #        return None, None, None, None

    #    min_year = years.min()
    #    max_year = years.max()
    #    year_counts = years.value_counts().sort_index()

    #    # Total de citas por año
    #    citations_per_year = df_filtered.groupby("Year")["Cited by"].sum().fillna(0).astype(int)

    #    return min_year, max_year, year_counts, citations_per_year

    #def get_publisher_info(file_path, selected_id):
    #    df = pd.read_csv(file_path, encoding='utf-8')
    #    if "Author(s) ID" not in df.columns or "Publisher" not in df.columns or "Cited by" not in df.columns:
    #        print("No se encontraron las columnas necesarias en el archivo.")
    #        return None

    #    df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
    #    publisher_stats = df_filtered.groupby("Publisher").agg(
    #        num_articles=("Title", "count"),
    #        total_citations=("Cited by", "sum")
    #    ).reset_index()

    #    return publisher_stats

    def plot_publications(year_counts, selected_id):
        if year_counts is not None and not year_counts.empty:
            fig, ax = plt.subplots(figsize=(10, 5))
            year_counts.plot(kind='bar', color='blue', ax=ax)
            ax.set_xlabel("Año de publicación")
            ax.set_ylabel("Número de publicaciones")
            ax.set_title(f"Publicaciones por año - ID {selected_id}")
            ax.set_xticklabels(year_counts.index, rotation=45)
            st.pyplot(fig)

    def plot_citations_per_year(citations_per_year, selected_id):
        if citations_per_year is not None and not citations_per_year.empty:
            fig, ax = plt.subplots(figsize=(10, 5))
            citations_per_year.plot(kind='bar', color='red', ax=ax)
            ax.set_xlabel("Año")
            ax.set_ylabel("Total de citas")
            ax.set_title(f"Citas por año - ID {selected_id}")
            ax.set_xticklabels(citations_per_year.index, rotation=45)
            st.pyplot(fig)


    

    def plot_publisher_info(publisher_info, selected_id):
        if publisher_info is not None and not publisher_info.empty:
            publisher_info = publisher_info.sort_values(by="num_articles", ascending=False).head(10)

            fig, ax1 = plt.subplots(figsize=(12, 6))  # Ajustar tamaño para mejor visibilidad en Streamlit

            # Barras para número de artículos
            bars = ax1.bar(publisher_info["Publisher"], publisher_info["num_articles"], label="Número de artículos", alpha=0.7)
            ax1.set_xlabel("Editorial")
            ax1.set_ylabel("Número de artículos", color="blue")
            ax1.tick_params(axis="y", labelcolor="blue")

            # Línea para número de citas
            ax2 = ax1.twinx()
            ax2.plot(publisher_info["Publisher"], publisher_info["total_citations"], marker="o", linestyle="dashed", color="red", label="Total de citas")
            ax2.set_ylabel("Total de citas", color="red")
            ax2.tick_params(axis="y", labelcolor="red")

            plt.title(f"Principales editoriales donde publica ID {selected_id}")

            # Rotar etiquetas en el eje X
            ax1.set_xticklabels(publisher_info["Publisher"], rotation=45, ha="right", fontsize=10)

            # Ajustar margen inferior
            plt.tight_layout()

            # Mostrar gráfico en Streamlit
            st.pyplot(fig)


    import streamlit as st
    import pandas as pd
    import re
    import seaborn as sns
    import matplotlib.pyplot as plt

    def process_author_data(file):
        #df = pd.read_csv(file, encoding='utf-8')
        df = load_data(uploaded_file)
        df.columns = df.columns.str.strip().str.replace(" ", "_")  # Reemplazar espacios en nombres de columnas

        # Verificar la existencia de las columnas necesarias
        required_columns = ["Author_full_names", "Author(s)_ID", "Cited_by"]
        if not all(col in df.columns for col in required_columns):
            st.error(f"Faltan columnas necesarias en el archivo: {', '.join(required_columns)}")
            return None

        # Crear un diccionario con nombres completos y sus IDs
        author_id_map = {}
        for row in df.dropna(subset=["Author_full_names"]).itertuples(index=False):
            author_entries = getattr(row, "Author_full_names").split(";")
            for entry in author_entries:
                match = re.match(r"(.*) \((\d+)\)", entry.strip())
                if match:
                    name, author_id = match.groups()
                    author_id = str(author_id)  # Convertir a string
                    author_id_map.setdefault(author_id, []).append(name)

        # Asignar el nombre más frecuente a cada ID
        author_name_map = {id_: max(set(names), key=names.count) for id_, names in author_id_map.items()}

        # Expandir filas con múltiples IDs
        df = df.assign(**{"Author(s)_ID": df["Author(s)_ID"].str.split(";")}).explode("Author(s)_ID")
        df["Author(s)_ID"] = df["Author(s)_ID"].str.strip()

        # Mapear nombres a los IDs de autores
        df["Authors"] = df["Author(s)_ID"].map(author_name_map)
        return df

    def build_author_collaboration_matrix(df, selected_author_id):
        if "Author(s)_ID" not in df.columns:
            st.error("No se encontró la columna 'Author(s)_ID' en el archivo.")
            return None

        df_filtered = df[df["Author(s)_ID"] == selected_author_id]

        collaboration_counts = {}
        for _, row in df_filtered.iterrows():
            coauthors = df[df["Title"] == row["Title"]]["Author(s)_ID"].unique()
            for coauthor in coauthors:
                if coauthor != selected_author_id:
                    collaboration_counts[coauthor] = collaboration_counts.get(coauthor, 0) + 1

        return collaboration_counts

    def build_author_citation_matrix(df, selected_author_id):
        if "Author(s)_ID" not in df.columns or "Cited_by" not in df.columns:
            st.error("No se encontraron las columnas necesarias en el archivo.")
            return None

        df_filtered = df[df["Author(s)_ID"] == selected_author_id]

        citation_counts = {}
        for _, row in df_filtered.iterrows():
            coauthors = df[df["Title"] == row["Title"]]["Author(s)_ID"].unique()
            citations = row["Cited_by"] if not pd.isna(row["Cited_by"]) else 0
            for coauthor in coauthors:
                if coauthor != selected_author_id:
                    citation_counts[coauthor] = citation_counts.get(coauthor, 0) + citations

        return citation_counts

    def plot_heatmap(data_dict, title, ylabel, cmap="Blues"):
        if not data_dict:
            st.warning(f"No hay suficientes datos para generar {title}.")
            return

        df_heatmap = pd.DataFrame(list(data_dict.items()), columns=["Coautor_ID", ylabel])
        df_heatmap = df_heatmap.sort_values(by=ylabel, ascending=False).head(20)

        fig, ax = plt.subplots(figsize=(14, 6))
        sns.heatmap(df_heatmap.set_index("Coautor_ID").T, annot=True, fmt=".0f", cmap=cmap, cbar=True, linewidths=0.5, ax=ax)
        ax.set_title(title)
        ax.set_xlabel("Coautores")
        ax.set_ylabel("")

        st.pyplot(fig)

    # **Interfaz en Streamlit**
    st.title("Análisis de Redes de Colaboración y Citas Académicas")

    #uploaded_file = st.file_uploader("Cargue el archivo CSV con los datos de autores", type=["csv"])

    if uploaded_file:
        #df=load_data(uploaded_file)
        df = process_author_data(uploaded_file)
    
        if df is not None:
            st.success("Datos cargados exitosamente.")

            # Selección de autor
            unique_authors = df["Author(s)_ID"].dropna().unique().tolist()
            selected_author_id = st.selectbox("Seleccione un ID de autor:", unique_authors)
            st.session_state["selected_author_id"] = selected_author_id

            
            if selected_author_id:
                st.subheader(f"Mapas de Calor para el ID: {selected_author_id}")

                # **Mapa de colaboraciones (Publicaciones compartidas)**
                collaboration_counts = build_author_collaboration_matrix(df, selected_author_id)
                plot_heatmap(collaboration_counts, f"Colaboraciones más frecuentes con {selected_author_id}", "Publicaciones Conjuntas", cmap="Blues")

                # **Mapa de citas (Citas compartidas entre coautores)**
                citation_counts = build_author_citation_matrix(df, selected_author_id)
                plot_heatmap(citation_counts, f"Citas recibidas por colaboraciones con {selected_author_id}", "Total Citas", cmap="Reds")
################################################################################################################



##############################################################

    import streamlit as st
    import pandas as pd
    import re
    import matplotlib.pyplot as plt
    import numpy as np
    from wordcloud import WordCloud, STOPWORDS
    from sklearn.feature_extraction.text import TfidfVectorizer
    from scipy.spatial.distance import cosine

    # --- PROCESAR ARCHIVO ---
    def process_author_data(df):
        """ Procesa el DataFrame cargado y estructura los datos de autores. """
        if df is None or df.empty:
            st.error("❌ No se pudo procesar el archivo. Verifica su contenido.")
            return None

        df.columns = df.columns.str.strip().str.replace(" ", "_")

        required_columns = ["Author_full_names", "Author(s)_ID", "Title"]
        if not all(col in df.columns for col in required_columns):
            st.error(f"❌ Faltan columnas necesarias en el archivo: {', '.join(required_columns)}")
            return None

        author_id_map = {}
        for row in df.dropna(subset=["Author_full_names"]).itertuples(index=False):
            author_entries = getattr(row, "Author_full_names").split(";")
            for entry in author_entries:
                match = re.match(r"(.*) \((\d+)\)", entry.strip())
                if match:
                    name, author_id = match.groups()
                    author_id = str(author_id)
                    author_id_map.setdefault(author_id, []).append(name)
    
        author_name_map = {id_: max(set(names), key=names.count) for id_, names in author_id_map.items()}

        df["Author(s)_ID"] = df["Author(s)_ID"].str.split(";")
        df = df.explode("Author(s)_ID")
        df["Author(s)_ID"] = df["Author(s)_ID"].str.strip()
        df["Authors"] = df["Author(s)_ID"].map(author_name_map)

        return df

    # --- EXTRAER TITULOS POR AUTOR ---
    def extract_author_titles(df, selected_author_id):
        return df[df["Author(s)_ID"] == selected_author_id]["Title"].dropna().tolist()

    # --- GENERAR NUBE DE PALABRAS ---
    def generate_wordcloud(text, selected_author_id):
        if not text:
            st.warning("⚠️ No hay títulos de publicaciones disponibles para generar la nube de palabras.")
            return

        stopwords = set(STOPWORDS)
        stopwords.update([
        "study", "analysis", "using", "approach", "model", "method", "based", "review", "system",
        "estudio", "análisis", "uso", "enfoque", "modelo", "método", "basado", "revisión", "sistema",
        "effect", "impact", "influence", "role", "characteristics", "performance",
        "efecto", "impacto", "influencia", "rol", "características", "desempeño",
        "case", "cases", "example", "examples", "context",
        "caso", "casos", "ejemplo", "ejemplos", "contexto",
        "comparison", "relation", "relationship", "association", "between",
        "comparación", "relación", "asociación", "entre", "de", "en", "y", "con"
        ])

        wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='coolwarm', stopwords=stopwords).generate(" ".join(text))

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        ax.set_title(f"Temas centrales en las publicaciones de {selected_author_id}", fontsize=14)
        st.pyplot(fig)

    # --- CALCULAR DIVERSIDAD LÉXICA ---
    def compute_lexical_diversity(titles):
        words = " ".join(titles).split()
        if not words:
            st.warning("⚠️ No hay palabras suficientes para calcular la diversidad léxica.")
            return None, None

        unique_words = set(words)

        shannon_entropy = -sum((words.count(word) / len(words)) * np.log2(words.count(word) / len(words)) for word in unique_words)
        simpson_index = sum((words.count(word) / len(words)) ** 2 for word in unique_words)

        return shannon_entropy, simpson_index

    # --- SIMILITUD TEMÁTICA ---
    def topic_clustering(titles):
        if not titles:
            st.warning("⚠️ No hay títulos suficientes para calcular similitud temática.")
            return None

        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(titles)

        if tfidf_matrix.shape[0] < 2:
            st.warning("⚠️ Se necesita más de un título para calcular similitud temática.")
            return None

        similarity_matrix = cosine(tfidf_matrix.toarray().mean(axis=0), tfidf_matrix.toarray().mean(axis=0))
        return 1 - similarity_matrix

    # --- INTERFAZ EN STREAMLIT ---
    st.title("📊 Análisis de Multidisciplinariedad en Publicaciones")
    import streamlit as st
    import pandas as pd

    @st.cache_data
    def load_data(file):
        df = pd.read_csv(file, encoding='utf-8')
        return df

    #uploaded_file = st.file_uploader("📂 Carga un archivo CSV con los datos de autores", type=["csv"])

    if uploaded_file:
        df = load_data(uploaded_file)
        #df = pd.read_csv(uploaded_file, encoding='utf-8')  # Cargar archivo CSV
        df = process_author_data(df)  # Procesar datos

        if df is not None and not df.empty:
            st.success("✅ Datos cargados y procesados correctamente.")

            # Selección de autor
            unique_authors = df["Author(s)_ID"].dropna().unique().tolist()
            #selected_author_id = st.selectbox("🔍 Selecciona un ID de autor:", unique_authors)

            if selected_author_id:
                st.subheader(f"📖 Análisis de publicaciones del autor: {selected_author_id}")

                # Obtener títulos del autor
                author_titles = extract_author_titles(df, selected_author_id)

                # **Generar nube de palabras**
                st.subheader("☁️ Nube de palabras de títulos de publicaciones")
                generate_wordcloud(author_titles, selected_author_id)

                # **Calcular diversidad léxica**
                st.subheader("📊 Diversidad Léxica")
                shannon_entropy, simpson_index = compute_lexical_diversity(author_titles)
                if shannon_entropy and simpson_index:
                    st.write(f"**🔹 Índice de Shannon:** {shannon_entropy:.4f}")
                    st.write(f"**🔹 Índice de Simpson:** {simpson_index:.4f}")

                # **Calcular similitud temática**
                st.subheader("📈 Similitud Temática entre Títulos")
                similarity_score = topic_clustering(author_titles)
                if similarity_score:
                    st.write(f"**🔹 Similitud Temática Promedio:** {similarity_score:.4f}")
        else:
            st.error("❌ No se pudieron procesar los datos. Verifica el contenido del archivo.")


    
#########################################################3333


    import streamlit as st
    import pandas as pd
    import numpy as np
    import re
    import matplotlib.pyplot as plt
    import plotly.express as px
    from wordcloud import WordCloud
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.decomposition import PCA
    from sklearn.cluster import KMeans

    # Procesamiento de datos de autores
    def process_author_data(df):
        df.columns = df.columns.str.strip().str.replace(" ", "_")
        if "Author_full_names" not in df.columns or "Author(s)_ID" not in df.columns or "Title" not in df.columns:
            st.error("No se encontraron las columnas necesarias en el archivo.")
            return None
        df["Author(s)_ID"] = df["Author(s)_ID"].str.split(";")
        df = df.explode("Author(s)_ID")
        df["Author(s)_ID"] = df["Author(s)_ID"].str.strip()
        return df

    # Extracción de títulos por autor
    def extract_author_titles(df, selected_author_id):
        return df[df["Author(s)_ID"] == selected_author_id][["Title"]].dropna()

    # Clustering de temas utilizando K-Means
    def topic_clustering_kmeans(titles_df):
        titles = titles_df["Title"].tolist()
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(titles)
        num_clusters = min(5, len(titles))  # Máximo 5 clusters o el número de títulos disponibles
        kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(tfidf_matrix)
        titles_df["Cluster"] = labels
        return titles_df, vectorizer, tfidf_matrix, labels, num_clusters

    # Visualización de distribución de temas con PCA
    def plot_topic_distribution(titles_df, labels, num_clusters):
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(titles_df["Title"])
        pca = PCA(n_components=2)
        reduced_data = pca.fit_transform(tfidf_matrix.toarray())
        titles_df["Componente 1"] = reduced_data[:, 0]
        titles_df["Componente 2"] = reduced_data[:, 1]
        titles_df["Cluster"] = labels
        fig = px.scatter(
            titles_df, x="Componente 1", y="Componente 2", color=titles_df["Cluster"].astype(str),
            title="Mapa de Similitud Temática (PCA)",
            hover_data={"Title": True, "Componente 1": False, "Componente 2": False, "Cluster": True},
            color_discrete_sequence=px.colors.qualitative.Dark24[:num_clusters]
        )
        st.plotly_chart(fig)

    # Generación de nubes de palabras por cluster
    def plot_wordclouds_by_cluster(titles_df, num_clusters):
        for cluster in range(num_clusters):
            titles_in_cluster = titles_df[titles_df["Cluster"] == cluster]["Title"].tolist()
            text = " ".join(titles_in_cluster)
            wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="Dark2").generate(text)
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            ax.set_title(f"Nube de Palabras - Cluster {cluster}")
            st.pyplot(fig)

    # Distribución de clusters (histograma)
    def plot_cluster_distribution(titles_df, num_clusters):
        df_clusters = pd.DataFrame({"Cluster": titles_df["Cluster"]})
        fig = px.histogram(df_clusters, x="Cluster", nbins=num_clusters, color="Cluster",
                       color_discrete_sequence=px.colors.qualitative.Dark24[:num_clusters])
        fig.update_layout(title="Distribución de Temas (Clusters K-Means)",
                      xaxis_title="Cluster",
                      yaxis_title="Número de Artículos",
                      bargap=0.2)
        st.plotly_chart(fig)

    # Cálculo de diversidad léxica
    def compute_lexical_diversity(titles_df):
        words = " ".join(titles_df["Title"]).split()
        unique_words = set(words)
        shannon_entropy = -sum((words.count(word) / len(words)) * np.log2(words.count(word) / len(words)) for word in unique_words)
        simpson_index = sum((words.count(word) / len(words)) ** 2 for word in unique_words)
        return shannon_entropy, simpson_index

    # Gráfico de diversidad léxica
    def plot_diversity_metrics(shannon_entropy, simpson_index):
        df_diversity = pd.DataFrame({"Índice": ["Shannon", "Simpson"], "Valor": [shannon_entropy, simpson_index]})
        fig = px.bar(df_diversity, x="Índice", y="Valor", color="Índice",
                 title="Índices de Diversidad Léxica",
                 color_discrete_sequence=px.colors.qualitative.Dark24[:2])
        fig.update_layout(yaxis_title="Valor de Diversidad")
        st.plotly_chart(fig)

    # Aplicación principal de Streamlit
    st.title("Análisis de Multidisciplinariedad en Publicaciones")

    #uploaded_file = st.file_uploader("Archivo CSV con los datos de autores", type=["csv"])

    if uploaded_file:
        df=load_data(uploaded_file)
        #df = pd.read_csv(uploaded_file, encoding='utf-8')
        df = process_author_data(df)

        if df is not None:
            st.success("Datos cargados exitosamente.")

            unique_authors = df["Author(s)_ID"].dropna().unique().tolist()
            #selected_author_id = st.selectbox("Selecciona un ID:", unique_authors)

            if selected_author_id:
                st.subheader(f"Análisis de publicaciones del autor: {selected_author_id}")

                author_titles_df = extract_author_titles(df, selected_author_id)

                if not author_titles_df.empty:
                    clustered_df, vectorizer, tfidf_matrix, labels, num_clusters = topic_clustering_kmeans(author_titles_df)

                    st.subheader("Mapa de Similitud Temática (PCA)")
                    plot_topic_distribution(clustered_df, labels, num_clusters)

                    st.subheader("Distribución de Temas (Clusters K-Means)")
                    plot_cluster_distribution(clustered_df, num_clusters)

                    st.subheader("Nubes de Palabras por Cluster")
                    plot_wordclouds_by_cluster(clustered_df, num_clusters)

                    st.subheader("Índices de Diversidad Léxica")
                    shannon_entropy, simpson_index = compute_lexical_diversity(clustered_df)
                    plot_diversity_metrics(shannon_entropy, simpson_index)
                else:
                    st.warning(f"No se encontraron títulos para el autor ID: {selected_author_id}")


    import streamlit as st
    import pandas as pd
    import numpy as np
    import re
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.express as px
    from wordcloud import WordCloud
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    from sklearn.tree import DecisionTreeClassifier
    from sklearn import tree
    from sklearn.model_selection import GridSearchCV, cross_val_score
    from sklearn.feature_selection import SelectFromModel
    from sklearn.ensemble import BaggingClassifier
    from xgboost import XGBClassifier

    # Función para procesar los datos de autores
    def process_author_data(df):
        df.columns = df.columns.str.strip().str.replace(" ", "_")
        if "Author_full_names" not in df.columns or "Author(s)_ID" not in df.columns or "Title" not in df.columns:
            st.error("No se encontraron las columnas necesarias en el archivo.")
            return None
        df["Author(s)_ID"] = df["Author(s)_ID"].str.split(";")
        df = df.explode("Author(s)_ID")
        df["Author(s)_ID"] = df["Author(s)_ID"].str.strip()
        return df

    # Extraer títulos de un autor específico
    def extract_author_titles(df, selected_author_id):
        return df[df["Author(s)_ID"] == selected_author_id][["Title", "Cited_by"]].dropna()

    # Clustering de artículos mediante K-Means
    def topic_clustering_kmeans(df, titles):
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(titles)
        num_clusters = min(5, len(titles))  # Máximo 5 clusters
        kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(tfidf_matrix)

        df_clustered = df.copy()
        df_clustered["Cluster"] = labels

        # Asignar nombres a los clusters
        terms = np.array(vectorizer.get_feature_names_out())
        cluster_names = {}
        for i in range(num_clusters):
            cluster_center = kmeans.cluster_centers_[i]
            top_terms = terms[np.argsort(cluster_center)[-3:]]  # Top 3 palabras clave
            cluster_names[i] = " - ".join(top_terms)

        df_clustered["Cluster Name"] = df_clustered["Cluster"].map(cluster_names)
        df_clustered["Cited_by"] = pd.to_numeric(df_clustered["Cited_by"], errors='coerce').fillna(0)

        return tfidf_matrix, labels, vectorizer, cluster_names, df_clustered

    # Ajuste de hiperparámetros y entrenamiento del árbol de decisión
    def train_decision_tree(tfidf_matrix, labels):
        param_grid = {
            'max_depth': [3, 5, 10, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'ccp_alpha': [0.0, 0.01, 0.1]
        }

        clf = DecisionTreeClassifier(random_state=42)
        grid_search = GridSearchCV(clf, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(tfidf_matrix.toarray(), labels)

        best_clf = grid_search.best_estimator_
        best_params = grid_search.best_params_
        return best_clf, best_params

    # Visualización del árbol de decisión
    def plot_decision_tree(clf, vectorizer, cluster_names):
        fig, ax = plt.subplots(figsize=(12, 6))
        tree.plot_tree(clf, feature_names=vectorizer.get_feature_names_out(),
                   class_names=[cluster_names[i] for i in set(clf.classes_)],
                   filled=True, rounded=True, ax=ax)
        plt.title("Árbol de Decisión para Clasificación de Artículos")
        st.pyplot(fig)

    # Ensamblado con Bagging
    def train_bagging_classifier(tfidf_matrix, labels):
        base_clf = DecisionTreeClassifier(random_state=42)
        bagging_clf = BaggingClassifier(estimator=base_clf, n_estimators=100, random_state=42)
        bagging_clf.fit(tfidf_matrix.toarray(), labels)
        return bagging_clf

    # Ensamblado con XGBoost
    def train_xgboost_classifier(tfidf_matrix, labels):
        xgb_clf = XGBClassifier(random_state=42, n_estimators=100, learning_rate=0.1, max_depth=5)
        xgb_clf.fit(tfidf_matrix.toarray(), labels)
        return xgb_clf

    # Selección de características
    def feature_selection(tfidf_matrix, labels):
        clf = DecisionTreeClassifier(random_state=42)
        clf.fit(tfidf_matrix.toarray(), labels)
        selector = SelectFromModel(clf, prefit=True)
        X_selected = selector.transform(tfidf_matrix.toarray())
        return X_selected

    # Streamlit Application
    st.title("Análisis de Clustering y Árboles de Decisión")

    #uploaded_file = st.file_uploader("Sube el archivo CSV de Scopus", type="csv")

    if uploaded_file is not None:
        df = load_data(uploaded_file)

        #df = pd.read_csv(uploaded_file, encoding='utf-8')
        df = process_author_data(df)

        if df is not None:
            st.success("Datos cargados exitosamente.")

            author_ids = df["Author(s)_ID"].unique().tolist()
            #selected_author_id = st.selectbox("Selecciona el ID del autor para analizar", author_ids)

            if selected_author_id:
                st.subheader(f"Análisis de publicaciones del autor: {selected_author_id}")

                author_data = extract_author_titles(df, selected_author_id)

                if not author_data.empty:
                    tfidf_matrix, labels, vectorizer, cluster_names, df_clustered = topic_clustering_kmeans(author_data, author_data["Title"].tolist())

                    st.subheader("Palabras clave por cluster:")
                    for cluster, keywords in cluster_names.items():
                        st.write(f"**Cluster {cluster}:** {keywords}")

                    st.subheader("Número de citas por cluster:")
                    citations_by_cluster = df_clustered.groupby("Cluster Name")["Cited_by"].sum()
                    st.bar_chart(citations_by_cluster)

                    # Entrenar árbol de decisión con hiperparámetros óptimos
                    best_clf, best_params = train_decision_tree(tfidf_matrix, labels)
                    st.subheader(f"Árbol de Decisión con hiperparámetros optimizados")
                    plot_decision_tree(best_clf, vectorizer, cluster_names)

                    # Evaluación con validación cruzada
                    scores = cross_val_score(best_clf, tfidf_matrix.toarray(), labels, cv=5, scoring='accuracy')
                    st.subheader(f"Precisión promedio con validación cruzada: {scores.mean():.4f}")

                    # Entrenar modelos de ensamblado
                    #st.subheader("Ensamblado con Bagging")
                    #bagging_clf = train_bagging_classifier(tfidf_matrix, labels)
                    #st.write("Modelo Bagging entrenado.")

                    #st.subheader("Ensamblado con XGBoost")
                    #xgb_clf = train_xgboost_classifier(tfidf_matrix, labels)
                    #st.write("Modelo XGBoost entrenado.")

                    # Selección de características
                    #st.subheader("Selección de Características")
                    #X_selected = feature_selection(tfidf_matrix, labels)
                    #st.write(f"Número de características seleccionadas: {X_selected.shape[1]}")

                else:
                    st.warning(f"No se encontraron títulos para el autor ID: {selected_author_id}")


#######################################################################################

    import streamlit as st
    import pandas as pd
    import itertools
    import networkx as nx
    import plotly.graph_objects as go
    from collections import Counter

    # --- FUNCIÓN PARA OBTENER AUTORES POR APELLIDO ---
    def get_author_options(df, author_last_name):
        """Devuelve un diccionario {ID: Nombre más común} para un apellido dado."""
        if "Authors" not in df.columns or "Author(s) ID" not in df.columns:
            return {}

        author_dict = {}
        for _, row in df.dropna(subset=["Authors", "Author(s) ID"]).iterrows():
            authors = row["Authors"].split(";")
            ids = str(row["Author(s) ID"]).split(";")
            for author, author_id in zip(authors, ids):
                author = author.strip()
                author_id = author_id.strip()
                if author_last_name.lower() in author.lower():
                    author_dict.setdefault(author_id, []).append(author)

        return {author_id: Counter(names).most_common(1)[0][0] for author_id, names in author_dict.items()}

    # --- FUNCIÓN PARA CREAR MAPEO ID -> NOMBRE ---
    def create_id_to_name_mapping(df):
        """Crea un diccionario {ID: Nombre más común del autor}."""
        if "Authors" not in df.columns or "Author(s) ID" not in df.columns:
            return {}

        id_to_name = {}
        for _, row in df.dropna(subset=["Authors", "Author(s) ID"]).iterrows():
            authors = row["Authors"].split(";")
            ids = str(row["Author(s) ID"]).split(";")
            for author, author_id in zip(authors, ids):
                author = author.strip()
                author_id = author_id.strip()
                id_to_name.setdefault(author_id, []).append(author)

        return {author_id: Counter(names).most_common(1)[0][0] for author_id, names in id_to_name.items()}

    # --- FUNCIÓN PARA GENERAR RED DE COLABORACIÓN ---
    def visualize_collaboration_network(df, selected_author_id, id_to_name, selected_year):
        """Genera una red de colaboración en Plotly con relación de aspecto equilibrada."""

        # Si se elige "Todos los años", generar redes para cada año individualmente
        if selected_year == "Todos los años":
            years = sorted(df["Year"].dropna().astype(int).unique())
            for year in years:
                st.subheader(f"🔗 Red de colaboración en {year}")
                visualize_collaboration_network(df[df["Year"] == year], selected_author_id, id_to_name, year)
            return

        # Filtrar el DataFrame por el año seleccionado
        df_filtered = df[df["Year"] == selected_year]

        if df_filtered.empty:
            st.warning(f"No se encontraron publicaciones para el autor con ID: {selected_author_id}")
            return

        # Crear la red de colaboración
        G = nx.Graph()
        for _, row in df_filtered.iterrows():
            coauthors = row["Author(s) ID"].split(";")
            coauthors = [author.strip() for author in coauthors if author]

            for i in range(len(coauthors)):
                for j in range(i + 1, len(coauthors)):
                    G.add_edge(coauthors[i], coauthors[j])

        if len(G.nodes) == 0:
            st.warning("⚠️ No hay colaboraciones registradas en este período.")
            return

        # Ajustar la distribución de nodos para evitar estiramiento
        pos = nx.spring_layout(G, seed=42, scale=1.5)

        # Crear trazas de bordes (edges)
        edge_trace = go.Scatter(
            x=[], y=[], line=dict(width=1.5, color="black"),  # Bordes negros
            hoverinfo="none", mode="lines"
        )

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace.x += (x0, x1, None)
            edge_trace.y += (y0, y1, None)
    
        # Crear trazas de nodos (nodes)
        node_x = []
        node_y = []
        node_color = []
        node_texts = []

        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_color.append("red" if node == selected_author_id else "blue")  # Autor principal en rojo
            most_common_name = id_to_name.get(node, "Nombre no disponible")
            node_texts.append(f"ID: {node}<br>Nombre: {most_common_name}")

        node_trace = go.Scatter(
            x=node_x, y=node_y, mode="markers",
            marker=dict(size=15, color=node_color, opacity=0.8),
            text=node_texts, hoverinfo="text"
        )

        # Crear figura en Plotly con relación de aspecto equilibrada
        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(
            title=f"Red de Colaboración en {selected_year}",
            showlegend=False, hovermode="closest",
            autosize=True,  # Ajuste automático del tamaño
            margin=dict(l=40, r=40, t=50, b=50),  # Márgenes más equilibrados
            xaxis=dict(showgrid=False, zeroline=False, scaleanchor='y', constrain="domain"),  
            yaxis=dict(showgrid=False, zeroline=False, constrain="domain")
        )

        # Mostrar la gráfica en Streamlit
        st.plotly_chart(fig)

    # --- INTERFAZ EN STREAMLIT ---
    st.title("📊 Análisis de Redes de Colaboración en Publicaciones")

    uploaded_file = st.file_uploader("📂 Cargue un archivo CSV con datos de autores", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file, encoding='utf-8')  # Cargar datos
        id_to_name = create_id_to_name_mapping(df)  # Crear mapeo ID -> Nombre

        # --- INPUT PARA FILTRAR POR APELLIDO ---
        author_last_name = st.text_input("🔎 Ingresar el apellido del autor:")

        if author_last_name:
            available_authors = get_author_options(df, author_last_name)

            if available_authors:
                # --- SELECCIÓN DEL AUTOR EN `st.selectbox` ---
                selected_id = st.selectbox(
                    "🎯 Seleccion del autor:",
                    options=list(available_authors.keys()),
                    format_func=lambda x: f"{available_authors[x]} (ID: {x})"  # Muestra nombre e ID en el menú
                )

                if selected_id:
                    df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
                    years = sorted(df_filtered["Year"].dropna().astype(int).unique())

                    # --- SELECCIÓN DEL AÑO ---
                    if years:
                        selected_year = st.selectbox("📅 Año de colaboración:", ["Todos los años"] + years)

                        # --- BOTÓN PARA GENERAR RED ---
                        if st.button("🔗 Red de Colaboración"):
                            visualize_collaboration_network(df_filtered, selected_id, id_to_name, selected_year)
                    else:
                        st.warning("⚠️ No se encontraron publicaciones con años registrados.")
            else:
                st.warning("⚠️ No se encontraron coincidencias para ese apellido.")


####################################################3

    import imageio
    import tempfile
    import os
    import io


    def generate_collaboration_gif(df, selected_id, id_to_name):
        """Genera un GIF mostrando la evolución de la red de colaboración año con año."""
        st.subheader("🎥 Evolución de la Red de Colaboración (GIF)")
        years = sorted(df["Year"].dropna().astype(int).unique())
        image_list = []  # Lista para almacenar imágenes en memoria

        # Crear una red global para fijar las posiciones de los nodos
        G_global = nx.Graph()
        for _, row in df.iterrows():
            coauthors = row["Author(s) ID"].split(";")
            for i in range(len(coauthors)):
                for j in range(i + 1, len(coauthors)):
                    G_global.add_edge(coauthors[i].strip(), coauthors[j].strip())
    
        fixed_pos = nx.spring_layout(G_global, seed=42)

        # Generar los grafos año por año y guardarlos como imágenes
        for year in years:
            #fig, _ = visualize_collaboration_network(df, selected_id, id_to_name, year, fixed_pos)
            fig, _ = visualize_collaboration_network(df_filtered, selected_id, id_to_name, selected_year)

            # Guardar la imagen en memoria
            temp_img_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
            fig.write_image(temp_img_path, format="png", width=800, height=600)
            image_list.append(imageio.imread(temp_img_path))
            os.remove(temp_img_path)

        # Crear un archivo temporal para guardar el GIF
        temp_gif_path = tempfile.NamedTemporaryFile(delete=False, suffix=".gif").name
        imageio.mimsave(temp_gif_path, image_list, format="GIF", duration=1.5, loop=0)  # FPS ajustado
    
        # Mostrar el GIF en Streamlit
        st.image(temp_gif_path, caption="Evolución de la Red de Colaboración", use_column_width=True)

        # Permitir la descarga del GIF
        with open(temp_gif_path, "rb") as file:
            gif_bytes = file.read()
        st.download_button(
            label="📥 Descargar GIF",
            data=gif_bytes,
            file_name="Evolucion_Red_Colaboracion.gif",
            mime="image/gif"
        )
    
        os.remove(temp_gif_path)  # Eliminar el archivo después de la descarga


    # 🔥 Integración con la interfaz de Streamlit
    if selected_id:
        if st.button("🎥 Generar GIF de Evolución"):
            generate_collaboration_gif(df_filtered, selected_id, id_to_name)




###################################################



elif pagina == "Equipo de trabajo":
    st.title("Configuración")
    st.write("Aquí puedes ajustar los parámetros de la aplicación.")


