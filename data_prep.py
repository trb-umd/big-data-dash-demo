import os
import pandas as pd
import requests
from tqdm import tqdm
import zipfile


def prep_data():
    # dataset from https://www.kaggle.com/simonlozada/coronavirus-in-argentina, 16,339,230 rows, 25 columns
    # if not present, will download from https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.zip

    if not os.path.isdir("./csv"):
        os.mkdir("./csv")

    # check for original CSV file, if not present, download and unzip

    if not os.path.isfile("Covid19Casos.csv"):

        if os.path.isfile("Covid19Casos.zip"):
            with zipfile.ZipFile("Covid19Casos.zip", "r") as zip_ref:
                zip_ref.extractall()

        print("Downloading data file...")
        url = "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.zip"
        data_zip = requests.get(url, stream=True, allow_redirects=True)
        total_size = int(data_zip.headers.get("content-length"))
        initial_position = 0

        with open("Covid19Casos.zip", "wb") as f:

            with tqdm(total=total_size, unit="B", unit_scale=True, desc="Covid19Casos.zip", initial=initial_position,
                      ascii=True) as pbar:

                for ch in data_zip.iter_content(chunk_size=1024):

                    if ch:
                        f.write(ch)
                        pbar.update(len(ch))

        print("Unzipping file...\n")

        with zipfile.ZipFile("Covid19Casos.zip", "r") as zip_ref:
            zip_ref.extractall()

    print("Loading original CSV file...\n")

    # Only load used columns for memory/speed considarations, pandas used due to reduced size and greater operational
    # speed over dask for present purposes

    used_cols = ["sexo", "edad", "residencia_provincia_nombre", "sepi_apertura", "fallecido", "origen_financiamiento"]

    data = pd.read_csv("Covid19Casos.csv", usecols=used_cols)

    # manually translate column names for naming/usage consistency
    translated_names = [
        "patient_gender", "patient_age", "residence_province", "pandemic_week", "patient_death", "financing_source"]

    data = data.rename(columns=dict(zip(used_cols, translated_names)))

    # apply translations, create csv files for rapid loading of utilized data

    patient_death = pd.DataFrame(data.query('patient_death == "SI"'))

    gender_death = patient_death.filter(["patient_gender", "patient_death"])
    gender_death = pd.DataFrame(gender_death.groupby("patient_gender").count()).reset_index()
    gender_death.to_csv("./csv/gender_death.csv", index=True)

    age_death = patient_death.filter(["patient_age", "patient_death"])
    age_death = pd.DataFrame(age_death.groupby("patient_age").count()).reset_index()
    age_death.to_csv("./csv/age_death.csv", index=True)

    financing_source = patient_death.filter(["financing_source", "patient_death"])
    financing_source = pd.DataFrame(financing_source.groupby("financing_source").count()).reset_index()
    financing_source["financing_source"] = \
        financing_source["financing_source"].replace({"Privado": "Private", "Público": "Public"})
    financing_source.to_csv("./csv/financing_source.csv", index=True)

    province_deaths = patient_death.filter(["residence_province", "patient_death"])
    province_deaths = pd.DataFrame(province_deaths.groupby(["residence_province"]).count()).reset_index()
    province_deaths["residence_province"] = \
        province_deaths["residence_province"].replace({"SIN ESPECIFICAR": "Unspecified"})
    province_deaths.to_csv("./csv/province_deaths.csv", index=True)

    week_deaths = patient_death.filter(["pandemic_week", "patient_death"])
    week_deaths = pd.DataFrame(week_deaths.groupby("pandemic_week").count()).reset_index()
    week_deaths.to_csv("./csv/week_deaths.csv", index=True)

    print("Processed csv files created.\n")

    # clear memory
    del data, patient_death, gender_death, age_death, financing_source, province_deaths, week_deaths
