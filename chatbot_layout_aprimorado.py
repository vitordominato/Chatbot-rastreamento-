
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Chatbot de Rastreamento", layout="centered")
st.title("🩺 Chatbot de Rastreamento com Diretrizes (Layout Aprimorado)")

st.markdown("### ✅ Preencha os dados do paciente:")

with st.form("formulario"):
    sexo = st.selectbox("Sexo:", ["", "Feminino", "Masculino"])
    idade = st.number_input("Idade:", 0, 120, step=1)
    col1, col2 = st.columns(2)
    with col1:
        imc_alto = st.checkbox("IMC ≥ 25")
        tabagista = st.checkbox("Tabagista ou ex-tabagista")
        historico_metabolico = st.checkbox("Doenças metabólicas (diabetes, HAS)")
    with col2:
        ca_mama = st.checkbox("Histórico familiar de câncer de mama")
        ca_prostata = st.checkbox("Histórico familiar de câncer de próstata")
        ca_colon = st.checkbox("Histórico familiar de câncer colorretal")
    submit = st.form_submit_button("Gerar Recomendações")

def exibir_pdf(nome, descricao):
    file_path = Path(nome)
    if file_path.exists():
        with open(file_path, "rb") as f:
            st.download_button(f"📎 Baixar PDF: {descricao}", f, file_name=nome)

if submit:
    respostas = []

    if sexo == "Feminino":
        if 40 <= idade <= 74:
            respostas.append(("✔️ Mamografia anual (40–74 anos)", "Rastreamento do câncer de mama.pdf"))
        if ca_mama and idade >= 35:
            respostas.append(("✔️ Mamografia antecipada por histórico familiar (≥ 35 anos)", "Rastreamento do câncer de mama.pdf"))
        if 25 <= idade <= 65:
            respostas.append(("✔️ Papanicolau recomendado (25–65 anos)", "diretrizes_para_o_rastreamento_do_cancer_do_colo_do_utero_2016_corrigido.pdf"))

    if sexo == "Masculino":
        if idade >= 50:
            respostas.append(("✔️ PSA e USG prostático (≥ 50 anos)", "rastreamento_próstat_2023_sociedades.pdf"))
        if ca_prostata and idade >= 45:
            respostas.append(("✔️ Rastreamento antecipado de próstata por histórico (≥ 45 anos)", "rastreamento_próstat_2023_sociedades.pdf"))

    if ca_colon and idade >= 38:
        respostas.append(("✔️ Colonoscopia antecipada por histórico familiar de câncer colorretal", "CÂNCER COLORRETAL_DO DIAGNÓSTICO AO TRATAMENTO.pdf"))

    if tabagista:
        if 50 <= idade <= 80:
            respostas.append(("✔️ TC de tórax de baixa dose (50–80 anos, tabagista)", "Recomendacoes da Sociedade Brasileira para o rastreamento do cancer de pulmao.pdf"))
        else:
            respostas.append(("ℹ️ Tabagismo presente, mas rastreio com TC de tórax é indicado entre 50 e 80 anos", None))

    if imc_alto or historico_metabolico:
        respostas.append(("✔️ Avaliação metabólica: perfil lipídico, glicemia, hemoglobina glicada, HOMA-IR, TSH", "Diretrizes-Brasileiras-de-Obesidade-2016.pdf"))

    if idade >= 50:
        respostas.append(("✔️ Rastreio de gamopatias monoclonais (≥ 50 anos): eletroforese e imunofixação", "Gamopatias_monoclonais_criterios_diagnosticos.pdf"))

    if respostas:
        st.subheader("📋 Recomendações:")
        for texto, arquivo in respostas:
            st.markdown(f"- {texto}")
            if arquivo:
                exibir_pdf(arquivo, arquivo.replace(".pdf", ""))
    else:
        st.warning("Nenhuma recomendação encontrada com os dados fornecidos.")
