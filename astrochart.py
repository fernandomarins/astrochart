import streamlit as st
import datetime
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from geopy.geocoders import Nominatim

def convert_coordinates(x, y):
    
    # check if the value is negative
    if x < 0:
        # convert to str
        x = str(x)
        # drop the first character
        x = x[1:]
        # split into two parts
        x = x.split('.')
        # addin the s letter for south
        x = x[0] + 's' +  x[1]
    else:
        x = str(x)
        x = x.split('.')
        # if it's not negative, then add the letter n
        x = x[0] + 'n' +  x[1]
    if y < 0:
        y = str(y)
        y = y[1:]
        y = y.split('.')
        # here we need to add the letter e, for east
        y = y[0] + 'e' +  y[1]
    else:
        y = str(y)
        print(y)
        y = y.split('.')
        print(y)
        # here we add the letter w for west
        y = y[0] + 'w' +  y[1]
        print(y)
    
    return (x, y)

def return_coordinates(local):
    geolocator = Nominatim(user_agent='geo')
    location = geolocator.geocode(local, timeout=10000)
    return (location.latitude, location.longitude)

dictionary_signs = {
    'Sun': {
        'Aries': 'Você tem tudo para brilhar ao ser corajoso, assertivo e dinâmico. Você se sente vitalizado quando alcança cada dia mais independência. Tem tam- bém a capacidade de liderar de forma criativa e inspirada. É uma pessoa que se destaca ao motivar e entusiasmar as pessoas.Assuma seu poder autoafirmativo, seu dinamismo e sua disposição em desbravar o novo. Ao se arriscar, seguindo sua intuição e seu impulso assertivo, você obterá o merecido reconhecimento de ser alguém único, especial e repleto de vida.',
        'Taurus': 'Você tem tudo para se destacar ao agir com praticidade, perseverança e cautela. Devagar se vai ao longe. Gradualmente, você conquista sua se- gurança e sua estabilidade, principalmente material e profissional. E isso lhe proporciona muita vitalidade.Você brilha ao ser um ponto de apoio para as pessoas. Sua postura firme e determinada ampara aqueles que precisam se sentir protegidos e apoiados. É, portanto, capaz de agir com simplicidade, competência e com um bom senso que harmoniza os ambientes e as pessoas. E, assim, obter o reconhecimento por ser essa pessoa que repercute a beleza, o conforto e o prazer por onde passa.',
        'Gemini': 'Você pode se destacar através de suas habilidades mentais, intelec- tuais, manuais e comunicativas. Você brilha quando está se socializando, trocando ideias, aprendendo e compartilhando seus conhecimentos.Você se sente cheio de vida quando pode demonstrar sua versatilida- de e sua capacidade de entender questões complexas. E também te pro- porciona muita vitalidade o fato de conseguir escrever, falar, enfim, se comunicar de uma maneira que faça as pessoas arejarem suas mentes e entenderem outros pontos de vista.',
        'Cancer': 'Você tende a brilhar quando desenvolve sua sensibilidade, seu espírito protetor e oferece segurança emocional às pessoas, principalmente de seu núcleo doméstico e familiar. Tende a se destacar através de sua imaginação, de seu dinamismo empreendedor e de sua capacidade de amparar emocionalmente as pessoas. Você se sente repleto de vida quando encara sua carência e amadurece sua maneira de lidar com as emoções. A conquista de segurança emocio- nal, familiar, doméstica e residencial também te deixa vitalizado.',
        'Leo': 'Você se destaca ao se expressar com criatividade, inspiração e auto- confiança. Você se sente cheio de vida quando se expõe de forma firme, calorosa e entusiasmada. Tem o poder de brilhar ao liderar e motivar as pessoas. Quando mais assumir seu brilho criativo, sua luz interior, empolgando as pessoas através do que intui e expressa, mais cheio de vida você será. Reconheça seu desejo por reconhecimento pessoal, por receber a atenção por ser quem é. Uma saudável vaidade é tremendamente importante no seu caminho de vida. Você nasceu para influenciar as pessoas através de seu carisma e poder expressivo.',
        'Virgo': 'Você brilha ao lidar com questões práticas, administrativas e que de- mandem um conhecimento especializado. Pode se destacar ao servir e ser útil às pessoas. Ao demonstrar sua eficiência e sua prestatividade, tem tudo para receber o merecido reconhecimento. Tem um jeito criativo de produzir e realizar suas metas, ainda mais se passar pelo paciente processo do planejamento e das constantes pesquisas a respeito daquilo que visa concretizar. Com perseverança, praticidade e senso de organização, você utiliza suas habilidades mentais, intelectuais e manuais de um jeito que te destaca.',
        'Libra': 'Você pode se destacar por meio de seu senso de justiça, filosófico e artístico. Pois brilha quando aplica sua inteligência e sua capacidade de enxergar os vários lados de cada questão para estabelecer acordos justos. Quanto mais utiliza sua habilidade diplomática, estética e estratégica, mais se sente vitalizado. Tem tudo para usar criativamente seu poder de conciliar e unir pessoas, ideias e ambientes aparentemente divergentes. Isso te proporciona prazer e reconhecimento.',
        'Scorpio': 'Você pode se destacar ao tratar de questões consideradas tabus ou sim- plesmente assumindo seu poder emocional, psíquico, financeiro, sexual e transformador. Pois você brilha ao superar crises e incentivar as pessoas a também renascerem. Tem a força de encarar o que não está tão aparente e agir com criatividade na expressão do que até então encontrava-se oculto, inconsciente, sob os véus do mistério. Sente-se repleto de vida quando reconhece determinados medos e in- veste corajosamente sua energia na superação dos mesmos. Daí o fato de poder obter o merecido reconhecimento por ser um agente catalisador de mudanças, principalmente por encarar com sabedoria a transitoriedade da vida e enxergar a força pessoal que se extrai das crises.',
        'Sagittarius': 'Você tem tudo para brilhar ao usar sua intuição, sua inspiração e suas habilidades professorais. Porque você se destaca ao ampliar a mente das pes- soas, alargando os horizontes perceptivos delas. Principalmente pelo fato de que você se sente vitalizado ao questionar as coisas com um olhar filosófico. Por isso, você pode obter o merecido reconhecimento por ser uma pessoa voltada para compreender a vida e encontrar um sentido maior para a mesma. Especialmente através de uma expansão cultural, religiosa, acadêmica, espiritual, jurídica e existencial. Enxergar longe e mostrar essa visão ampla das coisas é algo que te deixa entusiasmado.',
        'Capricorn': 'Você brilha ao demonstrar sua competência, sua produtividade e seu poder de influência social. Tem tudo para se destacar ao se preparar com muita paciência, praticidade e planejamento para assumir um papel de au- toridade na sociedade. Pode sentir-se vitalizado quando obtém o reconhecido por aquilo que empreende, produz e realiza. E essas ambições de conquistar um posição de sucesso, poder e respeitabilidade precisam ser assumidas com naturali- dade e criatividade. Desse modo, conquistará o merecido reconhecimento por agir de forma tão disciplinada e qualificada.',
        'Aquarius': 'Você tem tudo para se destacar ao assumir seu jeito original de ser, pensar e se expressar. Porque você brilha quando compartilha suas ideias avançadas, sua intuição visionária e seus conhecimentos humanitários. Com espí- rito fraterno e unido a um grupo de pessoas de ideais semelhantes aos seus, pode exercer uma liderança criativa e promover mudanças na sociedade. Assim, você se sente vitalizado quando pensa diferente, quando estuda algo avançado e quando comunica seus conhecimentos. Aí obterá o mere- cido reconhecimento ao agir com esse humanitarismo. Ainda mais se sua individualidade se destacar e deixar sua marca na comunidade por meio da defesa de seus ideais sociais.',
        'Piscis': 'Você tem tudo para brilhar ao se expressar de modo compassivo, ima- ginativo, artístico e sensível. Pois se destaca ao se doar e ajudar as pessoas, principalmente através de um saudável autossacrifício repleto de encanto, sabedoria e inspiração emocional. Obter o reconhecimento por ter uma afinidade com as questões espirituais, artísticas, oníricas, inconscientes e imaginativas pode demandar que aceite sua sensibilidade e reconheça a importância de momentos de solidão, reflexão e busca por uma sintonia com Deus/Vida.'
    },
    'Moon': {
        'Aries': '',
        'Taurus': '',
        'Gemini': '',
        'Cancer': '',
        'Leo': '',
        'Virgo': '',
        'Libra': '',
        'Scorpio': '',
        'Sagittarius': '',
        'Capricorn': '',
        'Aquarius': '',
        'Piscis': ''
    }
}

st.title('ASTROCHART')

st.header('Por favor coloque sua data, horário e local de nascimento ao lado')

date = st.sidebar.date_input('Data de Nascimento no formato ANO/MÊS/DIA', datetime.date.today()).strftime("%Y/%m/%d")
hour = st.sidebar.text_input('Horário de Nascimento no seguinte formato: 18:31', '18:31')
local = st.sidebar.text_input('Cidade de nascimento:', 'Araraquara')

lat, log = return_coordinates(local)
coord = convert_coordinates(lat, log)

full_date = Datetime(date, hour)

pos = GeoPos(coord[0], coord[1])
chart = Chart(full_date, pos)

sun = chart.getObject(const.SUN)
sun_sign = str(sun).split()[0][1:]

c1, c2 = st.beta_columns(2)
c1.subheader('Seu signo solar é:')
c2.subheader(sun.sign)

st.write(dictionary_signs[sun_sign][sun.sign])












