"""
Projeto nº1: Buggy Data Base (BDB)
Realizado por: Pedro Curto
Número de identificação do Técnico: ist1103091
Email institucional: pedro.a.curto@tecnico.ulisboa.pt
"""
# 1

def corrigir_palavra(documentacao):
    """
    corrigir_palavra: cad. carateres -> cad. carateres
    Recebe uma palavra e devolve a mesma palavra após se removerem todos os surtos de letras
    (pares maiúscula/minúscula seguidos da mesma letra, ex. "aA")
    """
    i = 0
    while i < len(documentacao) - 1:
        # verifica se existem duas letras seguidas apenas com diferença de maiusculização, e se sim, elimina-as
        if documentacao[i].lower() != documentacao[i + 1] and documentacao[i] != documentacao[i + 1].lower():
            i += 1
        elif documentacao[i] == documentacao[i + 1]:
            i += 1
        else:
            # retira-se um par maiúscula/minúscula e move-se uma posição de índice para trás para verificar outro par
            documentacao = documentacao[:i] + documentacao[i + 2:]
            i -= 1
    return documentacao

def eh_anagrama(string1, string2):
    """
    eh_anagrama: cad. carateres × cad. carateres -> booleano
    Analisa se duas palavras fornecidas são anagramas, ou seja, se têm as mesmas letras mas numa ordem diferente,
    devolvendo True nesse caso e False em caso contrário.
    """
    word1, word2 = string1.lower(), string2.lower()
    word2 = string2.lower()
    if len(word1) != len(word2):
        return False
    if sorted(word1) == sorted(word2):
        return True
    return False

def corrigir_doc(texto):
    """
    corrigir_doc: cad. carateres -> cad. carateres
    Corrige um texto, removendo os surtos de letras de palavras e, após isso, eliminando anagramas (exceto se forem
    palavras iguais), recorrendo às funções corrigir_palavra e eh_anagrama definidas acima; verifica inicialmente se
    o texto apenas contém letras separadas por um espaço
    """
    if not isinstance(texto, str) or not all(char.isalpha() or char.isspace() for char in texto):
        raise ValueError("corrigir_doc: argumento invalido")
    # verifica se existe mais que um espaço seguido entre palavras
    if "  " in texto:
        raise ValueError("corrigir_doc: argumento invalido")
    word_list = (corrigir_palavra(texto)).split()
    # recorre-se ao nested loop para emparelhar pelo menos 1x todos os elementos da lista
    for i in range(len(word_list)):
        for j in range(len(word_list)):
            if i == j or word_list[i].lower() == word_list[j].lower():
                continue
            if eh_anagrama(word_list[i], word_list[j]):
                word_list[j] = ""
    # transforma-se a lista resultante da remoção de anagramas numa documentacao de palavras separadas por um espaço
    filtered_string = ' '.join([word for word in word_list if word != ""])
    return filtered_string

# 2

def obter_posicao(movimento, posicao):
    """
    obter_posicao: cad. carateres × inteiro -> inteiro
    Devolve uma nova posição, resultante da aplicação de uma direção cima, esquerda, baixo ou direita a uma posição
    inicial
    """
    dct = {('C', 4): 1, ('C', 5): 2, ('C', 6): 3, ('C', 7): 4, ('C', 8): 5, ('C', 9): 6,
           ('D', 1): 2, ('D', 4): 5, ('D', 7): 8, ('D', 2): 3, ('D', 5): 6, ('D', 8): 9,
           ('B', 1): 4, ('B', 2): 5, ('B', 3): 6, ('B', 4): 7, ('B', 5): 8, ('B', 6): 9,
           ('E', 2): 1, ('E', 5): 4, ('E', 8): 7, ('E', 3): 2, ('E', 6): 5, ('E', 9): 8}
    # se o argumento de entrada estiver no dicionário, é um movimento válido;
    # caso contrário, devolve apenas a posição inicialmente dada
    if (movimento, posicao) in dct:
        return dct[(movimento, posicao)]
    else:
        return posicao

def obter_digito(sequencia, posicao):
    """
    obter_digito: cad. carateres × inteiro -> inteiro
    Devolve a posição resultante da aplicação de uma sequência de movimentos a uma posição inicial,
    recorrendo à função obter_posicao para cada um dos movimentos na sequência
    """
    # a cada iteração do for a posicao atualiza e é usada para obter a nova posição até terminar o ciclo
    for char in sequencia:
        posicao = obter_posicao(char, posicao)
    return posicao

def obter_pin(movimentos):
    """
    obter_pin: tuplo -> tuplo
    Devolve um tuplo com pins de acordo com cada sequência de movimentos dadas (posição inicial é 5),
    recorrendo às funções obter_posicao e obter_digito, após verificar a validade do argumento de entrada
    e de cada sequência dentro do tuplo
    """
    if not isinstance(movimentos, tuple) or len(movimentos) < 4 or len(movimentos) > 10:
        raise ValueError('obter_pin: argumento invalido')
    res = ()
    posicao = 5
    # valida-se cada sequência no tuplo e obtém-se a sua posição resultante, que é adicionada a um tuplo
    for sequencia in movimentos:
        if type(sequencia) != str or len(sequencia) == 0 or not all(char in 'CBED' for char in sequencia):
            raise ValueError('obter_pin: argumento invalido')
        posicao = obter_digito(sequencia, posicao)
        res += (posicao,)
    return res

# 3

def eh_entrada(bdb_entry):
    """
    eh_entrada: universal -> booleano
    Recebe um argumento de qualquer tipo e retorna True se e somente se este corresponde a uma entrada da BDB, ou seja,
    um tuplo com 3 campos: uma cifra, uma sequência de controlo e uma sequência de controlo; em caso contrário, retorna
    False.
    """
    if not isinstance(bdb_entry, tuple) or len(bdb_entry) != 3:
        return False
    cifra, checksum, seguranca = bdb_entry[0], bdb_entry[1], bdb_entry[2]
    if not isinstance(cifra, str) or not isinstance(checksum, str) or not isinstance(seguranca, tuple):
        return False
    # verifica o tamanho da cifra e se apenas contém letras, as quais têm de ser minúsculas
    if len(cifra) == 0 or not all(char.isalpha() or char == "-" for char in cifra) or not cifra.islower():
        return False
    if cifra[0] == "-" or cifra[-1] == "-":
        return False
    # verifica se a primeira e última posição são hífens, ou se existe um ou mais hífens seguidos na cifra
    for i in range(len(cifra)-1):
        if cifra[i] == cifra[i+1] and cifra[i] == '-':
            return False
    # verifica se a checksum e a sequência de controlo contêm o tamanho pretendido
    if len(checksum) != 7 or len(seguranca) < 2:
        return False
    if checksum[0] != '[' or checksum[6] != ']':
        return False
    # verificar se os caracteres na checksum são letras minúsculas
    if not all(element.isalpha() and element.islower() for element in checksum[1:6]):
        return False
    # verifica se os elementos na chave de segurança são inteiros positivos
    for element in seguranca:
        if type(element) != int or element <= 0:
            return False
    return True

def validar_cifra(cifra, controlo):
    """
    validar_cifra: cad. carateres × cad. carateres -> booleano
    Recebe uma cifra e uma sequência de controlo, retornando True se a sequência de controlo é coerente com a cifra,
    isto é, se contém as cinco letras mais frequentes por ordem decrescente (desempate por ordem alfabética). Se não
    for coerente, retorna False.
    """
    dictionary = {}
    new_controlo = controlo[1:6]
    # cria um dicionário com letras associadas a um valor de acordo com a sua frequência na cifra, excluíndo os "-"
    for letra in cifra:
        if letra != '-':
            if letra not in dictionary:
                dictionary[letra] = 1
            else:
                dictionary[letra] = dictionary[letra] + 1
    # ordena os itens do dicionário, primeiro por ordem decrescente de valor, e depois por ordem alfabética de chave,
    # se houver chaves com o mesmo valor (para isso recorre-se à função lambda)
    lst1 = sorted(dictionary.items(), key=lambda x: (-x[1], x[0]))
    return ''.join([x[0] for x in lst1[:5]]) == new_controlo

def filtrar_bdb(entradas_bdb):
    """
    filtrar_bdb: lista -> lista
    Recebe uma lista com entrada(s) da BDB, validando-se o argumento, recorrendo a eh_entrada, e devolvendo uma lista
    com entradas em que a sequência de controlo não é coerente com a cifra, recorrendo a validar_cifra.
    """
    invalid_list = []
    if not isinstance(entradas_bdb, list) or len(entradas_bdb) == 0:
        raise ValueError("filtrar_bdb: argumento invalido")
    for entrada in entradas_bdb:
        if not eh_entrada(entrada):
            raise ValueError("filtrar_bdb: argumento invalido")
        if not validar_cifra(entrada[0], entrada[1]):
            invalid_list.append(entrada)
    return invalid_list

# 4

def obter_num_seguranca(seq_seguranca):
    """
    obter_num_seguranca: tuplo -> inteiro
    Recebe um tuplo com inteiros positivos e retorna um número de segurança, que resulta da menor diferença positiva
    entre quaisquer dois números no tuplo.
    """
    # equivalente a mais infinito
    security_num = float('+inf')
    for idx1 in range(len(seq_seguranca)):
        for idx2 in range(idx1+1, len(seq_seguranca)):
        # se a diferença entre dois elementos for menor que o atual nº de segurança, esse passa a ser o nº de segurança
            security_num = min(security_num, abs(seq_seguranca[idx1]-seq_seguranca[idx2]))
    return security_num

def decifrar_texto(cifra, security_num):
    """
    decifrar_texto: cad. carateres × inteiro -> cad. carateres
    Recebe uma cifra codificada, e descodifica-a de acordo com o número de segurança: avança no alfabeto um número de
    vezes igual ao nº de segurança, +1 para as posições pares da cifra, e -1 para as posições ímpares da cifra, e
    transforma traços em espaaços. Retorna a cifra descodificada.
    """
    cifra = cifra.replace("-", " ")
    alfabeto = 'abcdefghijklmnopqrstuvwxyz' * 2
    result = ''
    increment = security_num % 26
    # enumerate permite obter de uma só vez cada caracter, e o seu índice respetivo
    for idx, char in enumerate(cifra):
        if char == ' ':
            result += char
        # índices pares
        elif idx % 2 == 0:
            result += alfabeto[alfabeto.index(char) + increment + 1]
        # índices ímpares
        else:
            result += alfabeto[alfabeto.index(char) + increment - 1]
    return result

def decifrar_bdb(lista_entradas):
    """
    decifrar_bdb: lista -> lista
    Recebe uma lista com entrada(s) da BDB; valida o argumento recorrendo a eh_entrada, e retorna uma lista com o mesmo
    tamanho, com cada cifra descodificada, recorrendo a obter_num_seguranca e decifrar_texto.
    """
    entradas_decifradas = []
    # validação do argumento de entrada, e de cada argumento dentro da lista
    if type(lista_entradas) != list:
        raise ValueError("decifrar_bdb: argumento invalido")
    for entrada in lista_entradas:
        if not eh_entrada(entrada):
            raise ValueError("decifrar_bdb: argumento invalido")
    for element in lista_entradas:
        num_seguranca = obter_num_seguranca(element[2])
        entradas_decifradas.append(decifrar_texto(element[0], num_seguranca))
    return entradas_decifradas

# 5

def eh_utilizador(user_info):
    """
    eh_utilizador: universal -> booleano
    Recebe qualquer argumento, e retorna True se e somente se este corresponde a um dicionário com informação de
    utilizador relevante da BDB; em caso contrário, retorna False.
    """
    # verificar tipo e tamanho do argumento de entrada
    if not isinstance(user_info, dict) or len(user_info) != 3:
        return False
    keys = list(user_info.keys())
    if keys != ['name', 'pass', 'rule']:
        return False
    name, password, rule = user_info['name'], user_info['pass'], user_info['rule']
    rvalues = list(user_info['rule'].values())
    if len(rvalues) != 2:
        return False
    vals, char = rvalues[0], rvalues[1]
    # verificar tipo das chaves
    if not isinstance(name, str) or not isinstance(password, str) or not isinstance(user_info['rule'], dict)\
            or len(user_info['rule']) != 2:
        return False
    # verificar nome e password
    if len(name) == 0 or len(password) == 0:
        return False
    # verificar valores em 'rule'
    if not isinstance(vals, tuple) or not isinstance(char, str) or len(vals) != 2 or len(char) != 1:
        return False
    # validar elementos do tuplo em 'rule'
    if not isinstance(vals[0], int) or not isinstance(vals[1], int) or vals[0] < 0 or vals[1] < vals[0]:
        return False
    # validar caracter em 'rule'
    if not char.isalpha() or not char.islower():
        return False
    return True

def eh_senha_valida(senha, regra):
    """
    eh_senha_valida: cad. carateres × dicionário -> booleano
    Recebe uma senha e um dicionário com a sua regra individual de criação; se a senha passar nas regras gerais de
    criação e na regra individual, retorna True; senão, retorna False.
    """
    count, count2, repeated = 0, 0, 0
    check = 'aeiou'
    lowerlim, upperlim = regra['vals'][0], regra['vals'][1]
    controlchar = regra['char']
    # regras gerais (verificar se existem pelo menos três vogais, e duas letras iguais consecutivas)
    for element in senha:
        if element in check:
            count += 1
    if count < 3:
        return False
    for idx in range(len(senha) - 1):
        if senha[idx] == senha[idx + 1]:
            repeated += 1
    if repeated < 1:
        return False
    # regras individuais
    for letra in senha:
        if letra == controlchar:
            count2 += 1
    if count2 > upperlim or count2 < lowerlim:
        return False
    return True

def filtrar_senhas(bdb_entries):
    """
    filtrar_senhas: lista -> lista
    Recebe uma lista com dicionário(s) correspondentes a informações de utilizador da BDB; após verificar o argumento
    e cada um dos dicionários, recorrendo a eh_utilizador, deteta aqueles em que a senha está errada, recorrendo a
    eh_senha_valida, e devolve uma lista com os nomes correspondentes às senhas erradas, por ordem alfabética.
    """
    usernames = []
    # verificação do tipo de argumento
    if not isinstance(bdb_entries, list) or len(bdb_entries) == 0:
        raise ValueError("filtrar_senhas: argumento invalido")
    # validação de cada entrada individual na lista
    for entry in bdb_entries:
        if not eh_utilizador(entry):
            raise ValueError("filtrar_senhas: argumento invalido")
    # detecção de passwords erradas
    for entrada in bdb_entries:
        if not eh_senha_valida(entrada['pass'], entrada['rule']):
            usernames.append(entrada['name'])
    return sorted(usernames)
