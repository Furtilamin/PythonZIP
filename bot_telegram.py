import telebot
import socket
from socks import setdefaultproxy, PROXY_TYPE_SOCKS5, socksocket
from settings import ID_ARR, PORT, TOKEN, IP

tb = telebot.TeleBot(TOKEN)
setdefaultproxy(PROXY_TYPE_SOCKS5, IP, PORT)
socket.socket = socksocket

for i in range(len(ID_ARR)):
    @tb.message_handler(content_types=['text'])
    def reminder_message(mes):
        tb.send_message(ID_ARR[i], text=mes)
