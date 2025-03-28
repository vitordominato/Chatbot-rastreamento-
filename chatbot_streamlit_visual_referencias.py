
import streamlit as st
import re

st.set_page_config(page_title="Chatbot de Rastreamento Médico", layout="centered")
st.title("Chatbot de Rastreamento Médico – Versão Leve com Alerta Visual")
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
            respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Mamografia anual recomendada para mulheres de 40 a 74 anos.\n\n📚 [INCA - Câncer de Mama](https://www.inca.gov.br/publicacoes/livros/controle-do-cancer-de-mama)")
        if idade and idade >= 35 and ("mãe" in texto and "câncer" in texto and any(p in texto for p in ["mama", "seio", "mamário", "mamária"])):
            respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ História familiar de câncer de mama.\n\n📄 Exames: Mamografia anual a partir dos 35 anos.\n\n📚 [INCA - Câncer de Mama](https://www.inca.gov.br/publicacoes/livros/controle-do-cancer-de-mama)")
        if idade and 25 <= idade <= 65:
            respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Rastreio de câncer do colo do útero indicado.\n\n📄 Exame: Papanicolau.\n\n📚 [INCA - Câncer do Colo do Útero](https://www.inca.gov.br/publicacoes/livros/controle-do-cancer-do-colo-do-utero)")

    if sexo == "masculino":
        if idade and idade >= 50:
            respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Rastreio de câncer de próstata indicado a partir dos 50 anos.\n\n📄 Exames: PSA e USG de próstata.\n\n📚 [SBU - Câncer de Próstata](https://portaldaurologia.org.br/publico/cancer-de-prostata/)")
        if idade and ("pai" in texto and "câncer" in texto and "próstata" in texto):
            if idade >= 45:
                respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Histórico familiar de câncer de próstata (pai afetado).\n\n📄 Exames: PSA e USG de próstata a partir dos 45 anos.\n\n📚 [SBU - Câncer de Próstata](https://portaldaurologia.org.br/publico/cancer-de-prostata/)")
            else:
                respostas.append("### ℹ️ ORIENTAÇÃO\n\n✔️ Histórico familiar de câncer de próstata.\n\n📌 Orientar início do rastreio com PSA e USG aos 45 anos.\n\n📚 [SBU - Câncer de Próstata](https://portaldaurologia.org.br/publico/cancer-de-prostata/)")

    if "câncer" in texto and any(colon in texto for colon in ["cólon", "colon", "colorretal"]):
        if idade and idade >= 38:
            respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Histórico familiar de câncer colorretal.\n\n📄 Exame: Colonoscopia antecipada.\n\n📚 [INCA - Câncer Colorretal](https://www.inca.gov.br/tipos-de-cancer/cancer-colorretal)")

    if idade and 50 <= idade <= 80 and any(p in texto for p in ["fuma", "tabagista", "ex-fumante"]):
        respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Risco elevado para câncer de pulmão por tabagismo.\n\n📄 Exame: TC de tórax de baixa dose.\n\n📚 [INCA - Câncer de Pulmão](https://www.inca.gov.br/controle-do-cancer-do-pulmao)")

    if "obeso" in texto or "imc" in texto:
        respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Obesidade ou sobrepeso com risco metabólico.\n\n📄 Exames: Perfil lipídico, glicemia, HOMA-IR, TSH.\n\n📚 [ABESO - Diretrizes da Obesidade](https://abeso.org.br/publicacoes/diretrizes/)")

    if not respostas:
        respostas.append("❗️ Nenhuma recomendação foi identificada com as informações fornecidas.\n\nInclua idade, sexo e histórico clínico relevante.")

    return "\n\n".join(respostas)

if st.button("Analisar"):
    if user_input.strip():
        st.subheader("Recomendações:")
        resultado = analisar(user_input)
        st.markdown(resultado)
    else:
        st.warning("Digite um perfil clínico para análise.")
