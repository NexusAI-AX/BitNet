import os
import sys
import signal
import platform
import argparse
import subprocess

# 이 스크립트는 bitnet.cpp에서 제공하는 `llama-cli` 실행 파일을 호출해
# 간단한 추론을 실행합니다. 명령 줄 인자를 받아 실행 명령을 구성하고
# 필요에 따라 채팅 모드를 켜 줍니다.

def run_command(command, shell=False):
    """주어진 시스템 명령을 실행하고 오류가 나면 바로 종료합니다."""
    try:
        subprocess.run(command, shell=shell, check=True)
    except subprocess.CalledProcessError as e:
        # 명령 실행 중 오류가 발생하면 메시지를 출력하고 프로그램 종료
        print(f"Error occurred while running command: {e}")
        sys.exit(1)

def run_inference():
    """llama-cli 실행 명령을 구성하고 실행한다."""
    build_dir = "build"  # 빌드가 생성되는 기본 폴더
    # 운영 체제에 따라 실행 파일 위치가 달라질 수 있다
    if platform.system() == "Windows":
        # Windows 빌드에서는 Release 폴더 안에 실행 파일이 있음
        main_path = os.path.join(build_dir, "bin", "Release", "llama-cli.exe")
        if not os.path.exists(main_path):
            # 없으면 일반 폴더에서 찾는다
            main_path = os.path.join(build_dir, "bin", "llama-cli")
    else:
        # 리눅스/맥에서는 바로 bin 디렉터리 안에 위치
        main_path = os.path.join(build_dir, "bin", "llama-cli")

    # llama-cli에 전달할 인자들을 순서대로 모아 실행 명령을 만든다
    command = [
        f'{main_path}',        # 실행 파일 경로
        '-m', args.model,      # 사용할 모델 파일
        '-n', str(args.n_predict),  # 생성할 토큰 수
        '-t', str(args.threads),    # 사용할 스레드 수
        '-p', args.prompt,     # 입력 프롬프트
        '-ngl', '0',           # GPU 비활성화
        '-c', str(args.ctx_size),   # 프롬프트 컨텍스트 크기
        '--temp', str(args.temperature),  # 생성 온도
        "-b", "1",            # 배치 크기 1로 고정
    ]
    # 채팅 모드가 필요한지 확인 후 옵션을 추가한다
    if args.conversation:
        command.append("-cnv")  # 대화형 모드

    # 준비된 명령을 실행
    run_command(command)

def signal_handler(sig, frame):
    """Ctrl+C 입력 시 깔끔하게 종료하기 위한 핸들러"""
    print("Ctrl+C pressed, exiting...")
    sys.exit(0)

if __name__ == "__main__":
    # Ctrl+C가 눌렸을 때 signal_handler를 호출하도록 등록
    signal.signal(signal.SIGINT, signal_handler)

    # 실행 시 사용할 인자 정의
    # 예시: python run_inference.py -p "Hello" -cnv
    # 명령줄 인자를 받을 파서
    parser = argparse.ArgumentParser(description='Run inference')

    # 모델 파일 경로
    parser.add_argument("-m", "--model", type=str,
                        help="Path to model file",
                        required=False,
                        default="models/bitnet_b1_58-3B/ggml-model-i2_s.gguf")

    # 생성할 토큰 수
    parser.add_argument("-n", "--n-predict", type=int,
                        help="Number of tokens to predict when generating text",
                        required=False, default=128)

    # 입력 프롬프트
    parser.add_argument("-p", "--prompt", type=str,
                        help="Prompt to generate text from", required=True)

    # 사용 스레드 수
    parser.add_argument("-t", "--threads", type=int,
                        help="Number of threads to use",
                        required=False, default=2)

    # 컨텍스트 크기
    parser.add_argument("-c", "--ctx-size", type=int,
                        help="Size of the prompt context",
                        required=False, default=2048)

    # 생성 온도
    parser.add_argument("-temp", "--temperature", type=float,
                        help="Temperature, a hyperparameter that controls the randomness of the generated text",
                        required=False, default=0.8)

    # 채팅 모드 사용 여부
    parser.add_argument("-cnv", "--conversation", action='store_true',
                        help="Whether to enable chat mode or not (for instruct models.)")

    args = parser.parse_args()  # 위에서 정의한 옵션을 파싱
    run_inference()             # 실제 추론 실행
