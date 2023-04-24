import requests
import folium

import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = ''

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def get_info_by_ip(ip='127.0.0.1'):
    try:
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
        # print(response)

        data = {
            '[IP]': response.get('query'),
            '[Provider]': response.get('isp'),
            '[Organisation]': response.get('org'),
            '[Country]': response.get('country'),
            '[Region]': response.get('regionName'),
            '[City]': response.get('city'),
            '[Postcode]': response.get('zip'),
            '[Width]': response.get('lat'),
            '[Longitude]': response.get('lon'),
        }
        res = '\n\n'.join([f'{k} : {v}' for k, v in data.items()]) + f'\n\n[Visualisation]: https://maps.google.com?saddr=Current+Location&daddr={response.get("lat")},{response.get("lon")}'

        area = folium.Map(location=[response.get('lat'), response.get('lon')])
        area.save(f'{response.get("query")}_{response.get("city")}.html')

        return res

    except requests.exceptions.ConnectionError:
        return '😢 Error on server, repeat request!'


def main(message):
    # preview_text = Figlet(font='slant')
    # print(preview_text.renderText('IP INFO'))
    # ip = input('Please enter a target IP: ')
    return get_info_by_ip(ip=message)



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(text="<b>😉 Hi! I'm IP SCAN bot!\n\n⬇ Send me an ip and I will give you basic information about it</b>", parse_mode="html")


@dp.message_handler()
async def ipecho(message: types.Message):
    await message.answer(text=f'<b>{get_info_by_ip(ip=message.text)}</b>', parse_mode="html")
    logging.info(f' The {message.from_user.username} has requested information on {message.text}')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
