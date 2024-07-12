from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

PROMPT_TEMPLATE_TEXT2 = """
Você é um analista de sentimentos da AluMind, uma startup focada em bem-estar e saúde mental. Sua tarefa é analisar os feedbacks dos usuários para determinar o sentimento e identificar possíveis melhorias. Os sentimentos possíveis são: POSITIVO, NEGATIVO ou INCONCLUSIVO.

Por favor, analise o seguinte feedback e forneça:
1. O sentimento do feedback (POSITIVO, NEGATIVO, INCONCLUSIVO).
2. Sugestões de melhorias, se houver.

Feedback: {text}

Sentimento: 
Melhorias e Códigos:
* ADICIONAR_MEDITAÇÕES_GUIADAS: Adicionar mais opções de meditação guiada para iniciantes.
* MELHORAR_EXPERIÊNCIA_USUÁRIO: Ajustar a interface para facilitar a navegação.
* CORRIGIR_PROBLEMA_LOGIN: Resolver problemas intermitentes de login.
"""

PROMPT_TEMPLATE_TEXT = """
Você é um analista de sentimentos da AluMind, uma startup focada em bem-estar e saúde mental. Sua tarefa é analisar os feedbacks dos usuários para determinar o sentimento e identificar possíveis melhorias. Os sentimentos possíveis são: POSITIVO, NEGATIVO ou INCONCLUSIVO. Um exemplo de como o retorno desse prompt deve ser feito está mais abaixo, em um formato de JSON.

Por favor, analise o seguinte feedback e forneça:
1. O sentimento do feedback (POSITIVO, NEGATIVO, INCONCLUSIVO).
2. Sugestões de melhorias, se houver.

Feedback: {text}

{{"sentiment": "POSITIVO", "requested_features": [{{"code": "EDITAR_PERFIL", "reason": "O usuário gostaria de realizar a edição do próprio perfil"}}]}}
"""



prompt = PromptTemplate(
        template=PROMPT_TEMPLATE_TEXT,
        input_variables=["text"]
    )
llm_gemini = GoogleGenerativeAI(
    model="gemini-1.0-pro",
    max_output_tokens=1024,
    google_api_key=os.environ.get('GOOGLE_AI_API_KEY'),
    temperature=0.5,
    top_p=0.5,
)
chain = LLMChain(llm=llm_gemini, prompt=prompt)    


def analyze_sentiment(text):
    response = chain.run({"text": text})
    return response

