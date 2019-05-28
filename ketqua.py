import argparse
import bs4
import requests
import log

from collections import defaultdict

logger = log.get_logger(__name__)


def crawl_prizes():
    """
    Using beautifulSoup to filter prizes from requests
    :param response: (string) Respone from requests
    :return: (list) Data after filter
    """

    base = 'http://ketqua.net'

    response = requests.get(base)

    tree = bs4.BeautifulSoup(response.text, 'html.parser')
    data = tree.select('td[id*=rs]')

    if not data:
        raise ValueError('No data found')

    all_prizes = defaultdict(list)
    for prize in data:
        name_prize = prize.get('id')[3]
        all_prizes[name_prize].append(prize.text)

    return all_prizes


def check_lucky_money(nums):
    """
    Check number win prize at website: ketqua.net

    :param nums: (iterable) Number need to check
    :return: (list) If any number in nums win prize.
             (dict) If no number win prize
    """

    all_prizes = crawl_prizes()

    # amount number digits need to check in prize
    match_number = {
        '7': 2,
        '6': 3,
        '5': 4,
        '4': 4,
        '3': 5,
        '2': 5,
        '1': 5,
        '0': 5
    }
    winning_numbers = []
    for num in nums:
        if len(str(num)) != 6:
            logger.error('Number not valid %s', num)
            continue

        for prize, number in all_prizes.items():
            if str(num)[-match_number[prize]:] in number:
                winning_numbers.append(
                    'Congratulations {} has won {}'.format(num,
                                                           int(prize) + 1))
                break  # a number just win only one prize

    if winning_numbers:
        return winning_numbers

    return all_prizes


def main():
    parse = argparse.ArgumentParser(
        description='Check lucky number at ketqua.net')

    parse.add_argument('nums',
                       nargs='+',
                       type=int,
                       help='Number to check prize')

    args = parse.parse_args()
    print(check_lucky_money(args.nums))


if __name__ == '__main__':
    main()
