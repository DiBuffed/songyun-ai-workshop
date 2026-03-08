# 접속 안 될 때 / MemoryError

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
