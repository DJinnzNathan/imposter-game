from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import random

rooms = {}
WORDS = [
    'Apfel', 'Banane', 'Kaffee', 'Auto', 'Hund', 'Katze', 'Buch', 'Stuhl', 'Lampe', 'Pizza',
]

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def create_room(request):
    # Erlaube GET und POST
    room_name = ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', k=5))
    # Host wird als Query-Parameter übergeben
    host = request.GET.get('host') or request.POST.get('host')
    if not host:
        # Wenn kein Host übergeben, generiere einen zufälligen Namen
        host = 'Leiter_' + ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ', k=3))
    rooms[room_name] = {'players': [host], 'started': False, 'word': None, 'imposter': None, 'host': host}
    # Leite mit Host-Name als Query-Parameter weiter
    return redirect(f'/room/{room_name}/?host={host}')

@csrf_exempt
def join_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if room_name in rooms:
            return redirect('room', room_name=room_name)
        else:
            return HttpResponse('Raum nicht gefunden.', status=404)
    return redirect('index')

def room(request, room_name):
    if room_name not in rooms:
        return HttpResponse('Raum nicht gefunden.', status=404)
    host = rooms[room_name].get('host')
    return render(request, 'game/room.html', {'room_name': room_name, 'host': host})
