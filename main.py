import tkinter as tk
from tkinter import messagebox
import customtkinter
from customtkinter import CTkLabel, CTkEntry, CTkButton, CTkFrame
import matplotlib.pyplot as plt
import json
import requests

couchdb_url = 'http://127.0.0.1:5984/'
url_banco = f'{couchdb_url}/gerenciador_despesas_db/'

username = 'edsdlc'
password = 'edsonabc12312'

class Despesa:
    def __init__(self, descricao, valor):
        self.descricao = descricao
        self.valor = valor

class ListaDespesas:
    def __init__(self):
        self.despesas = []
        self.observadores = []

    def adicionar_despesa(self, despesa):
        self.despesas.append(despesa)
        self.notificar_observadores()

    def registrar_observador(self, observador):
        self.observadores.append(observador)

    def notificar_observadores(self):
        for observador in self.observadores:
            observador.atualizar(self.despesas)

class ObservadorDespesas:
    def __init__(self, lista_despesas, root):
        self.lista_despesas = lista_despesas
        self.root = root

        self.exibicao_despesas_var = tk.StringVar()  # Crie uma nova variável de controle
        self.exibicao_despesas_var.set("")  # Inicialize a variável com uma string vazia

        self.exibicao_despesas = tk.Label(root, textvariable=self.exibicao_despesas_var, wraplength=300, justify="left")
        self.exibicao_despesas.pack()

    def atualizar(self, despesas):
        despesas_text = "\n".join([f"{despesa.descricao}: R$ {despesa.valor:.2f}" for despesa in despesas])
        self.exibicao_despesas_var.set(despesas_text)  # Atualize o valor da variável de controle

    def excluir_despesa(self, despesa):
        self.lista_despesas.despesas.remove(despesa)
        self.lista_despesas.notificar_observadores()

class GraficoStrategy:
    def gerar_grafico(self, categorias, valores):
        pass

class GraficoBarrasStrategy(GraficoStrategy):
    def gerar_grafico(self, categorias, valores):
        plt.bar(categorias, valores, color='blue')
        plt.xlabel('Categorias')
        plt.ylabel('Valor')
        plt.title('Gráfico de Barras')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

class GraficoSetoresStrategy(GraficoStrategy):
    def gerar_grafico(self, categorias, valores):
        plt.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Gráfico de Setores')
        plt.show()

class InterfaceGrafica:
    def __init__(self, root, lista_despesas):
        self.root = root
        self.lista_despesas = lista_despesas
        self.grafico_strategy = GraficoStrategy()

        self.root.title("Gestão de Despesas Residencial")
        self.root.geometry('250x505')
        self.root.resizable()

        # Define o fundo preto para a janela
        root.configure(bg="grey")

        self.frame_opcoes = customtkinter.CTkFrame(root)
        self.frame_opcoes.pack(pady=120)

        self.botao_adicionar_despesa = customtkinter.CTkButton(self.frame_opcoes, text="Adicionar Despesa", font=("Comics Sans MS", 15, "bold"), command=self.janela_adicionar_despesa, width=100, height=30)
        self.botao_adicionar_despesa.grid(padx=10, pady=12)

        self.botao_adicionar_salario = customtkinter.CTkButton(self.frame_opcoes, text="Adicionar Salário", font=("Comics Sans MS", 15, "bold"), command=self.janela_adicionar_salario, width=100, height=30)
        self.botao_adicionar_salario.grid(padx=10, pady=12)
        
        self.botao_ver_saldo = customtkinter.CTkButton(self.frame_opcoes, text="Ver Saldo", font=("Comics Sans MS", 15, "bold"), command=self.janela_gerar_saldo, width=100, height=30)
        self.botao_ver_saldo.grid(padx=10, pady=12)

        self.botao_gerar_grafico_barras = customtkinter.CTkButton(self.frame_opcoes, text="Gráfico de Barras", font=("Comics Sans MS", 15, "bold"), command=self.gerar_grafico_barras, width=100, height=30)
        self.botao_gerar_grafico_barras.grid(padx=10, pady=12)

        self.botao_gerar_grafico_setores = customtkinter.CTkButton(self.frame_opcoes, text="Gráfico de Setores", font=("Comics Sans MS", 15, "bold"), command=self.gerar_grafico_setores, width=100, height=30)
        self.botao_gerar_grafico_setores.grid(padx=10, pady=12)

        self.exibicao_despesas_var = tk.StringVar()
        self.exibicao_despesas_var.set("")

        self.frame_exibicao_despesas = tk.Frame(root)
        self.frame_exibicao_despesas.pack()

        self.exibicao_despesas = tk.Label(self.frame_exibicao_despesas, textvariable=self.exibicao_despesas_var, justify="left")
        self.exibicao_despesas.pack()

    def gerar_grafico_barras(self):
        if hasattr(self, 'salario') and self.lista_despesas.despesas:
            categorias = [despesa.descricao for despesa in self.lista_despesas.despesas]
            valores = [despesa.valor for despesa in self.lista_despesas.despesas]

            plt.bar(categorias, valores, color='blue')
            plt.xlabel('Categorias')
            plt.ylabel('Valor')
            plt.title('Gráfico de Barras')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showerror("Erro", "Por favor, adicione seu salário e despesas antes de gerar gráficos.")

    def gerar_grafico_setores(self):
        if hasattr(self, 'salario') and self.lista_despesas.despesas:
            categorias = [despesa.descricao for despesa in self.lista_despesas.despesas]
            valores = [despesa.valor for despesa in self.lista_despesas.despesas]

            plt.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')
            plt.title('Gráfico de Setores')
            plt.show()
        else:
            messagebox.showerror("Erro", "Por favor, adicione seu salário e despesas antes de gerar gráficos.")


    def usar_grafico_barras(self):
        self.grafico_strategy = GraficoBarrasStrategy()

    def usar_grafico_setores(self):
        self.grafico_strategy = GraficoSetoresStrategy()

    def janela_gerar_graficos(self):
            if hasattr(self, 'salario') and self.lista_despesas.despesas:
                categorias = [despesa.descricao for despesa in self.lista_despesas.despesas]
                valores = [despesa.valor for despesa in self.lista_despesas.despesas]

                self.grafico_strategy.gerar_grafico(categorias, valores)
            else:
                messagebox.showerror("Erro", "Por favor, adicione seu salário e despesas antes de gerar gráficos.")

    def janela_adicionar_despesa(self):
        janela_adicionar_despesa = tk.Toplevel(self.root)
        janela_adicionar_despesa.title("Adicionar Despesa")

        label_descricao = tk.Label(janela_adicionar_despesa, text="Descrição:")
        label_descricao.pack(pady=10)

        entrada_descricao = customtkinter.CTkEntry(janela_adicionar_despesa)
        entrada_descricao.pack()

        label_valor = tk.Label(janela_adicionar_despesa, text="Valor:")
        label_valor.pack(pady=10)

        entrada_valor = customtkinter.CTkEntry(janela_adicionar_despesa)
        entrada_valor.pack()

        botao_adicionar = customtkinter.CTkButton(janela_adicionar_despesa, text="Adicionar Despesa", font=("Comics Sans MS", 10, "bold"), command=lambda: self.adicionar_despesa(entrada_descricao.get(), entrada_valor.get(), janela_adicionar_despesa))
        botao_adicionar.pack(pady=20)
    
    def adicionar_despesa(self, descricao, valor, janela):
        if descricao and valor:
            despesa = Despesa(descricao, float(valor))
            self.lista_despesas.adicionar_despesa(despesa)
            self.adicionar_despesa_no_couchdb(descricao, valor)
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos.")

    def adicionar_despesa_no_couchdb(self, descricao, valor):
        despesa = {
            'descricao': descricao,
            'valor': valor
        }

        # Envie a despesa para o CouchDB
        response = requests.post(url_banco, auth = (username, password), json=despesa)

        # Verifique se a operação foi bem-sucedida
        if response.status_code == 201:
            print("Despesa adicionada com sucesso ao CouchDB.")
        else:
            print("Erro ao adicionar despesa ao CouchDB.")


    def janela_adicionar_salario(self):
        janela_adicionar_salario = tk.Toplevel(self.root)
        janela_adicionar_salario.title("Adicionar Salário")

        label_salario = tk.Label(janela_adicionar_salario, text="Salário Mensal:")
        label_salario.pack(pady=10)

        entrada_salario = customtkinter.CTkEntry(janela_adicionar_salario)
        entrada_salario.pack()

        botao_adicionar = customtkinter.CTkButton(janela_adicionar_salario, text="Adicionar Salário", font=("Comics Sans MS", 10, "bold"), command=lambda: self.adicionar_salario(entrada_salario.get(), janela_adicionar_salario))
        botao_adicionar.pack(pady=20)

    def adicionar_salario(self, salario, janela):
        try:
            salario = float(salario)
            self.salario = salario
            self.botao_adicionar_salario.configure(state=tk.DISABLED)
            janela.destroy()
            messagebox.showinfo("Salário Adicionado", f"Salário mensal de R$ {salario:.2f} adicionado com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido para o salário.")

    def calcular_soma_despesas(self):
        soma_despesas = sum(despesa.valor for despesa in self.lista_despesas.despesas)
        return soma_despesas

    def janela_gerar_graficos(self):
        # janela_gerar_graficos = tk.Toplevel(self.root)
        # janela_gerar_graficos.title("Gráfico de Despesas")

        if hasattr(self, 'salario') and self.lista_despesas.despesas:

            categorias = [despesa.descricao for despesa in self.lista_despesas.despesas]
            valores = [despesa.valor for despesa in self.lista_despesas.despesas]

            plt.figure(figsize=(8, 6))
            plt.bar(categorias, valores, color='blue')
            plt.xlabel('Categorias de Despesas')
            plt.ylabel('Valor (R$)')
            plt.title('Despesas em Relação ao Salário')
            plt.xticks(rotation=45)
            plt.tight_layout()

            plt.show()
        else:
            messagebox.showerror("Erro", "Por favor, adicione seu salário e despesas antes de gerar gráficos.")

    def janela_gerar_saldo(self):
        # janela_gerar_saldo = tk.Toplevel(self.root)
        # janela_gerar_saldo.title("Saldo")

        if hasattr(self, 'salario') and self.lista_despesas.despesas:
            soma_despesas = self.calcular_soma_despesas()
            diferenca = self.salario - soma_despesas

            if diferenca >= 0:
                cor_texto = 'green'
            else:
                cor_texto = 'red'

            messagebox.showinfo("Resumo de Gastos", f"Saldo: R$ {diferenca:.2f}")

            # Atualize a cor do texto
            self.exibicao_despesas.config(text="", fg=cor_texto)
        

if __name__ == "__main__":
    root = tk.Tk()
    lista_despesas = ListaDespesas()
    app = InterfaceGrafica(root, lista_despesas)

    observador_despesas = ObservadorDespesas(lista_despesas, root)
    lista_despesas.registrar_observador(observador_despesas)

    root.mainloop()