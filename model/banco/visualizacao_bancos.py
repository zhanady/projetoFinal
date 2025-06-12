import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


def visualizador_sqlite():
    def carregar_tabelas(event=None):
        banco = entrada_banco.get()
        try:
            conn = sqlite3.connect(banco)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tabelas = [t[0] for t in cursor.fetchall()]
            combo_tabelas["values"] = tabelas
            if tabelas:
                combo_tabelas.current(0)
                mostrar_tabela()
            else:
                tree.delete(*tree.get_children())
                messagebox.showinfo("Info", "Nenhuma tabela encontrada no banco selecionado.")
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao acessar o banco:\n{e}")

    def mostrar_tabela(event=None):
        banco = entrada_banco.get()
        tabela = combo_tabelas.get()

        try:
            conn = sqlite3.connect(banco)
            cursor = conn.cursor()

            # Buscar colunas
            cursor.execute(f"PRAGMA table_info({tabela})")
            colunas_info = cursor.fetchall()
            colunas = [col[1] for col in colunas_info]

            tree["columns"] = colunas
            tree["show"] = "headings"

            for col in colunas:
                tree.heading(col, text=col)
                tree.column(col, width=120)

            # Buscar dados
            cursor.execute(f"SELECT * FROM {tabela}")
            dados = cursor.fetchall()

            # Limpar e inserir
            tree.delete(*tree.get_children())
            for linha in dados:
                tree.insert("", tk.END, values=linha)

            conn.close()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tabela:\n{e}")

    # Janela principal
    janela = tk.Tk()
    janela.title("Visualizador de Tabelas SQLite")
    janela.geometry("800x500")

    frame_topo = tk.Frame(janela)
    frame_topo.pack(pady=10)

    tk.Label(frame_topo, text="Banco de Dados:").grid(row=0, column=0)
    entrada_banco = ttk.Entry(frame_topo, width=40)
    entrada_banco.insert(0, "hospital.db")  # valor padrão
    entrada_banco.grid(row=0, column=1, padx=5)

    botao_buscar = ttk.Button(frame_topo, text="Carregar Tabelas", command=carregar_tabelas)
    botao_buscar.grid(row=0, column=2)

    tk.Label(frame_topo, text="Tabela:").grid(row=1, column=0, pady=10)
    combo_tabelas = ttk.Combobox(frame_topo, state="readonly", width=37)
    combo_tabelas.grid(row=1, column=1, padx=5)
    combo_tabelas.bind("<<ComboboxSelected>>", mostrar_tabela)

    tree = ttk.Treeview(janela)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    janela.mainloop()
