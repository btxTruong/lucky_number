import requests
import bs4
import log
import argparse

from collections import defaultdict

logger = log.get_logger(__name__)


def respone_from_url(url, **kwargs):
    """
    Return response from url using requests module

    :param url: (string) **(Required)** A valid url need to fetch data
    :param redirect: (bool) (optional) Allow-redirect. Default is True
    :param timeout: (int) (optional) Time to wait connection. Default is 5
    :return: requests.models.Response
    """

    redirect = kwargs.get('redirect', True)
    timeout = kwargs.get('timeout', 5)

    if not url:
        raise ValueError('No url provied')

    if not url.startswith(('http://', 'https://')):
        url = ''.join(('http://', url))

    try:
        r = requests.get(url, allow_redirects=redirect, timeout=timeout)
    except requests.exceptions.Timeout:
        logger.error('Timeout')
        raise
    except requests.exceptions.InvalidURL:
        logger.error('Invalid URL')
        raise

    if r.status_code != 200:
        return False

    return r


def check_lucky_money(nums):
    """
    Check number win prize at website: ketqua.net

    :param nums: (iterable) Number need to check
    :return: (list) If any number in nums win prize.
             (dict) If no number win prize
    """

    if not nums:
        raise ValueError('No numbers provided')

    base_url = 'ketqua.net'
    r = respone_from_url(base_url)

    tree = bs4.BeautifulSoup(r.text, 'html.parser')
    data = tree.select('td[id*=rs]')

    if not data:
        raise ValueError('No data found')

    all_prizes = defaultdict(list)
    for prize in data:
        name_prize = prize.get('id')[3]
        all_prizes[name_prize].append(prize.text)

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
                    'Congratulations {} has won {}'
                    .format(num, int(prize) + 1))
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
