from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd


# Charger le modèle sauvegardé
model = joblib.load("random_forest_model.pkl")

# Initialiser l'application FastAPI
app = FastAPI()

# Définir le modèle de données pour la requête
class PredictionRequest(BaseModel):
    step: int
    type_payment: str  # "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"
    amount: float
    oldbalanceOrg: float
    newbalanceOrig: float
    oldbalanceDest: float
    newbalanceDest: float

@app.post("/predict")
def predict(request: PredictionRequest):
    # Convertir les données en DataFrame
    input_dict = request.dict()
    type_payment = input_dict.pop("type_payment")

# Convert type_payment into binary columns
    input_dict["type_CASH_OUT"] = int(type_payment == "CASH_OUT")
    input_dict["type_DEBIT"] = int(type_payment == "DEBIT")
    input_dict["type_PAYMENT"] = int(type_payment == "PAYMENT")
    input_dict["type_TRANSFER"] = int(type_payment == "TRANSFER")
    print(input_dict)

# Convert to DataFrame
    input_data = pd.DataFrame([input_dict])
    # Faire une prédiction
    prediction = model.predict(input_data)

    # Retourner la prédiction
    return {"prediction": int(prediction[0])}

# Pour exécuter l'application, utilisez la commande suivante dans le terminal :
# py -m uvicorn monapi:app --reload