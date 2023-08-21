import unittest
from tkinter import Tk
from unittest.mock import patch, Mock
from customtkinter import CTkButton

# Importe a classe que você deseja testar
from main import InterfaceGrafica, ListaDespesas, Despesa

class TestInterfaceGrafica(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.lista_despesas = ListaDespesas()
        self.app = InterfaceGrafica(self.root, self.lista_despesas)

    def tearDown(self):
        # Destrua a janela após cada teste
        self.root.destroy()

    def test_adicionar_despesa(self):

        mock_toplevel = Mock()

        # Simule a interação com a interface gráfica para adicionar uma despesa
        self.app.adicionar_despesa("Comida", 50.0, mock_toplevel)

        # Verifique se a despesa foi adicionada corretamente à lista de despesas
        self.assertEqual(len(self.lista_despesas.despesas), 1)
        self.assertEqual(self.lista_despesas.despesas[0].descricao, "Comida")
        self.assertEqual(self.lista_despesas.despesas[0].valor, 50.0)

    def test_adicionar_salario(self):

        mock_toplevel = Mock()

        # Teste se a função adicionar_salario atribui corretamente o valor do salário
        self.app.adicionar_salario("1000.0", mock_toplevel)
        self.assertEqual(self.app.salario, 1000.0)

    def test_calcular_soma_despesas(self):
        # Teste se a função calcular_soma_despesas calcula a soma correta das despesas
        self.lista_despesas.despesas = [Despesa("Comida", 50.0), Despesa("Transporte", 30.0)]
        soma = self.app.calcular_soma_despesas()
        self.assertEqual(soma, 80.0)

    def test_janela_gerar_saldo(self):
        # Teste se a função janela_gerar_saldo exibe a mensagem correta
        self.app.salario = 1000.0
        self.lista_despesas.despesas = [Despesa("Comida", 50.0), Despesa("Transporte", 30.0)]
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.janela_gerar_saldo()
            mock_showinfo.assert_called_with("Resumo de Gastos", "Saldo: R$ 920.00")

# Crie uma classe mock para a ListaDespesas
class MockListaDespesas:
    def __init__(self):
        self.despesas = []

if __name__ == '__main__':
    unittest.main()
