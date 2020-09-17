from tqdm.auto import tqdm
import fire
import spacy
import pandas as pd


def filter_dataset(input_file, output):
    """
    Filtra el dataset de entrada usando las palabras filtro
    """


    if input_file.endswith("xlsx"):
        df = pd.read_excel(input_file, header=0, names=["medio", "fecha", "titulo"])
    else:
        df = pd.read_csv(input_file)

    df["medio"] = df["medio"].str.lower()
    print(f"Tenemos {df.shape[0]} noticias")
    print(df["medio"].value_counts())

    nlp = spacy.load('es_core_news_sm')
    palabras_clave = {
        "alberto", "macri", "mauricio", "cfk", "cristina", "caño", "espert",
        "centurion", "pichetto", "pla", "pj", "peronismo", "fit", "izquierda", "cambiemos",
        "cambio", "lavagna", "urtubey", "rosales", "hotton"
    }

    print(f"Usando palabras clave: {' - '.join(palabras_clave)}")

    current_titles = set()
    important_indices = []

    for i, row in tqdm(df.iterrows(), total=len(df)):
        #title = unidecode.unidecode(row["titulo"].lower())
        title = row["titulo"]
        if type(title) is not str:
            continue

        if title in current_titles:
            continue
        for tok in nlp(title):
            if tok.text.lower() in palabras_clave:
                #print(f"{i} -- {tok.text} ---> {title}")
                important_indices.append(i)
                current_titles.add(title)
                break


    df_politico = df.loc[important_indices]
    print(f"Noticias recuperadas: {df_politico.shape[0]}")

    pd.set_option("max_colwidth", 300)
    pd.set_option("max_rows", 300)

    df_politico.to_csv(output)
if __name__ == '__main__':
    fire.Fire(filter_dataset)
