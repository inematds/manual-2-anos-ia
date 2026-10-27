# manual-2-anos-ia

[![Manual da IA](guia/assets/banner.jpg)](https://inematds.github.io/manual-2-anos-ia/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

Este é um manual curto para quem sente ansiedade com as notícias de inteligência artificial. Ele organiza o assunto em 4 passos: entender o que aconteceu, saber quem está falando e por quê, medir o que muda no seu trabalho e agir em doses pequenas. Vem com 5 ferramentas simples, que rodam no seu computador sem internet, e com o passo a passo de como montar um manual parecido para a sua família, equipe ou escola. Para ler, basta abrir a página; para as ferramentas, basta ter Python 3.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/manual-2-anos-ia/guia/**

## 🎬 Vídeos

- **Completo (16:9, ≈6 min):** https://www.youtube.com/watch?v=DnkFeQDB8AI
- **Curto (9:16, 41 s):** https://www.youtube.com/watch?v=XFDDBRPuvwE

## O método: 4 passos (você não controla o mar, só o leme)

| Passo | Pergunta | Ferramenta |
|---|---|---|
| 1. [Entender os ventos](manual/01-entender-os-ventos.md) | O que aconteceu? | `campo.py` |
| 2. [Ver através da névoa](manual/02-ver-atraves-da-nevoa.md) | Quem fala, e por quê? (3 campos + governo, A Janela) | `janela.py`, `campo.py` |
| 3. [Achar o farol](manual/03-achar-o-farol.md) | O que muda no MEU trabalho? (modelo TLC) | `tlc.py` |
| 4. [Remar até a praia](manual/04-remar-ate-a-praia.md) | O que eu faço agora? | `tarefa_dia.py`, `contribuicao.py` |

Versão de uma página para imprimir: **[manual/MANUAL.md](manual/MANUAL.md)**.
Como montar o seu próprio manual (processo + ferramentas): **[COMO-CRIAR-O-MANUAL.md](COMO-CRIAR-O-MANUAL.md)**.

## Estrutura

```
manual/                  o manual (1 arquivo por passo + MANUAL.md de uma página)
ferramentas/             5 ferramentas em Python 3, sem dependência, sem internet
  janela.py              A Janela: anotar manchetes e ler no horário fixo
  campo.py               cartão de leitura de notícia (campo, incentivo, fato × suposição)
  tlc.py                 modelo TLC: Confiança, Aprender, Contato
  tarefa_dia.py          uma tarefa por dia com IA + sequência
  contribuicao.py        sua contribuição + plano de 4 semanas
  tests/                 16 testes (python3 -m unittest)
COMO-CRIAR-O-MANUAL.md   como transformar um tema em manual + vídeos + ferramentas
guia/                    landing + guia (PT, en/, es/) no GitHub Pages
```

## O processo, do início ao fim

🧠 sessão com o Nei · ⚙️ script · 🤖 agente

| # | Passo | Comando | Quem |
|---|---|---|---|
| 1 | Escolher o tema e a referência; decidir o que o manual resolve | conversa | 🧠 |
| 2 | Baixar e transcrever a referência | `python baixar_v1.py --url <URL>` · `python transcrever_v1.py --in <video>` (inemavox) | ⚙️ |
| 3 | Extrair os passos, a metáfora e os exemplos; checar fatos com fonte | agente lendo a transcrição + busca na web | 🤖 |
| 4 | Escrever o manual em `manual/` | edição em Markdown | 🤖 + 🧠 revisa |
| 5 | Escrever as ferramentas e os testes | `python3 -m unittest` | 🤖 |
| 6 | Capa e banners (PT/EN/ES) | `gerar-capa.cjs` + `gerar-banner.sh --estilo live\|grade --lang pt\|en\|es` (Codex image_gen) e `cor_neutra.py corrigir` | 🤖 |
| 7 | Guia PT em `guia/index.html` | skill `projetos-landing-guia` | 🤖 |
| 8 | Traduzir guia e README para EN/ES | `inema-traduz` (tradutor central) | ⚙️ |
| 9 | Revisor independente | agente novo com a lista fixa | 🤖 |
| 10 | Publicar o repo e o Pages | `git push` (Pages via GitHub Actions) | ⚙️ |
| 11 | Portal inema.club + inemabuscas + PRO | skill `atualiza-portal` | 🤖 |
| 12 | Vídeos explicativos 16:9 e 9:16 do mesmo tema | explicavideos + estúdio HeyGen (outra sessão) | 🤖 + 🧠 aprova |

## Rodar as ferramentas

```bash
git clone https://github.com/inematds/manual-2-anos-ia && cd manual-2-anos-ia
python3 -m unittest                     # 16 testes, deve dar OK
cd ferramentas
python3 janela.py add "manchete" --campo seguranca
python3 janela.py listar
python3 tlc.py "Minha tarefa" --confianca s --aprende n --contato n
python3 campo.py                        # modo interativo
python3 tarefa_dia.py feito "pedi para a IA resumir um e-mail"
python3 contribuicao.py plano 1 --para "meus pais"
```

Os dados ficam em `~/.manual-ia/` (mude com `MANUAL_IA_DADOS=/outra/pasta` ou `--arquivo`).

## Complemento

Kit prático (14 dias, IA offline, segurança de contas, avaliar seu trabalho com IA):
**[sobreviver-ia](https://inematds.github.io/sobreviver-ia/guia/)**.

---

Conteúdo aberto e gratuito do **[INEMA.CLUB](https://inema.club)** · Licença MIT.
