from google import genai
import streamlit as st

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Assistente IA com Agendamento Dinâmico",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Styllus Barber - Assistente de Agendamento")
st.write(
    "Este protótipo consulta e atualiza um banco de dados em arquivo texto"
    " (`horarios.txt`)."
)

# Campo para o usuário inserir a chave da API
api_key = st.text_input("Insira sua Chave da API do Google Gemini:", type="password")


# 1. FUNÇÃO QUE LÊ O ARQUIVO EXTERNO (Banco de Dados)
def verificar_disponibilidade(data: str, horario: str) -> str:
  """Verifica no arquivo de banco de dados se um determinado dia e horário estão vagos.

  Args:
      data: A data desejada (ex: 'terça-feira')
      horario: O horário desejado (ex: '14:00')
  """
  try:
    with open("horarios.txt", "r", encoding="utf-8") as arquivo:
      linhas = arquivo.readlines()

    horarios_ocupados = []
    for linha in linhas:
      if "|" in linha:
        d, h = linha.strip().split("|")
        horarios_ocupados.append((d.lower().strip(), h.strip()))
  except FileNotFoundError:
    horarios_ocupados = []

  data_limpa = data.lower().strip()
  horario_limpo = horario.strip()

  if (data_limpa, horario_limpo) in horarios_ocupados:
    return (
        f"O horário {horario_limpo} em {data_limpa} JÁ ESTÁ OCUPADO. Por favor,"
        " sugira outro horário."
    )
  else:
    return (
        f"O horário {horario_limpo} em {data_limpa} ESTÁ VAGO! Pode prosseguir"
        " com o agendamento."
    )


if api_key:
  client = genai.Client(api_key=api_key)

  system_instruction = (
      "Você é um assistente virtual prestativo da barbearia 'Styllus Barber',"
      " administrada por Francisco Silva, localizada no bairro Centro de"
      " Imperatriz - MA. Informações dos serviços e preços:"
      " - Corte de Cabelo: R$ 35,00"
      " - Barba: R$ 25,00"
      " - Combo (Cabelo + Barba): R$ 50,00"
      " Horários de funcionamento: Segunda a Sábado das 09h às 19h."
      " QUANDO O CLIENTE QUISER MARCAR OU PERGUNTAR SOBRE UM HORÁRIO, você DEVE"
      " obrigatoriamente chamar a função 'verificar_disponibilidade' para checar"
      " se está vago antes de confirmar."
  )

  if "chat_history" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-3.6-flash",
        config={
            "system_instruction": system_instruction,
            "tools": [verificar_disponibilidade],
        },
    )
    st.session_state.messages = []

  # --- PAINEL LATERAL PARA ADICIONAR HORÁRIO MANUALMENTE NO TXT ---
  with st.sidebar:
    st.subheader("Painel Administrativo")
    st.write("Bloquear horário manualmente no `horarios.txt`:")
    novo_dia = st.text_input("Dia (ex: terça-feira):")
    novo_horario = st.text_input("Horário (ex: 14:00):")

    if st.button("Salvar Horário Ocupado"):
      if novo_dia and novo_horario:
        # Abre o arquivo em modo de adição ('a') e escreve a nova linha
        with open("horarios.txt", "a", encoding="utf-8") as f:
          f.write(f"\n{novo_dia.lower().strip()}|{novo_horario.strip()}")
        st.success(f"Horário {novo_horario} ({novo_dia}) salvo com sucesso!")
      else:
        st.warning("Preencha o dia e o horário.")

  # Exibe o histórico de mensagens na tela principal
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if pergunta_cliente := st.chat_input("Digite sua mensagem para o assistente..."):
    st.session_state.messages.append(
        {"role": "user", "content": pergunta_cliente}
    )
    with st.chat_message("user"):
      st.markdown(pergunta_cliente)

    with st.chat_message("assistant"):
      with st.spinner("O assistente está consultando a agenda..."):
        try:
          response = st.session_state.chat.send_message(pergunta_cliente)
          resposta_ia = response.text
          st.markdown(resposta_ia)
          st.session_state.messages.append(
              {"role": "assistant", "content": resposta_ia}
          )
        except Exception as e:
          st.error(f"Erro ao conectar com a IA: {e}")
else:
  st.info("Insira sua chave de API acima para começar a conversar com o assistente.")