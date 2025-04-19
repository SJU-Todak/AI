def load_test(test_name: str) -> str:
    def ask_questions(questions, scale, reverse_indices=None):
        total = 0
        for i, q in enumerate(questions, 1):
            score = input(f"{i}. {q} ({scale}) → ")
            try:
                score = int(score)
            except:
                score = 0
            if reverse_indices and i in reverse_indices:
                max_score = int(scale.split("~")[-1].replace("점", ""))
                score = max_score - score
            total += score
        return total

    if test_name == "PHQ-9":
        questions = [
            "흥미를 느끼거나 즐거움을 느끼는 일이 거의 없었다.",
            "기분이 가라앉거나 우울하거나 절망적인 느낌이 들었다.",
            "잠들기 어렵거나 자주 깼거나, 또는 너무 많이 잠을 잤다.",
            "피로감이나 기운이 없었다.",
            "식욕이 없거나 과식했다.",
            "자신을 실패자라고 느꼈거나, 자신이나 가족을 실망시켰다고 생각했다.",
            "집중하기 어려웠다 (예: 신문 읽기, TV 시청).",
            "주변 사람이 알아챌 정도로 말이나 행동이 느려졌거나, 너무 안절부절못했다.",
            "살아있는 것이 싫거나 자해 또는 죽음에 대해 생각했다."
        ]
        total = ask_questions(questions, "0~3점")
        if total >= 20:
            level = "중증 우울증"
        elif total >= 15:
            level = "중등도에서 중증 우울증"
        elif total >= 10:
            level = "중등도 우울증"
        elif total >= 5:
            level = "경증 우울증"
        else:
            level = "우울 증상 없음 또는 최소"
        return f"총점: {total}점 → 우울 수준: {level}"

    elif test_name == "GAD-7":
        questions = [
            "초조하거나 긴장된 느낌이 있었다.",
            "걱정을 멈추거나 조절하기 어려웠다.",
            "여러 가지 일들에 대해 지나치게 걱정했다.",
            "긴장을 푸는 것이 어려웠다.",
            "너무 안절부절못하거나 산만한 느낌이 들었다.",
            "쉽게 짜증이 났다.",
            "과도한 걱정 때문에 일상생활에 지장이 있었다."
        ]
        total = ask_questions(questions, "0~3점")
        if total >= 15:
            level = "중증 불안"
        elif total >= 10:
            level = "중등도 불안"
        elif total >= 5:
            level = "경증 불안"
        else:
            level = "불안 증상 없음 또는 최소"
        return f"총점: {total}점 → 불안 수준: {level}"

    elif test_name == "RSES":
        questions = [
            "나는 내 자신에 대해 긍정적으로 느낀다.",
            "나는 내 장점에 대해 자부심을 느낀다.",
            "나는 전반적으로 쓸모 있는 사람이라고 느낀다.",
            "나는 나에게 만족한다.",
            "나는 좋은 자질을 갖고 있다.",
            "나는 종종 내가 실패자라고 느낀다.",
            "나는 때때로 내가 아무 쓸모 없는 사람이라고 느낀다.",
            "나는 종종 나 자신을 부정적으로 평가한다.",
            "나는 나 자신에게 실망하는 경우가 많다.",
            "나는 나 자신을 존중한다."
        ]
        reverse = {6, 7, 8, 9}
        total = ask_questions(questions, "1~4점", reverse)
        if total >= 26:
            level = "높은 자존감"
        elif total >= 15:
            level = "정상 범위"
        else:
            level = "낮은 자존감"
        return f"총점: {total}점 → 자존감 수준: {level}"

    elif test_name == "PSS":
        questions = [
            "예상치 못한 일 때문에 불안하거나 당황한 적이 있었다.",
            "중요한 일들을 통제할 수 없다고 느꼈다.",
            "긴장하거나 스트레스를 받았다.",
            "일이 내 뜻대로 되지 않는다고 느꼈다.",
            "너무 많은 어려움으로 극복이 힘들다고 느꼈다.",
            "중요한 일을 잘 처리했다고 느꼈다.",
            "상황을 잘 통제하고 있다고 느꼈다.",
            "성질을 잘 조절했다고 느꼈다.",
            "일이 잘 풀린다고 느꼈다.",
            "개인 문제들을 잘 해결할 수 있다고 느꼈다."
        ]
        reverse = {6, 7, 8, 9, 10}
        total = ask_questions(questions, "0~4점", reverse)
        if total >= 27:
            level = "높은 스트레스"
        elif total >= 14:
            level = "중간 스트레스"
        else:
            level = "낮은 스트레스"
        return f"총점: {total}점 → 스트레스 수준: {level}"

    elif test_name == "ATA":
        questions = [
            "시험을 앞두고 잠들기 어렵다.",
            "시험 보는 날 아침에 배가 아프거나 소화가 안 된다.",
            "시험 중 머리가 하얘져서 아무것도 기억나지 않는다.",
            "좋은 성적을 받지 못할까 걱정된다.",
            "다른 친구들과 비교해 불안이 많은 편이라고 느낀다."
        ]
        total = ask_questions(questions, "1~5점")
        if total >= 21:
            level = "심각한 시험 불안"
        elif total >= 16:
            level = "중간 정도의 불안"
        elif total >= 11:
            level = "가벼운 불안"
        else:
            level = "정상 범위"
        return f"총점: {total}점 → 학업 불안 수준: {level}"

    elif test_name == "K-FACES IV":
        questions = [
            "우리 가족은 정서적으로 서로 가깝다.",
            "가족 문제를 해결할 때 융통성 있게 대처한다.",
            "가족 간 갈등을 솔직하게 이야기할 수 있다.",
            "우리 가족은 전반적으로 만족스럽다."
        ]
        total = ask_questions(questions, "1~5점")
        if total >= 18:
            level = "높은 가족 적응력"
        elif total >= 13:
            level = "보통 수준"
        else:
            level = "가족 기능 약화 가능성"
        return f"총점: {total}점 → 가족 기능 수준: {level}"

    elif test_name == "ReQo-10":
        emo_questions = [
            "연애 문제로 인해 하루 중 기분이 가라앉거나 예민해지는 날이 많다.",
            "관계 안에서 감정 기복이 크고, 혼자서 감정을 다루기 어렵다.",
            "연락이 없거나 대화가 어긋나면 머릿속이 복잡해지고 집중이 어려워진다.",
            "연애가 나에게 스트레스의 원인이 되는 것 같다.",
            "내가 충분히 사랑받고 있는지 계속 의심하게 된다.",
            "연애 중 내가 없어도 괜찮을 것 같다는 생각이 들거나, 관계에서 소외감을 느낀다."
        ]
        self_questions = [
            "나는 관계 안에서 내 감정을 솔직하게 표현할 수 있다.",
            "나는 연애를 하면서도 내 가치를 잊지 않는다.",
            "연애가 잘 되지 않을 때마다 내가 부족하다고 느낀다.",
            "나는 사랑받을 가치가 있는 사람이라는 확신이 흔들린다."
        ]
        emo_score = ask_questions(emo_questions, "0~3점")
        self_score = ask_questions(self_questions, "1~4점", reverse_indices={9, 10})

        if emo_score <= 5:
            emo_level = "정서 안정"
        elif emo_score <= 10:
            emo_level = "감정 부담 있음"
        else:
            emo_level = "감정적 과부하"

        if self_score >= 13:
            self_level = "건강한 자존감"
        elif self_score >= 9:
            self_level = "자기비판 경향 있음"
        else:
            self_level = "자존감 저하, 관계 의존 가능성"

        return f"감정 반응 점수: {emo_score}점 → {emo_level}\n자기 인식 점수: {self_score}점 → {self_level}"

    else:
        return f"[{test_name}] 검사는 테스트 환경에서 아직 구현되지 않았습니다."
