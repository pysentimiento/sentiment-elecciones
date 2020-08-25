import fire
import pandas as pd
import unidecode


def filter_dataset(input_file, output, filters=None):
    """
    Filtra el dataset de entrada usando las palabras filtro
    """


    df = pd.read_excel(input_file, header=0, names=["medio", "fecha", "titulo"])
    df["medio"] = df["medio"].str.lower()
    print(f"Tenemos {df.shape[0]} noticias")
    print(df["medio"].value_counts())

    palabras_clave = [
        "Alberto", "Macri", "Mauricio", "CFK", "Cristina", "Del Caño", "Espert",
        "Centurion", "Pichetto", "Del Pla", "PJ", "peronismo", "FIT", "Cambiemos",
        "Juntos por el Cambio", "Lavagna", "Urtubey", "Rosales", "Hotton"
    ]

    print(f"Usando palabras clave: {' - '.join(palabras_clave)}")
    important_indices = []
    current_titles = set()

    for i, row in df.iterrows():
        try:
            title = unidecode.unidecode(row["titulo"].lower())
            for clave in palabras_clave:
                if clave.lower() in title and title not in current_titles:
                    current_titles.add(title)
                    important_indices.append(i)
        except AttributeError as e:
            print(f"Posición {i+1}")
            print(e)

    df_politico = df.loc[important_indices]
    print(f"Noticias recuperadas: {df_politico.shape[0]}")

    pd.set_option("max_colwidth", 300)
    pd.set_option("max_rows", 300)

    df_politico.to_csv(output)
if __name__ == '__main__':
    fire.Fire(filter_dataset)
