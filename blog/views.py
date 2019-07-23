from .models import Post,Comment
from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from .form import Postform
from  django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages

def index(request):
    posts = Post.objects.all().order_by('-id')      
    return render(request, 'index.html', {'posts_show':posts})

def detail(request, post_id):
    post_detail = get_object_or_404(Post, pk = post_id)
    if request.user.is_authenticated:
            user = User.objects.get(username= request.user.get_username())
            return render(request,'detail.html', {'post':post_detail, 'user':user})
    else:
        return render(request, 'detail.html', {'post':post_detail})

def new(request): 
    return render(request, 'new.html') 

def create(request):   
    post = Post()    
    post.title = request.GET['title']    
    post.content = request.GET['content']    
    post.pub_date = timezone.datetime.now()    
    post.save()    
    return redirect('index')

def modify(request, post_id):    
    post_detail = get_object_or_404(Post, pk = post_id)    
    return render(request, 'modify.html', {'post':post_detail})

def update(request, post_id):        
    post = get_object_or_404(Post, pk = post_id)        
    post.title = request.GET['title']       
    post.content = request.GET['content']        
    post.save()        
    return redirect('/post/'+str(post.id))

def delete(request,post_id):
    post = get_object_or_404(Post, pk = post_id) 
    if post.author == User.objects.get(username = request.user.get_username()):
        post.delete()
        return redirect('index')

def newpost(request):
    if request.method == 'POST':
        form = Postform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)      #미리 저장하지 말고 일단 기다리는 느낌
            post.author = User.objects.get(username=request.user.get_username())
            post.save()
            return redirect('index')
    else:
        form = Postform()
        return render(request,'new.html',{'form':form})

def updatemodify(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = Postform(request.POST,request.FILES)
        if form.is_valid():
            post.title = form.cleaned_data['title']   
            post.content = form.cleaned_data['content']
            post.save()
            return redirect('index')
    else:
        form= Postform()
        return render(request,'modify.html',{'form':form})
        
def comment_write(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        content = request.POST.get('content')

        if not content:
            messages.info(request, "댓글을 쓸 수 없습니다.")
            return redirect('/blog/post/'+str(post_id))

        Comment.objects.create(post=post, comment_contents=content)
        return redirect('/blog/post/'+str(post_id))