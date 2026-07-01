"""Download the default tokenizer and chat template into helper/.

Only the files needed for tokenization are fetched (tokenizer.json /
tokenizer_config.json / vocab.json / merges.txt / special_tokens_map.json, etc.);
no model weights are downloaded.
"""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOK_DIR = PROJECT_ROOT / "helper" / "tokenizer" / "Qwen3.5-0.8B"
TPL_DIR = PROJECT_ROOT / "helper" / "chat_template"

ALLOW_FILES = {
    "tokenizer.json",
    "tokenizer_config.json",
    "vocab.json",
    "merges.txt",
    "special_tokens_map.json",
    "added_tokens.json",
    "chat_template.jinja",
}


def fetch_tokenizer(repo_id: str = "Qwen/Qwen3.5-0.8B") -> None:
    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        sys.exit("Please install huggingface_hub: pip install -e '.[dev]'")

    TOK_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_download(
        repo_id=repo_id,
        local_dir=str(TOK_DIR),
        allow_patterns=list(ALLOW_FILES),
        local_dir_use_symlinks=False,
    )
    print(f"Tokenizer fetched into {TOK_DIR}")


def install_chat_template() -> None:
    TPL_DIR.mkdir(parents=True, exist_ok=True)
    target = TPL_DIR / "qwen3.jinja"
    if target.exists():
        print(f"chat template already exists at {target}")
        return
    # Generic Qwen3 chat template; overwrite this file directly if you need an exact version.
    target.write_text(
        "{% for message in messages %}"
        "<|im_start|>{{ message['role'] }}\n{{ message['content'] }}<|im_end|>\n"
        "{% endfor %}"
        "{% if add_generation_prompt %}<|im_start|>assistant\n{% endif %}",
        encoding="utf-8",
    )
    print(f"chat template installed at {target}")


if __name__ == "__main__":
    fetch_tokenizer()
    install_chat_template()
