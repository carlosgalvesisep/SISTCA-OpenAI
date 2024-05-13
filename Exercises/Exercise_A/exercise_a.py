
import ast  
from openai import OpenAI
import pandas as pd  
import tiktoken  
from scipy import spatial  

EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"

client = OpenAI()


query = 'Which political force won the portuguese elections in 2024?'

response = client.chat.completions.create(
    messages=[
        {'role': 'system', 'content': 'You answer questions about the 2024 Portuguese Elections.'},
        {'role': 'user', 'content': query},
    ],
    model=GPT_MODEL,
    temperature=0,
)

print(response.choices[0].message.content)


wikipedia_article = """As eleições legislativas portuguesas de 2024 tiveram lugar no dia 10 de março de 2024 para eleger os membros da Assembleia da República para a 16.ª Legislatura da Terceira República Portuguesa. Ainda em curso, as eleições aguardam atualmente os resultados de 31 consulados, para definição final dos 230 lugares da Assembleia da República.

Estas foram as primeiras eleições legislativas desde 2005 em que os líderes dos dois principais partidos (Partido Socialista e Partido Social Democrata) lideram os seus partidos pela primeira vez, com cinco dos oito partidos com assento parlamentar a concorrerem com novas lideranças: os dois principais partidos mais a Iniciativa Liberal, o Bloco de Esquerda e o Partido Comunista Português (coligado com o Partido Ecologista "Os Verdes", que perdeu a representação parlamentar em 2022).
Contexto

O terceiro governo de António Costa tomou posse a 30 de março de 2022. Este governo foi muito instável com vários escândalos e/ou polémicas que o afetaram até meados de 2023, altura em que o governo já tinha sofrido treze demissões: onze secretários de Estado e dois ministros. A principal polémica que envolveu o governo foi um caso relativo à TAP Air Portugal e um pagamento de uma indemnização a um membro do Conselho de Administração, Alexandra Reis. Este caso foi seguido por um incidente, no final de abril de 2023, no edifício do Ministério das Infraestruturas entre funcionários do governo e um assessor do Ministro João Galamba relativamente a um alegado computador portátil roubado. A utilização dos Serviços Secretos portugueses neste caso gerou um conflito entre o presidente Marcelo Rebelo de Sousa e o primeiro-ministro António Costa relativamente à continuidade do ministro João Galamba e do próprio governo.
Ver artigo principal: Crise política portuguesa em 2023

No dia 7 de novembro de 2023, foi noticiado que a PSP e o Ministério Público haviam realizado buscas à residência oficial do primeiro-ministro, entre outros ministérios, e que o chefe de gabinete do primeiro-ministro tinha sido detido. Costa foi indiciado como suspeito num caso de corrupção envolvendo os negócios de lítio e hidrogénio. Após reunião com o presidente Marcelo Rebelo de Sousa no Palácio de Belém, Costa anunciou a sua demissão e que não seria candidato à reeleição.

O presidente ouviu todos os partidos após a demissão de António Costa. O Partido Socialista propôs um novo governo liderado por Augusto Santos Silva ou Mário Centeno que poderia durar até ao final do mandato em 2026, enquanto todos os partidos da oposição apelaram a eleições antecipadas.[1] A 9 de Novembro de 2023, o presidente Marcelo Rebelo de Sousa convocou eleições antecipadas para 10 de março de 2024.[2]
Sistema eleitoral

A Assembleia da República tem 230 deputados eleitos para mandatos de quatro anos. Os governos não exigem o apoio da maioria absoluta da Assembleia para ocupar o cargo, pois mesmo que o número de opositores ao governo seja maior que o dos apoiantes, o número de opositores ainda precisa ser igual ou superior a 116 (maioria absoluta) para que o Programa do Governo seja rejeitado ou seja aprovada uma moção de censura.[3]

O número de assentos atribuídos a cada círculo eleitoral depende da magnitude do distrito.[4] A utilização do método d'Hondt permite um limiar efetivo mais elevado do que alguns outros métodos de atribuição, como a quota Hare ou o método Sainte-Laguë, que são mais generosos para os pequenos partidos.[5]

Na sequência dos Censos 2021, nas eleições de 2024 o círculo eleitoral de Setúbal passou a eleger dezanove deputados (mais um) e o de Viana do Castelo cinco (menos um).[6][7]

A distribuição dos deputados por círculo eleitoral nas eleições legislativas de 2024 irá ser a seguinte:[7]
Distrito 	Número de deputados 	Mapa
Lisboa 	48 	
Porto 	40
Braga e Setúbal 	19
Aveiro 	16
Leiria 	10
Coimbra, Faro e Santarém 	9
Viseu 	8
Madeira 	6
Açores, Viana do Castelo e Vila Real 	5
Castelo Branco 	4
Beja, Bragança, Évora e Guarda 	3
Portalegre, Europa e Fora da Europa 	2 

Nas eleições legislativas mais disputadas da história portuguesa, a Aliança Democrática venceu por pouco, reunindo 28,8 por cento dos votos e conquistando 80 assentos.[87] A Aliança conquistou todos os distritos da Região Norte e recuperou o seu apoio em redutos como os distritos de Leiria e Viseu.[88] Durante o dia das eleições, AD emitiu um aviso de que muitos eleitores estavam votando na Alternativa Democrática Nacional (ADN) devido à confusão em torno do nome semelhante e da abreviatura nos boletins de voto.[89] Na noite eleitoral, o ADN obteve mais de 100 mil votos e muitos consideraram que esta confusão entre os nomes pode ter “roubado” assentos à Aliança Democrática.[90]

O Partido Socialista (PS) obteve 28,0 por cento dos votos e 77 assentos no parlamento. No entanto, apesar da estreita margem entre a Aliança e os Socialistas, o PS caiu mais de 13 pontos percentuais e mais de 40 assentos em comparação com as eleições de 2022.[87] Na noite eleitoral, o líder Pedro Nuno Santos admitiu a derrota e disse que o PS faria parte da oposição.[91]

O Chega obteve grandes ganhos, obtendo 18 por cento dos votos e recebendo mais de 1,1 milhão de votos.[92] O partido também conquistou 50 assentos e foi o mais votado no distrito de Faro e no círculo eleitoral da Europa, sendo a primeira vez desde as eleições legislativas de 1991 que um terceiro partido ganhou um distrito.[93] 
"""


query = f"""Use the below article on the 2024 Portuguese Elections to answer the subsequent question. If the answer cannot be found, write "I don't know."

Article:
\"\"\"
{wikipedia_article}
\"\"\"

Question: Which political force won the portuguese elections in 2024?"""

response = client.chat.completions.create(
    messages=[
        {'role': 'system', 'content': 'You answer questions about the 2024 Portuguese Elections.'},
        {'role': 'user', 'content': query},
    ],
    model=GPT_MODEL,
    temperature=0,
)

print(response.choices[0].message.content)