from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json

import os


PROMPT_TEMPLATE_TEXT = """
Você é um analista de sentimentos da AluMind, uma startup focada em bem-estar e saúde mental. Sua tarefa é analisar os feedbacks dos usuários para determinar o sentimento e identificar possíveis melhorias. Os sentimentos possíveis são: POSITIVO, NEGATIVO ou INCONCLUSIVO.

Aqui estão as descrições para cada tipo de sentimento:
- POSITIVO: Feedback que elogia ou destaca aspectos positivos do serviço ou produto. Exemplos: "O AluMind é uma excelente ferramenta para meditação" ou "As sessões de terapia são muito úteis."
- NEGATIVO: Feedback que critica ou aponta falhas, problemas ou insatisfações com o serviço ou produto. Exemplos: "A interface é confusa" ou "Encontrei dificuldades em exportar meus dados."
- INCONCLUSIVO: Feedback que não é claramente positivo ou negativo, podendo ser neutro, vago ou não fornecer informações suficientes para uma conclusão clara. Exemplos: "Preciso de mais orientações" ou "Adorei os artigos, mas gostaria de mais variedade."

Por favor, analise o seguinte feedback e forneça:
1. O sentimento do feedback (POSITIVO, NEGATIVO ou INCONCLUSIVO), com base nas descrições acima.
2. Sugestões de melhorias, se houver. O elemento "code" gerado deve conter **no máximo duas palavras**, sempre no formato de VERBO_OBJETO (exemplo: EDITAR_PERFIL, MEDITAR).

A resposta deve ser formatada como JSON, **como o exemplo no final deste prompt, nunca diferente do exemplo!**

Feedback: {text}

{{"sentiment": "POSITIVO", "requested_features": [{{"code": "CODIGO_FEATURE", "reason": "Razão para essa feature ser importante"}}]}}

"""



llm_gemini = GoogleGenerativeAI(
    model="gemini-1.0-pro",
    max_output_tokens=1024,
    google_api_key=os.environ.get('GOOGLE_AI_API_KEY'),
    temperature=0.1 # Temperatura baixa para a criação de codes ser mais precisa
)
 


def analyze_sentiment(text):
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE_TEXT,
        input_variables=["text"]
    )
    chain = LLMChain(llm=llm_gemini, prompt=prompt)   
    try:
        response = chain.run({"text": text})
        try:
            print(response)
            print(type(response))
            return str(response)
        except json.JSONDecodeError as e:
                return {"error": "Failed to decode response"}
    except Exception as e:
            return {"error": "An error occurred during sentiment analysis"}

def generate_email_content(report_data):
    sentiment_distribution = report_data['sentiment_distribution']
    top_features = report_data['top_features']

    sentiment_summary = f"Positivos: {sentiment_distribution['POSITIVO']}%, Negativos: {sentiment_distribution['NEGATIVO']}%"

    features_summary = "\n".join(
        [f"{feature['code']}: {feature['reason']}" for feature in top_features]
    )

    email_template = f"""
    Relatório Semanal de Feedbacks:

    Distribuição de Sentimentos:
    {sentiment_summary}

    Funcionalidades Mais Solicitadas:
    {features_summary}
    """

    prompt = f"Crie um email amigável e informativo com base no seguinte texto:\n\n{email_template}"
    chain = LLMChain(llm=llm_gemini, prompt=prompt) 
    response = chain.run({"text": prompt})
    return response