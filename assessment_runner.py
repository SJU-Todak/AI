from test_run import load_test

def run_assessment(age: int, concern: int):
    test = recommend_assessments(concern, age)
    if test is None:
        return

    print(f"\n[{test}] 검사 시작:")
    result_msg = load_test(test)  # 추후 작성할 함수에서 검사 실행 및 결과 반환
    print(f"\n[{test}] 결과 요약:\n{result_msg}")
    

def recommend_assessments(concern: int, age: int) -> str | None:
    # 나이대 구분
    if age <= 19:
        age_group = "teen"
    elif age <= 35:
        age_group = "adult"
    else:
        age_group = "senior"

    # 고민 번호 → 고민 텍스트 매핑
    concern_mapping = {
        1: "우울 / 무기력",
        2: "불안 / 긴장",
        3: "대인관계 / 소통 어려움",
        4: "진로 / 미래 불안",
        5: "학업 / 성적 스트레스",
        6: "직장 / 업무 스트레스",
        7: "가족 문제",
        8: "연애 / 이별",
        9: "자기이해 / 성격 혼란",
        10: "생활습관 / 신체 문제"
    }

    # 고민별 + 연령대별 검사 매핑표
    test_table = {
        "우울 / 무기력": {"teen": ["PHQ-9"], "adult": ["PHQ-9"], "senior": ["PHQ-9"]},
        "불안 / 긴장": {"teen": ["GAD-7"], "adult": ["GAD-7"], "senior": ["PSS"]},
        "대인관계 / 소통 어려움": {"teen": ["RSES"], "adult": ["RSES"], "senior": ["RSES"]},
        "진로 / 미래 불안": {"teen": ["PSS"], "adult": ["PSS"], "senior": ["PSS"]},
        "학업 / 성적 스트레스": {"teen": ["ATA"], "adult": ["PSS"], "senior": []},
        "직장 / 업무 스트레스": {"teen": [], "adult": ["PSS"], "senior": ["PSS"]},
        "가족 문제": {"teen": ["K-FACES IV"], "adult": ["K-FACES IV"], "senior": ["K-FACES IV"]},
        "연애 / 이별": {"teen": ["ReQo-10"], "adult": ["ReQo-10"], "senior": ["ReQo-10"]},
        "자기이해 / 성격 혼란": {"teen": ["RSES"], "adult": ["RSES"], "senior": ["RSES"]},
        "생활습관 / 신체 문제": {"teen": ["PSS"], "adult": ["PSS"], "senior": ["PSS"]}
    }

    concern_text = concern_mapping.get(concern)
    if not concern_text:
        print("⚠️ 유효하지 않은 고민 번호입니다.")
        return None

    tests = test_table.get(concern_text, {}).get(age_group)
    return tests[0] if tests else None
