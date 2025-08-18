from collections import Counter
import os
import joblib
import pandas as pd
from sklearn.model_selection import GridSearchCV
import numpy as np
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

col_data = []
spellname = []
basis_ordner = "/Users/jeffersonnguechoum/Desktop/IUI/group-e/project-one/python-recorder/recordings"
gesten = ["Orbrix", "Quadrix", "Threnix"]
columns = ["accX", "accY", "accZ", "gyroX", "gyroY", "gyroZ"]


# Schritt 1: Durchlaufe alle Gesten
def interpolate_block(df, num_points):
    interpolated = {}  # Neues leeres Dictionary für die neuen Spalten

    for col in columns:  # Gehe jede Spalte durch (accX, accY, ...)
        y = df[col].values  # Hole die Werte der Spalte als NumPy-Array
        # Alte Zeitachse (z. B. 0–1 bei 100 Werten)
        x_old = np.linspace(0, 1, len(y))
        x_new = np.linspace(0, 1, num_points)  # Neue Zeitachse mit 50 Punkten
        # Neue y-Werte durch lineare Interpolation
        y_new = np.interp(x_new, x_old, y)
        interpolated[col] = y_new  # Neue Spalte speichern

    return pd.DataFrame(interpolated)  # Rückgabe als DataFrame


def split_data(df):
    for geste in gesten:
        ordner = os.path.join(basis_ordner, geste)
        for datei in os.listdir(ordner):
            if datei.endswith(".csv"):
                pfad = os.path.join(ordner, datei)
                df = pd.read_csv(pfad, sep=";")
                df_interp = interpolate_block(df, 5)
                row = []
                for spalte in columns:
                    row.append(df_interp[spalte].std())
                    row.append(df_interp[spalte].mean())
                col_data.append(row)
                spellname.append(geste)
    return col_data, spellname


"""
num_points = 5, n_estimators = 24, max_depth = 5, min_samples_split = 4
Accuracy = 0.9737
"""
col_data, spellname = split_data(col_data)

col_data_train, col_data_test, spellname_train, spellname_test = train_test_split(
    col_data, spellname, test_size=0.2, random_state=42)

print("Verteilung im Testset:", Counter(spellname_test))

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(col_data_train)
X_test_scaled = scaler.transform(col_data_test)

rf = RandomForestClassifier(
    n_estimators=50, max_depth=7, min_samples_split=6, random_state=42)
rf.fit(X_train_scaled, spellname_train)
y_pred = rf.predict(X_test_scaled)


print(classification_report(spellname_test, y_pred))

joblib.dump(rf, "random_forest_model.joblib")
joblib.dump(scaler, "scaler_neu.joblib")
