import csv
import itertools
import json
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import timedelta, datetime
from CurrencyExchange.logger import setup_logging
import warnings
import requests


def currency_exchange(money_code: str, date: str):
    """
    Currency exchange rate for selected currency
    Args:
        money_code: ISO Code (3 Letters) or ISO Number (3 Digits) (https://en.wikipedia.org/wiki/ISO_4217)
        date: Date (include)

    Returns:
        Dict which contain at least
        Currency ISO Code
        Currency ISO Number
        Currency English Name
        Currency Exchange Rate
        Currency Scale

    """

    base_currency_url = 'https://www.nbrb.by/api/exrates/currencies/'
    start_url = 'https://www.nbrb.by/api/exrates/rates/'
    bank_code = get_bank_code(base_currency_url, money_code)
    try:
        currency_code = bank_code['Cur_ID']
    except TypeError as e:
        raise TypeError(e)
    url = start_url + str(currency_code)

    with requests.Session() as s:
        data = s.get(url, params={'ondate': date}, verify=False).json()
        return {
            "Currency ID": bank_code["Cur_ID"],
            "Currency ISO Code": bank_code["Cur_Abbreviation"],
            "Currency ISO Number": bank_code["Cur_Code"],
            "Currency English Name": bank_code["Cur_Name_Eng"],
            "Currency Scale": bank_code["Cur_Scale"],
            "Period": (
                bank_code["Cur_DateStart"],
                bank_code["Cur_DateEnd"],
            ),
            "Date": data["Date"],
            "Exchange Rate": data["Cur_OfficialRate"],
        }


def get_bank_code(url: str, money_code: str) -> dict:
    """Function return dict with currency information"""
    final_el = None
    with requests.Session() as s:
        result = s.get(url, verify=False).json()
        for currency in result:
            if currency['Cur_Code'] == money_code:
                final_el = currency
            if currency['Cur_Abbreviation'] == money_code:
                final_el = currency
    return final_el


def date_diff(start_date: str, end_date: str):
    """
    Function that return list with all day-dates between two dates
    Args:
        start_date: Date from (include)
        end_date: Date To (include)

    Returns:
        list with all day-dates between two dates
    """
    try:
        sdate = datetime.strptime(start_date, "%Y-%m-%d")
        edate = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError('incorrect format date')

    while sdate <= edate:
        yield sdate.strftime("%Y-%m-%d")
        sdate += timedelta(days=1)


def currency_generator(money_code: str,
                       start_date: str = None,
                       end_date: str = None,
                       number_of_workers: int = 1,
                       type_of_workers: str = 'thread'):
    if type_of_workers == 'thread':
        executor_type = ThreadPoolExecutor
    elif type_of_workers == 'process':
        executor_type = ProcessPoolExecutor
    else:
        raise ValueError('incorrect type of workers')
    with executor_type(max_workers=number_of_workers) as executor:
        result = executor.map(
            currency_exchange,
            itertools.repeat(money_code),
            date_diff(start_date, end_date),
        )

        yield from result


def main(money_code: str,
         start_date: str = None,
         end_date: str = None,
         output_file: str = None,
         output_format: str = 'csv',
         verbose_level: int = 2,
         number_of_workers: int = 1,
         type_of_workers: str = 'thread'):
    warnings.filterwarnings('ignore', message='Unverified HTTPS request')

    if verbose_level not in (0, 1, 2):
        raise ValueError('logger have only 0, 1, 2 levels')
    log = setup_logging(verbose_level)

    if not (isinstance(money_code, str) and len(money_code) == 3):
        log.error('money code should contain only 3 digits or 3 letters')
        raise ValueError
    if not start_date:
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if not (isinstance(start_date, str) and isinstance(end_date, str)):
        log.error('start date and end date should be string')
        raise ValueError
    if not (isinstance(number_of_workers, int) and isinstance(type_of_workers, str)):
        log.error('number_of_workers and type_of_workers are not correct')
        raise ValueError
    if number_of_workers <= 0:
        log.error('number_of_workers less then 0')
        raise ValueError

    result = currency_generator(money_code=money_code, start_date=start_date, end_date=end_date,
                                number_of_workers=number_of_workers, type_of_workers=type_of_workers)
    if output_file:
        log.info('Output format:' + output_format)
        if output_format == 'json':
            with open(output_file, 'w+') as file:
                for item in result:
                    json.dump(item, file, indent=4)
        elif output_format == 'csv':
            with open(output_file, 'w+') as file:
                first_time = True
                for item in result:
                    if first_time:
                        wr = csv.DictWriter(file, item.keys())
                        wr.writeheader()
                        first_time = False
                    wr.writerow(item)
        else:
            log.error('check output format, he should be csv or json')
            raise ValueError
    else:
        for item in result:
            log.info(item)


if __name__ == '__main__':
    main(money_code='EUR', start_date='2020-01-01',
         end_date='2020-01-01', number_of_workers=5, output_file='test.json',
         output_format='json', type_of_workers='thread', verbose_level=2)
