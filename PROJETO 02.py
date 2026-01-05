aluno = {
"nome":input("digite o nome do aluno:"),
"idade": int(input("digite a idade:")),
"nota":float(input("digite a nota:"))
}
print("n/DADOS DO ALUNO")
for chave, valor in aluno.items():
    print(f"{chave}: {valor}")
if aluno ["nota"] >= 7:
    print ("status: aprovado")
else:
    print ( "status:reprovado")


    import tkinter as tk

janela = tk.Tk()
janela.title("Cadastro de Alunos")
janela.geometry("400x400")

janela.mainloop()

tk.Label(janela, text="Nome").pack()
entrada_nome = tk.Entry(janela)
entrada_nome.pack()

tk.Label(janela, text="Idade").pack()
entrada_idade = tk.Entry(janela)
entrada_idade.pack()

tk.Label(janela, text="Nota").pack()
entrada_nota = tk.Entry(janela)
entrada_nota.pack()

alunos = []
def cadastrar_aluno():
    aluno = {
        "nome": entrada_nome.get(),
        "idade": int(entrada_idade.get()),
        "nota": float(entrada_nota.get())
    }

    alunos.append(aluno)

    resultado.config(text="Aluno cadastrado com sucesso!")

    entrada_nome.delete(0, tk.END)
    entrada_idade.delete(0, tk.END)
    entrada_nota.delete(0, tk.END)

def listar_alunos():
    texto = ""

    for aluno in alunos:
        texto += f"{aluno['nome']} - Nota: {aluno['nota']}\n"

    resultado.config(text=texto)

tk.Button(janela, text="Cadastrar", command=cadastrar_aluno).pack(pady=5)
tk.Button(janela, text="Listar Alunos", command=listar_alunos).pack(pady=5)

resultado = tk.Label(janela, text="", fg="blue")
resultado.pack(pady=10)
janela.mainloop()

