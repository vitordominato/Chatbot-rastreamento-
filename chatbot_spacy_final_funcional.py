
import streamlit as st
import spacy
import re

# Carregar modelo do spaCy
nlp = spacy.load("pt_core_news_sm")

st.set_page_config(page_title="Chatbot Inteligente com NLP", layout="centered")
st.title("Chatbot com IA – Rastreamento Médico por Linguagem Natural")
st.markdown("Digite o perfil do paciente em linguagem natural:")

user_input = st.text_area("Exemplo: Mulher, 36 anos, mãe com câncer de mama.")

def extrair_idade(texto):
    padrao = re.findall(r"(\d{2})\s*(anos|ano)", texto)
    if padrao:
        return int(padrao[0][0])
    return None

def extrair_sexo(texto):
    if "homem" in texto.lower() or "masculino" in texto.lower():
        return "masculino"
    elif "mulher" in texto.lower() or "feminino" in texto.lower():
        return "feminino"
    return None

def extrair_historico(texto):
    texto = texto.lower()
    historico = []

    if "pai" in texto and "câncer" in texto:
        historico.append("pai com câncer")
    if "mãe" in texto and "câncer" in texto:
        historico.append("mãe com câncer")
    if ("histórico" in texto and "próstata" in texto) or ("pai" in texto and "câncer" in texto and "próstata" in texto):
        historico.append("histórico de próstata")
    if "histórico" in texto and "mama" in texto:
        historico.append("histórico de mama")
    if "colorretal" in texto or "cólon" in texto:
        historico.append("câncer colorretal")
    if "tabagista" in texto or "ex-tabagista" in texto or "fuma" in texto:
        historico.append("tabagismo")
    if "obeso" in texto or "imc" in texto:
        historico.append("obesidade")

    return historico

def gerar_recomendacao(idade, sexo, historico, texto):
    respostas = []
    texto = texto.lower()

    if sexo == "feminino":
        if idade and 40 <= idade <= 74:
            respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Mamografia anual recomendada entre 40 e 74 anos.\n\n📄 **Exames a solicitar:**\n➡️ Encaminhar ao Ambulatório de Mastologia.\n📚 [INCA - Câncer de Mama](https://www.inca.gov.br/publicacoes/livros/controle-do-cancer-de-mama)")
        if (("histórico de mama" in historico) or ("mãe" in texto and "câncer" in texto and any(p in texto for p in ["mama", "mamária", "mamário", "seio"]))) and idade and idade >= 35:
            respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ História familiar de câncer de mama.\n\n📄 **Exames a solicitar:**\n➡️ Mamografia anual a partir dos 35 anos.\n📚 [INCA - Câncer de Mama](https://www.inca.gov.br/publicacoes/livros/controle-do-cancer-de-mama)")
        if idade and 25 <= idade <= 65:
            respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Papanicolau indicado.\n\n📄 **Exames a solicitar:**\n➡️ Encaminhar ao Ambulatório de Ginecologia.\n📚 [INCA - Câncer do Colo do Útero](https://www.inca.gov.br/publicacoes/livros/controle-do-cancer-do-colo-do-utero)")
        if "câncer colorretal" in historico and idade and idade >= 38:
            respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Histórico familiar de câncer colorretal.\n\n📄 **Exames a solicitar:**\n➡️ Colonoscopia antecipada.\n📚 [INCA - Câncer Colorretal](https://www.inca.gov.br/tipos-de-cancer/cancer-colorretal)")

    if sexo == "masculino":
        if idade and idade >= 50:
            respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ PSA e USG de próstata indicados.\n\n📄 **Exames a solicitar:**\n➡️ Encaminhar ao Ambulatório de Urologia.\n📚 [SBU - Câncer de Próstata](https://portaldaurologia.org.br/publico/cancer-de-prostata/)")
        if "histórico de próstata" in historico and idade:
            if idade >= 45:
                respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Histórico familiar de câncer de próstata.\n\n📄 **Exames a solicitar:**\n➡️ PSA e USG de próstata.\n📚 [SBU - Câncer de Próstata](https://portaldaurologia.org.br/publico/cancer-de-prostata/)")
            elif idade < 45:
                respostas.append("### ⚠️ ORIENTAÇÃO PROFISSIONAL\n\n✔️ Histórico familiar de câncer de próstata identificado.\n\n📌 Iniciar rastreamento com PSA e USG a partir dos 45 anos, conforme diretriz da SBU.\n📚 [SBU - Câncer de Próstata](https://portaldaurologia.org.br/publico/cancer-de-prostata/)")

    if "tabagismo" in historico and idade and 50 <= idade <= 80:
        respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Tabagismo com risco aumentado para câncer de pulmão.\n\n📄 **Exames a solicitar:**\n➡️ TC de tórax de baixa dose.\n📚 [INCA - Rastreamento do Câncer de Pulmão](https://www.gov.br/inca/pt-br/assuntos/noticias/2022/inca-lanca-nota-tecnica-sobre-rastreamento-do-cancer-de-pulmao)")

    if "obesidade" in historico:
        respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Obesidade com risco metabólico associado.\n\n📄 **Exames a solicitar:**\n➡️ Perfil lipídico, glicemia, HOMA-IR, TSH, hemoglobina glicada.\n📚 [ABESO - Diretrizes da Obesidade](https://abeso.org.br/publicacoes/diretrizes/)")

    if not respostas:
        respostas.append("❗️ Não encontrei recomendações com base nas informações fornecidas.\nTente incluir idade, sexo e histórico familiar.")

    return "\n\n".join(respostas)

if st.button("Analisar"):
    if user_input.strip():
        idade = extrair_idade(user_input)
        sexo = extrair_sexo(user_input)
        historico = extrair_historico(user_input)
        resultado = gerar_recomendacao(idade, sexo, historico, user_input)
        st.subheader("Recomendações:")
        st.markdown(resultado)
    else:
        st.warning("Digite um perfil clínico para análise.")
