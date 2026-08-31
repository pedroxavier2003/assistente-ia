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

  # Contexto/Instrução atualizado com preços e mais detalhes
  system_instruction = (
      "Você é um assistente virtual prestativo de uma barbearia local chamada"
      " 'Barbearia Estillo'. Responda dúvidas de clientes de forma educada,"
      " curta e direta. Informações dos serviços e preços:"
      " - Corte de Cabelo: R$ 35,00"
      " - Barba: R$ 25,00"
      " - Combo (Cabelo + Barba): R$ 50,00"
      " Horários de funcionamento: Segunda a Sábado das 09h às 19h."
      " Localização: Centro de Imperatriz - MA."
      " Sempre incentive o cliente a confirmar o melhor dia e horário para agendamento."
  )

  # Entrada de texto do cliente simulado
  pergunta_cliente = st.text_input("O que o cliente deseja perguntar?")

  if st.button("Enviar Pergunta"):
    if pergunta_cliente:
      with st.spinner("O assistente está pensando..."):
        try:
          # Chamada do modelo de IA usando a API nova do Google GenAI
          response = client.models.generate_content(
              model="gemini-3.6-flash",
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