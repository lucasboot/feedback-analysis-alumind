# app/utils/send_weekly_report.py
import smtplib
from email.mime.text import MIMEText
import requests
from celery import shared_task
import os
import re


from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# Configuração do LLM
llm_gemini = GoogleGenerativeAI(
    model="gemini-1.0-pro",
    max_output_tokens=1024,
    google_api_key=os.environ.get('GOOGLE_AI_API_KEY'),
    temperature=0.1 
)

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

    # Gerar o texto do e-mail usando o LLM
    prompt_template = PromptTemplate(template="Crie um email formal e informativo com base no seguinte texto, inicie o texto colocando como destinatário os stakeholders da AluMind e assine como Equipe de Inteligência da Alumind:\n\n{text}")
    chain = LLMChain(llm=llm_gemini, prompt=prompt_template)
    response = chain.run({"text": email_template})
    generated_email_content = response  

    return markdown_to_html(generated_email_content)

def markdown_to_html(text):
    # Substituir **por <b> e </b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    
    # Substituir *por <i> e </i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)

     # Substituir quebras de linha simples por <br>
    text = re.sub(r'(\S)\n(\S)', r'\1<br>\2', text)
    
    # Substituir duplas quebras de linha por parágrafo <p>
    text = re.sub(r'\n\n', r'</p><p>', text)
    
    return text


def send_email(subject, body, to_emails):
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    smtp_username = ''
    smtp_password = ''

    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = ', '.join(to_emails)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_emails, msg.as_string())

# Lista de emails
to_emails = ['lucasisastudent@gmail.com']


@shared_task
def send_weekly_report_email():
    response = requests.get('http://127.0.0.1:5000/generate_weekly_report')
    if response.status_code == 200:
        report_data = response.json()
        email_content = generate_email_content(report_data)
        send_email("Relatório Semanal de Feedbacks da AluMind", email_content, to_emails)
        print('Email enviado')
    else:
        print("Falha ao obter o relatório semanal.")
