# 다음 단계 (Next Steps)

## ✅ 완료된 것
- [x] GitHub 푸시: https://github.com/DiBuffed/songyun-ai-workshop
- [x] Hugging Face Space: https://huggingface.co/spaces/DiBuffed/songyun-ai-workshop (24/7)
- [x] 로컬 실행: `run.bat` → Gradio 앱

---

## 1. Railway 배포 (선택)

일반 웹사이트처럼 `https://xxx.railway.app` 주소로 24/7 서비스하려면:

1. [Railway](https://railway.app) 가입
2. **New Project** → **Deploy from GitHub repo**
3. `DiBuffed/songyun-ai-workshop` 선택
4. 배포 완료 후 생성된 URL 사용

자세한 내용: `Railway_배포_가이드.md`

---

## 2. HF Space 업데이트

코드 변경 후 Space에 반영하려면:

- **웹 업로드:** https://huggingface.co/spaces/DiBuffed/songyun-ai-workshop → Files → Upload
- **스크립트:** `Space_업로드.bat` 실행 (HF 토큰을 `hf_token.txt`에 붙여넣기)

---

## 3. GitHub 업데이트

수정 후 푸시:

```bash
git add .
git commit -m "설명"
git push
```

---

## 4. 워크숍 준비

- **로컬:** `run.bat` 실행 → 학생들에게 `http://localhost:8080` 또는 Gradio 공유 링크 전달
- **온라인:** HF Space 링크 공유 → PC 없이 브라우저만으로 접속 가능
