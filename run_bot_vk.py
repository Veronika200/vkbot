from config import *

import vk_api
import requests
import random


vk_bot = vk_api.VkApi(token=TOKEN)
long_poll = vk_bot.method('messages.getLongPollServer', {'need_pts': 1, 'lp_version': 3})
server, key, ts = long_poll['server'], long_poll['key'], long_poll['ts']

vk_bot_user = vk_api.VkApi(token=ACCOUNT_TOKEN) # wall.get for user only


print("Ready to work")
print(str(long_poll))


def write_msg(user_id, text):
    vk_bot.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': random.randint(0, 1000)})


def sprosit_zadanie(urok):
    write_msg(user_id, 'Привет, ' + (user_name[0]['first_name']) + ', что задано по ' + urok)


def write_msg_attach(user_id, text, att_url):
    vk_bot.method('messages.send',
                  {'user_id': user_id,
                   'attachment': att_url,
                   'message': text,
                   'random_id': random.randint(0, 1000)})

def get_last_post(owner_id, count, offset, filter): # wall.get
	response = vk_bot_user.method('wall.get',
		{'owner_id': owner_id,
		'count': count,
		'offset': offset,
		'filter': filter})
	return response['items'][0]['id'] # return id of post
				   
				   
while True:
    long_poll = requests.get(
        'https://{server}?act={act}&key={key}&ts={ts}&wait=2500'.format(server=server, act='a_check', key=key,
                                                                        ts=ts)).json()

    update = long_poll['updates']
    if update[0][0] == 4:
        print(update)
        user_id = update[0][3]
        user_name = vk_bot.method('users.get', {'user_ids': user_id})
        if 'Вероника' in (user_name[0]['first_name']):
            write_msg(user_id, 'Привет, ' + (user_name[0]['first_name']) + ', что задано по математике?')
        elif 'Сергей' in (user_name[0]['first_name']):
            sprosit_zadanie('физике')
        if 'красив' in update[0][6]: # search for 'красив'
            group_id = -35684707 # group id always starts from minus
            post_id = get_last_post(group_id, 1, 1, 'owner')
            attach = 'wall' + str(group_id) + ' ' + str(post_id) # make link to post
            write_msg_attach(user_id, 'вот тебе красота', attach)
        elif 'картинк' in update[0][6]:
            write_msg_attach(user_id,
                             'вот тебе огненная картинка',
                             'photo-171720905_456232035')
        elif 'Что задано' in update[0][6]:
            write_msg(user_id,
                             'Извини, но я не знаю, что задано')
        else:
            write_msg(user_id, 'Привет, ' + (user_name[0]['first_name']))  # message to user

        print(str(user_name[0]['first_name']) + ' ' +
              str(user_name[0]['last_name']) + ' has written to bot - ' +
              str(update[0][6]))  # msg to us

    ts = long_poll['ts']

