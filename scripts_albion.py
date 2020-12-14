import json
from main import cidades
with open('dados.json', 'r') as json_file:
    precos = json.load(json_file)

valor_item_recurso_refino = {2: 2,
                              3: 6,
                              4: 14,
                              5: 30,
                              6: 62,
                              7: 126,
                              8: 254}

transmutacao = {
    4: [-1, 600, 1800, 7200],
    5: [375, 750, 2100, 8400],
    6: [600, 1200, 3200, 12800],
    7: [1200, 2500, 5100, 20400],
    8: [5000, 10200, 20400, 40800]
}

quantidade_necessaria_refino_tier = [1, 2, 2, 3, 4, 5, 5]
quantidade_necessaria_refino_tier.reverse()
indice_tier = {8:0,
               7:1,
               6:2,
               5:3,
               4:4,
               3:5,
               2:6}


def quantidade_retorno(quantidade_refino, taxa_retorno=0.4, quant_necessaria_pra_1=2):
    sobra = quantidade_refino*taxa_retorno
    if sobra < quant_necessaria_pra_1:
        return 1
    else:
        return (quantidade_refino/quant_necessaria_pra_1) + quantidade_retorno(sobra, taxa_retorno=taxa_retorno, quant_necessaria_pra_1=quant_necessaria_pra_1)


def chute_refinado_para_cru(quantidade_refinada, taxa_retorno=0.4, quant_necessaria_pra_1=2):
    sobra = quantidade_refinada* (1-taxa_retorno)  #  exemplo taxa a 0.4, entao multiplica por 0,6 e depois multplica pela
                                                   #  quant_nece( 2 ), isso deixa o valor bem perto do real
    return sobra*quant_necessaria_pra_1


def refinado_para_cru(quantidade_refinada, taxa_retorno=0.4, quant_necessaria_pra_1=2):
    chute = chute_refinado_para_cru(quantidade_refinada, taxa_retorno=taxa_retorno, quant_necessaria_pra_1=quant_necessaria_pra_1)
    contador = 0
    while quantidade_refinada > quantidade_retorno(chute, taxa_retorno=taxa_retorno, quant_necessaria_pra_1=quant_necessaria_pra_1):
        acrescimo = contador/10
        chute += 1+acrescimo
        contador += 1
    return round(chute)


def refino_por_tier(tier, quantidade_refinada, taxa_retorno=0.36):
    lista_quantidade_tier = quantidade_necessaria_refino_tier[indice_tier[tier]:]
    quantidades_por_tier = {}
    for qnt_tier in lista_quantidade_tier:
        quantidades_por_tier[tier] = refinado_para_cru(quantidade_refinada, taxa_retorno=taxa_retorno, quant_necessaria_pra_1=qnt_tier)
        tier -=1
    return quantidades_por_tier


def valor_compra_venda(quantidades_por_tier, precos):
    valores = []
    for i in quantidades_por_tier:
        valores.append(quantidades_por_tier[i]*precos[i])
    return valores


def venda_compra_por_cidade(tier, item, quantidade, cidade, precos, taxa_cidade=0.07):
        return ((precos[cidade][item][str(tier)])*quantidade)*(1-taxa_cidade)


def venda_compra_por_cidades(tier, item, quantidade, cidades, precos, taxa_cidade=0.07):
    for cidade in cidades:
        preco_venda = venda_compra_por_cidade(tier, item, quantidade, cidade, precos, taxa_cidade=taxa_cidade)
        print("Em {} vc vende {} {} tier {} por {}(pedido de venda)".format(cidade,
                                                                            quantidade,
                                                                            item,
                                                                            tier,
                                                                            preco_venda - (preco_venda*taxa_cidade)))


def pedido_compra(item, quantidades_por_tier, precos, cidades):
    preco_por_cidade = {}
    for cidade in cidades:
        acumulador = 0
        for tier in quantidades_por_tier:
            acumulador += venda_compra_por_cidade(tier, item, quantidades_por_tier[tier], cidade, precos, taxa_cidade=0.07)
        preco_por_cidade[cidade] = acumulador
    return preco_por_cidade


quantidade_recurso_refinado = 3000
tier_recurso = 4
recursos_para_comprar = refino_por_tier(tier_recurso, quantidade_recurso_refinado)

print(recursos_para_comprar)
print("para comprar minerio {}".format(pedido_compra("FIBER",
                                                    recursos_para_comprar,
                                                    precos,
                                                    cidades)))

print("para vender o  barra de metal {}".format(pedido_compra("CLOTH",
                                                    recursos_para_comprar,
                                                    precos,
                                                    cidades)))
#venda_compra_por_cidade(tier_recurso, 'leather', quantidade_recurso_refinado, cidades, precos)
#venda_compra_por_cidade(tier_recurso, 'leather', quantidade_recurso_refinado, cidades, precos)