
import math
import json
from functools import reduce
plays = json.load(open('plays.json'))


class PerformanceCalculator:
    def __init__(self, a_performance, a_play):
        self.performance = a_performance
        self.play = a_play


    def amount(self):
        """
        a_performance - o prefixo 'a_' vem de array, pra mostrar a tipagem da variável
        """
        result = 0
        if self.performance['play']['type'] == "tragedy":
            result = 40000
            if self.performance['audience'] > 30:
                result += 1000 * (self.performance['audience'] - 30)
        elif self.performance['play']['type'] == "comedy":
            result = 30000
            if self.performance['audience'] > 20:
                result += 10000 + 500 * (self.performance['audience'] - 20)
            result += 300 * self.performance['audience']
        else:
            raise Exception(f"unknown type: {self.performance['play']['type']}")

        return result


def create_statement_data(invoice):
    statement_data = {}
    statement_data['customer'] = invoice['customer']
    statement_data['performances'] = list(
        map(enrich_performance, invoice['performances']))
    statement_data['total_amount'] = total_amount(statement_data)
    statement_data['total_volume_credits'] = total_volume_credits(
        statement_data)
    return statement_data


def enrich_performance(a_performance):
    calculator = PerformanceCalculator(a_performance, play_for(a_performance))
    result = a_performance.copy()
    result['play'] = calculator.play
    result['amount'] = amount_for(result)
    result['volume_credits'] = volume_credits_for(result)
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


def volume_credits_for(a_performance):
    result = 0
    result += max(a_performance['audience'] - 30, 0)
    # soma um crédito extra para cada dez espectadores de comédia
    if a_performance['play']['type'] == "comedy":
        result += math.floor(a_performance['audience'] / 5)
    return result


def total_amount(statement_data):
    return reduce(lambda current_amount, new_amount: current_amount + new_amount['amount'], statement_data['performances'], 0)


def total_volume_credits(statement_data):
    return reduce(lambda volume_credits, new_vol_credits: volume_credits + new_vol_credits['volume_credits'], statement_data['performances'], 0)
