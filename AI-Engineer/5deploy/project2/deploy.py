import joblib
import streamlit as st
import pandas as pd
from sklearn.pipeline import Pipeline

def load_model(model_path: str) -> Pipeline:
    return joblib.load(model_path)

def preprocess_input(prediciton_values: dict) -> pd.DataFrame:
    return pd.DataFrame(prediciton_values, columns=prediciton_values.keys())

def main():

    model = load_model('model.pkl')

    st.title('Previsão de Churn')
    st.subheader('Insira os dados do cliente')

    
    idade = st.number_input('Idade', min_value=18, max_value=100, value=18)
    uso_mensal = st.number_input('Uso Mensal', min_value=0, max_value=100, value=0)
    satisfacao = st.number_input('Satisfação do Cliente', min_value=1, max_value=5, value=1)
    valor_mensal = st.number_input('Valor Mensal', min_value=0, max_value=100, value=0)
    plano = st.selectbox('Plano', ['Basico', 'Premium', 'Standard'])
    contrato = st.selectbox('Contrato', ['Curto', 'Médio', 'Longo'])

    if st.button('Prever Churn'): 
        prediction_values = {
            'Idade': [idade],
            'UsoMensal': [uso_mensal],
            'Plano': [plano],
            'SatisfacaoCliente': [satisfacao],
            'TempoContrato': [contrato],
            'ValorMensal': [valor_mensal]
        }
        prediction = model.predict(preprocess_input(prediction_values))
        cancela = 'Sim' if prediction[0] == 1 else 'Não'
        st.write(f'Cancelará o plano: {cancela}')

main()