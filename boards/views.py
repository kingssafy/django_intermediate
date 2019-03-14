from django.shortcuts import render, redirect
from .models import Board, Comment
# Create your views here.

def index(request):
    boards = Board.objects.order_by('-pk')
    context = {"boards": boards}
    return render(request, 'boards/index.html', context)

def new(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        board = Board(title=title, content=content)
        board.save()
        return redirect('boards:detail', board.pk)
    else: 
        return render(request, 'boards/new.html')

def create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    board = Board(title=title, content=content)
    board.save()
    return redirect('boards:detail', board.pk)

def detail(request, board_pk):
    board = Board.objects.get(pk=board_pk)
    comments = board.comment_set.all()
    context = {"board": board,
            'comments': comments,
            }
    return render(request, 'boards/detail.html', context)

def delete(request, board_pk):
    board = Board.objects.get(pk=board_pk)
    if request.method == 'POST':
        board.delete()
        return redirect('boards:index')
    return redirect('boards:detail', board.pk)    

def edit(request, board_pk):
    if request.method == 'POST':
        return update(request, board_pk)
    else:
        board = Board.objects.get(pk=board_pk)
        context = dict(board=board)
        return render(request, 'boards/edit.html', context)

def update(request, board_pk):
    board = Board.objects.get(pk=board_pk)
    board.title = request.POST.get("title")
    board.content = request.POST.get('content')
    board.save()
    return redirect('boards:detail', board.pk)

def comments_create(request, board_pk):
    board = Board.objects.get(pk=board_pk)
    
    # get data form form
    content = request.POST.get('content')
    comment = Comment(board=board, content=content)
    comment.save()
    return redirect('boards:detail', board.pk)

def comments_delete(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    board = comment.board
    if request.method == "POST":
        comment.delete()
        return redirect('boards:detail', board.pk)
    else:
        return redirect('boards:detail', board_pk) 
