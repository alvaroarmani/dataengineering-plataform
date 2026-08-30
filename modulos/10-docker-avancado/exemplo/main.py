"""App de exemplo do M10 — imprime uma saudação e a versão do pandas."""
import pandas as pd

if __name__ == "__main__":
    df = pd.DataFrame({"n": [1, 2, 3]})
    print(f"Olá do container! soma = {int(df['n'].sum())} | pandas {pd.__version__}")
