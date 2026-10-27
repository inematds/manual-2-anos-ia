"""Onde as ferramentas guardam seus arquivos (tudo local, nada sai da máquina).

Padrão: ~/.manual-ia/  — troque com a variável MANUAL_IA_DADOS ou com --arquivo em cada ferramenta.
"""
import json
import os
from pathlib import Path


def pasta() -> Path:
    p = Path(os.environ.get("MANUAL_IA_DADOS", Path.home() / ".manual-ia"))
    p.mkdir(parents=True, exist_ok=True)
    return p


def caminho(nome: str, arquivo: str | None = None) -> Path:
    return Path(arquivo) if arquivo else pasta() / nome


def ler(path: Path, padrao):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return padrao


def gravar(path: Path, dados) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def sim_nao(valor: str) -> bool:
    v = valor.strip().lower()
    if v in ("s", "sim", "y", "yes", "si", "1", "true"):
        return True
    if v in ("n", "nao", "não", "no", "0", "false"):
        return False
    raise ValueError(f"responda s ou n (recebi: {valor!r})")
