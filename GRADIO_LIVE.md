# gradio.live 링크 얻기 (가장 간단한 공개 URL)

**목표:** `https://xxxxx.gradio.live` 형태의 링크로 누구나 접속 가능하게 하기

---

## 1단계: run.bat 실행

프로젝트 폴더에서 **run.bat** 더블클릭 (또는 터미널에서 `run.bat`)

---

## 2단계: 대기

- **첫 실행:** 모델 다운로드로 5~10분 소요
- "Loading model (this may take a minute on first run)..." 메시지 후
- "Running on public URL: https://xxxxx.gradio.live" 출력되면 완료

---

## 3단계: 링크 복사

- **팝업**이 뜨면 그 안의 URL 복사
- 또는 **PUBLIC_LINK.txt** 파일 열어서 URL 복사

---

## 주의사항

| 상황 | 설명 |
|------|------|
| 링크가 500 에러 | 앱이 꺼졌거나 PC가 절전 모드. **run.bat 다시 실행** |
| 링크 유효 기간 | PC가 켜져 있는 동안 유효 (최대 72시간) |
| 24/7 필요 | PC 항상 켜두거나, Hugging Face Space / Railway 배포 |

---

## .env 설정 (문제 있을 때)

`.env` 파일에서:

- **ROOT_PATH=** (비워두기) → `https://xxx.gradio.live/` 로 바로 접속
- **BASE_MODEL_ID=runwayml/stable-diffusion-v1-5** → 첫 로딩 더 빠름
