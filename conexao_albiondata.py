import requests
import json
from regras_negocio import CIDADES, TIERS
BANCO_DADOS = "dados.json"

global precos
precos = {}


def abrir_banco_dados():
    global base
    with open(BANCO_DADOS, 'r') as json_file:
        base = json.load(json_file)
    return base


def salvar_banco_dados():
    for cidade in base:  # Para tudo na base antiga
        for item in base[cidade]:
            try:
                precos[cidade][item]  # Tenta acessar o item na base criada atualmente
            except:
                precos[cidade][item] = base[cidade][item]  # Se der erro e pq nao tem na base atual(preco), precisa adicionar

    with open(BANCO_DADOS, 'w') as json_file:
        json.dump(precos, json_file, indent=4)


if __name__ == '__main__':
    base = abrir_banco_dados()

    for cidade in CIDADES:
        precos[cidade] = dict()

    def coleta_valor_item_manual(item, tier, cidade):
        valor = -1
        while valor < 0:
            try:
                print("Entre com o valor do recurso {} de Tier {} da cidade {} manualmente:(digite -1 para pular preco)".format(item, tier, cidade))
                valor = float(input())
                if valor == -1:
                    valor = 0
            except:
                print("Erro na leitura do dado, tente novamente")
                valor = -1

        return valor


    def busca_preco(item,cidade):
        preco_item = {}
        for i in TIERS:
            res = requests.get('https://www.albion-online-data.com/api/v2/stats/Prices/t{}_{}.json?locations={}'.format(i, item, cidade))
            aux = res.json().pop()
            if res.status_code==200:
                preco_item[i] = aux["sell_price_min"]

        for tier in preco_item:
                if preco_item[tier] == 0:
                    try:  # caso seja a primeira vez que esteja incluindo o item no json vai dar erro no base[cidade][!!!erro aqui!!!][str(i)] (acesso direto a uma area nao existente)
                        if base[cidade][item][str(tier)] < 1:  # caso o preco esteja inexistente na base de dados ja existente!
                            preco_item[tier] = coleta_valor_item_manual(item, tier, cidade)
                        else:  # Se não estiver inexistente e nao acho o preco recente usa o preco anterior da base de dados antiga
                            preco_item[tier] = base[cidade][item][str(tier)]
                    except:  # Se for a primeira inclusao desse item no json
                        preco_item[tier] = coleta_valor_item_manual(item, tier, cidade)

        precos[cidade][item] = preco_item


    def busca_todos_precos(item):
        try:
            for cidade in CIDADES:
                for i in item:
                    busca_preco(i, cidade)
        except:
            for cidade in CIDADES:
                busca_preco(item, cidade)


    #busca_todos_precos(['hide', 'leather', 'HEAD_LEATHER_SET2'])
    #busca_todos_precos(['METALBAR', 'ORE'])
    #busca_todos_precos(['2H_CLAWPAIR'])
    busca_todos_precos(['CLOTH', 'FIBER'])
    salvar_banco_dados()
