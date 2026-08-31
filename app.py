from google import genai
import streamlit as st

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Assistente IA para Negócios", page_icon="🤖", layout="centered"
)

st.title("🤖 Assistente Virtual Inteligente")
st.write(
    "Este protótipo simula um atendente automático para pequenos negócios locais."
)

# Campo para o usuário inserir a chave da API (ou você pode fixar ela para testes)
api_key = st.text_input("Insira sua Chave da API do Google Gemini:", type="password")

if api_key:
  # Configura o cliente da IA
  client = genai.Client(api_key=api_key)

  # Contexto/Instrução para a IA agir como atendente de um comércio local (ex: uma barbearia ou lojinha)
  system_instruction = (
      "Você é um assistente virtual prestativo de uma barbearia local chamada"
      " 'Barbearia Estillo'. Responda dúvidas de clientes de forma educada,"
      " curta e direta sobre cortes, barba, horários de funcionamento (Segunda a"
      " Sábado das 09h às 19h) e localização (Centro de Imperatriz - MA)."
  )

  # Entrada de texto do cliente simulado
  pergunta_cliente = st.text_input("O que o cliente deseja perguntar?")

  if st.button("Enviar Pergunta"):
    if pergunta_cliente:
      with st.spinner("O assistente está pensando..."):
        try:
          # Chamada do modelo de IA usando a API nova do Google GenAI
          response = client.models.generate_content(
              model="gemini-2.5-flash",
              contents=f"{system_instruction}\n\nCliente: {pergunta_cliente}",
          )
          st.success("Resposta do Assistente:")
          st.write(response.text)
        except Exception as e:
          st.error(f"Ocorreu um erro ao conectar com a IA: {e}")
    else:
      st.warning("Por favor, digite uma pergunta para o assistente.")
else:
  st.info("Insira sua chave de API acima para começar a testar o assistente.")