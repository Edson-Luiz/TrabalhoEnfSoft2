import unittest
import tkinter as tk
from main import Despesa, ListaDespesas, ObservadorDespesas, InterfaceGrafica


class TestListaDespesas(unittest.TestCase):
    def test_adicionar_despesa(self):
        lista_despesas = ListaDespesas()
        despesa = Despesa("Despesa de Teste", 50)
        lista_despesas.adicionar_despesa(despesa)
        self.assertEqual(len(lista_despesas.despesas), 1)

    def test_registrar_observador(self):
        lista_despesas = ListaDespesas()
        observador = ObservadorDespesas(lista_despesas, tk.Tk())
        lista_despesas.registrar_observador(observador)
        self.assertEqual(len(lista_despesas.observadores), 1)

class TestObservadorDespesas(unittest.TestCase):
    def test_atualizar(self):
        lista_despesas = ListaDespesas()
        observador = ObservadorDespesas(lista_despesas, tk.Tk())
        lista_despesas.registrar_observador(observador)

        despesa = Despesa("Despesa de Teste", 50)
        lista_despesas.adicionar_despesa(despesa)

        self.assertIn("Despesa de Teste", observador.exibicao_despesas.cget("text"))

class TestInterfaceGrafica(unittest.TestCase):
    def test_adicionar_despesa(self):
        root = tk.Tk()
        lista_despesas = ListaDespesas()
        app = InterfaceGrafica(root, lista_despesas)

        entrada_descricao = app.entrada_descricao
        entrada_valor = app.entrada_valor
        botao_adicionar = app.botao_adicionar

        entrada_descricao.insert(0, "Despesa de Teste")
        entrada_valor.insert(0, "50")
        botao_adicionar.invoke()

        self.assertEqual(len(lista_despesas.despesas), 1)

if __name__ == "__main__":
    unittest.main()
