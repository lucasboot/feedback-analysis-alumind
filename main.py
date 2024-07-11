import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import GoogleGenerativeAI

# Configuração da chave da API do Google
os.environ["GOOGLE_AI_API_KEY"] = 'AIzaSyBtQcjVG6D-44gaVZrCgVeOeG83ojmO-gs'

# Inicialização do modelo LLM do Google Gemini
llm_gemini = GoogleGenerativeAI(
    model="gemini-pro",
    max_output_tokens=1024,
    google_api_key=os.environ["GOOGLE_AI_API_KEY"],
)

# Definindo o template do prompt para análise de sentimento
PROMPT_TEMPLATE_TEXT = """
Você é um analista de sentimentos da AluMind, uma startup focada em bem-estar e saúde mental. Sua tarefa é analisar os feedbacks dos usuários para determinar o sentimento e identificar possíveis melhorias. Os sentimentos possíveis são: POSITIVO, NEGATIVO ou INCONCLUSIVO.

Por favor, analise o seguinte feedback e forneça:
1. O sentimento do feedback (POSITIVO, NEGATIVO, INCONCLUSIVO).
2. Sugestões de melhorias, se houver.
3. Crie um código simples para identificar cada melhoria encontrada, no formato: VERBO_ALVO (exemplo: EDITAR_PERFIL, ALTERAR_FOTO, ACESSAR_CHAT)

Feedback: {text}

Sentimento:
Melhorias e códigos:
"""

# Criação do template do prompt
prompt = PromptTemplate(
    template=PROMPT_TEMPLATE_TEXT,
    input_variables=["text"]
)

# Criação da cadeia de execução com o prompt e o modelo
chain = LLMChain(llm=llm_gemini, prompt=prompt)

# Função para analisar o sentimento
def analyze_sentiment(text):
    response = chain.run({"text": text})
    return response.strip()

# Exemplo de texto para análise de sentimento
texto = "Gosto muito de usar o Alumind! Está me ajudando bastante em relação a alguns problemas que tenho. Só queria que houvesse uma forma mais fácil de eu mesmo realizar a edição do meu perfil dentro da minha conta"

# Realizando a análise de sentimento
analise = analyze_sentiment(texto)
print(analise)
