
import untangle

# https://www.spokenlikeageek.com/2024/05/01/overcast-statistics/
FILENAME = '2024 FULL overcast data.opml'

from datetime import datetime
start_date = datetime.strptime("2023-01-01", "%Y-%m-%d")
end_date = datetime.strptime("2023-12-21", "%Y-%m-%d")
import untangle
XMLDATA = untangle.parse(FILENAME)

played_episodes = 0
episodes = 0
podcasts = 0

feeds = []

for child in XMLDATA.opml.body.children:
    if child['text'] == 'feeds':
        feeds.append(child)

results = []
i = 0

for obj in feeds:
    for playlist in obj.children:
        podcasts += 1
        attributes = playlist._attributes
        results.append({
            'title': attributes['title'],
            'url': attributes['htmlUrl'],
            'count': 0
        })
        for episode in playlist.children:
            attributes = episode._attributes
            date_string = attributes['userUpdatedDate']
            date_time = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)

            if start_date <= date_time <= end_date:
                if attributes.get('played') != "1":
                    episodes += 1
                else:
                    results[i]['count'] += 1
                    played_episodes += 1
        i += 1

results.sort(key=lambda x: x['count'], reverse=True)

# Save results as a markdown table in overcaststats.md
with open('overcaststats.md', 'w') as file:
    file.write('| Title | Count |\n')
    file.write('|-------|-------|\n')
    for result in results:
        if result['count'] > 1:
            if result['url']:
                file.write(f'| [{result["title"]}]({result["url"]}) | {result["count"]} |\n')
            else:
                file.write(f'| {result["title"]} | {result["count"]} |\n')

i = 0
# output results
with open('overcaststats.md', 'a') as file:
    while i < len(results):
        if results[i]['count'] > 0:
            file.write(f'{results[i]["title"]} {results[i]["count"]}\n')
        i += 1