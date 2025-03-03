import streamlit as st
import pandas as pd
import re

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

