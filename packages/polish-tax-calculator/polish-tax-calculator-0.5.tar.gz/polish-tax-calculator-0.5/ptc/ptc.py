import math

import click

health_insurance_full = 362.34
health_insurance_deduction = 312.02

labor_fund = 77.31

full_zus = 921.06
full_sickness_insurance = 77.31

reduced_zus = 163.97 + 67.20 + 14.03
reduced_sickness_insurance = 20.58

flat_tax_rate = 0.19

@click.command()
@click.argument('income', type=float)
@click.option('-t', '--tax-type',
              type=click.Choice(['flat', 'income'], case_sensitive=False), default='flat',
              help='"flat" to podatek liniowy, "income" to ryczalt, domyślnie "flat".')
@click.option('-c', '--costs', required=False, type=float, default=0.0, help="koszty uzyskania przychodu.")
@click.option('-z', '--zus-type', required=False, help='"full" to pełny ZUS, "reduce" to obniżony, domyślnie "full".',
              type=click.Choice(['full', 'reduced'], case_sensitive=False), default='full')
@click.option('-si', '--include-sickness-insurance', required=False,
              is_flag=True, default=False, help='(flaga) Czy składka chorobowa jest opłacana, domyślnie nie.')
@click.option('-itr', '--income-tax-rate', required=False, type=float, default=15, help='Stawka ryczałtu w procentach, domyślnie 15.')
@click.option('-v', '--verbose', required=False, is_flag=True, default=False)
def cli(income, tax_type, costs, zus_type, include_sickness_insurance, income_tax_rate, verbose):
    """
    Kalkulator podatkowy, oblicza wartość podatku dochodowego dla różnych wariantów rozliczeń.
    Uwzględniono stawki ZUS za 2021 rok.
    """

    zus_value = get_zus(zus_type, include_sickness_insurance)

    if tax_type == 'income':
        tax_base = math.ceil(income - zus_value - labor_fund)
        tax = max(0, int((tax_base * (income_tax_rate / 100)) - health_insurance_deduction))
        profit = income - zus_value - labor_fund - health_insurance_full - tax
        print_output(verbose, income, profit, tax, zus_value, labor_fund, health_insurance_full)
        return

    if tax_type == 'flat':
        tax_base = math.ceil(income - zus_value - labor_fund - costs)
        tax = max(0, int((tax_base * flat_tax_rate) - health_insurance_deduction))
        profit = income - zus_value - health_insurance_full - labor_fund - costs - tax
        print_output(verbose, income, profit, tax, zus_value, labor_fund, health_insurance_full)
        return


def print_output(verbose, income, profit, tax, zus_value, labor_found, health_insurance):
    if not verbose:
        click.echo("{:.2f}".format(profit))
        return

    click.echo("Składki ZUS: {:.2f}".format(zus_value))
    click.echo("Fundusz pracy: {:.2f}".format(labor_found))
    click.echo("Składka zdrowotna: {:.2f}".format(health_insurance))
    click.echo(click.style("Podatek: {:.2f}".format(tax), bold=True))
    click.echo(click.style("Zysk: {:.2f}".format(profit), bold=True))

    tax_wedge = income - profit
    tax_wedge_percent = tax_wedge / income * 100
    click.echo(click.style("Klin podatkowy: {:.0f}%".format(tax_wedge_percent),
                           bold=True) + " (tyle zabiera państwo)")


def get_zus(zus_type, include_sickness_insurance):
    sickness_insurance = get_full_sickness_insurance_value(zus_type, include_sickness_insurance)

    if zus_type == 'full':
        return full_zus + sickness_insurance
    return reduced_zus + sickness_insurance


def get_full_sickness_insurance_value(zus_type, include_sickness_insurance):
    if not include_sickness_insurance:
        return 0

    if zus_type == 'full':
        return full_sickness_insurance
    return reduced_sickness_insurance
