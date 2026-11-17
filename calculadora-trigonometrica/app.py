import tkinter as tk
from tkinter import messagebox

class AppTrigonometriaCompleta:
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

        self.lbl_resultado = tk.Label(root, text="Aguardando dados...", font=("Courier", 10), justify="left", relief="sunken", bg="#f9f9f9", width=85, height=8);
        self.lbl_resultado.pack(pady=5, padx=40);

    def calcUnicData(self, filled):
        if "angulo" in filled:
            degree = filled["angulo"];
            num, den = self.radConvert(int(degree));
            print(num, den, sep=" | ");
            return "radiano", f"{num}π/{den}";

    def mdc(self, a, b):
        while b:
            a, b = b, a % b;
        return a

    def radConvert(self, degrees):
        d = self.mdc(degrees, 180);
        return degrees // d, 180 //d;

    def simplifyFraction(self, num, den):
        mdc = self.mdc(num, den);
        return num // mdc, den // mdc;

    def verifyIntegrity(self, filled):
        dictErr = {};
        for index, value in filled:
            match (index):
                case "angulo":
                    if value is not (0 < value < 90):
                        dictErr = {"err", "o ângulo agudo deve estar entre 0 e 90 graus."};

        if len(filled) < 2 and (filled["angulo"] if filled["angulo"] else None) is not None:
            dictErr["err"] += "\n Informe mais um dado: outro lado ou um ângulo agudo.";

    def executar_calculo(self):
        try:
            data = {};
            for chave, entry in self.entries.items():
                valor = entry.get().strip();
                data[chave] = float(valor) if valor else None;

            filled = {k: v for k, v in data.items() if v is not None};
            empties = {};
            awns = "";

            dictErrIntegrity = self.verifyIntegrity(filled);
            if (dictErrIntegrity['err'] is not None):
                raise ValueError(dictErrIntegrity['err']);

            match len(filled):
                case 1:
                    index, awns = self.calcUnicData(filled);
                    empties[index] = awns;

            self.lbl_resultado.config(
                text=f"Dados informados ({len(filled)}):\n"
                + ", ".join([f"{k}: {v}" for k, v in filled.items()])
                + "\n"
                + f"Dados Calculados({len(empties)}):\n"
                + ", ".join([f"{i}: {val}" for i, val in empties.items()])
            )

        except ValueError:
            messagebox.showerror("Erro de Entrada", "Por favor, digite apenas números válidos nos campos preenchidos.");


if __name__ == "__main__":
    root = tk.Tk();
    app = AppTrigonometriaCompleta(root);
    root.mainloop();
