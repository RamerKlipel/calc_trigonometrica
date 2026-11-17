
import tkinter as tk
from tkinter import messagebox

TOLERANCIA = 0.01
PI = 3.141592653589793
INFINITO = float("inf")

def eh_finito(x):
    return x == x and abs(x) != INFINITO

def raiz(x):
    return x ** 0.5

def em_radianos(graus):
    return graus * PI / 180

def em_graus(rad):
    return rad * 180 / PI

def sen(x):
    termo = soma = x
    n = 1
    while abs(termo) > 1e-16:
        termo *= -x * x / ((2 * n) * (2 * n + 1))
        soma += termo
        n += 1
    return soma

def cos(x):
    termo = soma = 1.0
    n = 1
    while abs(termo) > 1e-16:
        termo *= -x * x / ((2 * n - 1) * (2 * n))
        soma += termo
        n += 1
    return soma

def arctan(x):
    inverter = x > 1
    if inverter:
        x = 1 / x
    for _ in range(2):
        x = x / (1 + raiz(1 + x * x))
    soma = potencia = x
    n = 1
    while abs(potencia) > 1e-17:
        potencia *= -x * x
        n += 2
        soma += potencia / n
    resultado = 4 * soma
    return PI / 2 - resultado if inverter else resultado

def arcsen(x):
    return arctan(x / raiz(1 - x * x))

def arccos(x):
    return PI / 2 - arcsen(x)

class AppTrigonometriaCompleta:
    RAZAO_PARA_ANGULO = {
        "seno": lambda x: arcsen(x),
        "cosseno": lambda x: arccos(x),
        "tangente": lambda x: arctan(x),
        "cossecante": lambda x: arcsen(1 / x),
        "secante": lambda x: arccos(1 / x),
        "cotangente": lambda x: arctan(1 / x),
    }
    LADOS = ("oposto", "adjacente", "hipotenusa")

    def __init__(self, root):
        self.root = root;
        self.root.title("Calculadora Trigonométrica");
        self.root.geometry("800x600");
        self.root.resizable(False, False);

        tk.Label( root, text="Preencha os dados que você possui:", font=("Arial", 12, "bold")).pack(pady=15);

        frame_principal = tk.Frame(root);
        frame_principal.pack(pady=5, padx=20, fill="x");

        coluna_Esquerda = tk.Frame(frame_principal);
        coluna_Esquerda.pack(side="left", fill="both", expand=True, padx=10);

        coluna_Direita = tk.Frame(frame_principal);
        coluna_Direita.pack(side="right", fill="both", expand=True, padx=10);

        self.entries = {};

        campos_esquerda = [
            ("angulo", "Ângulo (°):"),
            ("oposto", "Cateto Oposto:"),
            ("adjacente", "Cateto Adjacente:"),
            ("hipotenusa", "Hipotenusa:"),
            ("seno", "Seno (sin):"),
        ]

        campos_direita = [
            ("cosseno", "Cosseno (cos):"),
            ("tangente", "Tangente (tan):"),
            ("cossecante", "Cossecante (csc):"),
            ("secante", "Secante (sec):"),
            ("cotangente", "Cotangente (cot):"),
        ]

        def criar_campos(parent, campos):
            for chave, texto in campos:
                f = tk.Frame(parent);
                f.pack(fill="x", pady=4);
                tk.Label(f, text=texto, width=16, anchor="w", font=("Arial", 10)).pack(side="left");
                e = tk.Entry(f, width=15, font=("Arial", 10));
                e.pack(side="right");
                self.entries[chave] = e;

        criar_campos(coluna_Esquerda, campos_esquerda);
        criar_campos(coluna_Direita, campos_direita);

        tk.Button(root, text="Calcular Restantes", command=self.executar_calculo, font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=20);

        tk.Label(root, text="Resultados Calculados:", font=("Arial", 11, "bold")).pack(anchor="w", padx=40);

        self.lbl_resultado = tk.Label(root, text="Aguardando dados...", font=("Courier", 10), justify="left", anchor="nw", relief="sunken", bg="#f9f9f9", width=85, height=8);
        self.lbl_resultado.pack(pady=5, padx=40);

    def mdc(self, a, b):
        while b:
            a, b = b, a % b;
        return a

    def radConvert(self, degrees):
        d = self.mdc(degrees, 180);
        return degrees // d, 180 // d;

    def simplifyFraction(self, num, den):
        d = self.mdc(num, den);
        return num // d, den // d;

    def formatarRadiano(self, graus):
        if abs(graus - round(graus)) < 1e-9:
            num, den = self.radConvert(round(graus))
            if den == 1:
                return "π" if num == 1 else f"{num}π"
            if num == 1:
                return f"π/{den}"
            return f"{num}π/{den}"
        return f"{em_radianos(graus):.6f}"

    def verifyIntegrity(self, filled):
        if not filled:
            raise ValueError("Preencha pelo menos um campo.")

        for chave, valor in filled.items():
            if not eh_finito(valor):
                raise ValueError(f"'{chave}' precisa ser um número válido.")

            if chave == "angulo":
                if not (0 < valor <= 90):
                    raise ValueError("O ângulo agudo deve estar entre 0 e 90 graus (exclusivo).")
            elif chave in self.LADOS or chave in ("tangente", "cotangente"):
                if valor <= 0:
                    raise ValueError(f"'{chave}' deve ser maior que zero.")
            elif chave in ("seno", "cosseno"):
                if not (0 < valor < 1):
                    raise ValueError(f"'{chave}' deve estar entre 0 e 1 (exclusivo).")
            elif chave in ("cossecante", "secante"):
                if valor <= 1:
                    raise ValueError(f"'{chave}' deve ser maior que 1.")

        hip = filled.get("hipotenusa")
        if hip is not None:
            for cateto in ("oposto", "adjacente"):
                if cateto in filled and filled[cateto] >= hip:
                    raise ValueError("A hipotenusa deve ser maior que os catetos.")

    def anguloInformado(self, filled):
        """Ângulo em graus: o digitado ou, se não houver, deduzido de uma razão (seno, cosseno...)."""
        if "angulo" in filled:
            return filled["angulo"]
        for chave, func in self.RAZAO_PARA_ANGULO.items():
            if chave in filled:
                return em_graus(func(filled[chave]))
        return None

    def resolver(self, filled):
        """Recebe os dados válidos e devolve {campo: texto} com o que foi calculado."""
        angulo = self.anguloInformado(filled)
        op, adj, hip = (filled.get(l) for l in self.LADOS)
        qtd_lados = sum(x is not None for x in (op, adj, hip))

        if angulo is None and qtd_lados < 2:
            raise ValueError("Informe mais um dado: outro lado ou um ângulo agudo.")

        so_angulo = qtd_lados == 0

        if qtd_lados >= 2:
            if hip is None:
                hip = raiz(op ** 2 + adj ** 2)
            elif op is None:
                op = raiz(hip ** 2 - adj ** 2)
            elif adj is None:
                adj = raiz(hip ** 2 - op ** 2)
            elif abs(raiz(op ** 2 + adj ** 2) - hip) > TOLERANCIA * hip:
                raise ValueError("Dados inconsistentes: os lados não obedecem ao teorema de Pitágoras.")
            ang = em_graus(arctan(op / adj))
        else:
            rad = em_radianos(angulo)
            if hip is None:
                if so_angulo:
                    hip = 1.0
                elif op is not None:
                    hip = op / sen(rad)
                else:
                    hip = adj / cos(rad)
            op = hip * sen(rad)
            adj = hip * cos(rad)
            ang = angulo

        completos = {
            "angulo": ang,
            "oposto": op,
            "adjacente": adj,
            "hipotenusa": hip,
            "seno": op / hip,
            "cosseno": adj / hip,
            "tangente": op / adj,
            "cossecante": hip / op,
            "secante": hip / adj,
            "cotangente": adj / op,
        }

        for chave, valor in filled.items():
            esperado = completos[chave]
            if abs(valor - esperado) > TOLERANCIA * abs(esperado):
                raise ValueError(
                    f"Dados inconsistentes: '{chave}' informado ({valor:g}) "
                    f"não bate com o valor calculado ({esperado:.4f})."
                )

        if so_angulo:
            resultado = {}
            if "angulo" not in filled:
                resultado["angulo"] = f"{ang:.4f}°"
            resultado["radiano"] = self.formatarRadiano(ang)
            return resultado

        resultado = {k: f"{v:.4f}" for k, v in completos.items() if k not in filled}
        if "angulo" in resultado:
            resultado["angulo"] += "°"
        resultado["outro angulo"] = f"{90 - ang:.4f}°"
        resultado["radiano"] = self.formatarRadiano(ang)
        return resultado

    def emColunas(self, itens, largura=38):
        return "\n".join(
            "  ".join(item.ljust(largura) for item in itens[i:i + 2]).rstrip()
            for i in range(0, len(itens), 2)
        )

    def formatarSaida(self, filled, empties):
        informados = [f"{k}: {v:g}" for k, v in filled.items()]
        calculados = [f"{k}: {v}" for k, v in empties.items()]
        return (
            f"Dados informados ({len(informados)}):\n{self.emColunas(informados)}\n\n"
            f"Dados calculados ({len(calculados)}):\n{self.emColunas(calculados)}"
        )

    def executar_calculo(self):
        try:
            filled = {}
            for chave, entry in self.entries.items():
                texto = entry.get().strip().replace(",", ".")
                if texto:
                    try:
                        filled[chave] = float(texto)
                    except ValueError:
                        raise ValueError(f"'{chave}' precisa ser um número válido.")

            self.verifyIntegrity(filled)
            empties = self.resolver(filled)
            self.lbl_resultado.config(text=self.formatarSaida(filled, empties))

        except ValueError as e:
            messagebox.showerror("Erro de Entrada", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = AppTrigonometriaCompleta(root)
    root.mainloop()
