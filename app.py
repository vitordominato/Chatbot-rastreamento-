
import streamlit as st
import re
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Chatbot de Rastreamento Médico", layout="centered")
st.title("🤖 Chatbot de Rastreamento Médico")

st.markdown("""### 🧭 Exemplos:
- Mulher, 42 anos, mãe com câncer de mama
- Homem, 50 anos, tabagista há 20 anos
- Paciente, 56 anos, histórico de câncer de cólon no pai""")

with st.expander("🔽 Preencher por formulário (opcional)"):
    col1, col2 = st.columns(2)
    with col1:
        sexo_form = st.selectbox("Sexo", ["", "Feminino", "Masculino"])
    with col2:
        idade_form = st.number_input("Idade", min_value=0, max_value=120, step=1, format="%d")
    historico_form = st.text_area("Histórico clínico / familiar")

if sexo_form and idade_form and historico_form:
    user_input = f"{sexo_form}, {idade_form} anos, {historico_form}"
else:
    user_input = st.text_area("✍️ Ou digite livremente o perfil do paciente:", "")

historico_registro = []

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

    cancer_terms = ["cancer", "câncer", "ca", "adenocarcinoma", "carcinoma", "neoplasia", "tumor maligno"]
    tabagismo_terms = ["fuma", "fumante", "tabagista", "ex-fumante", "fumou", "tabagismo", "cigarro", "maços"]

    if sexo == "feminino":
        if idade and 40 <= idade <= 74:
            respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Mamografia anual indicada (40-74 anos).\n\n📚 [INCA – Câncer de Mama](https://www.inca.gov.br/publicacoes/cartilhas/cancer-de-mama-vamos-falar-sobre-isso)")
        if idade and idade >= 35 and ("mãe" in texto and any(t in texto for t in cancer_terms) and any(p in texto for p in ["mama", "mamaria", "mamário", "seio"])):
            respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Histórico familiar de câncer de mama.\n\n📄 Mamografia anual a partir dos 35 anos.\n\n📚 [INCA](https://www.inca.gov.br/publicacoes/cartilhas/cancer-de-mama-vamos-falar-sobre-isso)")
        if idade and 25 <= idade <= 65:
            respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Rastreio com Papanicolau indicado (25 a 65 anos).\n\n📚 [SBOC – Colo do Útero](https://sboc.org.br/images/Diretrizes-2024/pdf/10---Diretrizes-SBOC-2024---Colo-do-utero-v5-FINAL.pdf)")

    if sexo == "masculino":
        if idade and idade >= 50:
            respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Rastreio de próstata a partir de 50 anos.\n\n📄 PSA + USG.\n\n📚 [SBU – Próstata](https://portaldaurologia.org.br/publico/cancer-de-prostata/)")
        if idade and ("pai" in texto and any(t in texto for t in cancer_terms) and any(p in texto for p in ["prostata", "próstata"])):
            if idade >= 45:
                respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Histórico familiar de câncer de próstata.\n\n📄 PSA + USG a partir dos 45 anos.\n\n📚 [SBU – Próstata](https://portaldaurologia.org.br/publico/cancer-de-prostata/)")
            else:
                respostas.append("### ℹ️ ORIENTAÇÃO\n\n✔️ Início do rastreio recomendado aos 45 anos por histórico familiar.\n\n📚 [SBU – Próstata](https://portaldaurologia.org.br/publico/cancer-de-prostata/)")

    if any(t in texto for t in cancer_terms) and any(p in texto for p in ["colon", "cólon", "colorretal", "retal"]):
        if idade and idade >= 38:
            respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Histórico familiar de câncer colorretal.\n\n📄 Colonoscopia antecipada.\n\n📚 [INCA – Câncer Colorretal](https://www.inca.gov.br/tipos-de-cancer/cancer-colorretal)")

    if any(t in texto for t in tabagismo_terms):
        if idade and 50 <= idade <= 80:
            respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Tabagismo atual ou passado em idade de risco.\n\n📄 TC de tórax de baixa dose.\n\n📚 [INCA – Câncer de Pulmão](https://www.inca.gov.br/controle-do-cancer-do-pulmao)")
        else:
            respostas.append("### ℹ️ ORIENTAÇÃO\n\n✔️ Tabagismo identificado. O rastreio com TC de tórax é recomendado entre 50 e 80 anos.\n\n📚 [INCA – Câncer de Pulmão](https://www.inca.gov.br/controle-do-cancer-do-pulmao)")

    if idade and idade >= 50:
        respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Rastreio de gamopatias monoclonais.\n\n📄 Eletroforese de proteínas séricas e imunofixação.\n\n📚 [SBHH – Hematologia](https://www.hematologia.org.br/)")

    if "obeso" in texto or "sobrepeso" in texto or "imc" in texto:
        respostas.append("### ⚠️ ALERTA CLÍNICO\n\n✔️ Obesidade ou risco metabólico.\n\n📄 Perfil lipídico, glicemia, HOMA-IR, TSH.\n\n📚 [ABESO – Obesidade](https://abeso.org.br/publicacoes/diretrizes/)")

    if not respostas:
        respostas.append("❗️ Nenhuma recomendação foi identificada.\n\n💡 Este bot oferece sugestões de rastreio baseadas em idade, sexo e histórico pessoal/familiar.\n\n✍️ Exemplos:\n- Mulher, 42 anos, mãe com câncer de mama\n- Homem, 50 anos, tabagista\n- Paciente 56 anos, pai com câncer colorretal")

    return "\n\n".join(respostas)

if st.button("Analisar"):
    if user_input.strip():
        st.subheader("Recomendações:")
        resultado = analisar(user_input)
        st.markdown(resultado)

        historico_registro.append({"Data": datetime.now(), "Entrada": user_input, "Resposta": resultado})

        if st.download_button("📄 Exportar resposta (CSV)", pd.DataFrame(historico_registro).to_csv(index=False).encode(), file_name="rastreamento.csv"):
            st.success("Exportado com sucesso!")

        st.markdown("### 🙋 Feedback")
        colf1, colf2 = st.columns(2)
        with colf1:
            if st.button("👍 Ajudou"):
                st.toast("Obrigado pelo feedback! 🙌")
        with colf2:
            if st.button("👎 Não ajudou"):
                st.toast("Vamos melhorar! 💡")
    else:
        st.warning("Digite ou selecione dados para análise.")
