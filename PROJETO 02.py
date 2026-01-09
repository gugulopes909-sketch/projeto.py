import tkinter as tk
from tkinter import messagebox
import csv
import os

# --- 1. CONFIGURAÇÕES E DADOS ---
ARQUIVO = "alunos.csv"
alunos = []

def carregar_alunos():
    global alunos
    alunos = []
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
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
        nome = entrada_nome.get().strip()
        if not nome:
            messagebox.showwarning("Atenção", "O campo 'Nome' não pode estar vazio!")
            return

        for aluno in alunos:
            if aluno["nome"].lower() == nome.lower():
                messagebox.showwarning("Erro", f"O aluno '{nome}' já está cadastrado!")
                return

        idade = int(entrada_idade.get())
        nota = float(entrada_nota.get())
        
        if nota < 0 or nota > 10:
            messagebox.showwarning("Nota Inválida", "A nota deve ser entre 0 e 10!")
            return

        alunos.append({"nome": nome, "idade": idade, "nota": nota})
        salvar_alunos()
        messagebox.showinfo("Sucesso", f"Aluno {nome} cadastrado!")
        limpar_tela()
        listar_alunos()
    except ValueError:
        messagebox.showerror("Erro", "Idade e Nota precisam ser números!")

def remover_aluno():
    nome_busca = entrada_nome.get().strip().lower()
    if not nome_busca:
        messagebox.showwarning("Atenção", "Digite o nome do aluno para remover!")
        return

    for i, aluno in enumerate(alunos):
        if aluno["nome"].lower() == nome_busca:
            alunos.pop(i)
            salvar_alunos()
            listar_alunos()
            messagebox.showinfo("Sucesso", "Aluno removido!")
            limpar_tela()
            return
    messagebox.showwarning("Erro", "Aluno não encontrado!")

def editar_nota():
    nome_busca = entrada_nome.get().strip().lower()
    try:
        nova_nota = float(entrada_nota.get())
        if nova_nota < 0 or nova_nota > 10:
            messagebox.showwarning("Nota Inválida", "A nota deve ser entre 0 e 10!")
            return

        for aluno in alunos:
            if aluno["nome"].lower() == nome_busca:
                aluno["nota"] = nova_nota
                salvar_alunos()
                listar_alunos()
                messagebox.showinfo("Sucesso", "Nota atualizada!")
                return
        messagebox.showwarning("Erro", "Aluno não encontrado!")
    except ValueError:
        messagebox.showerror("Erro", "Digite uma nota válida para editar!")

def mostrar_estatisticas():
    if not alunos:
        messagebox.showwarning("Atenção", "Não há alunos cadastrados!")
        return
    notas = [aluno["nota"] for aluno in alunos]
    media = sum(notas) / len(notas)
    melhor_aluno = max(alunos, key=lambda x: x["nota"])
    
    mensagem = f"Média Geral: {media:.2f}\nMelhor Aluno: {melhor_aluno['nome']} ({melhor_aluno['nota']})"
    messagebox.showinfo("Estatísticas", mensagem)

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
janela = tk.Tk()
janela.title("Sistema Escolar Pro")
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

# Container para botões (Organização em Grade)
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

# Botões organizados (Linha, Coluna)
tk.Button(frame_botoes, text="Cadastrar", command=cadastrar_aluno, bg="green", fg="white", width=15).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_botoes, text="Listar", command=listar_alunos, bg="blue", fg="white", width=15).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_botoes, text="Editar Nota", command=editar_nota, bg="orange", width=15).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_botoes, text="Estatísticas", command=mostrar_estatisticas, bg="purple", fg="white", width=15).grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame_botoes, text="Remover", command=remover_aluno, bg="red", fg="white", width=15).grid(row=2, column=0, padx=5, pady=5)
tk.Button(frame_botoes, text="Limpar", command=limpar_tela, width=15).grid(row=2, column=1, padx=5, pady=5)

resultado = tk.Label(janela, text="Aguardando ação...", justify="left", font=("Arial", 10))
resultado.pack(pady=20)

if __name__ == "__main__":
    carregar_alunos()
    janela.mainloop() 