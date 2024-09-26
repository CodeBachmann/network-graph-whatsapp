import unicodedata
from textblob import TextBlob
import datetime as dt, calendar
import pandas as pd
from PIL import Image
import math
import numpy as np
import re
import demoji
from bs4 import BeautifulSoup
import language_tool_python
tool = language_tool_python.LanguageTool('pt-BR')


ontem = dt.datetime(2024, 1, 8, 9, 26, 25, 466967)
date_time = ontem.strftime(r"%Y-%m-%d %H:%M:%S")

# CONVERTE UMA VARIAVEL EPOCH INT PARA DATETIME

def epoch_to_datetime(date):
    date_dt = dt.datetime.fromtimestamp(date)
    return date_dt

# CONVERTE UMA VARIAVEL DATETIME PARA O EPOCH NO FORMATO STRING

def datetime_to_epoch(date):
    date_epoch = calendar.timegm(date.timetuple())
    return date_epoch

# CONVERTE DUAS DATAS PARA EPOCH

def start_end_datetime_epoch(startDate,endDate):
    startDate_epoch = datetime_to_epoch(startDate)
    endDate_epoch = datetime_to_epoch(endDate)
    return startDate_epoch, endDate_epoch

# CONVERTE SEGUNDOS EM HORAS, MINUTOS E SEGUNDOS

def deduct_time(startDate, endDate):
    time =  endDate - startDate
    return time

def seconds_to_time(epoch):
    hours = epoch/3600

    hours_rounded_down = math.floor(hours)
    if hours_rounded_down == -1:
        hours_rounded_down = 0

    minutes = (hours - hours_rounded_down)*60

    minutes_rounded_down = math.floor(minutes)
    if minutes_rounded_down == -1:
        minutes_rounded_down = 0

    seconds = (minutes - minutes_rounded_down )*60

    seconds_rounded_down = math.floor(seconds)
    if seconds_rounded_down == -1:
        seconds_rounded_down = 0

    if hours_rounded_down < 10:
        hours_rounded_down = f'0{hours_rounded_down}'
    
    if minutes_rounded_down < 10:
        minutes_rounded_down = f'0{minutes_rounded_down}'

    if seconds_rounded_down < 10:
        seconds_rounded_down = f'0{seconds_rounded_down}'

    time = f'{hours_rounded_down}:{minutes_rounded_down}:{seconds_rounded_down}'
    return time

def montar_query_insert(dic, table, now):
    column = '('
    values = '('
    for i in dic:
        a = dic[i]
        if a != "":
            column += f"{i}, "
            values += f"'{a}', "
    
    column = column[:-2]
    values = values[:-2]
    now = str(now).upper()
    if now == "SIM":
        column += ", data_criada"
        values += ", now()" 
    column += ')'
    values += ')'
    query = f"""INSERT INTO {table} {column} VALUES {values};"""
    return query

def montar_query_update(dic, table, where, id, now):
    column = []
    values = []
    for i in dic:
        a = dic[i]
        column.append(i)
        values.append(a)
        #INSERT INTO {table}() VALUES ()"
    vc = ''

    tamanho = len(column)
    cont_tamanho = 0
    for x in range(len(column)):
        cont_tamanho += 1
        if cont_tamanho != tamanho :
            if values[x] != '' or column[x] == 'pedido':
                vc += (f"{column[x]} = '{values[x]}', ")
            else:
               pass
        elif cont_tamanho == tamanho:
            if values[x] != '' or column[x] == 'pedido':
                vc += (f"{column[x]} = '{values[x]}'")


    vc = vc.rstrip(', ')

    if now == "sim":
        vc += ", data_atualizada = now()"
    query = f"""UPDATE {table} SET {vc} WHERE {where} = '{id}';"""
    return query

def montar_query_select(column, table):
    
    query = f"SELECT {column} FROM {table}"
    return query

def montar_query_ler_conversa(protocolo):

    query = f"select remetente, mensagem from mirante.HI_conversas where protocolo = '{protocolo}' order by indiceConversa"
    return query

def montar_query_view_where(dataInicio, dataFim, coluna, table):

    query = f"SELECT {coluna} FROM {table} where dataInicio > '{dataInicio}' and dataFim < '{dataFim}'"
    return query

def query_preguicosa_view_where(id_post):
    query = f"select shares, impressions, plays, video_views, reach, comments, navigation, likes, saved, total_interactions, profile_activity from IG_posts where idpostsInsta = '{id_post}'"
    return query

def montar_query_view_where_unitario(dic, table, now, where, comparativo):
    column = ''
    for i in dic:
        column += f"{i}, "
    column = column[:-2]
    if now == "sim":
        column += ", data_criada" 
    query = f"""Select {column} from {table} where {where} = {comparativo};"""
    return query



def convert_webp_to_jpg(input_file, output_file):
    try:
        # Open the WebP image
        with Image.open(input_file) as img:
            # Convert to RGB mode if the image is in CMYK mode
            if img.mode == 'CMYK':
                img = img.convert('RGB')
            
            # Save as JPG
            img.save(output_file, 'JPEG')
            
        print('Conversion successful!')
        
    except IOError:
        print(f'Unable to open {input_file}')

def limpa_requisicao_banco(response):
    lista_temp = []
    lista_data_temp = []
    for x in response:
        quantidades = len(x)
        for quant in range(quantidades):
            if isinstance(x[quant],str):
                lista_temp.append(x[quant])
            else:
                lista_temp.append(x[quant])

    return lista_temp

def limpa_requisicao_banco_dic(response):
    lista_temp = []
    lista_data_temp = []
    for x in response:
        quantidades = len(x)
        for quant in range(quantidades):
            if isinstance(x[quant],str):
                lista_temp.append(x[quant])
            else:
                lista_data_temp.append(x[quant])
    dic_temp = {

        "lista_temp":lista_temp,
        "lista_data_temp":lista_data_temp

    }
    return dic_temp

def pega_token_dinamize():
    xlsx = pd.read_excel("C:\\Users\\User\\Desktop\\Mirante_Automatiza\\Mirante\\Dinamize\\rf_token.xlsx")
    df = pd.DataFrame(xlsx)
    access_token = str(df.at[0,"Rf_token"])
    return access_token

def tempo_de_fila(telA, dataI, df_compara):

    df = pd.DataFrame(df_compara)
    horario_limite_quatro_meia = dt.time(13, 30, 0)
    horario_limite_tres_meia = dt.time(12, 30, 0)
    horario_limite_sete_meia = dt.time(4, 30, 0)

    # Converta a coluna 2 para o tipo datetime, se necessário
    df[1] = pd.to_datetime(df[1])

    # Filtra os dados
    filtered_df = df[(df[0] == telA) & (df[1] < dataI)]
    maxDfB = (filtered_df[1].max()).to_pydatetime()
    if pd.isnull(maxDfB) != True:   
        # Calcula a diferença entre y e maxDfB
        y_datetime = dataI  # Converte y para datetime

        # Filtro de Segunda a Quinta
        if maxDfB.weekday() < 4:
            if maxDfB.time() > horario_limite_quatro_meia:
                difference = y_datetime - maxDfB - (((maxDfB + dt.timedelta(days=1)).replace(hour=4, minute=30))-maxDfB)
            elif maxDfB.time() < horario_limite_sete_meia:
                difference = y_datetime - maxDfB - ((maxDfB.replace(hour=4, minute=30))-maxDfB)
            else:
                difference = y_datetime - maxDfB

        #Filtro de Sexta feira
        elif maxDfB.weekday() < 5:

            if maxDfB.time() > horario_limite_tres_meia:
                difference = y_datetime - maxDfB - (((maxDfB + dt.timedelta(days=3)).replace(hour=4, minute=30))-maxDfB)

            elif maxDfB.time() < horario_limite_sete_meia:
                difference = y_datetime - maxDfB - ((maxDfB.replace(hour=4, minute=30))-maxDfB)
            else:
                difference = y_datetime - maxDfB

        #Filtro de Sabado 
        elif maxDfB.weekday() < 6:
            difference = y_datetime - maxDfB - (((maxDfB + dt.timedelta(days=2)).replace(hour=4, minute=30))-maxDfB)

        #Filtro de Domingo
        else:
            difference = y_datetime - maxDfB - (((maxDfB + dt.timedelta(days=1)).replace(hour=4, minute=30))-maxDfB)

        # transforma os dias em horas
        if difference.days > 0:
            dias_em_horas = (int(difference.days))*24

        minutos_quebrados, horas = math.modf(int(difference.seconds)/3600)
        segundos_quebrados, minutos  =math.modf(minutos_quebrados*60)
        segundos = round(segundos_quebrados*60, 0)
        if difference.days > 0:
            horas += dias_em_horas

        horas = int(horas)
        minutos = int(minutos)
        segundos = int(segundos)

        tempo_de_fila = f'{horas}:{minutos}:{segundos}'

        return tempo_de_fila
    return False

def segundos_para_time(segundos):
    minutos_quebrados, horas = math.modf(int(segundos)/3600)
    segundos_quebrados, minutos  =math.modf(minutos_quebrados*60)
    segundos = round(segundos_quebrados*60, 0)
    
    if segundos > 59:
        segundos = 0
        minutos += 1

    if minutos > 59:
        minutos = 0
        horas += 1
    

    horas = int(horas)
    minutos = int(minutos)
    segundos = int(segundos)

    tempo_de_fila = f'{horas}:{minutos}:{segundos}'

    return tempo_de_fila

# Função para encontrar e-mails em uma string
def encontrar_emails(texto):
    # Padrão de expressão regular para encontrar e-mails
    padrao_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    
    # Encontrando todos os e-mails no texto usando o padrão
    emails_encontrados = re.findall(padrao_email, texto)
    
    return emails_encontrados

def encontrar_cpfs(texto):
    # Expressão regular para encontrar CPFs no formato "### ### ### ##"
    padrao_cpf_space = r'\b\d{3} \d{3} \d{3} \d{2}\b'

    # Encontrar todos os CPFs no texto usando a expressão regular
    cpfs_encontrados_space = re.findall(padrao_cpf_space, texto)

    # Expressão regular para encontrar CPFs no formato "###.###.###-##"
    padrao_cpf_point = r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b'

    # Encontrar todos os CPFs no texto usando a expressão regular
    cpfs_encontrados_point = re.findall(padrao_cpf_point, texto)

    padrao_cpf = r'\b\d{11}\b'

    # Encontrar todos os CPFs no texto usando a expressão regular
    cpfs_encontrados = re.findall(padrao_cpf, texto)

    for c in cpfs_encontrados_point:
        c = c.replace('.',"").replace(",","").replace('-','')
        cpfs_encontrados.append(c)
    
    for c in cpfs_encontrados_space:
        c = c.replace(' ',"")
        cpfs_encontrados.append(c)
    
    return(cpfs_encontrados)

def validar_cpf(cpf):
    # Remove caracteres não numéricos do CPF
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais (caso especial que não é um CPF válido)
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula o primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[9]):
        return False
    
    # Calcula o segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[10]):
        return False
    
    # Se passou por todas as verificações, o CPF é válido
    return True

# Função para formatar CNPJ com máscara
def formata_cnpj(cnpj):
    return '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])

# Função para encontrar CNPJs em uma string com ou sem pontuação explícita
def encontrar_cnpjs(texto):
    # Padrão de expressão regular para encontrar CNPJs
    padrao_cnpj = r'\b(?:CNPJ\s*é?|CNPJ\s*da\s*empresa\s*é?)\s*(\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2})\b|\b(\d{14})\b'
    
    # Encontrando todos os CNPJs no texto usando o padrão
    cnpjs_encontrados = re.findall(padrao_cnpj, texto)
    
    # Filtrando os resultados para retornar somente os CNPJs válidos
    cnpjs_validos = []
    for cnpj in cnpjs_encontrados:
        if cnpj[0]:  # Se encontrou o CNPJ com pontuação explícita
            if len(cnpj[0]) < 17:
                cnpj_formatado = formata_cnpj(cnpj[0])
                cnpjs_validos.append(cnpj_formatado)
            else:
                cnpjs_validos.append(cnpj[0])            
    
    return cnpjs_validos

# Função para encontrar números de pedido em um texto
def encontrar_pedidos(texto):
    # Padrão de expressão regular para encontrar números de pedido
    padrao_pedido = r'\b(\d{6})\b'
    
    # Encontrando todos os números de pedido no texto usando o padrão
    pedidos_encontrados = re.findall(padrao_pedido, texto)
    try:
        pedidos_encontrados = pedidos_encontrados.pop(123456)
    except:
        pass
    # Retornando os números de pedido encontrados
    return pedidos_encontrados

def extrair_dominio(email):
    print(email)
    # Split the email at '@'
    local_part, domain_part = email.split('@')
    
    # Split the domain part at '.'
    domain = domain_part.split('.')[0]
    
    return domain

def remove_emojis(text):
    """Remove emojis from text using demoji."""
    return demoji.replace(text, ' ')

def remove_html_and_css(text):
    """Remove HTML tags and CSS styles from text."""
    # Use BeautifulSoup to remove HTML tags
    soup = BeautifulSoup(text, 'html.parser')
    # Extract text without tags
    text_without_html = soup.get_text()
    # Remove CSS styles and other unwanted text
    text_without_css = re.sub(r'<style.*?>.*?</style>', '', text_without_html, flags=re.DOTALL)
    return text_without_css

def clean_text(text):
    """Remove emojis, HTML tags, and CSS styles."""
    text = str(text)
    text = remove_html_and_css(text)
    text = re.sub(r'\xa0', ' ', text) # Substituir \xa0 por espaço
    text = re.sub(r'\n', ' ', text)    # Substituir \n por espaço
    text = re.sub(r'\t', ' ', text)
    text = re.sub(r"'", "", text)
    return remove_emojis(text)


# Função para garantir que haja um espaço após as pontuações
def ultra_clean_text(text):
    text = clean_text(text)
    # Regex para encontrar pontuações seguidas por texto sem espaço
    pattern = r'([!?,.;])(?!\s)'
    
    # Substituir pontuações encontradas por elas mesmas seguidas de um espaço
    cleaned_text = re.sub(pattern, r'\1 ', text)
    
    return cleaned_text

def correct_text(text):
    """
    Corrige erros gramaticais e ortográficos no texto usando LanguageTool.

    Parameters:
    text (str): Texto com possíveis erros gramaticais e ortográficos.

    Returns:
    str: Texto corrigido.
    """
    # Inicializa o corretor para português
    
    
    # Encontra erros no texto
    matches = tool.check(text)
    
    # Corrige os erros
    corrected_text = language_tool_python.utils.correct(text, matches)
    
    return corrected_text


def corrigir_abreviacoes(texto):
    # Criar um padrão de regex para encontrar as abreviações

    abreviacoes = {
    "vc": "voce",
    "vcs" "voces"
    "tb": "também",
    "pq": "porque",
    "q": "que",
    "blz": "beleza",
    "sdds": "saudades",
    "sqn": "so que não",
    "vlw": "valeu",
    "tmj": "tamo junto",
    "mddc": "meu deus do ceu",
    "plmdds": "pelo amor de deus",
    "vdd": "verdade",
    "slk": "se é louco",
    "mlr": "melhor",
    "tlgd": "tá ligado",
    "pv": "privado",
    "plmns": "pelo menos",
    "ngc": "negócio",
    "dps": "depois",
    "ft": "foto",
    "fml": "família",
    "rlx": "relaxa",
    "fut": "futebol",
    "bj": "beijo",
    "ajd": "ajuda",
    "pls": "por favor",
    "obg": "obrigado",
    "att": "entendo",
    "msm": "mesmo",
    "msg": "mensagem",
    "add": "adicionar",
    "amg": "amigo",
    "cmg": "comigo",
    "glr": "galera",
    "pprt": "papo reto",
    "cvs": "conversar",
    "ss": "sim",
    "qt": "quanto",
    "nn": "nao",
    "clr": "celular",
    "sla": "sei la",
    "qria": "quero",
    "qser": "quiser",
    "pft": "perfeito",
    "dnv": "de novo",
    "vms": "vamos",
    "flw": "falou",
    "trd": "tarde",
    "aq": "aqui",
    "bnt": "bonito",
    "ngm": "ninguém",
    "vl": "vê lá",
    "krl": "caralho",
    "pnc": "pau no cu",
    "fdc": "foda-se",
    "tmb": "também",
    "ns": "nos",
    "td": "tudo",
    "tm": "tamo",
    "hj": "hoje",
    "ont": "ontem",
    "pds": "pode ser",
    "agr": "agora",
    "ndv": "nada a ver",
    "fdd": "fudeu",
    "xau": "tchau",
    "blz": "beleza",
    "tlg": "entendo",
    "pfv": "por favor",
    "nss": "nossa",
    "mlk": "moleque",
    "mds": "meu deus",
    "fds": "final de semana",
    "pprt": "falo serio",
    "atacado": "wholesale",
    "atacadista": "wholesale",
    "bermuda": "shorts"

    }
    
    padrao = re.compile(r'\b(' + '|'.join(re.escape(key) for key in abreviacoes.keys()) + r')\b')
    
    # Substituir as abreviações no texto
    texto_corrigido = padrao.sub(lambda x: abreviacoes[x.group()], texto)
    
    return texto_corrigido

def remover_acentos(texto):
    # Normaliza o texto para NFD (Normalização de Formas Decomponíveis)
    texto_normalizado = unicodedata.normalize('NFD', texto)
    
    # Filtra apenas os caracteres que não são marcas de combinação (acentos)
    texto_sem_acento = ''.join([char for char in texto_normalizado if not unicodedata.combining(char)])
    
    return texto_sem_acento

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', 'link', text, flags=re.MULTILINE)
    
    # Remove emails
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'mail', text)
    
    # Remove usernames (e.g., @username)
    text = re.sub(r'@\w+', 'user', text)
    
    # Remove special characters except for punctuation
    text = remover_acentos(text)
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)

    # Remove extra whitespace
    text = ' '.join(text.split())

    text = corrigir_abreviacoes(texto=text)
    
    return text

def replace_words(text):
    # Dicionário de substituições dentro da função
    alter_words = {

        ' gostaria ': ' quero ',
        ' nao ': ' nao ',
        ' preciso ': ' quero ',
        ' queria ': ' quero ',
        ' desejo ': ' quero ',
        ' negativo ':' nao ',
        ' camiseta': ' camisa ',
        ' quero ':' quero ',
        ' malha fria ':' malha-fria ',
        ' azul marinho ': ' azul-marinho ',
        ' dry fit ': ' dry-fit ',
        ' s ': ' ',
        ' pretendo ': ' quero ',
        ' almejo ': ' quero ',
        ' necessito ': ' quero ',
        ' n ':' nao ',
        ' cartao credito ': ' cartao-credito ',
        ' manga longa ': ' manga-longa ',
        ' loja mirante ': ' loja-mirante ',
        ' nota fiscal ' : ' nf '
        
    }
    
    # Substituindo palavras de acordo com o dicionário
    for word, replacement in alter_words.items():
        text = text.replace(word, replacement)
    return text
    

def remover_stopwords(text):
    
    stop_words = ['adeus','loja mirante', 'agradecemos', 'vou', 'fiz', 'aguardar','esperar', 'a', 'queria', 'certo', 'deu', 'escolha', 'fico', 'espero', 
                  'aguardo', 'ola', 'sim ','oi', 'ok','agora','ai','ainda','alem','algo','alguem','algum','alguma','algumas','alguns','ali',
                  'ampla','amplas','amplo','amplos','ano','anos','ante','antes','ao','aos','apenas','apoio','apos','aquela','aquelas','aquele','aqueles', 
                  'entendi','aqui','aquilo','area','as','as','assim','ate','atras','atraves','baixo','bastante','bem','boa','boas','bom','bons','breve',
                  'ca','cada','catorze','cedo','cento','certamente','certeza','cima','cinco','coisa','coisas','com','como','conselho','contra','contudo',
                  'custa','da','da','dao','daquela','daquelas','daquele','daqueles','dar','das','de','debaixo','dela','delas','dele','deles','demais','dentro',
                  'depois','desde','dessa','dessas','desse','desses','desta','destas','deste','destes','deve','devem','devendo','dever','devera','deverao',
                  'deveria','deveriam','devia','deviam','dez','dezenove','dezesseis','dezessete','dezoito','dia','diante','disse','disso','disto','dito',
                  'diz','dizem','dizer','do','dois','dos','doze','duas','duvida','e','e','ela','elas','ele','eles','em','embora','enquanto','entre','era',
                  'eram','eramos','es','essa','essas','esse','esses','esta','esta','estamos','estao','estar','estas','estas','estava','estavam','estavamos',
                  'este','esteja','estejam','estejamos','estes','esteve','estive','estivemos','estiver','estivera','estiveram','estiveramos','estiverem','estivermos',
                  'estivesse','estivessem','estivessemos','estiveste','estivestes','estou','etc','eu','exemplo','faco','falta','favor','faz','fazeis','fazem',
                  'fazemos','fazendo','fazes','feita','feitas','feito','feitos','fez','fim','final','foi','fomos','for','fora','foram','foramos','forem','forma',
                  'formos','fosse','fossem','fossemos','foste','fostes','fui','geral','grande','grandes','grupo','ha','haja','hajam','hajamos','hao','havemos',
                  'havia','hei','hoje','hora','horas','houve','houvemos','houver','houvera','houvera','houveram','houveramos','houverao','houverei','houverem',
                  'houveremos','houveria','houveriam','houveriamos','houvermos','houvesse','houvessem','houvessemos','isso','isto','ja','la','la','lado','lhe',
                  'lhes','lo','local','logo','longe','lugar','maior','maioria','mais','mal','mas','maximo','me','meio','menor','menos','mes','meses','mesma',
                  'mesmas','mesmo','mesmos','meu','meus','mil','minha','minhas','momento','muita','muitas','muito','muitos','na','nada', 'nao','naquela','naquelas',
                  'naquele','naqueles','nas','nem','nenhum','nenhuma','nessa','nessas','nesse','nesses','nesta','nestas','neste','nestes','ninguem','nivel','no',
                  'noite','nome','nos','nos','nossa','nossas','nosso','nossos','nova','novas','nove','novo','novos','num','numa','numero','nunca','o','obra','obrigada',
                  'obrigado','oitava','oitavo','oito','onde','ontem','onze','os','ou','outra','outras','outro','outros','para','parece','parte','partir','paucas','pela',
                  'pelas','pelo','pelos','pequena','pequenas','pequeno','pequenos','per','perante','perto','pode','pude','pode','podem','podendo','poder','poderia',
                  'poderiam','podia','podiam','poe','poem','pois','ponto','pontos','por','porem','porque','porque','posicao','possivel','possivelmente','posso','pouca',
                  'poucas','pouco','poucos','primeira','primeiras','primeiro','primeiros','propria','proprias','proprio','proprios','proxima','proximas','proximo',
                  'proximos','pude','puderam','quais','quais','qual','quando','quanto','quantos','quarta','quarto','quatro','que','que','quem','quer','quereis','querem',
                  'queremas','queres','questao','quinta','quinto','quinze','relacao','sabe','sabem','sao','se','segunda','segundo','sei','seis','seja','sejam',
                  'sejamos','sem','sempre','sendo','ser','sera','serao','serei','seremos','seria','seriam','seriamos','sete','setima','setimo','seu','seus','sexta',
                  'sexto','si','sido','sim','sistema','so','sob','sobre','sois','somos','sou','sua','suas','tal','talvez','tambem','tampouco','tanta','tantas','tanto',
                  'tao','tarde','te','tem','tem','tem','temos','tendes','tendo','tenha','tenham','tenhamos','tenho','tens','ter','tera','terao','terceira','terceiro',
                  'terei','teremos','teria','teriam','teriamos','teu','teus','teve','ti','tido','tinha','tinham','tinhamos','tive','tivemos','tiver','tivera','tiveram',
                  'tiveramos','tiverem','tivermos','tivesse','tivessem','tivessemos','tiveste','tivestes','toda','todas','todavia','todo','todos','trabalho','tres',
                  'treze','tu','tua','tuas','tudo','ultima','ultimas','ultimo','ultimos','um','uma','umas','uns','vai','vais','vao','varios','vem','vendo',
                  'vens','ver','vez','vezes','viagem','vindo','vinte','vir','voce','voces','vcs','s','vos','vos','vossa','vossas','vosso','vossos','zero','1','2','3','4','5','6','7','8','9','0','_']
        
    palavras = text.split()
    
    # Filtra as palavras, removendo aquelas que estão na lista
    palavras_filtradas = [palavra for palavra in palavras if palavra.lower() not in stop_words]
    
    # Junta as palavras filtradas de volta em um texto
    texto_filtrado = ' '.join(palavras_filtradas)
    
    return texto_filtrado
    

# Funcao para formatar o index do protocolo_index
def format_index(index_str):
    parts = index_str.split('-')
    if len(parts) == 3:
        return f"{parts[0]}-{parts[1]}-{int(parts[2]):02}"  # Garante que a última parte tenha dois dígitos
    return index_str