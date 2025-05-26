# bitnet.cpp 추론을 간단히 실행하는 스크립트
import os
import sys
import signal
import platform
import argparse
import subprocess

# 이 스크립트는 bitnet.cpp에서 제공하는 `llama-cli` 실행 파일을 호출하여
# 간단히 추론(inference)을 수행합니다.
# 파이썬에서 명령 줄 인자를 받아 실제 실행 명령을 만들어 주고,
# 필요하면 채팅(conversation) 모드를 켜는 역할을 합니다.

def run_command(command, shell=False):
    """주어진 시스템 명령을 실행하고 오류 발생 시 종료합니다."""
    try:
        subprocess.run(command, shell=shell, check=True)
    except subprocess.CalledProcessError as e:
        # 명령 실행 중 오류가 발생하면 메시지를 출력하고 프로그램 종료
        print(f"Error occurred while running command: {e}")
        sys.exit(1)

def run_inference():
    """llama-cli 실행 명령을 구성하여 실행합니다."""
    build_dir = "build"
    # 운영 체제에 따라 실행 파일 위치가 달라질 수 있음
    if platform.system() == "Windows":
        main_path = os.path.join(build_dir, "bin", "Release", "llama-cli.exe")
        if not os.path.exists(main_path):
            # Release 디렉터리에 없다면 일반 경로에서 찾음
            main_path = os.path.join(build_dir, "bin", "llama-cli")
    else:
        main_path = os.path.join(build_dir, "bin", "llama-cli")

    # llama-cli에 전달할 인자들을 순서대로 나열
    command = [
        f'{main_path}',        # 실행 파일 경로
        '-m', args.model,      # 모델 파일 경로
        '-n', str(args.n_predict),
        '-t', str(args.threads),
        '-p', args.prompt,     # 프롬프트
        '-ngl', '0',           # GPU 사용 안 함
        '-c', str(args.ctx_size),
        '--temp', str(args.temperature),
        "-b", "1",
    ]
    # 채팅 모드가 필요하면 옵션 추가
    if args.conversation:
        command.append("-cnv")

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
    parser = argparse.ArgumentParser(description='Run inference')
    parser.add_argument("-m", "--model", type=str,
                        help="Path to model file",
                        required=False,
                        default="models/bitnet_b1_58-3B/ggml-model-i2_s.gguf")
    parser.add_argument("-n", "--n-predict", type=int,
                        help="Number of tokens to predict when generating text",
                        required=False, default=128)
    parser.add_argument("-p", "--prompt", type=str,
                        help="Prompt to generate text from", required=True)
    parser.add_argument("-t", "--threads", type=int,
                        help="Number of threads to use",
                        required=False, default=2)
    parser.add_argument("-c", "--ctx-size", type=int,
                        help="Size of the prompt context",
                        required=False, default=2048)
    parser.add_argument("-temp", "--temperature", type=float,
                        help="Temperature, a hyperparameter that controls the randomness of the generated text",
                        required=False, default=0.8)
    parser.add_argument("-cnv", "--conversation", action='store_true',
                        help="Whether to enable chat mode or not (for instruct models.)")

    args = parser.parse_args()
    run_inference()
