import json

import pytest
from CurrencyExchange import currency_exchange


def test_get_bank_code_usd():
    right_dict = {"Cur_ID": 145, "Cur_ParentID": 145, "Cur_Code": "840", "Cur_Abbreviation": "USD",
                  "Cur_Name": "Доллар США",
                  "Cur_Name_Bel": "Долар ЗША", "Cur_Name_Eng": "US Dollar", "Cur_QuotName": "1 Доллар США",
                  "Cur_QuotName_Bel": "1 Долар ЗША", "Cur_QuotName_Eng": "1 US Dollar", "Cur_NameMulti": "Долларов США",
                  "Cur_Name_BelMulti": "Долараў ЗША", "Cur_Name_EngMulti": "US Dollars", "Cur_Scale": 1,
                  "Cur_Periodicity": 0,
                  "Cur_DateStart": "1991-01-01T00:00:00", "Cur_DateEnd": "2050-01-01T00:00:00"}
    url = 'https://www.nbrb.by/api/exrates/currencies/'
    usd_code = '840'
    result = currency_exchange.get_bank_code(url, usd_code)
    assert right_dict == result


def test_get_bank_code_with_bad_code():
    url = 'https://www.nbrb.by/api/exrates/currencies/'
    usd_code = '841'
    result = currency_exchange.get_bank_code(url, usd_code)
    assert result is None


def test_get_bank_code_with_bad_url():
    url = 'https://www.nbrb.by/api/exrateswe/currencies/'
    usd_code = '840'
    with pytest.raises(Exception):
        currency_exchange.get_bank_code(url, usd_code)


def test_date_diff_with_correct_date():
    start_date = '2020-01-01'
    end_date = '2020-01-03'
    lst = []
    result = currency_exchange.date_diff(start_date, end_date)
    for item in result:
        lst.append(item)
    right_list = ['2020-01-01', '2020-01-02', '2020-01-03']
    assert right_list == lst


def test_date_diff_where_end_date_less_then_start_date():
    start_date = '2020-01-03'
    end_date = '2020-01-01'
    lst = []
    result = currency_exchange.date_diff(start_date, end_date)
    for item in result:
        lst.append(item)
    right_list = []
    assert right_list == lst


def test_date_diff_where_with_incorrect_format():
    start_date = '2016-07-01T00:00:00'
    end_date = '2020-01-01'
    lst = []
    with pytest.raises(ValueError):
        result = currency_exchange.date_diff(start_date, end_date)
        for item in result:
            lst.append(item)


def test_currency_exchange_with_correct_data():
    money_code = 'EUR'
    date = '2021-01-31'
    result = currency_exchange.currency_exchange(money_code, date)
    right_dict = {'Currency ID': 292, 'Currency ISO Code': 'EUR', 'Currency ISO Number': '978',
                  'Currency English Name': 'Euro', 'Currency Scale': 1,
                  'Period': ('2016-07-01T00:00:00', '2050-01-01T00:00:00'), 'Date': '2021-01-31T00:00:00',
                  'Exchange Rate': 3.1798}
    assert result == right_dict


def test_currency_exchange_with_incorrect_code():
    money_code = 'EUU'
    date = '2021-01-31'
    with pytest.raises(TypeError):
        currency_exchange.currency_exchange(money_code, date)


def test_currency_exchange_with_incorrect_date():
    money_code = 'EUR'
    date = '3022-01-31'
    with pytest.raises(ValueError):
        currency_exchange.currency_exchange(money_code, date)


def test_main_with_correct_data():
    currency_exchange.main(money_code='EUR', start_date='2020-01-01',
                           end_date='2020-01-01', number_of_workers=5, output_file='test.json',
                           output_format='json', type_of_workers='process', verbose_level=2)
    correct_json = {
        "Currency ID": 292,
        "Currency ISO Code": "EUR",
        "Currency ISO Number": "978",
        "Currency English Name": "Euro",
        "Currency Scale": 1,
        "Period": [
            "2016-07-01T00:00:00",
            "2050-01-01T00:00:00"
        ],
        "Date": "2020-01-01T00:00:00",
        "Exchange Rate": 2.3637
    }
    with open('test.json') as json_file:
        data = json.load(json_file)
    assert data == correct_json


def test_main_with_incorrect_money_code_more_then_3():
    with pytest.raises(ValueError):
        currency_exchange.main(money_code='EURr', start_date='2020-01-01',
                               end_date='2020-01-01', number_of_workers=5, output_file='test.json',
                               output_format='json', type_of_workers='process', verbose_level=2)


def test_main_with_incorrect_money_code_less_then_3():
    with pytest.raises(ValueError):
        currency_exchange.main(money_code='EU', start_date='2020-01-01',
                               end_date='2020-01-01', number_of_workers=5, output_file='test.json',
                               output_format='json', type_of_workers='process', verbose_level=2)


def test_main_with_incorrect_money_is_not_string():
    with pytest.raises(ValueError):
        currency_exchange.main(money_code=123, start_date='2020-01-01',
                               end_date='2020-01-01', number_of_workers=5, output_file='test.json',
                               output_format='json', type_of_workers='process', verbose_level=2)


def test_main_with_incorrect_start_date_another_format():
    with pytest.raises(ValueError):
        currency_exchange.main(money_code='EUR', start_date=123213,
                               end_date='2020-01-01', number_of_workers=5, output_file='test.json',
                               output_format='json', type_of_workers='process', verbose_level=2)


def test_main_with_incorrect_end_date_another_format():
    with pytest.raises(ValueError):
        currency_exchange.main(money_code='EUR', start_date='2020-01-01',
                               end_date=1244, number_of_workers=5, output_file='test.json',
                               output_format='json', type_of_workers='process', verbose_level=2)


def test_main_with_incorrect_number_of_workers_less_then_0():
    with pytest.raises(ValueError):
        currency_exchange.main(money_code='EUR', start_date='2020-01-01',
                               end_date='2020-01-01', number_of_workers=-1, output_file='test.json',
                               output_format='json', type_of_workers='process', verbose_level=2)


def test_main_with_incorrect_number_of_workers_another_format():
    with pytest.raises(ValueError):
        currency_exchange.main(money_code='EUR', start_date='2020-01-01',
                               end_date='2020-01-01', number_of_workers='123', output_file='test.json',
                               output_format='json', type_of_workers='process', verbose_level=2)


def test_main_with_incorrect_output_format():
    with pytest.raises(ValueError):
        currency_exchange.main(money_code='EUR', start_date='2020-01-01',
                               end_date='2020-01-01', number_of_workers=1, output_file='test.json',
                               output_format='js', type_of_workers='process', verbose_level=2)


def test_main_with_incorrect_verbose_level():
    with pytest.raises(ValueError):
        currency_exchange.main(money_code='EUR', start_date='2020-01-01',
                               end_date='2020-01-01', number_of_workers=1, output_file='test.json',
                               output_format='js', type_of_workers='process', verbose_level=5)
