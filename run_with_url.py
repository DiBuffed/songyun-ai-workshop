"""
Launcher that runs the app and captures the public share URL.
Shows the URL in a popup and saves it to PUBLIC_LINK.txt so you can share it.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

# Load .env for ROOT_PATH
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except Exception:
    pass

OUTPUT_FILE = Path(__file__).parent / "PUBLIC_LINK.txt"
URL_PATTERN = re.compile(r"https://[a-zA-Z0-9-]+\.gradio\.live[^\s]*")


def _full_url(base: str) -> str:
    """Append ROOT_PATH if set (e.g. /songyun-ai-workshop)."""
    root = os.getenv("ROOT_PATH", "").strip()
    if root and not root.startswith("/"):
        root = "/" + root
    if root and not base.rstrip("/").endswith(root):
        return base.rstrip("/") + root
    return base


def show_url_popup(url: str) -> None:
    """Show URL in a simple popup (Windows)."""
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(  # type: ignore
            0,
            f"외부인 공유 링크 (복사해서 전달하세요):\n\n{url}\n\n"
            "이 링크는 PUBLIC_LINK.txt 파일에도 저장되었습니다.",
            "Songyun AI - 공개 링크",
            0x40,  # MB_ICONINFORMATION
        )
    except Exception:
        print("\n" + "=" * 50)
        print("  공개 링크 (외부인 공유용):")
        print(f"  {url}")
        print("=" * 50)
        print("  이 링크는 PUBLIC_LINK.txt 에도 저장되었습니다.")
        print("=" * 50 + "\n")


def main():
    print("Songyun AI Workshop 시작 중... (모델 로딩에 1~2분 소요)")
    print("공개 링크가 생성되면 팝업으로 표시됩니다.\n")

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    proc = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=Path(__file__).parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )

    url_found = None
    for line in proc.stdout:  # type: ignore
        print(line, end="")
        if url_found is None:
            match = URL_PATTERN.search(line)
            if match:
                url_found = _full_url(match.group(0).rstrip(".,;:)"))
                OUTPUT_FILE.write_text(url_found, encoding="utf-8")
                show_url_popup(url_found)

    proc.wait()
    sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
