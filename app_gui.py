import tkinter as tk
import requests

URL = "https://megometria-api.onrender.com/dados"

def atualizar():
    try:
        resposta = requests.get(URL, timeout=10)
        dados = resposta.json()

        lista.delete(0, tk.END)

        if not dados:
            lista.insert(tk.END, "Nenhum dado ainda...")
        else:
            for d in dados:
                texto = f"ID:{d[0]} | {d[1]} | {d[2]} MΩ | {d[3]}"
                lista.insert(tk.END, texto)

    except Exception as e:
        lista.delete(0, tk.END)
        lista.insert(tk.END, "Erro ao conectar:")
        lista.insert(tk.END, str(e))

    janela.after(3000, atualizar)

janela = tk.Tk()
janela.title("Megôhmetro Nuvem")

lista = tk.Listbox(janela, width=80, height=20)
lista.pack()

botao = tk.Button(janela, text="Atualizar", command=atualizar)
botao.pack()

atualizar()

janela.mainloop()