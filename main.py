from flask import Flask, render_template, url_for
import vk_api

app = Flask(__name__)
group_id = '{group_id}'

activities = {'likes': 0, 'comments': 0, 'subscribed': 0}
towns = set()
ages = {'12-18': 0, '18-21': 0, '21-24': 0, '24-27': 0, '27-30': 0, '30-35': 0, '35-45': 0, '45-100': 0}


def auth():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


bot_session = vk_api.VkApi(login=LOGIN, password=PASSWORD, auth_handler=auth)

bot_session.auth(token_only=True)
vk = bot_session.get_api()
inf = vk.stats.get(group_id=group_id, intervals_count=10)

for i in inf:
    if 'activity' in i:
        if 'likes' in i['activity']:
            activities['likes'] += i['activity']['likes']
        if 'comments' in i['activity']:
            activities['comments'] += i['activity']['comments']
        if 'subscribed' in i['activity']:
            activities['subscribed'] += i['activity']['subscribed']
    if 'visitors' in i:
        if 'cities' in i['visitors']:
            for j in i['visitors']['cities']:
                towns.add(j['name'])
        if 'age' in i['visitors']:
            for j in i['visitors']['age']:
                if not j['value'] in ages:
                    ages[j['value']] = 0
                ages[j['value']] += j['count']


@app.route('/')
@app.route('/vk_stat/<int:group_id>')
def index(group_id):
    return render_template('index.html', title=group_id, activities=activities, ages=ages, cities=list(towns))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
