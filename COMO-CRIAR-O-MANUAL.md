# Como criar este manual (e o seu)

Este documento mostra **como o INEMA transforma um tema em manual + vídeos + ferramentas**, passo a
passo, e **quais ferramentas ajudam em cada etapa**. No fim, uma lista de ferramentas públicas para
qualquer pessoa montar um manual parecido para a família, a equipe ou a escola.

A ideia central: **um tema vira três coisas que se reforçam** — um texto que se lê em 5 minutos, um
vídeo que se assiste em 3, e ferramentas pequenas que se usam todo dia.

```
tema/vídeo de referência
   │
   ├─ 1. capturar ─ 2. transcrever ─ 3. extrair a estrutura ─ 4. checar fatos
   │
   ├─ 5. escrever o manual (Markdown)        → manual/
   ├─ 6. virar ferramenta (o que se repete)  → ferramentas/
   ├─ 7. redesenhar exemplos em imagem       → guia/assets/
   ├─ 8. roteiro + vídeo explicativo         → 16:9 e 9:16
   ├─ 9. traduzir PT → EN/ES
   └─ 10. publicar (guia, YouTube, Telegram, portal)
```

## O processo, etapa por etapa

| # | Etapa | O que sai | Ferramentas que usamos | Quem faz |
|---|---|---|---|---|
| 1 | **Escolher o tema e a referência** | uma frase: "que medo/dúvida isto resolve?" | conversa, curadoria | 🧠 pessoa |
| 2 | **Baixar e transcrever** | texto com marcação de tempo | **inemavox** (nosso baixador e transcritor local), **yt-dlp** (download), **Whisper** local (transcrição) | ⚙️ script |
| 3 | **Extrair a estrutura** | os passos, a metáfora, os exemplos, as frases fortes | agente de IA lendo a transcrição | 🤖 agente |
| 4 | **Checar fatos** | lista "confirmado / não confirmado" com fonte | agente de IA + busca na web; regra: número sem fonte não entra | 🤖 + 🧠 |
| 5 | **Escrever o manual** | 1 arquivo por passo + 1 página imprimível | editor de texto, Markdown, agente para revisar a linguagem simples | 🧠 + 🤖 |
| 6 | **Transformar o que se repete em ferramenta** | scripts pequenos, locais, sem internet | Python 3 sem dependência, testes com `unittest` | 🤖 agente |
| 7 | **Redesenhar exemplos em imagem** | banners, diagramas, capas | **Codex image_gen** (texto em português certo na arte); **flux2-klein** local como reserva | 🤖 agente |
| 8 | **Roteiro e vídeo explicativo** | vídeo 16:9 e corte 9:16 | **explicavideos** (nosso motor de vídeo explicativo) + avatar e voz pelo estúdio **HeyGen** | 🤖 + 🧠 aprova |
| 9 | **Traduzir PT → EN/ES** | guia, README e vídeos em 3 idiomas | tradutor central do INEMA (um único comando, um modelo trocável num só lugar) | ⚙️ script |
| 10 | **Guia / landing** | página única no GitHub Pages | gerador de guia INEMA (HTML único, sem build) + GitHub Actions | 🤖 agente |
| 11 | **Publicar** | links no ar | YouTube (publicador de vídeo), grupo no Telegram, portal **inema.club** | ⚙️ + 🧠 |
| 12 | **Revisar com olhos novos** | nota e lista de defeitos | revisor independente: um agente novo que nunca viu o trabalho | 🤖 |

🧠 sessão com pessoa · ⚙️ script · 🤖 agente de IA

### Dicas que aprendemos fazendo

- **Sem crédito, sem cópia.** O manual é reescrito no nosso método e com os nossos exemplos. A
  referência serve para entender o tema, não para ser transcrita.
- **Um passo = uma metáfora = uma ferramenta.** Se um passo não vira nada que a pessoa *faça*, ele
  provavelmente é só opinião.
- **Ferramenta local primeiro.** Nada de conta, login ou internet para usar as ferramentas do
  manual. Dados ficam num JSON na máquina da pessoa.
- **Imagem com texto: confira com zoom.** Gerador de imagem às vezes troca uma letra.
- **Teste antes de publicar.** Toda ferramenta tem teste; o manual só sai com os testes passando.

## Ferramentas públicas para montar o seu manual

Qualquer pessoa pode montar um manual como este com ferramentas comuns. Uma linha para cada uma:

| Ferramenta | Para que serve no manual |
|---|---|
| **NotebookLM** | jogar transcrições e artigos e pedir resumo, perguntas e mapa dos passos. |
| **Obsidian** | escrever o manual em Markdown, um arquivo por passo, com links entre eles. |
| **Notion** | versão em equipe: cada passo uma página, checklist e comentários. |
| **Google Docs** | quem prefere documento comum para revisar com a família ou a equipe. |
| **Leitor de RSS** (Feedly, Inoreader, NetNewsWire) | a **Janela**: junte as fontes de notícia num lugar e só abra no horário fixo. |
| **Read-later** (Instapaper, Raindrop, lista de leitura do navegador) | guardar a manchete sem ler agora. |
| **Google Agenda / calendário do celular** | marcar o horário fixo semanal da Janela, com lembrete. |
| **App de hábitos** (Loop Habit Tracker, Habitica, Streaks) | a **tarefa por dia** e a sequência. |
| **ChatGPT, Claude, Gemini** | a própria tarefa do dia; e revisar o manual em linguagem simples. |
| **Busca reversa de imagem** (Google Lens, TinEye) | checar se uma foto que assusta é antiga ou falsa. |
| **Agências de checagem** (Lupa, Aos Fatos, Comprova) | conferir notícia antes de repassar. |
| **Canva** | transformar o `MANUAL.md` em cartaz de uma página para imprimir. |
| **GitHub Pages** | publicar o manual de graça como página web. |
| **Python 3** | rodar as ferramentas deste repo (`ferramentas/`), sem instalar mais nada. |

## Como adaptar este repo

1. Faça um fork ou baixe o ZIP.
2. Troque os exemplos de `manual/03-achar-o-farol.md` pelas tarefas reais do seu grupo.
3. Edite `ferramentas/contribuicao.py` (lista `CONTRIBUICOES`) com as contribuições que fazem
   sentido para vocês.
4. Rode `python3 -m unittest` para conferir que nada quebrou.
5. Imprima o `manual/MANUAL.md` e marque a primeira Janela.
