"""Upload Songyun AI Workshop files to Hugging Face Space."""
import os
import sys
from pathlib import Path
from huggingface_hub import HfApi, login

REPO_ID = "DiBuffed/songyun-ai-workshop"
REPO_TYPE = "space"
FILES = ["app.py", "requirements.txt", "prompts.json", "custom.css", "README.md"]

def main():
    token = os.environ.get("HF_TOKEN")
    if not token:
        token_file = Path(__file__).parent / "hf_token.txt"
        if token_file.exists():
            token = token_file.read_text(encoding="utf-8").strip()
            if token and len(token) > 20 and "huggingface.co" not in token:
                pass  # use token
            else:
                token = None
    if not token:
        print("HF_TOKEN이 설정되지 않았습니다.")
        print("hf_token.txt 파일을 열어 토큰을 한 줄에 붙여넣으세요.")
        print("토큰 발급: https://huggingface.co/settings/tokens (Write 권한)")
        sys.exit(1)
    
    api = HfApi(token=token)
    base = Path(__file__).parent / "huggingface-space"
    
    for f in FILES:
        path = base / f
        if path.exists():
            print(f"Uploading {f}...")
            api.upload_file(
                path_or_fileobj=str(path),
                path_in_repo=f,
                repo_id=REPO_ID,
                repo_type=REPO_TYPE,
            )
            print(f"  Done: {f}")
        else:
            print(f"  Skip (not found): {f}")
    
    print("\nUpload complete! Space will rebuild in a few minutes.")
    print(f"https://huggingface.co/spaces/{REPO_ID}")

if __name__ == "__main__":
    main()
