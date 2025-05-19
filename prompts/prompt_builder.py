# prompt_builder.py

from pathlib import Path

def normalize_key(key: str) -> str:
    """
    key 문자열에서 괄호나 공백 제거 등으로 파일명과 매칭되게 변환
    """
    return key.strip()

from pathlib import Path

def load_prompt(category: str, key: str) -> str:
    """
    주어진 카테고리(예: '단계', '반응', '치료법')와 키(예: '1단계', '저항적', 'CBT')에 해당하는 프롬프트 파일을 불러온다.
    """
    # 현재 파일(prompt_builder.py)이 있는 폴더가 바로 'prompts'이므로 parent만 써야 함
    prompt_path = Path(__file__).resolve().parent / category / f"{key}.txt"
    if not prompt_path.exists():
        print(f"❗ 프롬프트 파일 없음: {prompt_path}")
        return ""
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def build_prompt_with_strategies(reaction_type: str, stage: str, approach: str, order=("stage", "react", "cure")):
    prompt_map = {
        "stage": load_prompt("stage", stage),
        "react": load_prompt("react", reaction_type),
        "cure": load_prompt("cure", approach),
    }
    combined_prompt = "\n\n".join([prompt_map[k] for k in order if prompt_map[k]])
    return combined_prompt
