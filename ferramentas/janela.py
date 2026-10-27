#!/usr/bin/env python3
"""A Janela — adiamento da preocupação para notícias de IA.

Durante a semana você só anota. No horário fixo da janela, lista, lê e marca como lida.

  python3 janela.py add "Agentes saíram do sandbox em teste" --campo seguranca [--fonte URL]
  python3 janela.py listar            # pendentes, agrupadas por campo
  python3 janela.py listar --todas
  python3 janela.py ler 3             # marca o item 3 como lido
  python3 janela.py ler --todas       # fecha a janela
  python3 janela.py limpar            # apaga os já lidos
"""
import argparse
import sys
from datetime import datetime

import _dados

CAMPOS = {
    "seguranca": "Segurança (limites, regulação)",
    "acelera": "Aceleracionistas (velocidade, código aberto)",
    "centro": "Centristas (danos de hoje)",
    "governo": "Governo (corrida, economia)",
    "?": "Ainda não sei o campo",
}


def carregar(arq):
    return _dados.ler(arq, [])


def adicionar(itens, texto, campo="?", fonte="", agora=None):
    if campo not in CAMPOS:
        raise ValueError(f"campo inválido: {campo} (use {', '.join(CAMPOS)})")
    texto = texto.strip()
    if not texto:
        raise ValueError("manchete vazia")
    novo = {
        "id": max((i["id"] for i in itens), default=0) + 1,
        "texto": texto,
        "campo": campo,
        "fonte": fonte,
        "criado": (agora or datetime.now()).isoformat(timespec="minutes"),
        "lido": False,
    }
    itens.append(novo)
    return novo


def marcar_lido(itens, ident=None):
    n = 0
    for i in itens:
        if not i["lido"] and (ident is None or i["id"] == ident):
            i["lido"] = True
            n += 1
    return n


def limpar(itens):
    return [i for i in itens if not i["lido"]]


def formatar(itens, todas=False):
    mostrar = [i for i in itens if todas or not i["lido"]]
    if not mostrar:
        return "Janela vazia. Nada para ler — siga a semana."
    linhas = [f"{len(mostrar)} item(ns). Para cada um: o que estou supondo? quais os fatos? qual o incentivo?\n"]
    for campo, nome in CAMPOS.items():
        grupo = [i for i in mostrar if i["campo"] == campo]
        if not grupo:
            continue
        linhas.append(f"## {nome}")
        for i in grupo:
            marca = "x" if i["lido"] else " "
            fonte = f"  <{i['fonte']}>" if i.get("fonte") else ""
            linhas.append(f"  [{marca}] {i['id']:>3}. {i['texto']}{fonte}  ({i['criado'][:10]})")
        linhas.append("")
    return "\n".join(linhas).rstrip()


def main(argv=None):
    ap = argparse.ArgumentParser(description="A Janela: anote durante a semana, leia no horário fixo.")
    ap.add_argument("--arquivo", help="JSON (padrão ~/.manual-ia/janela.json)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add", help="anotar manchete")
    a.add_argument("texto")
    a.add_argument("--campo", default="?", choices=list(CAMPOS))
    a.add_argument("--fonte", default="")
    l = sub.add_parser("listar", help="listar na hora da janela")
    l.add_argument("--todas", action="store_true")
    r = sub.add_parser("ler", help="marcar como lido")
    r.add_argument("id", nargs="?", type=int)
    r.add_argument("--todas", action="store_true")
    sub.add_parser("limpar", help="apagar os lidos")
    args = ap.parse_args(argv)

    arq = _dados.caminho("janela.json", args.arquivo)
    itens = carregar(arq)
    if args.cmd == "add":
        novo = adicionar(itens, args.texto, args.campo, args.fonte)
        _dados.gravar(arq, itens)
        print(f"Anotado #{novo['id']}. Não leia agora: fica para a janela.")
    elif args.cmd == "listar":
        print(formatar(itens, args.todas))
    elif args.cmd == "ler":
        if args.id is None and not args.todas:
            ap.error("informe o id ou --todas")
        n = marcar_lido(itens, None if args.todas else args.id)
        _dados.gravar(arq, itens)
        print(f"{n} marcado(s) como lido(s)." + (" Janela fechada. Siga." if args.todas else ""))
    elif args.cmd == "limpar":
        resto = limpar(itens)
        _dados.gravar(arq, resto)
        print(f"{len(itens) - len(resto)} removido(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
