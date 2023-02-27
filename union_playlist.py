import requests
import math

user_id = ''
token = ''
headers = {'Accept':'application/json', 'Content-Type':'application/json', 
    'Authorization':'Bearer ' + token}
track_uris = set()
num_albums = 0

# Collect all of the tracks from saved albums
resp = requests.get('https://api.spotify.com/v1/me/albums', headers = headers).json()

while len(resp['items']) > 0:
    for album in resp['items']:
        num_albums += 1
        for song in album['album']['tracks']['items']:
            track_uris.add(song['uri'])
    if resp['next'] == None:
        break
    resp = requests.get(resp['next'], headers = headers).json()
    print(f'number of songs: {len(track_uris)}', end = '\r')

print(f'number of songs: {len(track_uris)}')
print(f'total number of albums: {num_albums}')

# Collect all saved tracks
resp = requests.get('https://api.spotify.com/v1/me/tracks', headers = headers).json()
while len(resp['items']) > 0:
    for track in resp['items']:
        track_uris.add(track['track']['uri'])
    if resp['next'] == None:
        break
    resp = requests.get(resp['next'], headers = headers).json()
    print(f'number of songs: {len(track_uris)}', end='\r')

# Create new playlist
data = {'name':'Union Playlist', 'description':'It\'s everything', 'public':'false'}
resp = requests.post('https://api.spotify.com/v1/users/' + user_id + '/playlists', 
    json = data, headers = headers).json()
playlist_id = resp['id']

print('Playlist created')

# Populate playlist with collected songs
list_of_tracks = list(track_uris)
for i in range(math.ceil(len(list_of_tracks)/100)):
    data = {'uris':list_of_tracks[100*i:100*(i+1)]}
    resp = requests.post(
        'https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks', 
        json = data, headers = headers)
    
print('Playlist populated')
