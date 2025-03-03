import streamlit as st
import pandas as pd
import re


import streamlit as st

st.set_page_config(page_title="App con Múltiples Páginas", layout="wide")

# Crear menú de navegación
pagina = st.selectbox("Selecciona una página", ["Inicio", "Análisis por base", "Análisis por autor", "Equipo de trabajo"])

# Mostrar contenido según la página seleccionada
if pagina == "Inicio":
    st.title("Inicio")
    st.write("Bienvenido a la aplicación de Streamlit.")
###############################################################################################################################
elif pagina == "Análisis por base":

    @st.cache_data
    def process_author_data(df):
        df.columns = df.columns.str.strip().str.replace(" ", "_")  # Reemplazar espacios en los nombres de columnas

        if "Author_full_names" not in df.columns or "Author(s)_ID" not in df.columns:
            st.error("Las columnas necesarias ('Author_full_names' y 'Author(s)_ID') no se encontraron en el archivo.")
            return None, None, None

        author_id_map = {}
        for row in df.dropna(subset=["Author_full_names"]).itertuples(index=False):
            author_entries = str(getattr(row, "Author_full_names")).split(";")
            for entry in author_entries:
                match = re.match(r"(.*) \((\d+)\)", entry.strip())
                if match:
                    name, author_id = match.groups()
                    author_id = str(author_id)  
                    if author_id in author_id_map:
                        author_id_map[author_id].append(name)
                    else:
                        author_id_map[author_id] = [name]

        author_name_map = {id_: max(set(names), key=names.count) for id_, names in author_id_map.items()}

        first_author_count = {}
        authors_per_article = {}

        for _, row in df.iterrows():
            author_list = str(row["Author(s)_ID"]).split(";")
            first_author_id = author_list[0].strip() if author_list else None
            if first_author_id:
                first_author_count[first_author_id] = first_author_count.get(first_author_id, 0) + 1
            for author_id in author_list:
                author_id = author_id.strip()
                if author_id:
                    if author_id not in authors_per_article:
                        authors_per_article[author_id] = []
                    authors_per_article[author_id].append(len(author_list))

        df = df.assign(**{"Author(s)_ID": df["Author(s)_ID"].astype(str).str.split(";")}).explode("Author(s)_ID")
        df["Author(s)_ID"] = df["Author(s)_ID"].str.strip()
        df["Authors"] = df["Author(s)_ID"].apply(lambda x: author_name_map.get(x, "Unknown Author"))

        return df, first_author_count, authors_per_article

    @st.cache_data
    def aggregate_author_data(df, first_author_count, authors_per_article):
        if "Author(s)_ID" not in df.columns or "Cited_by" not in df.columns:
            st.error("No se encontraron las columnas necesarias en el archivo.")
            return None

        df_filtered = df.dropna(subset=["Author(s)_ID", "Cited_by"])
        df_filtered["Cited_by"] = df_filtered["Cited_by"].astype(int)

        def most_cited_article(x):
            cited_subset = df_filtered.loc[x.index, ["Cited_by", "Title"]].dropna()
            cited_subset = cited_subset.drop_duplicates(subset=["Title"])
            if not cited_subset.empty and cited_subset["Cited_by"].max() > 0:
                return cited_subset.loc[cited_subset["Cited_by"].idxmax(), "Title"]
            return "No cited articles"

        aggregated_data = df_filtered.groupby("Author(s)_ID").agg(
            author_name=("Authors", lambda x: x.mode().iloc[0] if not x.mode().empty else "Unknown Author"),
            total_articles=("Title", "count"),
            total_citations=("Cited_by", "sum"),
            earliest_year=("Year", "min"),
            latest_year=("Year", "max"),
            avg_articles_per_year=("Year", lambda x: x.count() / (x.max() - x.min() + 1) if x.max() != x.min() else x.count()),
            most_cited_article=("Title", most_cited_article)
        ).reset_index()

        aggregated_data["total_first_author_articles"] = aggregated_data["Author(s)_ID"].map(first_author_count).fillna(0).astype(int)
        aggregated_data["avg_authors_per_article"] = aggregated_data["Author(s)_ID"].map(lambda x: sum(authors_per_article.get(x, [])) / len(authors_per_article.get(x, [])) if x in authors_per_article else 0)

        return aggregated_data

    st.title("Análisis de Autores en Scopus")

    uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
        df, first_author_count, authors_per_article = process_author_data(df)
    
        if df is not None:
            aggregated_data = aggregate_author_data(df, first_author_count, authors_per_article)
            if aggregated_data is not None:
                st.write("Datos agregados de autores:")
                st.dataframe(aggregated_data)

                csv = aggregated_data.to_csv(index=False).encode('utf-8')
                st.download_button("Descargar CSV", csv, "aggregated_author_data.csv", "text/csv")















    



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

# Función para cargar y almacenar el DataFrame en caché
#@st.cache_data
#def load_data(file):
#    return pd.read_csv(file, encoding='utf-8')

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
        ax.set_ylabel("Número de publicaciones")
        ax.set_title(f"Publicaciones por año - ID {selected_id}")
        ax.set_xticklabels(year_counts.index, rotation=45)
        st.pyplot(fig)


    uploaded_file = st.file_uploader("Suba un archivo CSV", type=["csv"])
    file_path = "scopusUdeC con financiamiento 17 feb-2.csv"
    # Función para cargar y almacenar el DataFrame en caché
    @st.cache_data
    def load_data(file):
        return pd.read_csv(file, encoding='utf-8')


    def get_total_citations(file_path, selected_id):
        df = pd.read_csv(file_path, encoding='utf-8')
        if "Author(s) ID" not in df.columns or "Cited by" not in df.columns:
            print("No se encontraron las columnas necesarias en el archivo.")
            return 0

        df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
        total_citations = df_filtered["Cited by"].fillna(0).astype(int).sum()

        return total_citations

    def get_total_articles(file_path, selected_id):
        df = pd.read_csv(file_path, encoding='utf-8')
        if "Author(s) ID" not in df.columns:
            print("No se encontraron las columnas necesarias en el archivo.")
            return 0

        df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
        total_articles = df_filtered.shape[0]

        return total_articles

    def get_publication_years(file_path, selected_id):
        df = pd.read_csv(file_path, encoding='utf-8')
        if "Author(s) ID" not in df.columns or "Year" not in df.columns:
            print("No se encontraron las columnas necesarias en el archivo.")
            return None, None, None, None

        df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
        years = df_filtered["Year"].dropna().astype(int)
        if years.empty:
            return None, None, None, None

        min_year = years.min()
        max_year = years.max()
        year_counts = years.value_counts().sort_index()

        # Total de citas por año
        citations_per_year = df_filtered.groupby("Year")["Cited by"].sum().fillna(0).astype(int)

        return min_year, max_year, year_counts, citations_per_year

    def get_publisher_info(file_path, selected_id):
        df = pd.read_csv(file_path, encoding='utf-8')
        if "Author(s) ID" not in df.columns or "Publisher" not in df.columns or "Cited by" not in df.columns:
            print("No se encontraron las columnas necesarias en el archivo.")
            return None

        df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
        publisher_stats = df_filtered.groupby("Publisher").agg(
            num_articles=("Title", "count"),
            total_citations=("Cited by", "sum")
        ).reset_index()

        return publisher_stats

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
                        plot_publications(author_stats['year_counts'], selected_id)

                    if not author_stats['publisher_info'].empty:
                        st.write("**Editoriales en las que ha publicado este ID:**")
                        st.dataframe(author_stats['publisher_info'])
                    
                    
                    print(f"Autores con ID {selected_id}: {', '.join(matching_authors)}")

                    total_citations = get_total_citations(file_path, selected_id)
                    print(f"Total de citas asociadas a ID {selected_id}: {total_citations}")

                    total_articles = get_total_articles(file_path, selected_id)
                    print(f"Total de artículos en los que participa ID {selected_id}: {total_articles}")

                    min_year, max_year, year_counts, citations_per_year = get_publication_years(file_path, selected_id)
                    if min_year and max_year:
                        print(f"Año más antiguo de publicación: {min_year}")
                        print(f"Año más reciente de publicación: {max_year}")
                        plot_publications(year_counts, selected_id)
                        plot_citations_per_year(citations_per_year, selected_id)
                    else:
                        print("No se encontraron años de publicación para este autor.")

                    publisher_info = get_publisher_info(file_path, selected_id)
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

    def get_author_options(file_path, author_last_name):
        df = pd.read_csv(file_path, encoding='utf-8')
        if "Authors" not in df.columns or "Author(s) ID" not in df.columns:
            print("No se encontraron las columnas necesarias en el archivo.")
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

    def get_authors_by_id(file_path, selected_id):
        df = pd.read_csv(file_path, encoding='utf-8')
        if "Authors" not in df.columns or "Author(s) ID" not in df.columns:
            print("No se encontraron las columnas necesarias en el archivo.")
            return []

        matching_authors = set()
        for _, row in df.dropna(subset=["Authors", "Author(s) ID"]).iterrows():
            authors = row["Authors"].split(";")
            ids = str(row["Author(s) ID"]).split(";")
            for author, author_id in zip(authors, ids):
                if author_id.strip() == selected_id:
                    matching_authors.add(author.strip())

        return list(matching_authors)

    def get_total_citations(file_path, selected_id):
        df = pd.read_csv(file_path, encoding='utf-8')
        if "Author(s) ID" not in df.columns or "Cited by" not in df.columns:
            print("No se encontraron las columnas necesarias en el archivo.")
            return 0

        df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
        total_citations = df_filtered["Cited by"].fillna(0).astype(int).sum()

        return total_citations

    def get_total_articles(file_path, selected_id):
        df = pd.read_csv(file_path, encoding='utf-8')
        if "Author(s) ID" not in df.columns:
            print("No se encontraron las columnas necesarias en el archivo.")
            return 0

        df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
        total_articles = df_filtered.shape[0]

        return total_articles

    def get_publication_years(file_path, selected_id):
        df = pd.read_csv(file_path, encoding='utf-8')
        if "Author(s) ID" not in df.columns or "Year" not in df.columns:
            print("No se encontraron las columnas necesarias en el archivo.")
            return None, None, None, None

        df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
        years = df_filtered["Year"].dropna().astype(int)
        if years.empty:
            return None, None, None, None

        min_year = years.min()
        max_year = years.max()
        year_counts = years.value_counts().sort_index()

        # Total de citas por año
        citations_per_year = df_filtered.groupby("Year")["Cited by"].sum().fillna(0).astype(int)

        return min_year, max_year, year_counts, citations_per_year

    def get_publisher_info(file_path, selected_id):
        df = pd.read_csv(file_path, encoding='utf-8')
        if "Author(s) ID" not in df.columns or "Publisher" not in df.columns or "Cited by" not in df.columns:
            print("No se encontraron las columnas necesarias en el archivo.")
            return None

        df_filtered = df[df["Author(s) ID"].str.contains(selected_id, na=False, case=False)]
        publisher_stats = df_filtered.groupby("Publisher").agg(
            num_articles=("Title", "count"),
            total_citations=("Cited by", "sum")
        ).reset_index()

        return publisher_stats

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
        df = pd.read_csv(file, encoding='utf-8')
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

    uploaded_file = st.file_uploader("Cargue el archivo CSV con los datos de autores", type=["csv"])

    if uploaded_file:
        df = process_author_data(uploaded_file)
    
        if df is not None:
            st.success("Datos cargados exitosamente.")

            # Selección de autor
            unique_authors = df["Author(s)_ID"].dropna().unique().tolist()
            selected_author_id = st.selectbox("Seleccione un ID de autor:", unique_authors)

            if selected_author_id:
                st.subheader(f"Mapas de Calor para el ID: {selected_author_id}")

                # **Mapa de colaboraciones (Publicaciones compartidas)**
                collaboration_counts = build_author_collaboration_matrix(df, selected_author_id)
                plot_heatmap(collaboration_counts, f"Colaboraciones más frecuentes con {selected_author_id}", "Publicaciones Conjuntas", cmap="Blues")

                # **Mapa de citas (Citas compartidas entre coautores)**
                citation_counts = build_author_citation_matrix(df, selected_author_id)
                plot_heatmap(citation_counts, f"Citas recibidas por colaboraciones con {selected_author_id}", "Total Citas", cmap="Reds")




    

elif pagina == "Equipo de trabajo":
    st.title("Configuración")
    st.write("Aquí puedes ajustar los parámetros de la aplicación.")


