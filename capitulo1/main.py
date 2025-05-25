import json
from create_statement_data import create_statement_data, render_plain_text


invoices = json.load(open('invoices.json'))[0]


def statement(invoices):
    return render_plain_text(create_statement_data(invoices))


print(statement(invoices))
