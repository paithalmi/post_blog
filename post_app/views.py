# Create your views here.


from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from post_app.models import defendant_potential
from django.template import Context,loader

def home(request):
     return HttpResponse("Hello, world. You're at the poll index.")
def index(request):
    user=request.user
    latest=Post.objects.all().order_by('-pub_date')[:5]
    context={
        'user':user,
        'latest_5post':latest,
    }
    return render_to_response('post_templates/index.html',context,context_instance=RequestContext(request))
     
def viewpost(request):
    latest_post = Post.objects.all().order_by('-pub_date')[:5]
    t=loader.get_template('post_templates/view_post.html')
    c=Context({
        'latest_post_list':latest_post,
    })
    return HttpResponse(t.render(c))
    #return render_to_response('post_app/post.html',context={},context_instance=RequestContext(request))
    
    
def comment(request,post):
    user=request.user
    latest_post=Post.objects.get(id=post)
    comments=Comment.objects.filter(post=post)
    #t=loader.get_template('post_templates/comment.html')
    context = {
        'user':user,
        'latest_post':latest_post,
        'comments':comments,
    }
    #c=Context()
    #return HttpResponse(t.render(c))
    
    
    if request.method=="POST":
        user_id=request.user

        if Post.objects.filter(id=int(post)):
            post_id=Post.objects.get(id=int(post))
        title=request.POST.get('c_title','')
        desc=request.POST.get('c_desc','')
        comment=Comment.objects.create(user=user_id,post=post_id,title=title,description=desc)
        comment.save()


     
    return render_to_response('post_templates/comment.html',context,context_instance=RequestContext(request))
     
def addpost(request):    
    user=request.user
    context = {
        'user':user,
    }    
    
    if request.method=="POST":
        user_id = request.user
        title=request.POST.get('title','')
        desc=request.POST.get('desc','')
            
        post = Post.objects.create(title=title,description=desc,user=user_id)
        post.save()
        return viewpost(request)
    return render_to_response('post_templates/post.html',context,context_instance=RequestContext(request))