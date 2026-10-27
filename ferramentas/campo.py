#!/usr/bin/env python3
"""Cartão de leitura de notícia: quem fala, de qual campo, qual o incentivo, fato × suposição.

  python3 campo.py --manchete "IA invade empresa em teste" --quem "laboratório X" \
      --campo seguranca --incentivo "mostrar que o modelo é poderoso" \
      --fato "teste autorizado, proteções reduzidas" --suposicao "vai acontecer em qualquer empresa amanhã" \
      [--decisao "alguém reduziu as proteções"] [--fonte URL] [--salvar cartoes.txt]
  python3 campo.py                    # modo interativo
"""
import argparse
import sys
from datetime import date

CAMPOS = {
    "seguranca": "Segurança",
    "acelera": "Aceleracionistas",
    "centro": "Centristas",
    "governo": "Governo",
    "?": "Não sei",
}


def cartao(d: dict, hoje: date | None = None) -> str:
    campo = CAMPOS.get(d.get("campo") or "?", "Não sei")
    fatos = [x for x in d.get("fatos", []) if x.strip()]
    sups = [x for x in d.get("suposicoes", []) if x.strip()]
    fonte = d.get("fonte") or "SEM FONTE ORIGINAL -> trate como 'não confirmado'"
    largura = 64
    linhas = [
        "+" + "-" * largura + "+",
        f"  CARTÃO DE LEITURA · {(hoje or date.today()).isoformat()}",
        f"  Manchete : {d.get('manchete', '').strip()}",
        f"  Quem fala: {d.get('quem') or '?'}",
        f"  Campo    : {campo}",
        f"  Incentivo: {d.get('incentivo') or '?'}",
        f"  Decisão humana antes: {d.get('decisao') or '?'}",
        "  FATOS (dá para conferir):",
        *[f"    - {x}" for x in (fatos or ["(nenhum ainda)"])],
        "  SUPOSIÇÕES (minhas ou de quem fala):",
        *[f"    - {x}" for x in (sups or ["(nenhuma anotada)"])],
        f"  Fonte    : {fonte}",
        f"  Veredito : {veredito(fatos, sups, d.get('fonte'))}",
        "+" + "-" * largura + "+",
    ]
    return "\n".join(linhas)


def veredito(fatos, sups, fonte) -> str:
    if not fonte:
        return "Não confirmado. Guarde para a janela e não repasse."
    if len(sups) > len(fatos):
        return "Mais suposição que fato. Leia de novo daqui a uma semana."
    return "Fato com contexto. Pense no que muda para você (passo 3) e siga."


def main(argv=None, entrada=input):
    ap = argparse.ArgumentParser(description="Checklist de leitura de notícia sobre IA.")
    ap.add_argument("--manchete")
    ap.add_argument("--quem")
    ap.add_argument("--campo", choices=list(CAMPOS))
    ap.add_argument("--incentivo")
    ap.add_argument("--decisao")
    ap.add_argument("--fato", action="append", default=[])
    ap.add_argument("--suposicao", action="append", default=[])
    ap.add_argument("--fonte", default="")
    ap.add_argument("--salvar", help="acrescenta o cartão neste arquivo de texto")
    args = ap.parse_args(argv)

    d = {
        "manchete": args.manchete, "quem": args.quem, "campo": args.campo,
        "incentivo": args.incentivo, "decisao": args.decisao,
        "fatos": args.fato, "suposicoes": args.suposicao, "fonte": args.fonte,
    }
    if not d["manchete"]:
        d["manchete"] = entrada("Manchete: ")
        d["quem"] = entrada("Quem fala (pessoa, empresa, veículo)? ")
        c = entrada(f"De qual campo vem? ({'/'.join(CAMPOS)}) ").strip() or "?"
        d["campo"] = c if c in CAMPOS else "?"
        d["incentivo"] = entrada("Qual o incentivo de quem fala? ")
        d["decisao"] = entrada("Qual decisão humana veio antes? ")
        d["fatos"] = [x.strip() for x in entrada("Fatos (separe por ;): ").split(";")]
        d["suposicoes"] = [x.strip() for x in entrada("O que estou supondo? (separe por ;): ").split(";")]
        d["fonte"] = entrada("Link da fonte original (vazio se não achou): ").strip()
    txt = cartao(d)
    print(txt)
    if args.salvar:
        with open(args.salvar, "a", encoding="utf-8") as f:
            f.write(txt + "\n\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
