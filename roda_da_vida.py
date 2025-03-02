import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

# Funções para carregar e salvar dados
def carregar_dados():
    dados = {}
    try:
        with open('dados_roda_vida.txt', 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                area, valor = linha.strip().split(': ')
                dados[area] = int(valor)
    except FileNotFoundError:
        dados = {
            "Recursos financeiros": 0,
            "Equilíbrio emocional": 0,
            "Saúde e disposição": 0,
            "Desenvolvimento intelectual": 0,
            "Família": 0,
            "Relacionamento amoroso": 0,
            "Vida social": 0,
            "Espiritualidade": 0,
            "Plenitude e felicidade": 0,
            "Hobbies e Diversão": 0,
            "Realização e propósito": 0,
            "Contribuição social": 0,
        }
    return dados

def salvar_dados(dados):
    with open('dados_roda_vida.txt', 'w', encoding='utf-8') as arquivo:
        for area, valor in dados.items():
            arquivo.write(f"{area}: {valor}\n")

def criar_grafico():
    habilidades = list(dados.keys())
    pontuacoes = list(dados.values())

    num_habilidades = len(habilidades)
    angles = np.linspace(0, 2 * np.pi, num_habilidades, endpoint=False).tolist()
    angles += angles[:1]
    pontuacoes += pontuacoes[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    ax.set_facecolor('#2e2e2e')
    ax.fill(angles, pontuacoes, color='gray', alpha=0.4)
    ax.plot(angles, pontuacoes, color='#39FF14', linewidth=2)
    ax.scatter(angles, pontuacoes, color='#39FF14', s=50, zorder=10)

    rotacoes_personalizadas = [
        270, 300, 330, 360, 30, 60, 90, 120, 150, 180, 210, 240
    ]

    for angle, label, rotation in zip(angles[:-1], habilidades, rotacoes_personalizadas):
        alignment = 'left' if 270 <= rotation <= 90 else 'right'
        ax.text(
            angle, 105, label,
            ha="center", va='center', fontsize=10,
            rotation=rotation,
            rotation_mode="anchor", color='#2e2e2e'
        )

    ax.set_yticklabels([])
    for y_tick, label in zip([15, 35, 54, 74, 90], ["20%", "40%", "60%", "80%", "100%"]):
        ax.text(0, y_tick, label, ha='center', va='center', fontsize=9, rotation=0, rotation_mode='anchor', color='white')

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])
    plt.title("Roda da Vida", size=16, color="#2e2e2e", y=1.1)
    ax.set_ylim(0, 100)
    ax.spines['polar'].set_visible(False)
    plt.tight_layout()
    return fig

def atualizar_grafico(canvas, frame_grafico):
    for widget in frame_grafico.winfo_children():
        widget.destroy()
    fig = criar_grafico()
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()
    return canvas

def incrementar(area, canvas, frame_grafico):
    if dados[area] < 100:
        dados[area] += 1
        atualizar_interface(canvas, frame_grafico)

def decrementar(area, canvas, frame_grafico):
    if dados[area] > 0:
        dados[area] -= 1
        atualizar_interface(canvas, frame_grafico)

def atualizar_interface(canvas, frame_grafico):
    for area, label in labels.items():
        label.config(text=f"{area}: {dados[area]}")
    atualizar_grafico(canvas, frame_grafico)

def salvar_e_atualizar(canvas, frame_grafico):
    salvar_dados(dados)
    messagebox.showinfo("Salvo", "Os dados foram salvos com sucesso!")
    atualizar_grafico(canvas, frame_grafico)

# Dados iniciais
dados = carregar_dados()

# Criar janela principal
janela = tk.Tk()
janela.title("Roda da Vida - Ajuste de Pontuações")
janela.geometry("1800x1000")

# Criar frame para os botões e labels
frame_controles = tk.Frame(janela)
frame_controles.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

labels = {}
for area in dados:
    container = tk.Frame(frame_controles)
    container.pack(pady=5, anchor='w')

    label = tk.Label(container, text=f"{area}: {dados[area]}", width=30, anchor='w')
    label.pack(side=tk.LEFT)
    labels[area] = label

    btn_incrementar = tk.Button(container, text="+1", command=lambda a=area: incrementar(a, canvas, frame_grafico))
    btn_incrementar.pack(side=tk.LEFT, padx=5)

    btn_decrementar = tk.Button(container, text="-1", command=lambda a=area: decrementar(a, canvas, frame_grafico))
    btn_decrementar.pack(side=tk.LEFT)

# Botão para salvar
btn_salvar = tk.Button(frame_controles, text="Salvar Dados", command=lambda: salvar_e_atualizar(canvas, frame_grafico))
btn_salvar.pack(pady=20)

# Criar área para o gráfico
frame_grafico = tk.Frame(janela)
frame_grafico.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

fig = criar_grafico()
canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

janela.mainloop()
