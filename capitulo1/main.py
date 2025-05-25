import json
from create_statement_data import create_statement_data


invoices = json.load(open('invoices.json'))[0]


def statement(invoices):
    return render_plain_text(create_statement_data(invoices))

def render_plain_text(statement_data):
    result = f"Statement for {statement_data['customer']} \n"
    for perf in statement_data['performances']:
        result += f" {perf['play']['name']}: {usd(perf['amount'])} ({perf['audience']} seats)\n"

    result += f"Amount owed is {usd(statement_data['total_amount'])}\n"
    result += f"You earned {statement_data['total_volume_credits']} credits\n"
    return result

def html_statement(invoices):
    return render_html(create_statement_data(invoices))

def render_html(statement_data):
    result = f"<h1>Statement for {statement_data['customer']}</h1>\n"
    result += "<table>\n"
    result += "<tr><th>play</th><th>seats</th><th>cost</th></tr>"
    for perf in statement_data['performances']:
        result += f"<tr><td>{perf['play']['name']}</td><td>{perf['audience']}</td><td>{usd(perf['amount'])}</td></tr>\n"
    result += "</table>\n"
    result += f"<p>Amount owed is <em>{usd(statement_data['total_amount'])}</em></p>\n"
    result += f"<p>You earned <em>{statement_data['total_volume_credits']}</em> credits</p>\n"
    return result


def usd(a_number):
    return f"$ "'{:,.2f}'.format(a_number / 100)

print(statement(invoices))
