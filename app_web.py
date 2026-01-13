import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

# --- 1. FUNÇÕES DO BANCO DE DADOS (LÓGICA SQL) ---

def conectar():
    return sqlite3.connect("escola.db")

def criar_banco():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            nota REAL
        )
    """)
    conexao.commit()
    conexao.close()

def cadastrar_aluno_db(nome, idade, nota):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO alunos (nome, idade, nota) VALUES (?, ?, ?)", (nome, idade, nota))
    conexao.commit()
    conexao.close()

def listar_alunos_db():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM alunos")
    dados = cursor.fetchall()
    conexao.close()
    return dados

def excluir_aluno_db(nome_busca):
    conexao = conectar()
    cursor = conexao.cursor()
    # Busca primeiro para ver se existe
    cursor.execute("SELECT id FROM alunos WHERE nome LIKE ?", (f"%{nome_busca}%",))
    aluno = cursor.fetchone()
    
    if aluno:
        cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno[0],))
        conexao.commit()
        conexao.close()
        return True
    conexao.close()
    return False

# --- 2. FUNÇÕES DA INTERFACE (PONTE COM O BANCO) ---

def acao_cadastrar():
    try:
        nome = entrada_nome.get().strip()
        idade = int(entrada_idade.get())
        nota = float(entrada_nota.get())
        
        if not nome or nota < 0 or nota > 10:
            messagebox.showwarning("Atenção", "Dados inválidos!")
            return

        cadastrar_aluno_db(nome, idade, nota)
        messagebox.showinfo("Sucesso", f"Aluno {nome} cadastrado!")
        limpar_tela()
        acao_listar()
    except ValueError:
        messagebox.showerror("Erro", "Idade e Nota precisam ser números!")

def acao_listar():
    alunos = listar_alunos_db()
    texto = "--- LISTA DE ALUNOS (DB) ---\n"
    for a in alunos:
        status = "Aprovado" if a[3] >= 7 else "Reprovado"
        texto += f"ID: {a[0]} | {a[1]} - Nota: {a[3]} ({status})\n"
    resultado.config(text=texto, fg="blue")

def acao_remover():
    nome_busca = entrada_nome.get().strip()
    if not nome_busca:
        messagebox.showwarning("Atenção", "Digite o nome para remover!")
        return

    if excluir_aluno_db(nome_busca):
        messagebox.showinfo("Sucesso", "Aluno removido!")
        acao_listar()
        limpar_tela()
    else:
        messagebox.showwarning("Erro", "Aluno não encontrado!")

def limpar_tela():
    entrada_nome.delete(0, tk.END)
    entrada_idade.delete(0, tk.END)
    entrada_nota.delete(0, tk.END)
    entrada_nome.focus()

# --- 3. INTERFACE GRÁFICA ---

criar_banco() # Garante que o banco existe ao abrir
janela = tk.Tk()
janela.title("Sistema Escolar Pro - SQLite")
janela.geometry("450x600")

# Entradas
tk.Label(janela, text="Nome do Aluno:").pack(pady=2)
entrada_nome = tk.Entry(janela)
entrada_nome.pack()

tk.Label(janela, text="Idade:").pack(pady=2)
entrada_idade = tk.Entry(janela)
entrada_idade.pack()

tk.Label(janela, text="Nota:").pack(pady=2)
entrada_nota = tk.Entry(janela)
entrada_nota.pack()

# Botões
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

tk.Button(frame_botoes, text="Cadastrar", command=acao_cadastrar, bg="green", fg="white", width=15).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_botoes, text="Listar", command=acao_listar, bg="blue", fg="white", width=15).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_botoes, text="Remover por Nome", command=acao_remover, bg="red", fg="white", width=15).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_botoes, text="Limpar", command=limpar_tela, width=15).grid(row=1, column=1, padx=5, pady=5)

resultado = tk.Label(janela, text="Aguardando ação...", justify="left", font=("Arial", 10))
resultado.pack(pady=20)

janela.mainloop()










