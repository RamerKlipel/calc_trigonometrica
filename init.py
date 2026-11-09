import math
import tkinter as tk
from tkinter import messagebox


def calcular():
  try:
    # Pega o valor inserido no campo de texto
    angulo_graus = float(entry_angulo.get())

    # O módulo math do Python trabalha com radianos
    radianos = math.radians(angulo_graus)

    seno = math.sin(radianos)
    cosseno = math.cos(radianos)

    # Tratamento para ângulos onde a tangente tende ao infinito (ex: 90°, 270°)
    try:
      tangente = math.tan(radianos)
      tangente_str = f"{tangente:.4f}"
    except ValueError:
      tangente_str = "Indefinida (Tendência ao Infinito)"

    # Atualiza o texto do resultado na tela
    resultado_texto = (
        f"Seno: {seno:.4f}\n"
        f"Cosseno: {cosseno:.4f}\n"
        f"Tangente: {tangente_str}"
    )
    lbl_resultado.config(text=resultado_texto)

  except ValueError:
    messagebox.showerror(
        "Erro de Entrada", "Por favor, digite um número válido."
    )


# Configuração da janela principal
root = tk.Tk()
root.title("Calculadora Trigonométrica")
root.geometry("320x280")
root.resizable(False, False)

# Componentes da interface
lbl_instrucao = tk.Label(root, text="Digite o ângulo (em graus):", font=("Arial", 11))
lbl_instrucao.pack(pady=15)

entry_angulo = tk.Entry(root, font=("Arial", 14), justify="center")
entry_angulo.pack(pady=5)
entry_angulo.focus()

btn_calcular = tk.Button(
    root, text="Calcular", command=calcular, font=("Arial", 11, "bold")
)
btn_calcular.pack(pady=15)

lbl_resultado = tk.Label(
    root, text="Aguardando dados...", font=("Arial", 11), justify="left"
)
lbl_resultado.pack(pady=10)

# Inicia o loop da interface gráfica
root.mainloop()
