# Railway 배포 가이드

일반 사이트처럼 `https://xxx.up.railway.app` 주소로 24시간 접속 가능하게 합니다.

---

## 1단계: Railway 계정

1. [railway.app](https://railway.app) 접속
2. **Login** → GitHub로 가입/로그인

---

## 2단계: GitHub에 코드 올리기

1. [github.com](https://github.com) 로그인
2. **New repository** → 이름: `songyun-ai-workshop`
3. **Create repository**
4. 아래 파일들을 업로드 (또는 Git으로 push):
   - `app.py`
   - `requirements.txt`
   - `prompts.json`
   - `custom.css`
   - `Procfile`
   - `runtime.txt`

---

## 3단계: Railway에서 배포

1. [railway.app/new](https://railway.app/new) 접속
2. **Deploy from GitHub repo** 선택
3. `songyun-ai-workshop` 저장소 선택
4. **Deploy** 클릭
5. 배포가 시작됩니다 (첫 빌드 10~20분 소요)

---

## 4단계: 도메인 확인

1. Railway 대시보드 → 프로젝트 클릭
2. **Settings** → **Networking** → **Generate Domain**
3. `https://xxx.up.railway.app` 형태의 URL 생성됨
4. 이 링크로 누구나 접속 가능

---

## 5단계: 환경 변수 (선택)

Railway 대시보드 → **Variables**에서 설정:

| 변수 | 값 | 설명 |
|------|-----|------|
| `BASE_MODEL_ID` | `runwayml/stable-diffusion-v1-5` | 기본값 사용 시 생략 가능 |
| `HF_SPACE_URL` | `https://huggingface.co/spaces/DiBuffed/songyun-ai-workshop` | 앱 내 링크 표시용 |

---

## 참고

- **무료 크레딧**: Railway는 월 $5 크레딧 제공 (소규모 앱 가능)
- **메모리**: Stable Diffusion은 4GB+ 필요 → 유료 플랜 권장
- **첫 배포**: 모델 다운로드로 15~30분 걸릴 수 있음

---

## 문제 해결

| 증상 | 해결 |
|------|------|
| 빌드 실패 | Logs에서 에러 확인, requirements.txt 버전 조정 |
| 메모리 부족 | Railway 유료 플랜 또는 HF Space 사용 |
| 502 에러 | 앱 시작 대기 (모델 로딩 시간) |
