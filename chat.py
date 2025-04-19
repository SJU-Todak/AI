import json
from pathlib import Path
from agents.counselor_agent import CounselorAgent
from agents.evaluator_agent import EvaluatorAgent
from agents.sub_llm import SubLLMAgent
from config import get_config, set_openai_api_key
from DB import get_chat_log, save_chat_log, save_user_info, get_user_info  # DB.py에서 import
from assessment_runner import run_assessment 


# API 키 설정
set_openai_api_key()
from pymongo import MongoClient
from datetime import datetime

# 연결 문자열 사용
client = MongoClient("mongodb+srv://j2982477:EZ6t7LEsGEYmCiJK"
"@mindAI.zgcb4ae.mongodb.net/?retryWrites=true&w=majority&appName=mindAI")

# 'mindAI' 데이터베이스에 연결
db = client['mindAI']
# TherapySimulation 클래스에서 사용자 정보 확인
class TherapySimulation:
    def __init__(self, persona_type: str, chat_id: str, user_id: str, max_turns: int = 20):
        self.persona_type = persona_type
        self.chat_id = chat_id
        self.user_id = user_id
        self.max_turns = max_turns
        self.history = []
        self.current_session = []

        # Check if the user exists in the database
        user_info = get_user_info(self.user_id)
        if user_info:
            # If the user exists, load their information
            self.name = user_info["name"]
            self.age = user_info["age"] 
            self.gender = user_info["gender"] 
            self.concern = user_info.get("concern", "")

        else:
            # If the user doesn't exist, prompt for information
            print(f"{self.user_id}는 새로운 사용자입니다. 사용자 정보를 입력해주세요.")
            self.name = input("이름을 입력해주세요: ")
            self.age = int(input("나이를 입력해주세요: "))
            self.gender = input("성별을 입력해주세요(남자/여자): ")
            # 고민 카테고리 선택
            self.concern = int(input("1. 우울 / 무기력, 2. 불안 / 긴장, 3. 대인관계 / 소통 어려움\n4. 진로 / 미래 불안, 5. 학업 / 성적 스트레스, 6. 직장 / 업무 스트레스,\n7. 가족 문제, 8. 연애 / 이별, 9. 자기이해 / 성격 혼란, 10. 생활습관 / 신체 문제\n최근 고민에 해당하는 번호를 입력하세요: "))

            # Save new user info including concern to DB
            save_user_info(self.user_id, self.name, self.age, self.gender) 
            
            # Run appropriate assessment
            run_assessment(self.age, self.concern)  # 검사지 선정 및 실행

        # Load chat log if it exists
        chat_log = get_chat_log(self.chat_id)
        if chat_log:
            self.history = chat_log
        else:
            self.history.append({
                "role": "client",
                "message": f"{self.name}님, 안녕하세요. 오늘 하루는 어떠셨나요?"
            })

        # SubLLM analysis
        self.subllm_agent = SubLLMAgent()
        self.evaluator_agent = EvaluatorAgent()

         # 상담자 에이전트와 평가자 에이전트 초기화
        self.counselor_agent = CounselorAgent(
            client_info=f"{self.name}, {self.age}세, {self.gender}",
            persona_type=persona_type,
            emotion="없음",
            distortion="없음"
        )

        self._init_history()
    def _init_history(self):
        """
        채팅을 위한 초기화 작업을 처리하는 메서드입니다.
        현재로서는 간단하게 'client' 역할로 기본 메시지를 설정합니다.
        """
        if not self.history:  # history가 비어 있으면 초기 메시지를 추가
            self.history.append({
                "role": "client",
                "message": f"{self.name}님, 안녕하세요. 오늘 하루는 어떠셨나요?"
            })
    def run(self):
        for turn in range(self.max_turns):
            print(f"\n--- Turn {turn + 1} ---")
            client_msg = input(f"{self.name}: ")
            #print("="*20)
            self.history.append({"role": "client", "message": client_msg})
            self.current_session.append({"role": "client", "message": client_msg})
            # Sub LLM 분석 실행
            analysis_result = self.subllm_agent.analyze(client_msg)
            self.counselor_agent.emotion = analysis_result.get("감정", "없음")
            self.counselor_agent.distortion = analysis_result.get("인지왜곡", "없음")

            # 상담자 응답 생성
            if "[/END]" in client_msg:
                client_msg = client_msg.replace("[/END]", "")
                self.history[-1]["message"] = client_msg
                self.current_session[-1]["message"] = client_msg
                break
            
            counselor_msg = self.counselor_agent.generate_response(self.history, client_msg, current_session=self.current_session)
            self.history.append({"role": "counselor", "message": counselor_msg})
            self.current_session.append({"role": "counselor", "message": counselor_msg})
            print(counselor_msg)

            # 5. 채팅 로그 저장
            save_chat_log(self.user_id, self.chat_id, client_msg, counselor_msg)  # 채팅 로그를 MongoDB에 저장
            # 6. 종료 조건 체크

        # 7. 평가 수행
        current_conversation = self.current_session.copy()
        print("=" * 40)
        print("\n현재 세션 대화 기록")
        print("=" * 40)
        for msg in self.current_session:
            role = "내담자" if msg["role"] == "client" else "상담자"
            print(f"{role}: {msg['message']}")

        evaluation_result = self.evaluator_agent.evaluate_all(current_conversation)

        # 7. 결과 반환
        print("\n평가")
        print("="*40)
        for 항목, 설명 in evaluation_result.items():
            print(f"{항목}: {설명}")

        return {
            "persona": self.persona_type,
            "history": self.history,
            "evaluation": evaluation_result,
            "emotion": analysis_result.get("감정", "없음"),
            "distortion": analysis_result.get("인지왜곡", "없음")
        }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_file", default=None)
    parser.add_argument("--persona_type", required=True)
    parser.add_argument("--chat_id", required=True)  # chat_id 추가
    parser.add_argument("--user_id", required=True)  # 사용자 이름

    args = parser.parse_args()

    sim = TherapySimulation(
            persona_type=args.persona_type,
            chat_id=args.chat_id,
            user_id=args.user_id, 
        )    
    result = sim.run()

    if args.output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output_file = f"results/result_{timestamp}.json"

    Path(args.output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
