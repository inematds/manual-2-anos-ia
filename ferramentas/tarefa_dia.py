#!/usr/bin/env python3
"""Uma tarefa por dia com IA — registro e sequência (streak).

  python3 tarefa_dia.py feito "pedi para a IA resumir o e-mail do condomínio"
  python3 tarefa_dia.py feito "..." --data 2026-10-26
  python3 tarefa_dia.py status
  python3 tarefa_dia.py listar [--ultimos 10]
"""
import argparse
import sys
from datetime import date, timedelta

import _dados


def registrar(dados, texto, dia: date):
    texto = texto.strip()
    if not texto:
        raise ValueError("descreva a tarefa")
    dados.append({"data": dia.isoformat(), "tarefa": texto})
    return dados


def dias(dados):
    return sorted({date.fromisoformat(d["data"]) for d in dados})


def sequencias(dados, hoje: date):
    ds = dias(dados)
    if not ds:
        return {"atual": 0, "melhor": 0, "dias": 0, "tarefas": 0, "fez_hoje": False}
    melhor = corrida = 1
    for a, b in zip(ds, ds[1:]):
        corrida = corrida + 1 if b - a == timedelta(days=1) else 1
        melhor = max(melhor, corrida)
    # sequência atual: termina hoje ou ontem (ainda dá tempo hoje)
    s = set(ds)
    ponto = hoje if hoje in s else hoje - timedelta(days=1)
    atual = 0
    while ponto in s:
        atual += 1
        ponto -= timedelta(days=1)
    return {"atual": atual, "melhor": melhor, "dias": len(ds), "tarefas": len(dados), "fez_hoje": hoje in s}


def texto_status(r) -> str:
    if r["tarefas"] == 0:
        return "Nenhuma tarefa ainda. Comece com algo pequeno hoje: resumir um e-mail, explicar um boleto."
    barra = "■" * min(r["atual"], 30)
    extra = "" if r["fez_hoje"] else "  (falta a de hoje!)"
    return (f"Sequência atual: {r['atual']} dia(s) {barra}{extra}\n"
            f"Melhor sequência: {r['melhor']} · dias com tarefa: {r['dias']} · tarefas: {r['tarefas']}\n"
            "Medo evitado cresce; enfrentado em doses pequenas diminui.")


def main(argv=None, hoje: date | None = None):
    ap = argparse.ArgumentParser(description="Uma tarefa por dia com IA.")
    ap.add_argument("--arquivo", help="JSON (padrão ~/.manual-ia/tarefas.json)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("feito")
    f.add_argument("tarefa")
    f.add_argument("--data", help="AAAA-MM-DD (padrão hoje)")
    sub.add_parser("status")
    l = sub.add_parser("listar")
    l.add_argument("--ultimos", type=int, default=10)
    args = ap.parse_args(argv)

    hoje = hoje or date.today()
    arq = _dados.caminho("tarefas.json", args.arquivo)
    dados = _dados.ler(arq, [])
    if args.cmd == "feito":
        dia = date.fromisoformat(args.data) if args.data else hoje
        registrar(dados, args.tarefa, dia)
        _dados.gravar(arq, dados)
        print("Registrado.\n" + texto_status(sequencias(dados, hoje)))
    elif args.cmd == "status":
        print(texto_status(sequencias(dados, hoje)))
    else:
        for d in sorted(dados, key=lambda x: x["data"])[-args.ultimos:]:
            print(f"{d['data']}  {d['tarefa']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
