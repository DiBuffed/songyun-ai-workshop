"""Pre-download model during Docker build. Run by Dockerfile."""
from diffusers import StableDiffusionPipeline

StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype="float32",
    safety_checker=None,
    low_cpu_mem_usage=True,
)
print("Model cached for runtime.")
