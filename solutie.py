import csv
import os
import json
import streamlit as st
from datetime import date

TMP = "demo_data"
os.makedirs(TMP, exist_ok=True)

calea_db = os.path.join(TMP, "biblioteca.json")

STARI = ["de citit", "in curs", "terminat"]
TIPURI = ['carte', "film"]
def incarca_titluri():
    if os.path.exists(calea_db):
        with open(calea_db, encoding='utf-8') as f:
            return json.load(f)
    else:
        return []
def salveaza_titluri(titluri):
    with open(calea_db, mode='w', encoding="utf-8") as f:
        json.dump(titluri,f, indent=2)
def normalizeaza_rand(rand_brut):
    return {
        'titlu': str(rand_brut['titlu'].strip()),
        'tip': str(rand_brut['tip']).strip(),
        'autor': str(rand_brut['autor']).strip(),
        'an': int(rand_brut['an']),
        'stare': "de citit",
        'rating': None,
        'data_terminarii': None,
        'notite': ""
    }
def citeste_csv_incarcat(fisier):
    linii_text = fisier.read().decode("utf-8").splitlines()
    return [normalizeaza_rand(r) for r in csv.DictReader(linii_text)]

def adauga_titluri_noi(existente, importate):
    """ Adaugam DOAR titlurile noi care nu exista deja"""
    titluri_existente = {rand['titlu'].lower() for rand in existente}
    de_adaugat = [rand for rand in importate if rand['titlu'].lower() not in titluri_existente]
    return existente+de_adaugat, len(de_adaugat)

st.set_page_config(page_title="Jurnal carti/filme")
st.title("Jurnalul meu cu carti/filme")

titluri = incarca_titluri()
st.header("1. Import date CSV")
fisier_incarcat = st.file_uploader("Lista de titluri de adaugat", type="csv")

if fisier_incarcat is not None:
    importate = citeste_csv_incarcat(fisier_incarcat)
    titluri_previzualitate, cate_noi = adauga_titluri_noi(titluri, importate)
    st.caption(f"{cate_noi} titluri noi gasite")
    if cate_noi > 0 and st.button(f"Adauga cele {cate_noi} titluri noi"):
        salveaza_titluri(titluri_previzualitate)
        st.success(f"{cate_noi} titluri noi au fost adaugate!")
        st.rerun()
st.header("2. Biblioteca mea")
if not titluri:
    st.info("Nu exista niciun titlu adaugat.")
else:
    col_tip, col_stare = st.columns(2)

    with col_tip:
        tip_ales = st.selectbox("Filtreaza dupa tip", TIPURI )
    with col_stare:
        stare_aleasa = st.selectbox("Filtreaza dupa stare", STARI)
    titluri_filtrare = [t for t in titluri if t['tip'] == tip_ales and t['stare'] == stare_aleasa]

    st.dataframe(titluri_filtrare)
with st.form("form_adaugare"):
    titlu_nou = st.text_input("Introduceti un titlu")
    tip_nou = st.selectbox("Tip", TIPURI)
    autor_nou = st.text_input("Introduceti un autor")
    an_adaugat = st.number_input("Introduceti anul cartii", min_value=2000, step=1, value=2026)
    adauga = st.form_submit_button("Adauga in biblioteca")

    if adauga and titlu_nou:
        titluri.append({
            "titlu": titlu_nou,
            "tip": tip_nou,
            "autor": autor_nou,
            "an": an_adaugat,
            "stare": "de citit",
            "rating": None,
            "data_terminarii": None,
            "notite": ""
        })

        salveaza_titluri(titluri)
        st.toast("Felicitari ai adaugat o carte noua!")
