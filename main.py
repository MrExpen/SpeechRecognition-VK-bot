import vk_api
import vk_api.longpoll
import config
import time
import urllib3
import stt
import random


def download(url):
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    with open('audio.ogg', 'wb') as file:
        file.write(r.data)
    return 'audio.ogg'


def main():
    vk_session = vk_api.VkApi(token=config.TOKEN)
    longpoll = vk_api.longpoll.VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == vk_api.longpoll.VkEventType.MESSAGE_NEW:
            if event.to_me:
                if event.attachments.get('attachments'):
                    link = event.attachments['attachments']
                    link = link[link.find('"link_ogg":"'):][12:]
                    link = link[:link.find('","')]
                    file_name = download(link)
                    text = stt.stt(file_name)
                    print(text)
                    if text:
                        if not event.from_chat:
                            vk_session.method('messages.send', {
                                'user_id': event.user_id,
                                'random_id': random.getrandbits(64),
                                'message': 'Создано на основе голосового сообщения:\n' + text
                            })
                        else:
                            vk_session.method('messages.send', {
                                'chat_id': event.chat_id,
                                'random_id': random.getrandbits(64),
                                'message': 'Создано на основе голосового сообщения:\n' + text
                            })



if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt at', time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()))
            break
        except NameError as e:
            print(e, time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()))
