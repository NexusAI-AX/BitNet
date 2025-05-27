import os
import sys
import signal
import platform
import argparse
import subprocess

# 간단한 서버를 실행하기 위한 스크립트

def run_command(command, shell=False):
    """시스템 명령을 실행하고 실패하면 종료한다."""
    try:
        subprocess.run(command, shell=shell, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running command: {e}")
        sys.exit(1)

def run_server():
    """llama-server 실행 명령을 구성하고 실행한다."""
    build_dir = "build"  # 빌드 디렉터리
    if platform.system() == "Windows":
        # Windows에서는 Release 폴더를 우선 확인
        server_path = os.path.join(build_dir, "bin", "Release", "llama-server.exe")
        if not os.path.exists(server_path):
            # 없으면 기본 경로에서 찾는다
            server_path = os.path.join(build_dir, "bin", "llama-server")
    else:
        # 기타 OS는 bin 폴더 안에 위치
        server_path = os.path.join(build_dir, "bin", "llama-server")
    
    # 서버 실행을 위한 명령어 목록
    command = [
        f'{server_path}',                # 실행 파일 위치
        '-m', args.model,                # 모델 파일
        '-c', str(args.ctx_size),        # 컨텍스트 크기
        '-t', str(args.threads),         # 스레드 수
        '-n', str(args.n_predict),       # 예측 토큰 수
        '-ngl', '0',                     # GPU 비활성화
        '--temp', str(args.temperature), # 샘플링 온도
        '--host', args.host,             # 서버 주소
        '--port', str(args.port),        # 포트 번호
        '-cb'                            # 지속 배칭 활성화
    ]
    
    if args.prompt:
        # 시스템 프롬프트가 있을 경우 함께 전달
        command.extend(['-p', args.prompt])
    
    # Note: -cnv flag is removed as it's not supported by the server
    
    print(f"Starting server on {args.host}:{args.port}")  # 실행 정보 출력
    run_command(command)

def signal_handler(sig, frame):
    """Ctrl+C를 누르면 서버를 종료하기 위한 핸들러"""
    print("Ctrl+C pressed, shutting down server...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    # 명령줄 파서 준비
    parser = argparse.ArgumentParser(description='Run llama.cpp server')
    parser.add_argument("-m", "--model", type=str, help="Path to model file", required=False, default="models/bitnet_b1_58-3B/ggml-model-i2_s.gguf")
    parser.add_argument("-p", "--prompt", type=str, help="System prompt for the model", required=False)
    parser.add_argument("-n", "--n-predict", type=int, help="Number of tokens to predict", required=False, default=4096)
    parser.add_argument("-t", "--threads", type=int, help="Number of threads to use", required=False, default=2)
    parser.add_argument("-c", "--ctx-size", type=int, help="Size of the context window", required=False, default=2048)
    parser.add_argument("--temperature", type=float, help="Temperature for sampling", required=False, default=0.8)
    parser.add_argument("--host", type=str, help="IP address to listen on", required=False, default="127.0.0.1")
    parser.add_argument("--port", type=int, help="Port to listen on", required=False, default=8080)

    args = parser.parse_args()  # 인자 파싱
    run_server()                # 서버 시작
