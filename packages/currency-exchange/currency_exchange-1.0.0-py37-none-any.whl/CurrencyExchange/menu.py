import argparse
from CurrencyExchange.currency_exchange import main


def arg():
    try:
        parser = argparse.ArgumentParser(description='Currency Exchange')

        parser.add_argument("--number_of_workers", action='store', dest='number_of_workers',
                            help='Simple value', default=1)
        parser.add_argument("--type_of_workers", action='store', dest='type_of_workers',
                            help='process or tread', default='thread')
        parser.add_argument("--verbose", action="store", dest='verbose_level',
                            help="Set level from logger", default=2)
        parser.add_argument("--start_date", action="store", dest='start_date',
                            help="Date from (include)")
        parser.add_argument("--end_date", action="store", dest='end_date',
                            help="Date to (include)")
        parser.add_argument("--output_file", action="store",
                            help="name of directory")
        parser.add_argument("--output_format", action="store", default='csv',
                            help="name of file format")
        parser.add_argument('money_code', metavar='Money code', type=str)

        args = parser.parse_args()

        keyword_args = {
            key: getattr(args, key) for key in vars(args) if not key.startswith("__")
        }
        main(**keyword_args)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    arg()
