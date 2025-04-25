import openai
import os
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
        return response.content 