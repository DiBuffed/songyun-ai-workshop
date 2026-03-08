# 접속 안 될 때 / MemoryError

## Fetching 0%에서 멈출 때 (다운로드 느림/멈춤)

모델 다운로드가 0%에서 진행되지 않을 때:

### 1. .env에 HF 미러 추가 (가장 효과적)

`.env` 파일을 열고 다음 줄을 **맨 위에** 추가:

```
HF_ENDPOINT=https://hf-mirror.com
```

저장 후 `run.bat` 다시 실행.

### 2. 모델 미리 다운로드

`download_model.bat` 실행 → 다운로드 완료 대기 → `run.bat` 실행

(첫 실행 시 venv 필요. `run.bat` 한 번 실행 후 사용)

### 3. HF 토큰 (선택)

[huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)에서 토큰 생성 후 `.env`에:

```
HF_TOKEN=hf_xxxx
```

---

## MemoryError (메모리 부족)

모델 로딩 시 **MemoryError**가 나면 RAM이 부족한 상태입니다.

### 해결 방법

1. **다른 프로그램 종료**
   - Chrome, 게임, 동영상 편집 등 메모리를 많이 쓰는 프로그램을 모두 종료한 뒤 다시 실행해보세요.

2. **RAM 확인**
   - Stable Diffusion 모델 로딩에는 **최소 8GB, 권장 16GB** 이상의 RAM이 필요합니다.
   - 작업 관리자 → 성능 → 메모리에서 사용 가능한 RAM을 확인하세요.

3. **모델 변경**
   - `.env`에서 `BASE_MODEL_ID`를 다음 중 하나로 바꿔보세요:
   ```
   BASE_MODEL_ID=runwayml/stable-diffusion-v1-5
   ```
   또는
   ```
   BASE_MODEL_ID=Lykon/dreamshaper-8
   ```
   (Hugging Face에서 자동 다운로드)

4. **다른 PC 사용**
   - RAM이 16GB 이상인 PC에서 실행해보세요.

---

## 접속 주소

앱이 정상 실행되면:

- **이 PC**: http://localhost:8080/songyun-ai-workshop
- **같은 네트워크**: http://<이 PC IP>:8080/songyun-ai-workshop
- **인터넷 공유**: 콘솔에 표시되는 `https://xxx.gradio.live/songyun-ai-workshop`

**ROOT_PATH**를 비워두면: `http://localhost:8080` (경로 없이 접속)
