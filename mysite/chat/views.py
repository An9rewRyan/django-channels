from django.shortcuts import render
from chat.models import Comment, Game
from django.views.generic.base import View
import datetime
from django.contrib.auth.models import User

def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    context = {
        'room_name': room_name
    }
    return render(request, 'chat/room.html', context)

def game(request, game_id):

    comments_arr = []

    game = Game.objects.get(pk = game_id)
    comments_clean = Comment.objects.filter(game=game_id, reply_to_id__isnull = True)
    comments_dirty = Comment.objects.filter(game=game_id, reply_to_id__isnull = False)

    for comment in comments_clean:
        comments_arr.append(comment)
    
    for comment in comments_dirty:
        parent = Comment.objects.get(pk=comment.reply_to_id)
        if parent.reply_to_id is None:
            parent_pos = comments_arr.index(parent)
            comments_arr.insert(parent_pos+1, comment)
        else:
            if parent in comments_arr:
                parent_pos = comments_arr.index(parent)
                comments_arr.insert(parent_pos+1, comment)
            else:
                while comment not in comments_arr:
                    comment = Comment.objects.get(pk=comment.reply_to_id)
                parent_pos = comments_arr.index(comment)
                comments_arr.insert(parent_pos+1, comment)

    context = {'game':game, 'comments':comments_arr}

    return render(request, 'game.html', context)



# def get(self, request, game_id, comment_id):
#     if comment_id == 'solo':
#         link = 'https://localhost:8000/gamedetails/{}/solo/comment/'.format(game_id)
#     else:
#         link = 'https://localhost:8000/gamedetails/{}/{}/comment/'.format(game_id, comment_id)
#     context = {'game_id':game_id}  
#     return render(request, 'comment.html',context)
    