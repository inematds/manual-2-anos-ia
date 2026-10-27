#!/usr/bin/env python3
"""Ache sua contribuição — "não dá para forrar a Terra de couro, mas dá para calçar um par de sapatos".

  python3 contribuicao.py listar
  python3 contribuicao.py plano 1 [--para "meus pais"] [--salvar plano.md]
  python3 contribuicao.py             # modo interativo
"""
import argparse
import sys

CONTRIBUICOES = [
    {
        "titulo": "Ensinar pais e avós a reconhecer deepfake e golpe de voz",
        "para": "pais e avós",
        "semanas": [
            "Conversa de 15 min: mostre 2 exemplos de vídeo ou áudio falso e combine uma PALAVRA-SENHA da família para pedidos de dinheiro.",
            "Treino: mande 3 mensagens (uma verdadeira, duas suspeitas) e peça para dizerem qual é golpe e por quê.",
            "Configure junto: bloqueio de chamadas desconhecidas, confirmação em duas etapas no WhatsApp e no banco.",
            "Revisão: repitam a palavra-senha, escrevam num papel na geladeira as 3 regras (desconfie, ligue de volta, nunca com pressa).",
        ],
    },
    {
        "titulo": "Combinar regras de uso de IA com os filhos",
        "para": "seus filhos",
        "semanas": [
            "Usem uma IA juntos por 20 min em algo da escola. Perguntem: onde ela errou?",
            "Escrevam juntos 5 regras (ex.: IA ajuda a entender, não faz a lição; nunca enviar foto do rosto; contar quando algo assustar).",
            "Combinem um sinal para 'vi algo estranho' (deepfake de colega, conversa esquisita com robô) sem bronca.",
            "Revejam as regras, ajustem o que não funcionou e coloquem num lugar visível.",
        ],
    },
    {
        "titulo": "Ser quem ajuda os colegas a usar IA sem medo",
        "para": "seus colegas de trabalho",
        "semanas": [
            "Escolha 1 tarefa chata da equipe e mostre como fazer com IA em 5 min (ao vivo, com erro e tudo).",
            "Monte uma lista de 5 pedidos (prompts) que funcionam no seu trabalho e compartilhe.",
            "Ofereça 15 min de 'plantão de dúvidas' na semana. Anote as perguntas.",
            "Com as perguntas anotadas, escreva uma página 'o que pode e o que não pode' com a liderança.",
        ],
    },
    {
        "titulo": "Montar um manual como este para o seu grupo",
        "para": "sua equipe, escola, igreja ou associação",
        "semanas": [
            "Leia o MANUAL.md e anote o que faz sentido para o seu grupo e o que falta.",
            "Adapte os exemplos do passo 3 (TLC) para as tarefas reais do grupo.",
            "Apresente em 20 min e combine a Janela coletiva (um horário por semana para falar de notícias de IA).",
            "Recolha as dúvidas, atualize o manual e marque a próxima conversa.",
        ],
    },
]


def plano(idx: int, para: str | None = None) -> str:
    if not 1 <= idx <= len(CONTRIBUICOES):
        raise ValueError(f"escolha de 1 a {len(CONTRIBUICOES)}")
    c = CONTRIBUICOES[idx - 1]
    alvo = para or c["para"]
    linhas = [f"# Plano de 4 semanas — {c['titulo']}", "", f"Para: {alvo}", ""]
    for n, s in enumerate(c["semanas"], 1):
        linhas += [f"## Semana {n}", f"- [ ] {s}", ""]
    linhas.append("Um par de sapatos de cada vez.")
    return "\n".join(linhas)


def listar() -> str:
    return "\n".join(f"{i}. {c['titulo']}" for i, c in enumerate(CONTRIBUICOES, 1))


def main(argv=None, entrada=input):
    ap = argparse.ArgumentParser(description="Escolha sua contribuição e gere um plano de 4 semanas.")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("listar")
    p = sub.add_parser("plano")
    p.add_argument("numero", type=int)
    p.add_argument("--para")
    p.add_argument("--salvar")
    args = ap.parse_args(argv)

    if args.cmd == "listar":
        print(listar())
        return 0
    if args.cmd == "plano":
        idx, para, salvar = args.numero, args.para, args.salvar
    else:
        print(listar())
        idx = int(entrada("Qual número? ").strip())
        para = entrada("Para quem (enter = padrão)? ").strip() or None
        salvar = None
    try:
        txt = plano(idx, para)
    except ValueError as e:
        ap.error(str(e))
    print(txt)
    if salvar:
        with open(salvar, "w", encoding="utf-8") as f:
            f.write(txt + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
