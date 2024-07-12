from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os


PROMPT_TEMPLATE_TEXT = """
Você é um analista de sentimentos da AluMind, uma startup focada em bem-estar e saúde mental. Sua tarefa é analisar os feedbacks dos usuários para determinar o sentimento e identificar possíveis melhorias. Os sentimentos possíveis são: POSITIVO, NEGATIVO ou INCONCLUSIVO.

Por favor, analise o seguinte feedback e forneça:
1. O sentimento do feedback (POSITIVO, NEGATIVO ou INCONCLUSIVO).
2. Sugestões de melhorias, se houver. O elemento "code" gerado deve conter **no máximo duas palavras**, sempre no formato de VERBO_OBJETO (exemplo: EDITAR_PERFIL, MEDITAR).

A resposta deve ser formatada como JSON, como o exemplo no final deste prompt.

Feedback: {text}


{{"sentiment": "POSITIVO", "requested_features": [{{"code": "CODIGO_FEATURE", "reason": "Razão para essa feature ser importante"}}]}}

"""


prompt = PromptTemplate(
        template=PROMPT_TEMPLATE_TEXT,
        input_variables=["text"]
    )
llm_gemini = GoogleGenerativeAI(
    model="gemini-1.0-pro",
    max_output_tokens=1024,
    google_api_key=os.environ.get('GOOGLE_AI_API_KEY'),
    temperature=0.6
)
chain = LLMChain(llm=llm_gemini, prompt=prompt)    


def analyze_sentiment(text):
    response = chain.run({"text": text})
    return response

