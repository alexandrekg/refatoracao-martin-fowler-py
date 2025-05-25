
import math
import json
from functools import reduce
plays = json.load(open('plays.json'))


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
    calculator = create_performance_calculator(
        a_performance, play_for(a_performance))
    result = a_performance.copy()
    result['play'] = calculator.play
    result['amount'] = calculator.amount()
    result['volume_credits'] = calculator.volume_credits()
    return result


def play_for(a_performance):
    return plays[a_performance['playID']]


def total_amount(statement_data):
    return reduce(lambda current_amount, new_amount: current_amount + new_amount['amount'], statement_data['performances'], 0)


def total_volume_credits(statement_data):
    return reduce(lambda volume_credits, new_vol_credits: volume_credits + new_vol_credits['volume_credits'], statement_data['performances'], 0)


def amount_for(a_performance):
    return PerformanceCalculator(a_performance, play_for(a_performance)).amount()


def create_performance_calculator(a_performance, a_play):
    play_type = a_play['type']
    if play_type == "tragedy":
        return TragedyCalculator(a_performance, a_play)
    elif play_type == "comedy":
        return ComedyCalculator(a_performance, a_play)
    else:
        raise Exception(f"unknown type: {play_type}")


class PerformanceCalculator:
    def __init__(self, a_performance, a_play):
        self.performance = a_performance
        self.play = a_play

    def amount(self):
        raise NotImplementedError("Subclasses must implement this method")

    def volume_credits(self):
        return max(self.performance['audience'] - 30, 0)


class TragedyCalculator(PerformanceCalculator):
    def amount(self):
        result = 40000
        if self.performance['audience'] > 30:
            result += 1000 * (self.performance['audience'] - 30)
        return result


class ComedyCalculator(PerformanceCalculator):
    def amount(self):
        result = 30000
        if self.performance['audience'] > 20:
            result += 10000 + 500 * (self.performance['audience'] - 20)
        result += 300 * self.performance['audience']
        return result

    def volume_credits(self):
        return super().volume_credits() + math.floor(self.performance['audience'] / 5)


def volume_credits_for(a_performance):
    result = 0
    result += max(a_performance['audience'] - 30, 0)
    # soma um crédito extra para cada dez espectadores de comédia
    if a_performance['play']['type'] == "comedy":
        result += math.floor(a_performance['audience'] / 5)
    return result
