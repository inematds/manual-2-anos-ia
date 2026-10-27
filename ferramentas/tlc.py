#!/usr/bin/env python3
"""TLC — quanto uma tarefa ou profissão está exposta à IA.

T = Trust/Confiança: exige alguém que responde pelo resultado?     sim = barreira
L = Learn/Aprender: a IA aprende rápido? (digital, repetível, fácil de conferir)   não = barreira
C = Contact/Contato: precisa de contato físico com o mundo?        sim = barreira

  python3 tlc.py "Atendimento por chat" --confianca n --aprende s --contato n
  python3 tlc.py                      # modo interativo
"""
import argparse
import sys

import _dados

NIVEIS = {
    0: ("ALTA", "A IA já faz boa parte disso. Aprenda a fazer COM IA agora e mude o seu papel para "
                "quem confere, decide e responde pelo resultado."),
    1: ("MÉDIA-ALTA", "Uma barreira só. Use IA nas partes repetíveis e reforce a barreira que você tem "
                      "(relação de confiança ou presença)."),
    2: ("MÉDIA-BAIXA", "Duas barreiras. A IA vira assistente. Ganhe tempo com ela e invista em domínio "
                       "da área e conexão humana."),
    3: ("BAIXA", "Três barreiras. Risco baixo nos próximos anos. Use IA para a papelada e cuide do que "
                 "é humano no seu trabalho."),
}


def pontuar(confianca: bool, aprende_rapido: bool, contato: bool) -> dict:
    barreiras = {
        "T": bool(confianca),
        "L": not aprende_rapido,
        "C": bool(contato),
    }
    n = sum(barreiras.values())
    nivel, conselho = NIVEIS[n]
    return {"barreiras": barreiras, "total": n, "exposicao": nivel, "conselho": conselho}


def relatorio(nome: str, r: dict) -> str:
    b = r["barreiras"]
    ok = lambda x: "barreira" if x else "aberto"
    return "\n".join([
        f"Tarefa: {nome}",
        f"  T Confiança : {ok(b['T'])}",
        f"  L Aprender  : {ok(b['L'])}",
        f"  C Contato   : {ok(b['C'])}",
        f"Barreiras: {r['total']}/3  ->  exposição {r['exposicao']}",
        f"O que fazer: {r['conselho']}",
    ])


def perguntar(texto: str, entrada=input) -> bool:
    while True:
        try:
            return _dados.sim_nao(entrada(f"{texto} [s/n] "))
        except ValueError as e:
            print(e)


def main(argv=None, entrada=input):
    ap = argparse.ArgumentParser(description="Modelo TLC: Confiança, Aprender, Contato.")
    ap.add_argument("tarefa", nargs="?")
    ap.add_argument("--confianca", help="exige confiança/responsabilidade? s|n")
    ap.add_argument("--aprende", help="a IA aprende rápido o que você faz? s|n")
    ap.add_argument("--contato", help="precisa de contato físico? s|n")
    args = ap.parse_args(argv)

    nome = args.tarefa or entrada("Qual tarefa ou profissão? ").strip() or "(sem nome)"
    try:
        t = _dados.sim_nao(args.confianca) if args.confianca else perguntar(
            "T: o trabalho exige confiança e alguém que responde pelo resultado?", entrada)
        l = _dados.sim_nao(args.aprende) if args.aprende else perguntar(
            "L: é digital, repetível e fácil de conferir (a IA aprende rápido)?", entrada)
        c = _dados.sim_nao(args.contato) if args.contato else perguntar(
            "C: precisa de contato físico com o mundo (mãos, corpo, presença)?", entrada)
    except ValueError as e:
        ap.error(str(e))
    print(relatorio(nome, pontuar(t, l, c)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
