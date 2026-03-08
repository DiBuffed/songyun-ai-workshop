"""
모델을 미리 다운로드합니다. (0%%에서 멈출 때 사용)

.env의 HF_ENDPOINT, HF_TOKEN을 사용합니다.
다운로드 완료 후 run.bat 실행 시 캐시에서 바로 로드됩니다.
"""
import os
import sys
from pathlib import Path

# .env 로드 (HF_ENDPOINT, HF_TOKEN)
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except Exception:
    pass

# HF transfer 비활성화 (멈춤 방지)
os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "0")

def main():
    model_id = os.getenv("BASE_MODEL_ID", "runwayml/stable-diffusion-v1-5")
    print(f"Downloading {model_id}...")
    print("(Use HF_ENDPOINT=https://hf-mirror.com in .env if slow)")
    print()

    from diffusers import StableDiffusionPipeline

    StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype="float32",
        safety_checker=None,
        low_cpu_mem_usage=True,
        resume_download=True,
    )
    print(f"\nDone! Model cached. Run run.bat to start the app.")

if __name__ == "__main__":
    main()
