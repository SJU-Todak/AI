import openai
import os
import json
from config import load_config, load_prompt
from langchain_openai import ChatOpenAI

class MissionAgent:
    def __init__(self, model_name="gpt-4o-mini", temperature=0.7):
        config = load_config()
        openai.api_key = config["openai"]["key"]
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.prompt_template = load_prompt("mission_prompt.txt")

    def provide_mission(self, history, evaluation):
        prompt = self.prompt_template.format(history=history, evaluation=evaluation)

        response = self.llm.invoke(prompt)
        mission_content = response.content

        # JSON 형식으로 저장
        mission_data = {
            "mission": mission_content
        }
        self.save_mission_to_json(mission_data)

        return mission_content

    def save_mission_to_json(self, mission_data, file_path="mission_output.json"):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(mission_data, f, ensure_ascii=False, indent=4)
        print(f"Mission data saved to {file_path}")

# 사용 예시
if __name__ == "__main__":
    history = "사용자와의 대화 이력"
    evaluation = "대화 평가 결과"

    agent = MissionAgent()
    mission = agent.provide_mission(history, evaluation)
    print("Provided Mission:", mission)