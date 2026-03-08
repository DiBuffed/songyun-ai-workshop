# Songyun AI Workshop - 빠른 시작

## 한 줄로 실행 (Windows)

프로젝트 폴더에서 **명령 프롬프트**나 **PowerShell**을 열고:

```
run.bat
```

또는 **run.bat** 파일을 더블클릭하세요.

---

## 처음 실행 시

1. 가상환경 생성
2. 패키지 설치 (몇 분 소요)
3. `.env` 자동 생성
4. 앱 실행

**첫 실행 시** base 모델 다운로드(~4GB)로 5~10분 정도 걸릴 수 있습니다.

---

## 접속 주소

### 24/7 공개 링크 (PC 없이 누구나 접속)
**https://huggingface.co/spaces/DiBuffed/songyun-ai-workshop**

### 로컬 실행 시
- 이 PC: `http://localhost:8080`
- 같은 네트워크: `http://<이 PC IP>:8080`
- Gradio 터널: 팝업 및 PUBLIC_LINK.txt (앱 실행 중에만 유효)

**로딩이 안 될 때:** `run_fresh.bat` 실행 후 새 링크로 접속, 브라우저에서 Ctrl+Shift+R 강력 새로고침.

---

## 필요 사항

- **Python 3.10+** ([python.org](https://python.org)에서 설치)
- **GPU** (권장, CPU도 가능하지만 느림)
