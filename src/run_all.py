import os
import re
import json
import subprocess
from pathlib import Path


def extract_json_from_output(output: str) -> str:
    """
    main.py 전체 출력에서 JSON 부분만 추출.
    '[' 또는 '{'로 시작해 마지막 ']' 또는 '}'로 끝나는 블록만 반환.
    """
    start = re.search(r"[\[\{]", output)
    if not start:
        return ""
    start_idx = start.start()
    end_idx = max(output.rfind("]"), output.rfind("}"))
    if end_idx == -1:
        return ""
    return output[start_idx : end_idx + 1].strip()


# --- 경로 설정 ---
base_dir = Path(__file__).resolve().parent
bank_dir = base_dir.parent / "bank"
prompt_dir = bank_dir / "prompt"
save_dir = base_dir.parent / "save"
save_dir.mkdir(exist_ok=True)

# --- prompt 파일 전부 순회 ---
for prompt_file in prompt_dir.glob("*_prompt.txt"):
    prefix = prompt_file.stem.replace("_prompt", "")  # ex) LC_A_ADV
    comprehension_type, problem_type, level = prefix.split("_")

    result_path = save_dir / f"{prefix}_result.json"
    print(f">>> Running {prefix} -> {result_path}")

    # main.py 실행 (현재 src에 있다고 가정)
    cmd = [
        "python",
        "main.py",
        "--comprehension_type",
        comprehension_type,
        "--problem_type",
        problem_type,
        "--level",
        level,
    ]

    process = subprocess.run(
        cmd,
        cwd=base_dir,
        text=True,
        capture_output=True,
    )

    if process.returncode != 0:
        print(f"!!! ERROR on {prefix}")
        print(process.stderr)
        continue

    # 표준출력에서 JSON만 추출
    json_str = extract_json_from_output(process.stdout)

    if not json_str:
        print(f"!!! No valid JSON found in output for {prefix}")
        continue

    # 실제 JSON 저장
    with open(result_path, "w", encoding="utf-8") as f_out:
        f_out.write(json_str)

    print(f">>> Done: {result_path}\n")

print("=== ALL DONE ===")
