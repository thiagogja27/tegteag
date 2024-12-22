import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_modal import Modal

# Ler o arquivo Excel
df = pd.read_excel("TWILIO-MODELO_MENSAGENS.xlsx")

# Criar a barra lateral
st.sidebar.title("Opções")
opcao = st.sidebar.selectbox("Escolha uma opção:", ["Tabela", "Gráfico", "Adicionar Dados"])

# Exibir a tabela ou o gráfico com base na seleção
if opcao == "Tabela":
    st.title("Tabela de Mensagens")
    st.write(df)
elif opcao == "Gráfico":
    st.title("Gráfico de Mensagens")
    fig = px.bar(df, x='nome', y='tempo_em_mins', title='Gráfico de Mensagens')
    st.plotly_chart(fig)
elif opcao == "Adicionar Dados":
    modal = Modal("Adicionar Dados", key="adicionar_dados")
    if st.sidebar.button("Abrir Formulário"):
        modal.open()
    
    if modal.is_open():
        with modal.container():
            st.title("Adicionar Dados")
            nome = st.text_input("Nome")
            tempo_em_mins = st.number_input("Tempo em minutos", min_value=0)
            if st.button("Salvar"):
                # Adicionar os dados à tabela
                new_data = {"nome": nome, "tempo_em_mins": tempo_em_mins}
                df = df.append(new_data, ignore_index=True)
                df.to_excel("TWILIO-MODELO_MENSAGENS.xlsx", index=False)
                st.success("Dados adicionados com sucesso!")