import streamlit as st
import requests


# Définir l'URL de l'API
API_URL = "http://127.0.0.1:8000/predict/"

# Titre de l'application
st.title("Détection de Fraude - Interface")

# Formulaire pour saisir les données
step = st.number_input("Step (unité de temps)", min_value=0, step=1)

# Liste déroulante pour les types de transaction
type_payment = st.selectbox(
    "Type de transaction",
    ["CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]  # Options uniques
)

# Convertir le type sélectionné en indicateurs binaires
type_CASH_OUT = int(type_payment == "CASH_OUT")
type_DEBIT = int(type_payment == "DEBIT")
type_PAYMENT = int(type_payment == "PAYMENT")
type_TRANSFER = int(type_payment == "TRANSFER")

# Autres champs du formulaire
amount = st.number_input("Montant de la transaction", min_value=0.0, step=0.01)
oldbalanceOrg = st.number_input("Ancien solde de l'expéditeur", min_value=0.0, step=0.01)
newbalanceOrig = st.number_input("Nouveau solde de l'expéditeur", min_value=0.0, step=0.01)
oldbalanceDest = st.number_input("Ancien solde du destinataire", min_value=0.0, step=0.01)
newbalanceDest = st.number_input("Nouveau solde du destinataire", min_value=0.0, step=0.01)

# Afficher les valeurs sélectionnées (facultatif)
st.write("Type sélectionné:", type_payment)
st.write("Indicateurs binaires:", type_CASH_OUT, type_DEBIT, type_PAYMENT, type_TRANSFER)

# Bouton pour soumettre les données
if st.button("Prédire"):
    # Préparer les données pour l'API
    data = {
        "step": step,
        "type_payment": type_payment,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest,
    }

    # Envoyer une requête POST à l'API
    response = requests.post(API_URL, json=data)

    # Afficher le résultat
    if response.status_code == 200:
        prediction = response.json()["prediction"]
        if prediction == 1:
            st.error("Fraude détectée !")
        else:
            st.success("Pas de fraude détectée.")
    else:
        st.error("Erreur lors de la communication avec l'API.")