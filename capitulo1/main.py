import json
import math


def statement():
    total_amount = 0
    volume_credits = 0
    invoices = json.load(open('invoices.json'))[0]
    
    result = f"Statement for {invoices['customer']} \n"
    for perf in invoices['performances']:
        play = play_for(perf)
        this_amount = amount_for(perf, play)
        # soma créditos por volume
        volume_credits += max(perf['audience'] - 30, 0)

        # soma um crédito extra para cada dez espectadores de comédia
        if play['type'] == "comedy":
            volume_credits += math.floor(perf['audience'] / 5)

        # exibe a linha para esta requisição
        result += f" {play['name']}: ${'{:,.2f}'.format(this_amount / 100)} ({perf['audience']} seats)\n"
        total_amount += this_amount
    result += f"Amount owed is ${'{:,.2f}'.format(total_amount / 100)}\n"
    result += f"You earned {volume_credits} credits\n"
    return result


def play_for(a_performance):
    plays = json.load(open('plays.json'))
    return plays[a_performance['playID']]

def amount_for(a_performance, play):
    """
    a_performance - o prefixo 'a_' vem de array, pra mostrar a tipagem da variável
    """
    result = 0
    if play['type'] == "tragedy":
        result = 40000
        if a_performance['audience'] > 30:
            result += 1000 * (a_performance['audience'] - 30)
    elif play['type'] == "comedy":
        result = 30000
        if a_performance['audience'] > 20:
            result += 10000 + 500 * (a_performance['audience'] - 20)
        result += 300 * a_performance['audience']
    else:
        raise Exception(f"unknown type: {play['type']}")
    
    return result


print(statement())
