from google import genai
import streamlit as st

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Assistente IA para Negócios", page_icon="🤖", layout="centered"
)

st.title("🤖 Assistente Virtual Inteligente")
st.write(
    "Este protótipo simula um atendente automático interativo para pequenos"
    " negócios locais."
)

# Campo para o usuário inserir a chave da API
api_key = st.text_input("Insira sua Chave da API do Google Gemini:", type="password")

if api_key:
  # Configura o cliente da IA
  client = genai.Client(api_key=api_key)

  # Contexto/Instrução da barbearia
  system_instruction = (
      "Você é um assistente virtual prestativo de uma barbearia local chamada"
      " 'Barbearia Estillo'. Responda dúvidas de clientes de forma educada,"
      " curta e direta. Informações dos serviços e preços:"
      " - Corte de Cabelo: R$ 35,00"
      " - Barba: R$ 25,00"
      " - Combo (Cabelo + Barba): R$ 50,00"
      " Horários de funcionamento: Segunda a Sábado das 09h às 19h."
      " Localização: Centro de Imperatriz - MA."
      " Sempre conduza o cliente para realizar o agendamento de forma amigável."
  )

  # Inicializa o histórico de mensagens na tela do Streamlit se não existir
  if "chat_history" not in st.session_state:
    # Criamos o objeto de chat da IA passando a instrução de sistema
    st.session_state.chat = client.chats.create(
        model="gemini-3.6-flash",
        config={"system_instruction": system_instruction},
    )
    # Lista para guardar as mensagens visuais da tela
    st.session_state.messages = []

  # Exibe as mensagens anteriores na tela para rolar o histórico
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  # Caixa de texto do chat na parte inferior
  if pergunta_cliente := st.chat_input("Digite sua mensagem para o assistente..."):
    # Adiciona a mensagem do usuário no histórico visual
    st.session_state.messages.append(
        {"role": "user", "content": pergunta_cliente}
    )
    with st.chat_message("user"):
      st.markdown(pergunta_cliente)

    # Envia a mensagem para a IA mantendo o contexto da conversa
    with st.chat_message("assistant"):
      with st.spinner("O assistente está digitando..."):
        try:
          response = st.session_state.chat.send_message(pergunta_cliente)
          resposta_ia = response.text
          st.markdown(resposta_ia)
          # Salva a resposta da IA no histórico visual
          st.session_state.messages.append(
              {"role": "assistant", "content": resposta_ia}
          )
        except Exception as e:
          st.error(f"Erro ao conectar com a IA: {e}")
else:
  st.info("Insira sua chave de API acima para começar a conversar com o assistente.")