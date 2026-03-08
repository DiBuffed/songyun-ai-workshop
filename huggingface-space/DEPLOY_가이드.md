# Hugging Face Spaces 배포 가이드

## 1단계: Hugging Face 계정

1. [huggingface.co](https://huggingface.co) 접속
2. **Sign Up** → 이메일로 가입

---

## 2단계: 새 Space 생성

1. 로그인 후 오른쪽 상단 **+** → **Create new Space**
2. 설정:
   - **Space name:** `songyun-ai-workshop` (원하는 이름)
   - **License:** MIT
   - **Select the Space SDK:** **Gradio**
   - **Space hardware:** **CPU basic** (무료) 또는 **GPU** (유료)
3. **Create Space** 클릭

---

## 3단계: 파일 업로드

**`huggingface-space` 폴더에서 아래 5개 파일만 Space에 업로드하세요.**  
*(DEPLOY_가이드.md는 업로드하지 않아도 됩니다.)*

| 파일 | 설명 |
|------|------|
| `app.py` | 메인 앱 |
| `requirements.txt` | 패키지 목록 |
| `prompts.json` | 프리셋 프롬프트 |
| `custom.css` | 스타일 |
| `README.md` | Space 설명 (HF 메타데이터 포함) |

**방법 A – 웹에서 업로드**
1. Space 페이지에서 **Files** 탭
2. **Add file** → **Upload files**
3. 위 파일들을 드래그 앤 드롭
4. **Commit changes to main**

**방법 B – Git으로 업로드**
```bash
git clone https://huggingface.co/spaces/당신사용자명/songyun-ai-workshop
cd songyun-ai-workshop
# app.py, requirements.txt, prompts.json, custom.css, README.md 복사
git add .
git commit -m "Add Songyun AI Workshop"
git push
```

---

## 4단계: 빌드 대기

- 업로드 후 Space가 자동으로 빌드됩니다 (5~10분)
- **Building** → **Running** 상태가 되면 완료
- Space URL: `https://huggingface.co/spaces/당신사용자명/songyun-ai-workshop`

---

## 5단계: 접속

- PC를 꺼도 24시간 접속 가능
- 무료 CPU는 이미지 1장당 1~3분 정도 소요

---

## 문제 해결

| 증상 | 해결 |
|------|------|
| 빌드 실패 | requirements.txt 버전 확인, Space 로그 확인 |
| 메모리 부족 | CPU basic 사용 시 512×512 권장 |
| 느림 | GPU 업그레이드 (유료) |
