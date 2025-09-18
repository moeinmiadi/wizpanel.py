from json import dumps
from requests import post

update = {'message': {'message_id': 10, 'from': {'first_name': 'iRLords', 'username': 'py_sudo', 'id': 6111469113}, 'chat': {'id': 6111469113}, 'text': '➕ افزودن ادمین'}}
update2 = {'message': {'message_id': 11, 'from': {'first_name': 'iRLords', 'username': 'py_sudo', 'id': 6111469113}, 'chat': {'id': 6111469113}, 'text': '5263923993'}}

print(post('https://www.boting.piko-host.ir/xuigod/index.php', data=dumps(update)))
print(post('https://www.boting.piko-host.ir/xuigod/index.php', data=dumps(update2)))