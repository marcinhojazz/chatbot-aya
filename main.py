from flask import Flask, request
import logging
from twilio.twiml.messaging_response import MessagingResponse
import random
import datetime
import re

app = Flask(__name__)
logging.basicConfig(filename='chatbot.log', level=logging.INFO)

# Dicionário para armazenar dados do usuário e estados
user_data = {}

# Variável para armazenar a última vez que um usuário enviou uma mensagem
last_message_time = {}
# Variável para armazenar a contagem de mensagens enviadas por um usuário em um minuto
message_count = {}

text_backmenu = "\n\nCaso queira voltar para o Menu Inicial/Principal digite *0*"

# STATE START
STATE_MAIN_MENU = 'state_main_menu'

# STATES OF SUBMENU 4
STATE_REPORT_CITY = 'state_report_city'
STATE_REPORT_NEIGHBORHOOD = 'state_report_neighborhood'
STATE_REPORT_ZIP = 'state_report_zip'
STATE_REPORT_PROBLEM = 'state_report_problem'

# STATES OF SUBMENU 5
STATE_MENU5 = 'state_menu5'

# STATES MENU 6
STATE_FEEDBACK_RATING = 'state_feedback_rating'
STATE_FEEDBACK_COMMENT = 'state_feedback_comment'

# Log function
def log_message(direction, phone_number, message):
    if direction == "incoming":
        logging.info(f"User ({phone_number}) Input: {message}")
    elif direction == "outgoing":
        logging.info(f"Bot Response to ({phone_number}): {message}")

def send_main_menu():
    return """
Oie! Sou a *Aya*, a ativista climática digital que veio pra somar! 😄💚
Tô aqui pra te ajudar com informações sobre o clima e meio ambiente no seu dia a dia.
E você pode me chamar a qualquer momento para saber sobre:

*1 -* Vamos revolucionar nossa quebrada: Dicas incríveis para proteger e lutar pelo meio ambiente.
*2 -* Baixe nosso ebook para entender como agir para se proteger em desastres socioambientais e eventos extremos.
*3 -* Orientações: Números de órgãos de apoio em situações de risco do seu território.
*4 -* Existe algum problema no seu bairro com lixo, esgoto, risco de deslizamento ou desmatamento? Vem me contar!
*5 -* Se informe sobre as ações do Instituto DuClima.
*6 -* Me conte o que achou da Pré-Conferência realizada no Rio de Janeiro._

_Por favor, responda com o número do item que deseja e vou adorar te ajudar! Foco no clima e nos nossos_ ✊🏿💚
"""

def handle_state_main_menu(incoming_msg, user, phone_number):
    greeting_pattern = re.compile(r'^(oi|olá|oie|hey|hello|eai|eaí|fala|boa|tudo bem|tudo bom|Como vai?|como vai?|oiiiieee|oiii|ooi|).*$', re.I)

    
    if greeting_pattern.match(incoming_msg) or incoming_msg == "0":
        return send_main_menu(), STATE_MAIN_MENU
    
    elif incoming_msg == "1":
        tips = [
            "🌱 De onde vem a comida que você come? Da indústria ou da terra? Plantar os alimentos que vão pra sua mesa não precisa ser difícil nem de muito espaço! Você pode começar construindo uma mini horta com vegetais como alface, couve, tomate cereja e outros temperos. É sustentável e mais barato 🥬🍅.",
            
            "🚲 Se puder, vá de bike ou a pé: Opte por meios de transporte ecológicos, economize grana e faça um exercício saudável 💪🚴‍♀️",
            
            "💡 Economize energia: Apague as luzes e desligue aparelhos quando não estiver usando. Ajudar o planeta é bom pra todos 💡🌍",
            
            "🗣️ Junte a comunidade: Participe de movimentos sociais e lute por políticas públicas que cuidem do clima e da nossa quebrada 👥📢",
            "*Dica 5:* Considere isso...",
            
            "🔄 Reutilize e recicle: Antes de jogar fora, pense se dá pra reutilizar ou reciclar ♻️🗑️",
            
            "📚 Conhecimento é poder: Estude sobre o clima e Racismo Ambiental. O saber fortalece nossa luta 📚💪",

            "🍴 Compartilhe a comida: Se tiver sobrando, compartilhe com quem precisa. Vamos combater o desperdício e a fome 🍽️🤝",
            
            "🤝 Organize a galera: Mobilize a comunidade para ações sustentáveis. Juntos, somos mais fortes 🤝🌍",
        ]
        return random.choice(tips) + text_backmenu, STATE_MAIN_MENU
    
    elif incoming_msg == "2":
        return "*Baixe nosso livro digital no link a seguir:* https://www.instagram.com/institutoduclima/" + text_backmenu, STATE_MAIN_MENU
    
    elif incoming_msg == "3":
        return (
            """*Se você estiver em uma situação de emergência, ligue para um desses órgãos, eles vão te ajudar a qualquer momento!*
• Defesa Civil – 199
• Polícia Militar – 190
• Bombeiros – 193
• SAMU – 192""" + text_backmenu, STATE_MAIN_MENU
        )

    elif incoming_msg == "4":
        return "Qual município que você mora?" + text_backmenu, STATE_REPORT_CITY
    
    elif incoming_msg == "5":
        return (
            """*5 - Sobre qual ação do Instituto você gostaria de falar?*
            
*1* - Pré-Conferência de Racismo Ambiental, Eventos Climáticos Extremos e Justiça Climática do Rio de Janeiro
*2* - Plataforma de educação climática inKetu
*3* - Ações territoriais nacionais
*4* - Litigância climática e incidência política popular 
*5* - Projetos de Leis em incidência 
""" + text_backmenu, STATE_MENU5
        )
    
    elif incoming_msg == "6":
        return "*6 -* De 1 a 10, quanto você recomendaria a Pré-Conferência de Racismo Ambiental, Eventos Climáticos Extremos e Justiça Climática do Rio de Janeiro para seus amigos e parentes?" + text_backmenu, STATE_FEEDBACK_RATING
            
# STATES OF SUBMENU 4    
def handle_state_report_city(incoming_msg, user, phone_number):
    user["city"] = incoming_msg  # Armazena o município informado pelo usuário
    return "Em qual bairro você encontrou esse problema?" + text_backmenu, STATE_REPORT_NEIGHBORHOOD

def handle_state_report_neighborhood(incoming_msg, user, phone_number):
    user["neighborhood"] = incoming_msg  # Armazena o bairro informado pelo usuário
    return "Qual o *CEP* do local em que o problema está acontecendo?" + text_backmenu, STATE_REPORT_ZIP

def handle_state_report_zip(incoming_msg, user, phone_number):
    user["zip"] = incoming_msg  # Armazena o CEP informado pelo usuário
    response = """
Agora nos diga qual tipo de problema você está enfrentando na sua comunidade?

*1 - Falta de saneamento de água*
*2 - Falta de saneamento de esgoto*
*3 - Desmatamento de área verde*
*4 - Risco de deslizamento*
*5 - Outros*
""" + text_backmenu
    
    

    return response, STATE_REPORT_PROBLEM

def handle_state_report_problem(incoming_msg, user, phone_number):
        problems = {
            "1": "Falta de saneamento de água",
            "2": "Falta de saneamento de esgoto",
            "3": "Desmatamento de área verde",
            "4": "Risco de deslizamento",
            "5": "Outros"
        }
        selected_problem = problems.get(incoming_msg)
        if selected_problem:
            user["problem"] = selected_problem  # Armazena o problema informado pelo usuário
            return f"Obrigado por informar o problema: *{selected_problem}*. Vamos agir juntos!" + text_backmenu, STATE_MAIN_MENU
        else:
            return "Opção inválida. Por favor, selecione uma opção de 1 a 5." + text_backmenu, STATE_REPORT_PROBLEM

# STATES OF MENU 5
def handle_state_menu5(incoming_msg, user, phone_number):
    if incoming_msg == "1":
        return ("""
*5.1 A Pré-Conferência no Rio de Janeiro aconteceu dia 19 de agosto de 2023 e recebeu mais mais de 350 pessoas, abordando a necessidade de combater o racismo ambiental, eventos climáticos extremos e promoção de uma justiça climática antirracista. Foi um passo essencial para a construção de um presente menos desigual 💚🌎
""" + text_backmenu), STATE_MAIN_MENU

    elif incoming_msg == "2":
        return ("""
*5.2 🌱 Plataforma de educação climática inKetu:* inKetu é nossa plataforma de educação climática projetada para capacitar indivíduos com conhecimento e insights acionáveis sobre questões socio ambientais e climáticas. É um recurso fantástico para aprender e realizar ações positivas para o planeta. 🌿📚
""" + text_backmenu), STATE_MAIN_MENU

    elif incoming_msg == "3":
        return ("""
*5.3 🏞️ Ações Territoriais Nacionais:* Nossa iniciativa de Ações Territoriais Nacionais se concentra nos esforços locais para proteger grupos e territórios vulnerabilizados (comunidade negra, indígena, quilombola, caiçara, em vulnerabilidade social). Se você tem alguma ideia de ação que podemos fazer na sua comunidade, é só nos contar! 🌳💪 
""" + text_backmenu), STATE_MAIN_MENU
    
    elif incoming_msg == "4":
        return ("""
*5.4 🏞️ Ações Territoriais Nacionais:* Nossa iniciativa de Ações Territoriais Nacionais se concentra nos esforços locais para proteger grupos e territórios vulnerabilizados (comunidade negra, indígena, quilombola, caiçara, em vulnerabilidade social). Se você tem alguma ideia de ação que podemos fazer na sua comunidade, é só nos contar! 🌳💪 
""" + text_backmenu), STATE_MAIN_MENU
    
    elif incoming_msg == "5":
        return ("""
*5.5 🏞️ Ações Territoriais Nacionais:* Nossa iniciativa de Ações Territoriais Nacionais se concentra nos esforços locais para proteger grupos e territórios vulnerabilizados (comunidade negra, indígena, quilombola, caiçara, em vulnerabilidade social). Se você tem alguma ideia de ação que podemos fazer na sua comunidade, é só nos contar! 🌳💪 
""" + text_backmenu), STATE_MAIN_MENU

    else:
        return "Opção inválida." + text_backmenu, STATE_MENU5
    
def handle_state_feedback_rating(incoming_msg, user, phone_number):
    # Verificar se a mensagem é um número entre 0 e 10
    try:
        rating = int(incoming_msg)
        if 0 <= rating <= 10:
            user["rating"] = rating
            return "Obrigado pela classificação!\n\nQuais temas e ações práticas de demandas dos territórios e grupos mais afetados precisam ser abordadas em ações de incidência e justiça climática antirracista pelo Duclima?", STATE_FEEDBACK_COMMENT
        else:
            return "Por favor, forneça uma classificação de 0 a 10." + text_backmenu, STATE_FEEDBACK_RATING
    except ValueError:
        return "Por favor, forneça uma classificação válida de 0 a 10." + text_backmenu, STATE_FEEDBACK_RATING

def handle_state_feedback_comment(incoming_msg, user, phone_number):
    # Armazenar o feedback do usuário (se necessário)
    user["feedback"] = incoming_msg

    # Remover o usuário de user_data para finalizar a sessão
    if phone_number in user_data:
        del user_data[phone_number]
    return "Obrigado pelo seu feedback! Ele é muito importante para nós. Até a próxima!", None

# Funções de manipulador de estado para os outros estados conforme necessário
state_handlers = {
    STATE_MAIN_MENU: handle_state_main_menu,
    # states hndlers menu 4
    STATE_REPORT_CITY: handle_state_report_city,
    STATE_REPORT_NEIGHBORHOOD: handle_state_report_neighborhood,
    STATE_REPORT_ZIP: handle_state_report_zip,
    STATE_REPORT_PROBLEM: handle_state_report_problem,
    # states hndlers menu 5
    STATE_MENU5: handle_state_menu5,
    # states handler menu 6
    STATE_FEEDBACK_RATING: handle_state_feedback_rating,
    STATE_FEEDBACK_COMMENT: handle_state_feedback_comment,
}

@app.route('/bot', methods=['POST'])
def bot():
    phone_number = request.values.get('From', '')  # <--- DEFINIÇÃO DE phone_number DEVE SER A PRIMEIRA COISA
    incoming_msg = request.values.get('Body', '').strip().lower()
    log_message("incoming", phone_number, incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()

    user = user_data.get(phone_number, {})
    current_state = user.get("state", STATE_MAIN_MENU)

    # Obtenha a hora atual
    now = datetime.datetime.now()

    # Se o número de telefone do usuário já existir em user_data, verifique a duração desde a última mensagem
    if phone_number in user_data:
        time_since_last_message = now - user_data[phone_number].get("last_message_time", now)

        # Aplicar temporizador de sessão
        if time_since_last_message > datetime.timedelta(minutes=2):  # Tempo de sessão de 2 minutos
            # Aqui é onde você adiciona o log
            logging.info(f"Sessão expirada para o número de telefone {phone_number}")
            
            del user_data[phone_number]
            msg.body("Sua sessão expirou. Por favor, comece novamente.")
            return str(resp)

        # Aplicar o limite de mensagens por minuto
        if time_since_last_message < datetime.timedelta(minutes=1):
            message_count[phone_number] = message_count.get(phone_number, 0) + 1
            if message_count[phone_number] > 20:  # Limite de 5 mensagens por minuto
                msg.body("Você enviou muitas mensagens em um curto período de tempo. Por favor, aguarde um minuto.")
                return str(resp)
        else:
            message_count[phone_number] = 1
        user_data[phone_number]["last_message_time"] = now
    else:
        # Se é a primeira vez que o usuário envia uma mensagem, inicialize seus dados
        user_data[phone_number] = {
            "last_message_time": now,
            "message_count": 1
        }

    if current_state in state_handlers:
        response, next_state = state_handlers[current_state](incoming_msg, user, phone_number)
    else:
        response, next_state = state_handlers[incoming_msg](incoming_msg, user, phone_number)

    if next_state:
        user["state"] = next_state
        user_data[phone_number] = user

    log_message("outgoing", phone_number, response)

    msg.body(response)
    return str(resp)


if __name__ == '__main__':
    app.run(debug=True)
