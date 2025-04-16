from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

# Initialiser l'application FastAPI
app = FastAPI()

# Ajouter le middleware CORS après avoir initialisé FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplace "*" par l'URL de ton frontend si nécessaire
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charger le modèle sauvegardé
model = joblib.load("random_forest_model.pkl")

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

    # Convert to DataFrame
    input_data = pd.DataFrame([input_dict])

    # Faire une prédiction
    prediction = model.predict(input_data)

    # Retourner la prédiction
    return {"prediction": int(prediction[0])}
