from requests import get

php_file_code = """<?php
$TOKEN = "[*TOKEN*]";
echo "if u see this message u lose";
?>"""

token = input('enter your bot token : ')
if get(f'https://api.telegram.org/bot{token}/getme').json()['ok']:
    with open('created.php', 'w') as f:
        f.write(php_file_code.replace('[*TOKEN*]', token))
    print('your token is valid. check the created.php file.')
else:
    print('token is invalid.')