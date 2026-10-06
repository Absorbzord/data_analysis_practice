import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast


# Ustawienia strony Streamlit
st.set_page_config(page_title="s34596_final", layout="wide")
st.title("Dashboard Steam")
st.write("Analiza 100 najbardziej grywalnych gier z ostatnich 2 tygodni na Steam")

# Funkcja ładująca dane (przy użyciu cache)
@st.cache_data
def load_data():
    df = pd.read_csv("top100.csv")
    # Konwersja release_date do datetime i wyodrębnienie release_year
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['release_year'] = df['release_date'].dt.year
    return df



#  Ładujemy dane
df_cleaned = load_data()

def extract_date(val):
    # jeżeli jest już słownikiem, wyciągnij po kluczu "date"
    if isinstance(val, dict):
        return val.get("date", np.nan)
    # Spróbuj przekonwertować do słownika
    if isinstance(val, str):
        try:
            parsed_val = ast.literal_eval(val)
            if isinstance(parsed_val, dict):
                return parsed_val.get("date", np.nan)
        except Exception as e:
            return np.nan
    return np.nan

if "release_date" in df_cleaned.columns:
    df_cleaned["release_date"] = df_cleaned["release_date"].apply(extract_date)
    df_cleaned["release_date"] = pd.to_datetime(df_cleaned["release_date"], format="%d %b, %Y", errors="coerce").dt.date
#  Wyświetlamy pełną listę gier
st.write("### Top 100 najchętniej granych gier z ostatnich 2 tygodni")
st.dataframe(df_cleaned.head(100))

#  Interaktywne wyświetlanie informacji o wybranej grze
if 'name' in df_cleaned.columns:
    selected_game = st.selectbox("Wybierz grę, aby zobaczyć więcej szczegółów:", df_cleaned["name"].unique())
    game_details = df_cleaned[df_cleaned["name"] == selected_game]
    st.write("### Szczegóły gry")
    st.dataframe(game_details)

#Wykres słupkowy dla średniego rozłożenia czasu gry (average_2weeks)
if 'average_2weeks' in df_cleaned.columns and 'name' in df_cleaned.columns:
    st.write("### Średnie rozłożenie czasu gry ostatnich 2 tygodni")
    chart_data = df_cleaned.set_index('name')['average_2weeks']
    st.bar_chart(chart_data)

# Sidebar filtr: Wydawca
st.sidebar.header("Filtry")
if 'publisher' in df_cleaned.columns:
    publishers = np.insert(df_cleaned['publisher'].dropna().unique(), 0, "All")
    selected_publisher = st.sidebar.selectbox("Select a Publisher", publishers)
    if selected_publisher != "All":
        df_filtered = df_cleaned[df_cleaned['publisher'] == selected_publisher]
    else:
        df_filtered = df_cleaned.copy()
else:
    df_filtered = df_cleaned.copy()

#  Wykres dla top 10 wydawców
if 'publisher' in df_cleaned.columns:
    st.subheader("Top 10 wydawców gier")
    top_publishers = df_cleaned['publisher'].value_counts().nlargest(10).index
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(data=df_cleaned[df_cleaned['publisher'].isin(top_publishers)], 
                  y='publisher', order=top_publishers, ax=ax)
    ax.set_title("Top 10 wydawców")
    ax.set_xlabel("Ilość gier")
    ax.set_ylabel("Wydawca")
    st.pyplot(fig)

#  Wykres liczby gier według roku (release_year)

if "release_date" in df_cleaned.columns:
    df_cleaned["release_year"] = df_cleaned["release_date"].dt.year

    # Tworzymy figurę i oś do wykresu
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Ustalamy kolejność lat na osi X
    order_years = sorted(df_cleaned["release_date"].dropna().unique())
    sns.countplot(data=df_cleaned, x="release_date", order=order_years, ax=ax)
    
    ax.set_title("Ilość gier wg roku wydania")
    ax.set_xlabel("Rok wydania")
    ax.set_ylabel("Ilość")
    plt.xticks(rotation=45)
    
    # Wyświetlamy wykres w Streamlit
    st.pyplot(fig)