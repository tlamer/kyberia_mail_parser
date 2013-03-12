#!/usr/bin/python3

from bs4 import BeautifulSoup
import argparse
import re
from os.path import expanduser, isdir

desc = """Kyberia maildump parser. Creates indifidual file for every id.
maildump: http://kyberia.sk/id/1997411"""

par = argparse.ArgumentParser(description=desc, prog='kyberia_mail_parser')

par.add_argument('-i', required=True, type=str, dest='fname',
                 help='path to kyberia maildump file, in form: maildump-<id>.xml')
par.add_argument('-o', type=str, default='', dest='dname',
                 help='path to output directory')

args = par.parse_args()
m = re.search('[0-9]+', args.fname)
k_id = m.group(0)

try:
    f = open(expanduser(args.fname), 'r')
except:
    print('Can not open maildump file. Exiting.')
    exit()

soup = BeautifulSoup(f)
mails = soup.find_all('mail')


def parse_mail(mail):
    if (mail.find('from')['id'] == k_id):
        other = mail.find('to').text
    elif (mail.find('to')['id'] == k_id):
        other = mail.find('from').text
    else:
        print('Can not find your id in mail. Exiting.')
        exit()

    text = mail.find('datetime').text + '\n' + mail.find('from').text + ' --> ' + mail.find('to').text + '\n' + mail.find('text').text.strip() + '\n-----------------------------\n\n'

    if isdir(args.dname):
        filename = args.dname + other + '.txt'
    else:
        print('Can not find output directory. Exiting')
        exit()

    try:
        with open(filename, 'a') as f:
            f.write(text)
    except:
        print('Can not open file for writing. Exiting.')
        exit()


for mail in mails:
    parse_mail(mail)

f.close()
