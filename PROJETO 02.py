import tkinter as tk
from tkinter import messagebox
import csv
import os

# --- 1. CONFIGURAÇÕES E DADOS ---
ARQUIVO = "alunos.csv"
alunos = []

def carregar_alunos():
    global alunos
    alunos = [] # Limpa a lista antes de carregar
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            # Corrigido: csv.DictReader (D maiúsculo e sem ponto extra)
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                alunos.append({
                    "nome": linha["nome"],
                    "idade": int(linha["idade"]),
                    "nota": float(linha["nota"])
                })

def salvar_alunos():
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["nome", "idade", "nota"])
        for aluno in alunos:
            escritor.writerow([aluno["nome"], aluno["idade"], aluno["nota"]])

# --- 2. FUNÇÕES DE LÓGICA ---

def cadastrar_aluno():
    try:
        nome = entrada_nome.get().strip() # .strip() remove espaços vazios antes/depois
        idade_str = entrada_idade.get()
        nota_str = entrada_nota.get()

        # Validação básica: não aceitar nome vazio
        if not nome:
            messagebox.showwarning("Atenção", "O campo 'Nome' não pode estar vazio!")
            return

        # --- NOVA LÓGICA: VERIFICAÇÃO DE DUPLICADOS ---
        # Percorre a lista de alunos e compara os nomes em letras minúsculas
        for aluno in alunos:
            if aluno["nome"].lower() == nome.lower():
                messagebox.showwarning("Erro", f"O aluno '{nome}' já está cadastrado!")
                return # Para a função aqui e não cadastra
        # ----------------------------------------------

        idade = int(idade_str)
        nota = float(nota_str)
        
        novo_aluno = {"nome": nome, "idade": idade, "nota": nota}
        alunos.append(novo_aluno)
        salvar_alunos() # Salva no CSV imediatamente
    
        messagebox.showinfo("Sucesso", f"Aluno {nome} cadastrado!")
        limpar_tela()
        listar_alunos() # Atualiza a lista na tela automaticamente

    except ValueError:
        messagebox.showerror("Erro", "Idade e Nota precisam ser números!")



def listar_alunos():
    texto = "--- LISTA DE ALUNOS ---\n"
    for aluno in alunos:
        status = "Aprovado" if aluno["nota"] >= 7 else "Reprovado"
        texto += f"{aluno['nome']} - Nota: {aluno['nota']} ({status})\n"
    resultado.config(text=texto, fg="blue")

def limpar_tela():
    entrada_nome.delete(0, tk.END)
    entrada_idade.delete(0, tk.END)
    entrada_nota.delete(0, tk.END)
    resultado.config(text="Aguardando ação...", fg="black")
    entrada_nome.focus()

# --- 3. INTERFACE GRÁFICA ---
carregar_alunos()

janela = tk.Tk()
janela.title("Sistema Escolar v1.0")
janela.geometry("400x500")

# Elementos da Tela
tk.Label(janela, text="Nome:").pack(pady=2)
entrada_nome = tk.Entry(janela)
entrada_nome.pack()

tk.Label(janela, text="Idade:").pack(pady=2)
entrada_idade = tk.Entry(janela)
entrada_idade.pack()

tk.Label(janela, text="Nota:").pack(pady=2)
entrada_nota = tk.Entry(janela)
entrada_nota.pack()

# Botões
tk.Button(janela, text="Cadastrar", command=cadastrar_aluno, bg="green", fg="white").pack(pady=5)
tk.Button(janela, text="Listar Alunos", command=listar_alunos, bg="blue", fg="white").pack(pady=5)
tk.Button(janela, text="Limpar", command=limpar_tela).pack(pady=5)

# Painel de Resultado
resultado = tk.Label(janela, text="Aguardando ação...", justify="left")
resultado.pack(pady=20)

janela.mainloop() 