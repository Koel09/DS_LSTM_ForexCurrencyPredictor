import streamlit as st
import requests
import papermill as pm
import os

st.title("Forex Currency Predictor")

currency_options = ["Select Currency","AUSTRALIAN DOLLAR", "EURO", "NEW ZEALAND DOLLAR",
                    "GREAT BRITAIN POUNDS", "BRAZILIAN REAL", "CANADIAN DOLLAR",
                    "CHINESE YUAN$", "HONG KONG DOLLAR", "INDIAN RUPEE",
                    "KOREAN WON$", "MEXICAN PESO", "SOUTH AFRICAN RAND$",
                    "SINGAPORE DOLLAR", "DANISH KRONE", "JAPANESE YEN$",
                    "MALAYSIAN RINGGIT", "NORWEGIAN KRONE", "SWEDEN KRONA",
                    "SRILANKAN RUPEE", "SWISS FRANC", "NEW TAIWAN DOLLAR", "THAI BAHT"]

user_currency_choice = st.selectbox("Select currency", currency_options)
forecast_length = st.number_input("Enter number of days:", min_value=1, max_value=120)

st.write("You selected:", user_currency_choice)
st.write("Forecast duration:", forecast_length)

# RAW URLs
NOTEBOOK_URL = "https://raw.githubusercontent.com/Koel09/DS_LSTM_ForexCurrencyPredictor/main/ForexCurrencyPredictor_LSTM_using_saved_model.ipynb"
MODEL_URL = f"https://raw.githubusercontent.com/Koel09/DS_LSTM_ForexCurrencyPredictor/main/models/{user_currency_choice}_lstm_model.keras"
DATASET_URL = "https://raw.githubusercontent.com/Koel09/DS_LSTM_ForexCurrencyPredictor/main/data/Foreign_Exchange_Rates.xls"




# Temporary paths
input_nb  = "ForexCurrencyPredictor_LSTM_using_saved_model.ipynb"
output_nb = "ForexCurrencyPredictor_LSTM_using_saved_model_output.ipynb"
model_file = f"models/{user_currency_choice}_lstm_model.keras"
dataset_file = "data/Foreign_Exchange_Rates.xls"

def extract_plots(nb_path):
    import base64
    import nbformat

    nb = nbformat.read(nb_path, as_version=4)
    images = []

    for cell in nb.cells:
        if "outputs" in cell:
            for output in cell.outputs:
                if output.output_type == "display_data" and "image/png" in output.data:
                    img = base64.b64decode(output.data["image/png"])
                    images.append(img)
    return images

if st.button("Run Notebook"):
    # st.info("Downloading files...")

    open(input_nb, "wb").write(requests.get(NOTEBOOK_URL).content)
    open(model_file, "wb").write(requests.get(MODEL_URL).content)
    open(dataset_file, "wb").write(requests.get(DATASET_URL).content)

    # st.success("Downloaded! Running notebook...")

    pm.execute_notebook(
        input_nb,
        output_nb,
        parameters=dict(
            Currency=user_currency_choice,
            Forecast_len=forecast_length,
            Data_path=dataset_file,
            Model_path=model_file
        ),
        # kernel_name="tf310"
        kernel_name="python3"
    )

    st.success("Notebook executed!")

    # st.info("Extracting charts...")
    charts = extract_plots(output_nb)

    st.write("### Generated Charts")

    for i, chart in enumerate(charts):
        st.image(chart, caption=f"Chart {i+1}")



