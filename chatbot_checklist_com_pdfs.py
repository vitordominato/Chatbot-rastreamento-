
import streamlit as st
import base64

st.set_page_config(page_title="Rastreamento com Diretrizes", layout="centered")
st.title("📋 Chatbot de Rastreamento com Diretrizes Incorporadas")

st.markdown("### ✅ Preencha os dados do paciente para receber recomendações de rastreio:")

with st.form("form"):
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

def visualizar_pdf(nome, titulo):
    with open(nome, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(f"#### 📄 {titulo}")
        st.download_button("⬇️ Baixar PDF", f, file_name=nome)
        st.markdown(f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500px" type="application/pdf"></iframe>', unsafe_allow_html=True)

if submit:
    respostas = []

    if sexo == "Feminino":
        if 40 <= idade <= 74:
            respostas.append("✔️ Mamografia anual (40–74 anos)")
            visualizar_pdf("Rastreamento do câncer de mama.pdf", "Diretriz – Câncer de Mama")
        if ca_mama and idade >= 35:
            respostas.append("✔️ Mamografia antecipada por histórico familiar (≥ 35 anos)")
            visualizar_pdf("Rastreamento do câncer de mama.pdf", "Diretriz – Câncer de Mama")
        if 25 <= idade <= 65:
            respostas.append("✔️ Papanicolau recomendado (25–65 anos)")
            visualizar_pdf("diretrizes_para_o_rastreamento_do_cancer_do_colo_do_utero_2016_corrigido.pdf", "Diretriz – Colo do Útero")

    if sexo == "Masculino":
        if idade >= 50:
            respostas.append("✔️ PSA e USG prostático (≥ 50 anos)")
            visualizar_pdf("rastreamento_próstat_2023_sociedades.pdf", "Diretriz – Câncer de Próstata")
        if ca_prostata and idade >= 45:
            respostas.append("✔️ Rastreamento de próstata antecipado por histórico (≥ 45 anos)")
            visualizar_pdf("rastreamento_próstat_2023_sociedades.pdf", "Diretriz – Câncer de Próstata")

    if ca_colon and idade >= 38:
        respostas.append("✔️ Colonoscopia antecipada por histórico familiar de câncer colorretal")
        visualizar_pdf("CÂNCER COLORRETAL_DO DIAGNÓSTICO AO TRATAMENTO.pdf", "Diretriz – Câncer Colorretal")

    if tabagista:
        if 50 <= idade <= 80:
            respostas.append("✔️ TC de tórax de baixa dose (50–80 anos, tabagista)")
            visualizar_pdf("Recomendacoes da Sociedade Brasileira para o rastreamento do cancer de pulmao.pdf", "Diretriz – Câncer de Pulmão")
        else:
            respostas.append("ℹ️ Tabagismo presente, mas rastreio com TC de tórax é indicado entre 50 e 80 anos")

    if imc_alto or historico_metabolico:
        respostas.append("✔️ Avaliação metabólica recomendada")
        visualizar_pdf("Diretrizes-Brasileiras-de-Obesidade-2016.pdf", "Diretriz – Obesidade / Metabólico")

    if idade >= 50:
        respostas.append("✔️ Rastreio de gamopatias monoclonais (≥ 50 anos)")
        visualizar_pdf("Gamopatias_monoclonais_criterios_diagnosticos.pdf", "Diretriz – Gamopatias Monoclonais")

    if respostas:
        st.subheader("📌 Recomendações Geradas:")
        for r in respostas:
            st.markdown(f"- {r}")
    else:
        st.warning("Nenhuma recomendação foi gerada com os dados fornecidos.")
