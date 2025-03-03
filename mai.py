import streamlit as st
import pandas as pd
import re

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

# Interfaz en Streamlit
#st.title("Análisis de Autores en Scopus")

#uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])

#if uploaded_file:
#df = load_data(uploaded_file)

# Input para apellido del autor
author_last_name = st.text_input("Ingrese el apellido del autor")

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
                else:
                    st.warning("No se encontraron editoriales para este autor.")
        else:
            st.warning("No se encontraron autores con ese ID.")
    else:
        st.warning("No se encontraron coincidencias para ese apellido.")
