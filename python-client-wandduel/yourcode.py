# IMPORTANT: Please make all your changes to this file
import joblib
import numpy as np
import pandas as pd
from random import randrange
from sklearn.ensemble import RandomForestClassifier

# interpolate_block kommt aus init, wo auch der Random Forest trainiert wird
from __init__ import interpolate_block

spellname1 = "Orbrix"
spellname2 = "Quadrix"
spellname3 = "Threnix"


def process_spell(pandas_df: pd.DataFrame):
    # Interpolation auf 15 Punkte (beste Einstellung aus Training)
    columns = ["accX", "accY", "accZ", "gyroX", "gyroY", "gyroZ"]
    features = interpolate_block(pandas_df[columns], num_points=5)

    # Feature-Vektor: Mittelwert, Standardabweichung usw.
    row = []
    for name in columns:
        row.append(pandas_df[name].std())
        row.append(pandas_df[name].mean())

    X_input = np.array(row).reshape(1, -1)

    # Modell & Skaler laden
    scaler = joblib.load("scaler_neu.joblib")
    model = joblib.load("random_forest_model.joblib")

    # Skalieren
    X_scaled = scaler.transform(X_input)

    # Vorhersage
    prediction = model.predict(X_scaled)[0]

    # Klassenzuordnung
    if prediction == spellname1:
        return 1, get_spellname(1)
    elif prediction == spellname2:
        return 2, get_spellname(2)
    elif prediction == spellname3:
        return 3, get_spellname(3)
    else:
        return 0, "Unknown"


def get_spellname(id):
    if id == 1:
        return spellname1
    if id == 2:
        return spellname2
    if id == 3:
        return spellname3
    return "Unknown Spell"
