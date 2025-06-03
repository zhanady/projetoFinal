import sqlite3
import tkinter as tk
from tkinter import ttk


def visualizar_tabela_sqlite(nome_banco, nome_tabela):
    # Função interna para mostrar a tabela
    def mostrar_tabela():
        try:
            conn = sqlite3.connect(nome_banco)
            cursor = conn.cursor()

            # Obter informações das colunas
            cursor.execute(f"PRAGMA table_info({nome_tabela})")
            colunas_info = cursor.fetchall()

            if not colunas_info:
                print(f"Tabela '{nome_tabela}' não encontrada no banco '{nome_banco}'.")
                conn.close()
                return

            colunas = [coluna[1] for coluna in colunas_info]

            # Configurar Treeview dinamicamente
            tree["columns"] = colunas
            tree["show"] = "headings"

            for coluna in colunas:
                tree.heading(coluna, text=coluna)
                tree.column(coluna, width=100)

            # Buscar dados da tabela
            cursor.execute(f"SELECT * FROM {nome_tabela}")
            dados = cursor.fetchall()

            # Limpar dados antigos
            for item in tree.get_children():
                tree.delete(item)

            # Inserir dados na Treeview
            for linha in dados:
                tree.insert("", tk.END, values=linha)

            conn.close()

        except sqlite3.Error as e:
            print("Erro ao acessar o banco:", e)

    # Criar janela
    janela = tk.Tk()
    janela.title(f"Tabela: {nome_tabela} | Banco: {nome_banco}")
    janela.geometry("700x400")

    # Criar Treeview
    tree = ttk.Treeview(janela)
    tree.pack(expand=True, fill="both")

    # Botão para atualizar os dados
    botao_atualizar = tk.Button(janela, text="Atualizar Tabela", command=mostrar_tabela)
    botao_atualizar.pack(pady=10)

    # Mostrar dados inicialmente
    mostrar_tabela()

    janela.mainloop()
