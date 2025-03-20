import streamlit as st
import yfinance as yf
import pandas as pd
import json
import requests

# Chargement / Sauvegarde de la watchlist
def load_watchlist():
    try:
        with open("watchlist.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_watchlist(watchlist):
    with open("watchlist.json", "w") as f:
        json.dump(watchlist, f)

# Fonction pour récupérer les indicateurs macroéconomiques
def get_macro_data():
    url = "https://api.tradingeconomics.com/indicators"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

# Interface principale
st.set_page_config(page_title="Investment Helper", layout="wide")

# Chargement de la watchlist
watchlist = load_watchlist()

# Navigation avec onglets colorés
tabs = ["Infos Rapides", "Indicateurs Macro", "Recommandations", "Watchlist"]
selected_tab = st.selectbox("Navigation", tabs)

if selected_tab == "Infos Rapides":
    st.title("📈 Infos Rapides")
    
    search_query = st.text_input("Rechercher un placement")
    
    # Sélection du type de placement
    placement_type = st.selectbox("Sélectionnez le type de placement", ["Actions", "Obligations", "FNB"])
    
    # Liste déroulante des placements dynamiques
    if placement_type == "Actions":
        options = ["AAPL", "MSFT", "GOOGL", "TSLA"]
    elif placement_type == "Obligations":
        options = ["US 10Y Treasury", "EU 10Y Bond"]
    else:
        options = ["SPY", "VOO", "QQQ"]
    
    if search_query:
        options = [o for o in options if search_query.upper() in o]
    
    selected_placement = st.selectbox("Choisissez un placement", options)
    
    if st.button("Ajouter à la watchlist"):
        if selected_placement not in watchlist:
            watchlist.append(selected_placement)
            save_watchlist(watchlist)
            st.success(f"{selected_placement} ajouté à la watchlist")
    
    # Affichage des informations détaillées
    data = yf.Ticker(selected_placement).info
    st.write(f"**Nom**: {data.get('longName', 'N/A')}")
    st.write(f"**Prix actuel**: {data.get('currentPrice', 'N/A')}")
    st.write(f"**Variation**: {data.get('dayHigh', 'N/A')} - {data.get('dayLow', 'N/A')}")
    
    if placement_type == "Actions":
        st.write(f"**P/E Ratio**: {data.get('trailingPE', 'N/A')}")
        st.write(f"**Taux de dividende**: {data.get('dividendYield', 'N/A')}")
        st.write(f"**Description**: {data.get('longBusinessSummary', 'N/A')}")
    elif placement_type == "Obligations":
        st.write("Affichage de la courbe de rendement en cours de développement...")
    elif placement_type == "FNB":
        st.write(f"**Indice suivi**: {data.get('benchmark', 'N/A')}")
        st.write(f"**Performance**: {data.get('performanceOverview', 'N/A')}")
        st.write(f"**Description**: {data.get('fundFamily', 'N/A')}")
    
    # Graphique des prix historiques
    hist = yf.Ticker(selected_placement).history(period="6mo")
    st.line_chart(hist['Close'])

elif selected_tab == "Indicateurs Macro":
    st.title("🌍 Indicateurs Macroéconomiques")
    macro_data = get_macro_data()
    if macro_data:
        for item in macro_data[:5]:
            st.write(f"**{item['category']} ({item['country']})**: {item['value']} {item['unit']}")
    else:
        st.write("Données macroéconomiques indisponibles.")
    
elif selected_tab == "Recommandations":
    st.title("📊 Recommandations des experts")
    st.write(f"Analyse des recommandations pour {selected_placement}...")
    
elif selected_tab == "Watchlist":
    st.title("🔍 Watchlist")
    
    if not watchlist:
        st.write("Votre watchlist est vide.")
    else:
        for item in watchlist:
            col1, col2 = st.columns([4, 1])
            col1.write(item)
            if col2.button("❌", key=item):
                watchlist.remove(item)
                save_watchlist(watchlist)
                st.experimental_rerun()
