import json
import math


def statement():
    total_amount = 0
    volume_credits = 0
    invoices = json.load(open('invoices.json'))[0]
    plays = json.load(open('plays.json'))
    result = f"Statement for {invoices['customer']} \n"
    for perf in invoices['performances']:
        play = plays[perf['playID']]
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


def amount_for(perf, play):
    this_amount = 0
    if play['type'] == "tragedy":
        this_amount = 40000
        if perf['audience'] > 30:
            this_amount += 1000 * (perf['audience'] - 30)
    elif play['type'] == "comedy":
        this_amount = 30000
        if perf['audience'] > 20:
            this_amount += 10000 + 500 * (perf['audience'] - 20)
        this_amount += 300 * perf['audience']
    else:
        raise Exception(f"unknown type: {play['type']}")
    
    return this_amount


print(statement())
