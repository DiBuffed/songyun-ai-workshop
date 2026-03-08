"""
Songyun AI Workshop - Local image generation web app.

A workshop-friendly Gradio app for generating Song Dynasty style (宋韵) images
using Stable Diffusion + Songyun LoRA. Designed for local use on a GPU machine.
"""

import json
import os
import random
import socket
import sys
from pathlib import Path

import gradio as gr
import torch
from dotenv import load_dotenv
from diffusers import StableDiffusionPipeline

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------

load_dotenv()


def load_config() -> dict:
    """Load and validate configuration from environment variables."""
    device_raw = os.getenv("DEVICE", "").lower()
    if not device_raw:
        device_raw = "cuda" if torch.cuda.is_available() else "cpu"

    root_path = os.getenv("ROOT_PATH", "").strip()
    if root_path and not root_path.startswith("/"):
        root_path = "/" + root_path

    return {
        "base_model_id": os.getenv(
            "BASE_MODEL_ID", "runwayml/stable-diffusion-v1-5"
        ),
        "lora_path": os.getenv("LORA_PATH", "").strip(),
        "device": device_raw,
        "default_negative_prompt": os.getenv(
            "DEFAULT_NEGATIVE_PROMPT",
            "ugly, blurry, low quality, distorted, deformed, watermark, text",
        ),
        "max_image_size": int(os.getenv("MAX_IMAGE_SIZE", "768")),
        # Server / URL settings (for workshop sharing)
        "server_port": int(os.getenv("SERVER_PORT", "8080")),
        "root_path": root_path,
        "app_title": os.getenv("APP_TITLE", "Songyun AI Workshop / 宋韵"),
        "hf_space_url": os.getenv("HF_SPACE_URL", "").strip(),
        # Workshop-friendly defaults
        "default_width": 512,
        "default_height": 512,
        "default_guidance_scale": 7.5,
        "default_steps": 28,
        "default_lora_scale": 0.8,
    }


# Config and constants (loaded once)
CONFIG = load_config()
LORA_ADAPTER_NAME = "songyun"

# Global pipeline (set by model loading)
_pipeline = None
_lora_loaded = False


# -----------------------------------------------------------------------------
# HEALTH CHECK
# -----------------------------------------------------------------------------


def health_check() -> tuple[bool, list[str]]:
    """
    Validate required configuration at startup.
    Returns (success, list of error messages).
    """
    errors = []

    if not CONFIG["base_model_id"]:
        errors.append("BASE_MODEL_ID is not set. Please add it to your .env file.")

    if CONFIG["base_model_id"]:
        # Only validate local paths (not Hugging Face IDs like "org/model")
        base = CONFIG["base_model_id"]
        is_local_path = (
            base.startswith("/")
            or (len(base) > 2 and base[1] == ":" and base[2] in ("/", "\\"))
            or base.startswith(".")
        )
        if is_local_path and not os.path.exists(base):
            errors.append(
                f"Base model path not found: {base}. "
                "Please check BASE_MODEL_ID in .env."
            )

    if CONFIG["lora_path"]:
        if not os.path.exists(CONFIG["lora_path"]):
            errors.append(
                f"LoRA file not found: {CONFIG['lora_path']}. "
                "Please check LORA_PATH in .env, or leave it empty to run without LoRA."
            )
        else:
            path = Path(CONFIG["lora_path"])
            if path.is_file() and path.suffix != ".safetensors":
                errors.append(
                    f"LoRA path should point to a .safetensors file. Got: {path.suffix}"
                )

    if CONFIG["max_image_size"] < 256 or CONFIG["max_image_size"] > 1024:
        errors.append("MAX_IMAGE_SIZE should be between 256 and 1024.")

    return len(errors) == 0, errors


# -----------------------------------------------------------------------------
# MODEL LOADING
# -----------------------------------------------------------------------------


def get_device() -> str:
    """Resolve device: CUDA if available and requested, else CPU."""
    if CONFIG["device"] == "cuda" and torch.cuda.is_available():
        return "cuda"
    return "cpu"


def get_dtype():
    """Use float16 on CUDA for speed, float32 on CPU for compatibility."""
    return torch.float16 if get_device() == "cuda" else torch.float32


def load_pipeline() -> None:
    """Load Stable Diffusion pipeline and optional LoRA. Called once at startup."""
    global _pipeline, _lora_loaded

    device = get_device()
    dtype = get_dtype()
    model_path = CONFIG["base_model_id"]

    _pipeline = StableDiffusionPipeline.from_pretrained(
        model_path,
        torch_dtype=dtype,
        safety_checker=None,
        low_cpu_mem_usage=True,
    )
    _pipeline = _pipeline.to(device)
    if device == "cuda":
        _pipeline.enable_attention_slicing()

    # Load LoRA if configured and valid
    lora_path = CONFIG["lora_path"]
    if lora_path and os.path.exists(lora_path):
        path = Path(lora_path)
        if path.is_file() and path.suffix == ".safetensors":
            pipe_dir = str(path.parent)
            weight_name = path.name
        else:
            pipe_dir = str(path)
            safetensors = list(path.glob("*.safetensors")) if path.is_dir() else []
            weight_name = safetensors[0].name if safetensors else None

        if weight_name:
            _pipeline.load_lora_weights(
                pipe_dir,
                weight_name=weight_name,
                adapter_name=LORA_ADAPTER_NAME,
            )
            _pipeline.set_adapters(
                [LORA_ADAPTER_NAME],
                adapter_weights=[CONFIG["default_lora_scale"]],
            )
            _lora_loaded = True


def _get_local_ip() -> str:
    """Get this machine's local IP for LAN access."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "?"


def log_startup_status(port: int) -> None:
    """Print clear startup status and access URLs."""
    device = get_device()
    root = CONFIG["root_path"] or ""
    local_ip = _get_local_ip()

    print("=" * 60)
    print("  Songyun AI Workshop / 宋韵 AI 工作坊")
    print("=" * 60)
    print(f"  Device:        {device.upper()}")
    print(f"  Base model:    {CONFIG['base_model_id']}")
    print(f"  LoRA loaded:   {'Yes' if _lora_loaded else 'No'}")
    if CONFIG["lora_path"] and not _lora_loaded:
        print(f"  (LoRA path set but not loaded: {CONFIG['lora_path']})")
    print("=" * 60)
    print("  Access URLs (share with workshop participants):")
    print(f"    This machine:  http://localhost:{port}{root}")
    if local_ip != "?":
        print(f"    Same network: http://{local_ip}:{port}{root}")
    print(f"    Public (share): https://[xxx].gradio.live{root}  (see below)")
    print("=" * 60)
    if device == "cpu":
        print(
            "  Note: Running on CPU. Generation will be slow. "
            "A GPU is recommended for workshops."
        )
        print("=" * 60)
    print()


# -----------------------------------------------------------------------------
# PRESETS
# -----------------------------------------------------------------------------


def load_presets() -> list[dict]:
    """Load preset prompts from prompts.json."""
    preset_path = Path(__file__).parent / "prompts.json"
    if not preset_path.exists():
        return []
    try:
        with open(preset_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("prompts", [])
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not load prompts.json: {e}")
        return []


def apply_preset(choice: str, presets: list[dict]) -> str:
    """Return the prompt text for the selected preset."""
    if not choice or not presets:
        return ""
    for p in presets:
        if p.get("name") == choice:
            return p.get("prompt", "")
    return ""


# -----------------------------------------------------------------------------
# GENERATION
# -----------------------------------------------------------------------------


def validate_dimensions(width: int, height: int) -> tuple[bool, str]:
    """Validate width and height."""
    max_size = CONFIG["max_image_size"]
    if width > max_size or height > max_size:
        return False, (
            f"Image size must be at most {max_size} pixels. "
            "Please reduce width or height."
        )
    if width < 64 or height < 64:
        return False, "Image size must be at least 64 pixels."
    return True, ""


def _user_friendly_error(exc: Exception) -> str:
    """Convert technical errors into user-friendly messages."""
    msg = str(exc).lower()
    if "out of memory" in msg or "cuda" in msg:
        return (
            "Your GPU ran out of memory. Try a smaller image size (e.g. 512×512) "
            "or close other programs using the GPU."
        )
    if "no such file" in msg or "not found" in msg:
        return (
            "A required file or model could not be found. "
            "Please ask the workshop host to check the setup."
        )
    if "permission" in msg or "access" in msg:
        return "Permission denied. Check that the model folder is readable."
    return f"Something went wrong: {str(exc)}"


def generate_image(
    prompt: str,
    negative_prompt: str,
    width: int,
    height: int,
    guidance_scale: float,
    num_steps: int,
    seed: int,
    lora_scale: float,
    use_random_seed: bool,
) -> tuple[object, str]:
    """Generate a single image. Returns (PIL.Image or None, status_message)."""
    if _pipeline is None:
        return None, "The model is not ready. Please restart the app and try again."

    ok, err = validate_dimensions(int(width), int(height))
    if not ok:
        return None, err

    if use_random_seed or seed == -1:
        seed = random.randint(0, 2**32 - 1)

    full_prompt = prompt.strip()
    if not full_prompt:
        return None, "Please enter a prompt describing the image you want."

    if _lora_loaded and "songyun" not in full_prompt.lower():
        full_prompt = f"songyun, {full_prompt}"

    neg = negative_prompt.strip() or CONFIG["default_negative_prompt"]

    try:
        if _lora_loaded:
            _pipeline.set_adapters(
                [LORA_ADAPTER_NAME], adapter_weights=[lora_scale]
            )

        generator = torch.Generator(device=get_device()).manual_seed(int(seed))

        output = _pipeline(
            prompt=full_prompt,
            negative_prompt=neg,
            width=int(width),
            height=int(height),
            guidance_scale=guidance_scale,
            num_inference_steps=int(num_steps),
            generator=generator,
        )

        image = output.images[0]
        return image, f"Done! Seed used: {seed}"

    except torch.cuda.OutOfMemoryError:
        return None, (
            "Your GPU ran out of memory. Try a smaller image size (e.g. 512×512) "
            "or close other programs using the GPU."
        )
    except Exception as e:
        return None, _user_friendly_error(e)


# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------

CUSTOM_CSS = """
    .section-card, .output-card {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 1.25rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    }
    .section-title {
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 1px solid #f1f5f9 !important;
    }
    .output-card { min-height: 420px !important; }
    .songyun-footer {
        text-align: center !important;
        font-size: 0.75rem !important;
        color: #64748b !important;
        margin-top: 2rem !important;
        padding: 1.25rem !important;
        border-top: 1px solid #e2e8f0 !important;
        background: #f8fafc !important;
    }
    .gradio-container, .contain, main { background: #f8fafc !important; }
"""

HELP_MARKDOWN = """
### What is 宋韵 / Songyun?

**Songyun (宋韵)** is a lightweight LoRA model based on Stable Diffusion, aiming to generate painting works of traditional Chinese culture in the style of the Song Dynasty (960–1279).

**宋韵 LoRA** 是一个基于 Stable Diffusion 的轻量化模型，旨在生成具有宋代风格的传统中华文化绘画作品。

---

### Purpose / 用途

**English:** Suitable for generating illustrations in the style of the Song Dynasty, artistic creations, cultural promotional posters, cultural and creative designs, etc.

**中文:** 适合生成宋代风格的插画、艺术创作、文化宣传画、文创设计等。

---

### Features / 特点

- Elegant lines, soft colors and delicate textures in Song Dynasty paintings  
- Typical themes: landscape paintings (山水画), flower-and-bird paintings (花鸟画)  
- Supports personalized adjustments to generation intensity and resolution  

- 模仿宋代绘画中的优雅线条、柔和色彩和细致纹理  
- 能够表现山水画、花鸟画等典型宋代题材  
- 支持用户个性化调整生成强度和分辨率  

---

### Usage Scenarios / 使用场景

- Creation of ancient-style illustrations / 古风插画创作  
- Display of traditional culture / 传统文化展示  
- Design of cultural and creative products / 文创产品设计  
- Game art / 游戏美术  

---

### Usage Instructions / 使用说明

**1. Model loading:** Place the Songyun LoRA model in the LoRA folder.  
**模型加载:** 将宋韵 LoRA 模型放入 Stable Diffusion 的 LoRA 文件夹。

**2. Trigger words:** Select LoRA model `songyun-v3`, or add `songyun` or `songyun-v3:1.0` in prompt.  
**触发词使用:** 选择 Lora 模型 songyun-v3，或在 prompt 中添加对应 tag 以触发模型生成宋代风格绘画效果。

**3. Recommended settings:**  
**推荐设置:**  
- **LoRA strength:** 0.7–0.9 (效果最佳)  
- **Resolution:** 512×512 (推荐，有助于提升细节效果)  
- **Base model:** Stable Diffusion v1.5, recommended dreamshaper_8.safetensors  

---

### How to use preset prompts

1. Open the **"Preset"** dropdown below.
2. Select a preset (e.g. "Misty mountains" or "Scholar by the river").
3. The prompt will be filled in automatically. You can edit it if you like.
4. Click **Generate** to create your image.

---

### Tips

- **Prompt:** Describes what you want (e.g. mountains, pavilion, scholar).
- **LoRA strength:** 0.7–0.9 works best for Songyun style.
- Try different combinations to get the look you want.
"""


PUBLIC_LINK_FILE = Path(__file__).parent / "PUBLIC_LINK.txt"


def get_share_link() -> str:
    """Get the public share URL. Prefer HF Space (24/7) over local Gradio tunnel."""
    if CONFIG.get("hf_space_url"):
        return CONFIG["hf_space_url"]
    if PUBLIC_LINK_FILE.exists():
        try:
            return PUBLIC_LINK_FILE.read_text(encoding="utf-8").strip()
        except Exception:
            pass
    return ""


def get_reset_values() -> list:
    """Return default values for reset button."""
    return [
        "",
        CONFIG["default_negative_prompt"],
        CONFIG["default_width"],
        CONFIG["default_height"],
        CONFIG["default_guidance_scale"],
        CONFIG["default_steps"],
        -1,
        CONFIG["default_lora_scale"],
        True,
    ]


def build_ui():
    """Build the Gradio interface."""
    presets = load_presets()
    preset_names = [p["name"] for p in presets] if presets else ["(No presets)"]
    cfg = CONFIG

    with gr.Blocks(title=cfg.get("app_title", "Songyun AI Workshop / 宋韵")) as demo:
        gr.HTML(
            """
            <div id="songyun-header" data-version="2" style="
                text-align: center;
                padding: 1.75rem 2rem;
                margin: -1rem -1rem 1.5rem -1rem;
                background: #ffffff;
                border-bottom: 1px solid #e2e8f0;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            ">
                <div style="font-size: 1.5rem; font-weight: 600; color: #0f172a; margin: 0 0 0.25rem 0;">Songyun AI Workshop</div>
                <div class="sub" style="font-size: 0.95rem; color: #64748b; margin-top: 0.2rem;">宋韵 AI 工作坊</div>
                <div class="sub" style="font-size: 0.8rem; color: #64748b; margin-top: 0.5rem;">Traditional Chinese Song Dynasty style image generation</div>
            </div>
            """
        )

        with gr.Accordion("About Songyun (宋韵)", open=False, elem_id="about-songyun"):
            gr.Markdown(HELP_MARKDOWN)

        with gr.Row():
            # Left column: controls
            with gr.Column(scale=1):
                with gr.Group(elem_classes=["section-card"]):
                    gr.HTML('<div class="section-title">Prompt</div>')
                    prompt = gr.Textbox(
                        label="Describe your image",
                        placeholder="e.g. misty mountains, ink wash, literati style...",
                        lines=3,
                        show_label=True,
                    )
                    preset_dropdown = gr.Dropdown(
                        choices=preset_names,
                        label="Preset",
                        value=preset_names[0] if preset_names else None,
                    )
                    negative_prompt = gr.Textbox(
                        label="Negative prompt",
                        placeholder="What to avoid...",
                        value=cfg["default_negative_prompt"],
                        lines=2,
                    )

                with gr.Group(elem_classes=["section-card"]):
                    gr.HTML('<div class="section-title">Image</div>')
                    with gr.Row():
                        width = gr.Slider(
                            minimum=64,
                            maximum=cfg["max_image_size"],
                            value=cfg["default_width"],
                            step=64,
                            label="Width",
                        )
                        height = gr.Slider(
                            minimum=64,
                            maximum=cfg["max_image_size"],
                            value=cfg["default_height"],
                            step=64,
                            label="Height",
                        )
                    guidance_scale = gr.Slider(
                        minimum=1.0,
                        maximum=20.0,
                        value=cfg["default_guidance_scale"],
                        step=0.5,
                        label="Guidance scale",
                    )
                    num_steps = gr.Slider(
                        minimum=10,
                        maximum=50,
                        value=cfg["default_steps"],
                        step=1,
                        label="Steps",
                    )

                with gr.Accordion("Advanced", open=False):
                    lora_scale = gr.Slider(
                        minimum=0.0,
                        maximum=1.5,
                        value=cfg["default_lora_scale"],
                        step=0.05,
                        label="LoRA strength (0.7–0.9 for Songyun)",
                    )
                    use_random_seed = gr.Checkbox(
                        label="Random seed",
                        value=True,
                    )
                    seed = gr.Number(
                        label="Seed",
                        value=-1,
                        precision=0,
                    )

                with gr.Row():
                    generate_btn = gr.Button("Generate", variant="primary", elem_classes=["primary-btn"])
                    reset_btn = gr.Button("Reset")

            # Right column: output + help
            with gr.Column(scale=1):
                with gr.Group(elem_classes=["output-card"]):
                    output_image = gr.Image(
                        label="Output",
                        type="pil",
                        height=380,
                    )
                    status = gr.Textbox(
                        label="Status",
                        value="Ready. Enter a prompt and click Generate.",
                        interactive=False,
                    )

                with gr.Group(elem_classes=["section-card"]):
                    gr.HTML(
                        '<div class="section-title">External Share Link (24/7, no PC needed)</div>'
                    )
                    share_msg = get_share_link()
                    if not share_msg and os.getenv("SPACE_ID"):
                        share_msg = "https://huggingface.co/spaces/DiBuffed/songyun-ai-workshop"
                    if not share_msg:
                        share_msg = "Shown here when you run the app via run.bat."
                    share_link_display = gr.Textbox(
                        label="Public Link",
                        value=share_msg,
                        interactive=False,
                        max_lines=2,
                    )
                    def refresh_share_link():
                        url = get_share_link()
                        if url:
                            return url
                        if os.getenv("SPACE_ID"):
                            return "https://huggingface.co/spaces/DiBuffed/songyun-ai-workshop"
                        return "Not yet generated. Make sure you started the app via run.bat."

                    gr.Button("Refresh Link").click(
                        fn=refresh_share_link,
                        inputs=[],
                        outputs=[share_link_display],
                    )

        gr.HTML(
            """
            <div class="songyun-footer" style="
                text-align: center;
                font-size: 0.75rem;
                color: #64748b;
                margin-top: 2rem;
                padding: 1.25rem;
                border-top: 1px solid #e2e8f0;
                background: #f8fafc;
            ">
                Songyun AI Workshop — Local demo for 宋韵 image generation<br>
                <span style="font-size:0.65rem;opacity:0.8">UI v4 · Songyun LoRA info · 2025-03-08</span>
            </div>
            """
        )

        # Wire preset dropdown
        preset_dropdown.change(
            fn=lambda c: apply_preset(c, presets),
            inputs=[preset_dropdown],
            outputs=[prompt],
        )

        # Wire reset
        reset_btn.click(
            fn=get_reset_values,
            inputs=[],
            outputs=[
                prompt,
                negative_prompt,
                width,
                height,
                guidance_scale,
                num_steps,
                seed,
                lora_scale,
                use_random_seed,
            ],
        )

        # Wire generate
        generate_btn.click(
            fn=generate_image,
            inputs=[
                prompt,
                negative_prompt,
                width,
                height,
                guidance_scale,
                num_steps,
                seed,
                lora_scale,
                use_random_seed,
            ],
            outputs=[output_image, status],
        )

    return demo


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------


def main():
    """Entry point: health check, load model, build UI, launch."""
    # Fix console encoding for Unicode (e.g. 宋韵) on Windows
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    ok, errors = health_check()
    if not ok:
        print("Configuration errors:")
        for e in errors:
            print(f"  • {e}")
        print("\nPlease fix your .env file and try again.")
        sys.exit(1)

    print("Loading model (this may take a minute on first run)...")
    try:
        load_pipeline()
    except FileNotFoundError as e:
        print(f"Error: Model or LoRA file not found. {e}")
        print("Check BASE_MODEL_ID and LORA_PATH in your .env file.")
        sys.exit(1)
    except Exception as e:
        import traceback
        print(f"Error loading model: {e}")
        traceback.print_exc()
        sys.exit(1)

    port = CONFIG["server_port"]
    log_startup_status(port)

    demo = build_ui()
    css_path = Path(__file__).parent / "custom.css"
    head_content = '<style>#songyun-header div{color:#0f172a!important}#songyun-header .sub{color:#64748b!important}</style>'

    # Hugging Face Spaces: simple launch (Spaces handles URL, port, etc.)
    if os.getenv("SPACE_ID"):
        demo.launch(
            theme=gr.themes.Soft(primary_hue="blue", secondary_hue="slate"),
            css_paths=[str(css_path)] if css_path.exists() else None,
            head=head_content,
        )
    else:
        demo.launch(
            server_name="0.0.0.0",
            server_port=port,
            root_path=CONFIG["root_path"] or None,
            share=True,
            theme=gr.themes.Soft(primary_hue="blue", secondary_hue="slate"),
            css_paths=[str(css_path)] if css_path.exists() else None,
            head=head_content,
        )


if __name__ == "__main__":
    main()
