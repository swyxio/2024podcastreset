
import untangle

# https://yaleman.org/post/2020/2020-02-03-simple-overcast-stats/
FILENAME = '2024 FULL overcast data.opml'
XMLDATA = untangle.parse(FILENAME)
played_episodes, episodes, podcasts = 0, 0, 0

feeds = [obj for obj in XMLDATA.opml.body.children if obj['text'] == 'feeds']

for obj in feeds:
    for playlist in obj.children:
        podcasts += 1
        for episode in playlist.children:
            if episode['played'] != "1":
                episodes += 1
            else:
                played_episodes += 1

print(f"Podcasts: {podcasts}")
print(f"Outstanding Episodes: {episodes} (played: {played_episodes})")