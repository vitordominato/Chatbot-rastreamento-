
import streamlit as st
from pathlib import Path
from fpdf import FPDF

st.set_page_config(page_title="Chatbot de Rastreamento – Institucional", layout="centered")
st.title("🩺 Chatbot de Rastreamento com Diretrizes Incorporadas")

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

def gerar_pdf(titulo, linhas):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, titulo, ln=True)
    pdf.set_font("Arial", "", 12)
    for linha in linhas:
        pdf.multi_cell(0, 10, linha)
    nome_pdf = "resumo_rastreamento.pdf"
    pdf.output(nome_pdf)
    return nome_pdf

def baixar_pdf(arquivo, descricao, key):
    path = Path(arquivo)
    if path.exists():
        with open(path, "rb") as f:
            st.download_button(f"📎 {descricao}", f, file_name=arquivo, key=key)

if submit:
    respostas = []

    if sexo == "Feminino":
        if 40 <= idade <= 74:
            respostas.append(("✔️ Mamografia anual (40–74 anos). Encaminhar ao Ambulatório de Mastologia, se necessário.", "rastreamaneto_cancer_mama.pdf"))
        if ca_mama and idade >= 35:
            respostas.append(("✔️ Mamografia antecipada por histórico familiar (≥ 35 anos). Encaminhar ao Ambulatório de Mastologia.", "rastreamaneto_cancer_mama.pdf"))
        if 25 <= idade <= 65:
            respostas.append(("✔️ Papanicolau recomendado (25–65 anos). Encaminhar ao Ambulatório de Ginecologia.", "rastreamento_cancer_colo_utero.pdf"))

    if sexo == "Masculino":
        if idade >= 50:
            respostas.append(("✔️ PSA e USG prostático (≥ 50 anos). Encaminhar ao Ambulatório de Urologia.", "rastreamento_próstat_2023_sociedades.pdf"))
        if ca_prostata and idade >= 45:
            respostas.append(("✔️ Rastreamento antecipado de próstata por histórico (≥ 45 anos). Encaminhar ao Ambulatório de Urologia.", "rastreamento_próstat_2023_sociedades.pdf"))

    if ca_colon and idade >= 38:
        respostas.append(("✔️ Colonoscopia antecipada por histórico familiar de câncer colorretal. Encaminhar ao Ambulatório de Proctologia.", "CÂNCER COLORRETAL_DO DIAGNÓSTICO AO TRATAMENTO.pdf"))

    if tabagista:
        if 50 <= idade <= 80:
            respostas.append(("✔️ TC de tórax de baixa dose (50–80 anos, tabagista). Encaminhar ao Ambulatório de Pneumologia.", "Recomendacoes da Sociedade Brasileira para o rastreamento do cancer de pulmao.pdf"))
        else:
            respostas.append(("ℹ️ Tabagismo presente, mas rastreio com TC de tórax é indicado entre 50 e 80 anos.", None))

    if imc_alto or historico_metabolico:
        respostas.append(("✔️ Avaliação metabólica: perfil lipídico, glicemia, hemoglobina glicada, HOMA-IR, TSH. Encaminhar ao Centro de Obesidade.", "Diretrizes-Brasileiras-de-Obesidade-2016.pdf"))

    if idade >= 50:
        respostas.append(("✔️ Rastreio de gamopatias monoclonais (≥ 50 anos): eletroforese e imunofixação. Encaminhar ao Ambulatório de Hematologia.", "Gamopatias_monoclonais_criterios_diagnosticos.pdf"))

    if respostas:
        st.subheader("📋 Recomendações:")
        for i, (texto, pdf) in enumerate(respostas):
            st.markdown(f"- {texto}")
            if pdf:
                baixar_pdf(pdf, "📚 Acessar diretriz", key=f"{pdf}_{i}")
        if st.button("📄 Gerar PDF com resumo"):
            texto_respostas = [r[0] for r in respostas]
            nome_pdf = gerar_pdf("Resumo de Rastreamento", texto_respostas)
            with open(nome_pdf, "rb") as f:
                st.download_button("⬇️ Baixar Resumo em PDF", f, file_name=nome_pdf)
    else:
        st.warning("⚠️ Nenhuma recomendação foi identificada com os dados fornecidos. Reavalie faixa etária, histórico familiar ou fatores clínicos.")
