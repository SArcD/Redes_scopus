import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt

# Función para cargar y almacenar el DataFrame en caché
@st.cache_data
def load_data(file):
    return pd.read_csv(file, encoding='utf-8')

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
st.title("Análisis de Autores en Scopus")

uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)

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
