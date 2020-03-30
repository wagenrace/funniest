from django.shortcuts import render

# Create your views here.
def game(request, room_name):
    return render(request, 'tictactoe/game.html', {
        'room_name': room_name
    })