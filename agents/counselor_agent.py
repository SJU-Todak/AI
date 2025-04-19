from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
import os

class CounselorAgent:
    def __init__(self, client_info, persona_type, emotion, distortion=None, model_name="gpt-4o-mini", temperature=0.7):
        self.client_info = client_info
        self.emotion = emotion if emotion else "없음"
        self.distortion = distortion if distortion else "없음"
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)

        # Load persona prompt based on persona_type
        persona_path = f"prompts/{persona_type}.txt"
        with open(persona_path, "r", encoding="utf-8") as f:
            self.persona_prompt = f.read()

        self.prompt_template = self.load_prompt_template()

    def load_prompt_template(self):
        with open("prompts/counselor_prompt.txt", "r", encoding="utf-8") as f:
            return f.read()
    
    
    def generate_response(self, history, latest_client_message, current_session=None):
        # history를 문자열로 변환
        formatted_history = "\n".join([f"{msg['role'].capitalize()}: {msg['message']}" for msg in history])
        
        session_dialogue = "\n".join(
            [f"{'내담자' if msg['role'] == 'client' else '상담자'}: {msg['message']}" for msg in current_session]
        ) if current_session else ""

        filled_prompt = self.prompt_template.format(
            client_info=self.client_info,
            history=formatted_history,
            persona_prompt=self.persona_prompt,
            emotion=self.emotion,
            distortion=self.distortion,
            latest_client_message=latest_client_message,
            session_dialogue=session_dialogue
        )

        # ✅ 프롬프트 출력 추가
        #print(filled_prompt)

        response = self.llm.invoke(filled_prompt)

        if isinstance(response, AIMessage):
            return response.content 
        return str(response)
