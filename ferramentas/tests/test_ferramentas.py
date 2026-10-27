"""Testes das 5 ferramentas. Rodar na raiz do repo: python3 -m unittest"""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AQUI))

import campo  # noqa: E402
import contribuicao  # noqa: E402
import janela  # noqa: E402
import tarefa_dia  # noqa: E402
import tlc  # noqa: E402


def rodar(fn, *a, **kw):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*a, **kw)
    return buf.getvalue()


class TestJanela(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.arq = os.path.join(self.tmp.name, "j.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_fluxo_completo(self):
        rodar(janela.main, ["--arquivo", self.arq, "add", "Agentes saíram do sandbox", "--campo", "seguranca"])
        rodar(janela.main, ["--arquivo", self.arq, "add", "Modelo aberto novo", "--campo", "acelera", "--fonte", "http://x"])
        saida = rodar(janela.main, ["--arquivo", self.arq, "listar"])
        self.assertIn("2 item(ns)", saida)
        self.assertIn("Segurança", saida)
        self.assertIn("<http://x>", saida)
        rodar(janela.main, ["--arquivo", self.arq, "ler", "1"])
        self.assertIn("1 item(ns)", rodar(janela.main, ["--arquivo", self.arq, "listar"]))
        self.assertIn("2 item(ns)", rodar(janela.main, ["--arquivo", self.arq, "listar", "--todas"]))
        rodar(janela.main, ["--arquivo", self.arq, "ler", "--todas"])
        self.assertIn("Janela vazia", rodar(janela.main, ["--arquivo", self.arq, "listar"]))
        rodar(janela.main, ["--arquivo", self.arq, "limpar"])
        self.assertEqual(json.loads(Path(self.arq).read_text()), [])

    def test_ids_crescem_e_campo_invalido(self):
        itens = []
        janela.adicionar(itens, "a")
        janela.adicionar(itens, "b", "governo")
        self.assertEqual([i["id"] for i in itens], [1, 2])
        with self.assertRaises(ValueError):
            janela.adicionar(itens, "c", "outro")
        with self.assertRaises(ValueError):
            janela.adicionar(itens, "   ")


class TestTLC(unittest.TestCase):
    def test_programacao_passa_pelas_tres(self):
        r = tlc.pontuar(confianca=False, aprende_rapido=True, contato=False)
        self.assertEqual(r["total"], 0)
        self.assertEqual(r["exposicao"], "ALTA")

    def test_enfermagem_tres_barreiras(self):
        r = tlc.pontuar(confianca=True, aprende_rapido=False, contato=True)
        self.assertEqual(r["total"], 3)
        self.assertEqual(r["exposicao"], "BAIXA")

    def test_niveis_intermediarios(self):
        self.assertEqual(tlc.pontuar(True, True, False)["exposicao"], "MÉDIA-ALTA")
        self.assertEqual(tlc.pontuar(True, False, False)["exposicao"], "MÉDIA-BAIXA")

    def test_cli_argumentos(self):
        s = rodar(tlc.main, ["Atendimento por chat", "--confianca", "n", "--aprende", "s", "--contato", "n"])
        self.assertIn("Barreiras: 0/3", s)
        self.assertIn("Atendimento por chat", s)

    def test_interativo(self):
        respostas = iter(["Eletricista", "talvez", "s", "n", "s"])
        s = rodar(tlc.main, [], entrada=lambda _: next(respostas))
        self.assertIn("Barreiras: 3/3", s)


class TestCampo(unittest.TestCase):
    def test_sem_fonte_nao_confirmado(self):
        c = campo.cartao({"manchete": "IA invade empresa", "campo": "seguranca", "fatos": ["teste"]},
                         hoje=date(2026, 10, 27))
        self.assertIn("2026-10-27", c)
        self.assertIn("Segurança", c)
        self.assertIn("Não confirmado", c)

    def test_mais_suposicao_que_fato(self):
        v = campo.veredito(["a"], ["b", "c"], "http://f")
        self.assertIn("Mais suposição", v)

    def test_cli_salva(self):
        with tempfile.TemporaryDirectory() as t:
            arq = os.path.join(t, "c.txt")
            rodar(campo.main, ["--manchete", "X", "--campo", "centro", "--fato", "f1",
                               "--fonte", "http://f", "--salvar", arq])
            txt = Path(arq).read_text()
            self.assertIn("Centristas", txt)
            self.assertIn("Fato com contexto", txt)

    def test_interativo(self):
        r = iter(["Manchete", "Fulano", "governo", "corrida", "liberou", "f1;f2", "s1", ""])
        s = rodar(campo.main, [], entrada=lambda _: next(r))
        self.assertIn("Governo", s)
        self.assertIn("- f2", s)


class TestTarefaDia(unittest.TestCase):
    def test_sequencia(self):
        dados = []
        for d in ["2026-10-20", "2026-10-21", "2026-10-22", "2026-10-25", "2026-10-26"]:
            tarefa_dia.registrar(dados, "t", date.fromisoformat(d))
        r = tarefa_dia.sequencias(dados, hoje=date(2026, 10, 27))
        self.assertEqual(r["atual"], 2)       # 25, 26 (hoje ainda dá tempo)
        self.assertEqual(r["melhor"], 3)
        self.assertFalse(r["fez_hoje"])
        r2 = tarefa_dia.sequencias(dados, hoje=date(2026, 10, 28))
        self.assertEqual(r2["atual"], 0)      # pulou o dia 27

    def test_vazio_e_cli(self):
        self.assertEqual(tarefa_dia.sequencias([], date(2026, 1, 1))["atual"], 0)
        with tempfile.TemporaryDirectory() as t:
            arq = os.path.join(t, "t.json")
            hoje = date(2026, 10, 27)
            rodar(tarefa_dia.main, ["--arquivo", arq, "feito", "resumi e-mail", "--data", "2026-10-26"], hoje=hoje)
            s = rodar(tarefa_dia.main, ["--arquivo", arq, "feito", "expliquei boleto"], hoje=hoje)
            self.assertIn("Sequência atual: 2", s)
            self.assertIn("expliquei boleto", rodar(tarefa_dia.main, ["--arquivo", arq, "listar"], hoje=hoje))


class TestContribuicao(unittest.TestCase):
    def test_plano_tem_4_semanas(self):
        p = contribuicao.plano(1, "minha mãe")
        self.assertEqual(p.count("## Semana"), 4)
        self.assertIn("minha mãe", p)

    def test_indice_invalido(self):
        with self.assertRaises(ValueError):
            contribuicao.plano(99)

    def test_cli(self):
        self.assertIn("4.", rodar(contribuicao.main, ["listar"]))
        with tempfile.TemporaryDirectory() as t:
            arq = os.path.join(t, "p.md")
            rodar(contribuicao.main, ["plano", "3", "--salvar", arq])
            self.assertIn("Semana 4", Path(arq).read_text())


if __name__ == "__main__":
    unittest.main()
