# bitnet.cpp 한국어 안내

이 프로젝트는 1비트 LLM(예: BitNet b1.58)을 위한 공식 추론 프레임워크입니다. CPU와 GPU에서 빠르고 손실 없는 추론을 제공하도록 최적화된 커널을 포함합니다.

## 빌드 방법

1. 저장소 클론
```bash
git clone --recursive https://github.com/microsoft/BitNet.git
cd BitNet
```

2. 의존성 설치(권장: conda 환경)
```bash
conda create -n bitnet-cpp python=3.9
conda activate bitnet-cpp
pip install -r requirements.txt
```

3. 모델 다운로드 및 환경 설정
```bash
huggingface-cli download microsoft/BitNet-b1.58-2B-4T-gguf --local-dir models/BitNet-b1.58-2B-4T
python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s
```

## 추론 실행

### 명령줄에서 실행
```bash
python run_inference.py -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf -p "당신은 도움이 되는 어시스턴트입니다" -cnv
```
주요 옵션:
- `-m`, `--model`: 모델 파일 경로
- `-p`, `--prompt`: 입력 프롬프트
- `-n`, `--n-predict`: 생성할 토큰 수

### 서버 모드 실행
```bash
python run_inference_server.py -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf --host 0.0.0.0 --port 8080
```
서버가 시작되면 지정한 호스트와 포트로 API 호출을 할 수 있습니다.

