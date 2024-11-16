import streamlit as st
import pandas as pd

@st.cache_data
def load_data(path: str):
    return pd.read_csv(path)

def inject_css():
    st.markdown('''
            <style>
            .card-container {
                width:100%;
                aspect-ratio: 367/512; 
                margin-bottom: 1em; 
                display: flex; 
                justify-content: center;
                align-items: center;
                padding: 0;
                box-shadow: 0 0 10px 4px #cccccc;
                border: none;
                border-radius: 5%/3.5%;
                color: #cccccc;
                font-size: 2em;
                background: transparent;
            }
            </style>
            ''', unsafe_allow_html=True)
    return

def display_all_cards(series_url: str, card_count: int, column_count: int, owned, view: str):
    i = 0

    while i < card_count:
        columns = st.columns(column_count)
        j = 0

        while j < column_count and i < card_count:
            with columns[j]:
                i += 1

                image = f"background: url('https://www.serebii.net/tcgpocket/{series_url}/{i}.jpg') round;"
                grayscale = ""
                content = ""

                if not owned[i]:
                    if view == "Show Art":
                        grayscale = "filter: grayscale(100%);"
                    else:
                        image = ""
                        content = f"{i:03}"

                card_container = f'''<button class="card-container" style="{image} {grayscale}">{content}</button>'''
                
                if owned[i] or not view == "Hide":
                    st.markdown(card_container, unsafe_allow_html=True)
                    j += 1
    return i


def main():
    # st.sidebar.file_uploader("Import Data", type="tcgp", accept_multiple_files=False, label_visibility="collapsed")
    df_series = load_data("data/series.csv")


    columns = st.columns(2)

    with columns[0]:
        series_row = df_series.iloc[
            st.selectbox(
                "Series",
                range(0, len(df_series["Name"])), 
                format_func=lambda i: df_series["Name"][i]
            )
        ]

        series_data = [True] * (series_row["Count"] + 1)
        series_data[2] = False
        series_data[3] = False
        series_data[4] = False
        series_data[5] = False
        series_data[8] = False
    
    with columns[1]:
        selected_view = st.selectbox("Missing", ["Hide", "Show Entry #", "Show Art"], index = 1)


    inject_css()
    st.divider()
    display_all_cards(series_url=series_row["URL"], card_count=series_row["Count"], column_count=5, owned=series_data, view=selected_view)
    

if __name__ == "__main__":
    main()