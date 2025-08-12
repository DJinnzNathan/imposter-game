import json
from channels.generic.websocket import AsyncWebsocketConsumer
import random

# In-Memory-Raumliste und Wortliste (wie in views.py)
rooms = {}
WORDS = [
    'Apfel', 'Banane', 'Kaffee', 'Auto', 'Hund', 'Katze', 'Buch', 'Stuhl', 'Lampe', 'Pizza',
]

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'room_{self.room_name}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send_players()

    async def disconnect(self, close_code):
        if self.room_name in rooms and hasattr(self, 'player_name'):
            if self.player_name in rooms[self.room_name]['players']:
                rooms[self.room_name]['players'].remove(self.player_name)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.send_players()

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('type') == 'join':
            self.player_name = data.get('user')
            if self.room_name not in rooms:
                rooms[self.room_name] = {'players': [], 'started': False, 'word': None, 'imposter': None, 'host': self.player_name}
            if self.player_name not in rooms[self.room_name]['players']:
                rooms[self.room_name]['players'].append(self.player_name)
            await self.send_players()
        elif data.get('type') == 'start':
            # Nur Host darf starten
            if rooms[self.room_name].get('host') == data.get('user'):
                await self.start_game()
        elif data.get('type') == 'restart':
            # Nur Host darf neue Runde starten
            if rooms[self.room_name].get('host') == data.get('user'):
                await self.restart_game()

    async def send_players(self):
        if self.room_name in rooms:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'players_list',
                    'players': rooms[self.room_name]['players'],
                }
            )

    async def players_list(self, event):
        await self.send(text_data=json.dumps({
            'type': 'players',
            'players': event['players'],
        }))

    async def start_game(self):
        if self.room_name in rooms:
            players = rooms[self.room_name]['players']
            if len(players) < 3:
                return
            word = random.choice(WORDS)
            imposter = random.choice(players)
            rooms[self.room_name]['started'] = True
            rooms[self.room_name]['word'] = word
            rooms[self.room_name]['imposter'] = imposter
            for player in players:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'word_message',
                        'player': player,
                        'word': word if player != imposter else None,
                    }
                )

    async def word_message(self, event):
        if hasattr(self, 'player_name') and self.player_name == event['player']:
            await self.send(text_data=json.dumps({
                'type': 'word',
                'word': event['word'],
            }))

    async def restart_game(self):
        if self.room_name in rooms:
            players = rooms[self.room_name]['players']
            if len(players) < 3:
                return
            word = random.choice(WORDS)
            imposter = random.choice(players)
            rooms[self.room_name]['started'] = True
            rooms[self.room_name]['word'] = word
            rooms[self.room_name]['imposter'] = imposter
            for player in players:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'word_message',
                        'player': player,
                        'word': word if player != imposter else None,
                    }
                )
