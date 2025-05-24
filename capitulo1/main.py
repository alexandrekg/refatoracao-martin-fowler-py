import json
import math





def statement(invoices):
    statement_data = {}
    statement_data['customer'] = invoices['customer']
    statement_data['performances'] = [enrich_performance(perf) for perf in invoices['performances']]
    return render_plain_text(statement_data)

def render_plain_text(statement_data):
    result = f"Statement for {statement_data['customer']} \n"
    for perf in statement_data['performances']:
        result += f" {perf['play']['name']}: {usd(perf['amount'])} ({perf['audience']} seats)\n"

    result += f"Amount owed is {usd(total_amount(statement_data))}\n"
    result += f"You earned {total_volume_credits(statement_data)} credits\n"
    return result


def total_amount(statement_data):
    result = 0
    for perf in statement_data['performances']:
        result += perf['amount']
    return result


def total_volume_credits(statement_data):
    result = 0
    for perf in statement_data['performances']:
        result += perf['volume_credits']
    return result


def usd(a_number):
    return f"$ "'{:,.2f}'.format(a_number / 100)


def volume_credits_for(a_performance):
    result = 0
    result += max(a_performance['audience'] - 30, 0)    
    # soma um crédito extra para cada dez espectadores de comédia
    if a_performance['play']['type'] == "comedy":
        result += math.floor(a_performance['audience'] / 5)
    return result


def play_for(a_performance):
    return plays[a_performance['playID']]


def amount_for(a_performance):
    """
    a_performance - o prefixo 'a_' vem de array, pra mostrar a tipagem da variável
    """
    result = 0
    if a_performance['play']['type'] == "tragedy":
        result = 40000
        if a_performance['audience'] > 30:
            result += 1000 * (a_performance['audience'] - 30)
    elif a_performance['play']['type'] == "comedy":
        result = 30000
        if a_performance['audience'] > 20:
            result += 10000 + 500 * (a_performance['audience'] - 20)
        result += 300 * a_performance['audience']
    else:
        raise Exception(f"unknown type: {a_performance['play']['type']}")

    return result

def enrich_performance(a_performance):
    result = a_performance.copy()
    result['play'] = play_for(a_performance)
    result['amount'] = amount_for(result)
    result['volume_credits'] = volume_credits_for(result)
    return result


plays = json.load(open('plays.json'))
invoices = json.load(open('invoices.json'))[0]
print(statement(invoices))
