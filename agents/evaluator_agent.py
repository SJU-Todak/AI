from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from config import load_prompt
import os

class EvaluatorAgent:
    def __init__(self, model_name="gpt-4o-mini", temperature=0.7):
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.prompt_template = self.load_prompt_template()

    def load_prompt_template(self):
        prompt_path = "prompts/evaluation_final.txt"
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    def evaluate(self, history):
        conversation = '\n'.join([
            f"{item['role'].capitalize()}: {item['message']}" for item in history
        ])
        
        filled_prompt = self.prompt_template.format(conversation=conversation)
        response = self.llm.invoke(filled_prompt)

        if isinstance(response, AIMessage):
            return response.content
        return str(response)

    def evaluate_all(self, history):
        result = self.evaluate(history)
        return {
            "총평": result
        }

# 사용 예시
if __name__ == "__main__":
    history = [
        {"role": "counselor", "message": "안녕하세요, 로라. 어떻게 지내세요?"},
        {"role": "client", "message": "요즘 너무 벅차게 느껴져요."},
        # 여기에 실제 상담 대화 내용 추가
    ]
    
    evaluator = EvaluatorAgent()
    result = evaluator.evaluate_all(history)
    
    # 결과 출력
    print(result)