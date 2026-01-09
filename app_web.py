import streamlit as st
import pandas as pd
import os

ARQUIVO = "alunos.csv"

# --- LÓGICA DE DADOS (Igual ao que você já aprendeu) ---
def carregar_dados():
    if os.path.exists(ARQUIVO):
        return pd.read_csv(ARQUIVO)
    return pd.DataFrame(columns=["nome", "idade", "nota"])

def salvar_dados(df):
    df.to_csv(ARQUIVO, index=False)

# --- INTERFACE WEB COM STREAMLIT ---
st.title("🎓 Sistema de Gestão Escolar")

# Criando abas no topo do site
aba_cadastrar, aba_listar = st.tabs(["Cadastrar", "Visualizar Lista"])

df_alunos = carregar_dados()

with aba_cadastrar:
    st.header("Novo Cadastro")
    nome = st.text_input("Nome do Aluno")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    nota = st.number_input("Nota", min_value=0.0, max_value=10.0, step=0.1)

    if st.button("Salvar Aluno"):
        if nome:
            novo_aluno = pd.DataFrame([[nome, idade, nota]], columns=["nome", "idade", "nota"])
            df_alunos = pd.concat([df_alunos, novo_aluno], ignore_index=True)
            salvar_dados(df_alunos)
            st.success(f"Aluno {nome} cadastrado com sucesso!")
        else:
            st.error("O nome é obrigatório!")

with aba_listar:
    st.header("Alunos Cadastrados")
    if not df_alunos.empty:
        # Adiciona a coluna de status automaticamente
        df_alunos['status'] = df_alunos['nota'].apply(lambda x: "✅ Aprovado" if x >= 7 else "❌ Reprovado")
        st.dataframe(df_alunos) # Mostra uma tabela interativa
    else:   
        st.info("Nenhum aluno cadastrado.") # Esta linha DEVE estar recuada para a direita