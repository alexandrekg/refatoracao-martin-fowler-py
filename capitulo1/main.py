import json
import math


invoices = json.load(open('invoices.json'))[0]


def statement():
    statement_data = {}
    return render_plain_text(statement_data)

def render_plain_text(statement_data):
    result = f"Statement for {invoices['customer']} \n"
    for perf in invoices['performances']:
        result += f" {play_for(perf)['name']}: {usd(amount_for(perf))} ({perf['audience']} seats)\n"

    result += f"Amount owed is {usd(total_amount())}\n"
    result += f"You earned {total_volume_credits()} credits\n"
    return result


def total_amount():
    result = 0
    for perf in invoices['performances']:
        result += amount_for(perf)
    return result


def total_volume_credits():
    result = 0
    for perf in invoices['performances']:
        result += volume_credits_for(perf)
    return result


def usd(a_number):
    return f"$ "'{:,.2f}'.format(a_number / 100)


def volume_credits_for(a_performance):
    result = 0
    result += max(a_performance['audience'] - 30, 0)
    # soma um crédito extra para cada dez espectadores de comédia
    if play_for(a_performance)['type'] == "comedy":
        result += math.floor(a_performance['audience'] / 5)
    return result


def play_for(a_performance):
    plays = json.load(open('plays.json'))
    return plays[a_performance['playID']]


def amount_for(a_performance):
    """
    a_performance - o prefixo 'a_' vem de array, pra mostrar a tipagem da variável
    """
    result = 0
    if play_for(a_performance)['type'] == "tragedy":
        result = 40000
        if a_performance['audience'] > 30:
            result += 1000 * (a_performance['audience'] - 30)
    elif play_for(a_performance)['type'] == "comedy":
        result = 30000
        if a_performance['audience'] > 20:
            result += 10000 + 500 * (a_performance['audience'] - 20)
        result += 300 * a_performance['audience']
    else:
        raise Exception(f"unknown type: {play_for(a_performance)['type']}")

    return result


print(statement())
