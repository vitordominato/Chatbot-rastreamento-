import streamlit as st
import re

st.set_page_config(page_title="Chatbot de Rastreamento Médico", layout="centered")
st.title("Chatbot de Rastreamento Médico – Versão Leve (sem spaCy)")
st.markdown("Digite o perfil do paciente em linguagem natural:")

user_input = st.text_area("Exemplo: Mulher, 36 anos, mãe com câncer de mama")

def extrair_idade(texto):
    match = re.search(r"(\d{2})\s*(anos|ano)", texto)
    return int(match.group(1)) if match else None

def extrair_sexo(texto):
    if "homem" in texto.lower() or "masculino" in texto.lower():
        return "masculino"
    elif "mulher" in texto.lower() or "feminino" in texto.lower():
        return "feminino"
    return None

def analisar(texto):
    idade = extrair_idade(texto)
    sexo = extrair_sexo(texto)
    texto = texto.lower()
    respostas = []

    if sexo == "feminino":
        if idade and 40 <= idade <= 74:
            respostas.append("✔️ Mamografia anual recomendada (40-74 anos).")
        if idade and idade >= 35 and ("mãe" in texto and "câncer" in texto and any(p in texto for p in ["mama", "seio", "mamário", "mamária"])):
            respostas.append("✔️ História familiar de câncer de mama. Mamografia anual a partir dos 35 anos.")
        if idade and 25 <= idade <= 65:
            respostas.append("✔️ Papanicolau indicado entre 25 e 65 anos.")
    if sexo == "masculino":
        if idade and idade >= 50:
            respostas.append("✔️ PSA e USG de próstata indicados a partir dos 50 anos.")
        if idade and idade >= 45 and ("pai" in texto and "câncer" in texto and "próstata" in texto):
            respostas.append("✔️ História familiar de câncer de próstata. PSA e USG a partir dos 45 anos.")
        elif idade and idade < 45 and ("pai" in texto and "câncer" in texto and "próstata" in texto):
            respostas.append("✔️ História familiar de câncer de próstata. Orientar início do rastreio aos 45 anos.")
    if "câncer" in texto and any(colon in texto for colon in ["cólon", "colon", "colorretal"]):
        if idade and idade >= 38:
            respostas.append("✔️ Histórico familiar de câncer colorretal. Colonoscopia antecipada a partir dos 38 anos.")
    if idade and 50 <= idade <= 80 and any(p in texto for p in ["fuma", "tabagista", "ex-fumante"]):
        respostas.append("✔️ Tabagismo atual ou passado. Solicitar TC de tórax de baixa dose para rastreamento de câncer de pulmão.")
    if "obeso" in texto or "imc" in texto:
        respostas.append("✔️ Obesidade detectada. Solicitar exames metabólicos e avaliar com equipe multidisciplinar.")

    if not respostas:
        respostas.append("❗️ Não encontrei recomendações com base no que foi informado. Verifique idade, sexo e histórico.")

    return "\n\n".join(respostas)

if st.button("Analisar"):
    if user_input.strip():
        st.subheader("Recomendações:")
        resultado = analisar(user_input)
        st.markdown(resultado)
    else:
        st.warning("Digite um perfil clínico para análise.")
