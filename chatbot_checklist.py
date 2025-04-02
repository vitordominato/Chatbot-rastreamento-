
import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Chatbot de Rastreamento Médico", layout="centered")
st.title("🩺 Chatbot de Rastreamento Médico – Versão com Checklist")

st.markdown("""### ✅ Selecione as informações do paciente:
As recomendações serão geradas com base nos fatores abaixo.""")

with st.form("formulario"):
    sexo = st.selectbox("Sexo do paciente:", ["", "Feminino", "Masculino"])
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)

    col1, col2 = st.columns(2)
    with col1:
        imc_alto = st.checkbox("IMC ≥ 25")
        tabagista = st.checkbox("Tabagista ou ex-tabagista")
        historico_metabolico = st.checkbox("Doenças metabólicas (ex: diabetes, HAS)")
    with col2:
        ca_mama = st.checkbox("Histórico familiar de câncer de mama")
        ca_prostata = st.checkbox("Histórico familiar de câncer de próstata")
        ca_colon = st.checkbox("Histórico familiar de câncer colorretal")

    submit = st.form_submit_button("Gerar Recomendações")

if submit:
    respostas = []

    if sexo == "Feminino":
        if 40 <= idade <= 74:
            respostas.append("✔️ Mamografia anual (40 a 74 anos).")
        if ca_mama and idade >= 35:
            respostas.append("✔️ Mamografia precoce devido a histórico familiar de câncer de mama (≥ 35 anos).")
        if 25 <= idade <= 65:
            respostas.append("✔️ Papanicolau recomendado (25 a 65 anos).")

    if sexo == "Masculino":
        if idade >= 50:
            respostas.append("✔️ PSA e USG de próstata (≥ 50 anos).")
        if ca_prostata and idade >= 45:
            respostas.append("✔️ Rastreio de próstata antecipado por histórico familiar (≥ 45 anos).")

    if ca_colon and idade >= 38:
        respostas.append("✔️ Colonoscopia antecipada por histórico familiar de câncer colorretal.")

    if tabagista:
        if 50 <= idade <= 80:
            respostas.append("✔️ TC de tórax de baixa dose para rastreio de câncer de pulmão (50–80 anos, tabagista).")
        else:
            respostas.append("ℹ️ Tabagismo detectado, mas rastreio com TC de tórax é indicado apenas entre 50 e 80 anos.")

    if imc_alto or historico_metabolico:
        respostas.append("✔️ Avaliação metabólica: perfil lipídico, glicemia, hemoglobina glicada, HOMA-IR, TSH.")

    if idade >= 50:
        respostas.append("✔️ Rastreio de gamopatias monoclonais: eletroforese de proteínas séricas e imunofixação.")

    if respostas:
        st.subheader("📋 Recomendações:")
        for r in respostas:
            st.markdown(f"- {r}")
        st.markdown("📚 Referências: [INCA](https://www.inca.gov.br) • [SBU](https://portaldaurologia.org.br) • [ABESO](https://abeso.org.br) • [SBHH](https://www.hematologia.org.br)")
    else:
        st.warning("Nenhuma recomendação encontrada com os dados fornecidos.")
