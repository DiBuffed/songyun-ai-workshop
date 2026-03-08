# Songyun AI Workshop / 宋韵 AI 工作坊

A **local, workshop-friendly** web app for generating traditional Chinese Song Dynasty style (宋韵) images using Stable Diffusion and the [Songyun LoRA](https://civitai.com/models/968377/chinese-painting-in-the-song-dynasty-lora).

> **Note:** This is a demo app for workshops and learning. It is not intended for production deployment. Students use only the browser—no manual plugin installation or model folder setup required.

---

## Quick Start (복사해서 실행)

**Windows:** 프로젝트 폴더에서 `run.bat` 더블클릭 또는 터미널에서:

```
run.bat
```

처음 실행 시 패키지 설치와 모델 다운로드가 자동으로 진행됩니다. 완료 후 브라우저에서 `http://localhost:8080/songyun-ai-workshop` 접속.

---

## For Student Assistants: Setup Guide

Use this guide to prepare the workshop environment before students arrive.

### Prerequisites

- **Python 3.10+** installed
- **GPU with CUDA** (recommended; CPU works but is slow)
- **Base model**: A Stable Diffusion 1.5–compatible checkpoint
- **Songyun LoRA**: Download the `.safetensors` file from [Civitai](https://civitai.com/models/968377/chinese-painting-in-the-song-dynasty-lora)

The LoRA alone is not enough—you must have a compatible base model. The Songyun LoRA is designed for SD 1.5.

---

### Step 1: Create a virtual environment

Open a terminal in the project folder and run:

```bash
cd songyun-workshop
python -m venv venv
```

**Activate the environment:**

| Platform | Command |
|----------|---------|
| Windows (PowerShell) | `.\venv\Scripts\Activate.ps1` |
| Windows (CMD) | `venv\Scripts\activate.bat` |
| macOS / Linux | `source venv/bin/activate` |

You should see `(venv)` in your prompt when it’s active.

---

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

This may take a few minutes. Wait for it to finish without errors.

---

### Step 3: Configure the environment

Copy the example config file:

```bash
copy .env.example .env    # Windows
# or
cp .env.example .env      # macOS/Linux
```

Edit `.env` and set:

- **`BASE_MODEL_ID`** – Either:
  - A Hugging Face model ID (e.g. `runwayml/stable-diffusion-v1-5`), or
  - The full path to your local base model folder (e.g. `C:/models/dreamshaper_8`)
- **`LORA_PATH`** – Full path to the Songyun LoRA `.safetensors` file (e.g. `C:/models/songyun.safetensors`)

If you leave `LORA_PATH` empty, the app will run without the Songyun style (not recommended for the workshop).

---

### Step 4: Run the app

```bash
python app.py
```

You should see:

1. A short loading message
2. A startup status block showing:
   - Device (CUDA or CPU)
   - Base model
   - Whether LoRA was loaded successfully
3. A local URL

Open your browser at **http://localhost:8080** (or the URL shown in the console).

---

### Pre‑workshop checklist

Before the workshop:

- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created and configured
- [ ] App runs successfully (`python app.py`)
- [ ] Test image generated in the browser
- [ ] Network access: if students use other machines, share `http://<this-machine-ip>:8080` (ensure firewall allows port 8080)

---

## Example Folder Structure

```
songyun-workshop/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
├── prompts.json        # Preset prompts
├── .env                # Your config (create from .env.example)
├── .env.example        # Example config
└── README.md           # This file

# Your models (anywhere on disk; paths go in .env):
C:\models\                    # Example Windows
├── dreamshaper_8\            # Base model folder
│   └── ...
└── songyun.safetensors       # Songyun LoRA file
```

---

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `BASE_MODEL_ID` | Hugging Face ID or local path to SD 1.5 model | `runwayml/stable-diffusion-v1-5` or `C:/models/dreamshaper_8` |
| `LORA_PATH` | Path to Songyun LoRA `.safetensors` file | `C:/models/songyun.safetensors` |
| `DEVICE` | `cuda` or `cpu` (empty = auto-detect) | `cuda` |
| `DEFAULT_NEGATIVE_PROMPT` | Default negative prompt | `ugly, blurry, low quality...` |
| `MAX_IMAGE_SIZE` | Max width/height in pixels | `768` |
| `SERVER_PORT` | Port number | `8080` |
| `ROOT_PATH` | URL path (e.g. `/songyun`) | `/songyun` |
| `APP_TITLE` | Browser tab title | `Songyun AI Workshop / 宋韵` |

---

## Sample Prompts

Try these in the app or use the preset dropdown:

| Style | Example prompt |
|-------|----------------|
| Misty landscape | `misty mountains, ink wash painting, literati style, subtle blank space, Song dynasty aesthetic` |
| Pavilion | `ancient pavilion in the mountains, soft brush texture, Song dynasty landscape, ink and wash` |
| Scholar | `scholar by the river, restrained colors, elegant composition, literati painting` |
| Pine & peaks | `pine trees, distant peaks, quiet atmosphere, traditional Chinese painting, ink wash` |
| Flower & bird | `flower and bird painting, delicate brushwork, Song dynasty style, soft colors` |

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| **"CUDA out of memory"** | Lower width/height (e.g. 512×512) or close other GPU apps |
| **"Model not found"** | Check `BASE_MODEL_ID` in `.env`; use a valid path or Hugging Face ID |
| **"LoRA file not found"** | Ensure `LORA_PATH` points to an existing `.safetensors` file |
| **"Configuration errors"** | Run the app and read the printed errors; fix the listed `.env` values |
| **Slow generation** | GPU is recommended; on CPU, generation can take several minutes per image |
| **Port in use** | Change `SERVER_PORT` in `.env` (e.g. `8080` → `8888`) |
| **MemoryError** | RAM 부족. 다른 프로그램 종료 후 재시도. 또는 `.env`에서 `BASE_MODEL_ID=runwayml/stable-diffusion-v1-5` 사용 (더 가벼움) |

---

## Sharing with Others

The app listens on `0.0.0.0`, so **other devices on the same network** can access it:

1. Run the app and check the console for the **"Same network"** URL.
2. Share that URL with participants (e.g. `http://192.168.1.100:8080`).
3. Ensure your firewall allows incoming connections on the port (8080 by default).

**Custom URL:** Set `ROOT_PATH` in `.env` to change the path (e.g. `/songyun-workshop`). Leave empty for root: `http://yourserver:8080/`.

---

## LoRA Tips (from Civitai)

- **Strength**: 0.7–0.9 works best for Songyun (default in app: 0.8)
- **Resolution**: 512×512 is recommended for good detail
- **Trigger word**: The app adds `songyun` to prompts when the LoRA is loaded

---

## License & Credits

- Songyun LoRA by [C_c_lab176](https://civitai.com/user/c_lab176) on [Civitai](https://civitai.com/models/968377/chinese-painting-in-the-song-dynasty-lora)
- Built with [Gradio](https://gradio.app), [Hugging Face Diffusers](https://huggingface.co/docs/diffusers), and [PyTorch](https://pytorch.org)
