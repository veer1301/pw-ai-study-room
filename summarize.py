import openai
from openai import AzureOpenAI
from prompt import prompt_summary
from api_config import chat_api_key, chat_api_base, chat_api_version, chat_model
import time
class GPTService:
    def __init__(self, api_key: str, api_base: str, api_version: str, model: str):
        self.api_key = api_key
        self.api_base = api_base
        self.api_version = api_version
        self.model = model
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            base_url=f"{self.api_base}/openai/deployments/{self.model}",
        )

    def classify_sentence(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": ""},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                    ],
                },
            ],
            max_tokens=2000,
            temperature=0,
        )

        result = response.choices[0].message.content
        token_usage = response.usage.total_tokens  # Extract token usage
        return result, token_usage

    def infer_message_class_from_prompting(self, paragraph: str, output_language: str):
        prompt = prompt_summary.format(paragraph=paragraph, output_language=output_language, )
        predicted_summary, token_usage = self.classify_sentence(prompt)
        response = predicted_summary
        return response

# Example usage
if __name__ == "__main__":
    gpt_service = GPTService(chat_api_key, chat_api_base, chat_api_version, chat_model)
    sentence = """📘 கல்வியின் முக்கியத்துவம்
கல்வி என்பது மனித வாழ்க்கையின் அடிப்படையான தூணாகும். அறிவை வளர்க்கும், திறன்களை மேம்படுத்தும், சமூகத்தில் உயர்வடைய உதவும் முக்கியமான கருவி கல்வி ஆகும். இது மனிதனை அறிவாளியாக மாற்றும், சமூகத்தில் நல்ல முறையில் வாழ வழிகாட்டும்.
"""
    result = gpt_service.infer_message_class_from_prompting(sentence, "hindi")
    print(result)