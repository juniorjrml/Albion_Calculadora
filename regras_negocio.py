import json

with open('dados.json', 'r') as json_file:
    precos = json.load(json_file)



#   "Lymhurst", "Martlock", "Thetford"
TIERS = [2, 3, 4, 5, 6, 7, 8]
ENCANTOS = ['', '@1', '@2', '@3']
CIDADES = ["Bridgewatch", "Caerleon", "Fort Sterling"]

# valores por tier de quanto cada recurso
# custa(valor no jogo, não é em prata, é
# usado na formula pra calcular o valor em
# prata com a taxa)
VALOR_ITEM_RECURSO_REFINO = {2: 2,
                             3: 6,
                             4: 14,
                             5: 30,
                             6: 62,
                             7: 126,
                             8: 254}
# dicionario com o valor em prata
# para transformar um recurso no
# tier seguinte TRANSMUTACAO[recurso][tier]
TRANSMUTACAO = {
    'STONEBLOCK': {
        5: 375,
        6: 1200,
        7: 2500,
        8: 10200
    },
    'other': {
    4: [-1, 600, 1800, 7200],
    5: [375, 750, 2100, 8400],
    6: [600, 1200, 3200, 12800],
    7: [1200, 2500, 5100, 20400],
    8: [5000, 10200, 20400, 40800]}
}

# lista onde o indice representa o (tier-2) e o valor
# representa a quantidade de material bruto usado para
# refinar em 1 material refinado
QUANTIDADE_NECESSARIA_REFINO_TIER = [1, 2, 2, 3, 4, 5, 5]
QUANTIDADE_NECESSARIA_REFINO_TIER.reverse()
# resolve o problema de acesso de (tier-2) da variavel
# QUANTIDADE_NECESSARIA_REFINO_TIER
# exemplo:
# QUANTIDADE_NECESSARIA_REFINO_TIER[INDICE_TIER[8]]
INDICE_TIER = {8: 0,
               7: 1,
               6: 2,
               5: 3,
               4: 4,
               3: 5,
               2: 6}

TAXA_RETORNO = {
    'cidade_apropriada_recurso': 0.36
}


class item_mercado:
    def __init__(self, item, quantidade, imposto =0.07):
        self.nome = item
        self.quantidade_desejada = quantidade
        self.quantidade_adquirida = 0
        self.pedidos = {}
        self.prata = 0
        self.historico = []
        self.imposto_compra = imposto



    def __str__(self):
        return "pedido de {}: faltam {} e a prata é {}".format(self.nome, self.quantidade_desejada, self.prata)

    def log(self, quantidade, preco):
        #preco = preco*self.is_compra
        self.historico.append((quantidade, preco))


    def add_ao_mercado(self, quantidade, preco):
        #preco = preco * self.is_compra
        self.quantidade_desejada -= quantidade
        self.quantidade_adquirida += quantidade
        self.log(quantidade, preco)

    def add_pedido_no_mercado(self, quantidade, preco):
        #preco = preco * self.is_compra
        try:
            self.pedidos[preco].append(quantidade)
            self.prata +=  (quantidade * preco * self.imposto_compra)
        except:
            self.pedidos[preco] = [quantidade]
            self.prata += (quantidade * preco * self.imposto_compra)

    def confirmar_pedido(self, quantidade, preco):
        #preco = preco * self.is_compra
        try:
            # se a quantidade no pedido e menor que a quantidade
            for quant in self.pedidos[preco]:
                indice = self.pedidos[preco].index(quant)
                if quant >= quantidade:
                    self.pedidos[preco*self.is_compra][indice] -= quantidade
                    self.add_ao_mercado(quantidade, preco)
                    quantidade = 0
                elif quantidade > 0:
                    quantidade -= self.pedidos[preco][indice]
                    self.add_ao_mercado(self.pedidos[preco][indice], preco)
                    self.pedidos[preco][indice] = 0
        except:
            self.add_ao_mercado(quantidade, preco)
            self.prata += (quantidade * preco) - (quantidade * preco * self.imposto_compra)




class pacote:
    def __init__(self, nome):
        self.nome = nome
        self.valor_total = 0
        self.custo_total = 0
        self.itens_compra = {}
        self.itens_venda = {}
        self.itens_para_refino = {}


    def __str__(self):
        pass


    def add_item_para_vender(self, item):
        pass


    def add_item_para_comprar(self, item):
        pass


    def add_item_para_refinar(self, item):
        pass




if __name__ == '__main__':
    def quantidade_retorno(quantidade_refino, taxa_retorno=TAXA_RETORNO['cidade_apropriada_recurso'], quant_necessaria_pra_1=2):
        """
        usada para saber a quantidade final de recurso refinado
        dado uma quantidade de recurso bruto

        :param quantidade_refino: Quantidade de recurso bruto
        :param taxa_retorno: taxa de retorno daquele material para a cidade onde sera refinado
        :param quant_necessaria_pra_1: quantos recursos brutos precisa para fazer um refinado
        :return: quantidade de recurso refinado
        """
        sobra = quantidade_refino*taxa_retorno
        if sobra < quant_necessaria_pra_1:
            return 1
        else:
            return (quantidade_refino/quant_necessaria_pra_1) + \
                   quantidade_retorno(sobra,
                                      taxa_retorno=taxa_retorno,
                                      quant_necessaria_pra_1=quant_necessaria_pra_1)


    def chute_refinado_para_cru(quantidade_refinada, taxa_retorno=TAXA_RETORNO['cidade_apropriada_recurso'], quant_necessaria_pra_1=2):
        """
        gera um valor bem proximo da quantidade de material bruto
        que precisa para gerar uma certa quantidade
        de recurso refinado dado

        :param quantidade_refinada: quantidade de recurso refinado dado
        :param taxa_retorno: taxa de retorno daquele material para a cidade onde sera refinado
        :param quant_necessaria_pra_1: quantos recursos brutos precisa para fazer um refinado
        :return: valor aproximado da quantidade necessaria de recursos bruto
        """
        sobra = quantidade_refinada * (1-taxa_retorno)
        # exemplo taxa a 0.4, entao multiplica por 0,6
        # e depois multplica pela
        # quant_nece( 2 ), isso deixa o valor bem perto do real
        return sobra*quant_necessaria_pra_1


    def refinado_para_cru(quantidade_refinada, taxa_retorno=TAXA_RETORNO['cidade_apropriada_recurso'], quant_necessaria_pra_1=2):
        """
        usado como inversa da quantidade_retorno
        dado uma quantidade de material refinado diz
        quanto de material bruto do mesmo tier e
        necessario

        :param quantidade_refinada: quantidade de material refinado
        :param taxa_retorno: taxa de retorno daquele material para a cidade onde sera refinado
        :param quant_necessaria_pra_1: quantos recursos brutos precisa para fazer um refinado
        :return: quantidade material bruto
        """
        chute = chute_refinado_para_cru(quantidade_refinada,
                                        taxa_retorno=taxa_retorno,
                                        quant_necessaria_pra_1=quant_necessaria_pra_1)  # gera um chute
        contador = 0
        # enquanto a quantidade_retorno(chute) for menor que i quantidade passada devemos aumentar o chute
        while quantidade_refinada > quantidade_retorno(chute,
                                                       taxa_retorno=taxa_retorno,
                                                       quant_necessaria_pra_1=quant_necessaria_pra_1):
            # quanto mais interações tiver mais rapido vai crescer o chute
            acrescimo = contador/10
            chute += 1+acrescimo
            contador += 1
        return round(chute)


    def refino_por_tier(tier, quantidade_refinada, taxa_retorno=TAXA_RETORNO['cidade_apropriada_recurso']):
        """
        diz quanto de material bruto(todos os tiers) vai precisar para refinar uma certa quantia de um tier

        :param tier: tier do material que se quer refinar
        :param quantidade_refinada: quantidade de recurso que se quer refinar
        :param taxa_retorno: taxa de retorno daquele material para a cidade onde sera refinado
        :return: dicionario com todos as quantidades necessarias onde a chave é o tier
        """
        # reduz a lista so para os tiers que serao usados
        # exemplo: tier = 4
        # QUANTIDADE_NECESSARIA_REFINO_TIER[INDICE_TIER[4]] == [2, 2, 1]
        #  que é igual a quantidades dos tiers [4, 3, e 2] respectivamente
        lista_quantidade_tier = QUANTIDADE_NECESSARIA_REFINO_TIER[INDICE_TIER[tier]:]
        quantidades_por_tier = {}
        for qnt_tier in lista_quantidade_tier:
            quantidades_por_tier[tier] = refinado_para_cru(quantidade_refinada,
                                                           taxa_retorno=taxa_retorno,
                                                           quant_necessaria_pra_1=qnt_tier)
            tier -= 1
        return quantidades_por_tier


    def valor_compra_venda(quantidades_por_tier, precos):
        valores = []
        for i in quantidades_por_tier:
            valores.append(quantidades_por_tier[i]*precos[i])
        return valores


    def venda_compra_por_cidade(tier, item, quantidade, cidade, precos, taxa_cidade=0.07):
            preco = precos[cidade][item][str(tier)]
            return preco * quantidade * (1-taxa_cidade)


    def venda_compra_por_cidades(tier, item, quantidade, cidades, precos, taxa_cidade=0.07):
        for cidade in cidades:
            preco_venda = venda_compra_por_cidade(tier, item, quantidade, cidade, precos, taxa_cidade=taxa_cidade)
            print("Em {} vc vende {} {} tier {} por {}(pedido de venda)".format(cidade,
                                                                                quantidade,
                                                                                item,
                                                                                tier,
                                                                                preco_venda-(preco_venda*taxa_cidade)))


    def pedido_compra(item, quantidades_por_tier, precos, cidades):
        preco_por_cidade = {}
        for cidade in cidades:
            acumulador = 0
            for tier in quantidades_por_tier:
                acumulador += venda_compra_por_cidade(tier, item, quantidades_por_tier[tier],
                                                      cidade, precos, taxa_cidade=0.07)
            preco_por_cidade[cidade] = acumulador
        return preco_por_cidade


    quantidade_recurso_refinado = 3000
    tier_recurso = 4
    recursos_para_comprar = refino_por_tier(tier_recurso, quantidade_recurso_refinado)

couro = item_mercado('hide_t4', 3000)
couro.add_pedido_no_mercado(1500, -200)
couro.add_pedido_no_mercado(1500, -210)
couro.confirmar_pedido(500, -200)
couro.confirmar_pedido(500, -210)
couro.confirmar_pedido(500, -218)
print(couro)

pedra = item_mercado('rock', 3000)
pedra.add_pedido_no_mercado(1500, 200)
pedra.add_pedido_no_mercado(1500, 210)
pedra.confirmar_pedido(500, 200)
pedra.confirmar_pedido(500, 210)
pedra.confirmar_pedido(500, 218)
print(pedra)

