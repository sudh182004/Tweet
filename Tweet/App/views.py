from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Tweet,Like,Comments
from .forms import tweet_form ,CommentForm

from django.shortcuts import render
from .models import Tweet, Like, Comments

def dashboard(request):
    # Fetch all tweets of the current user
    tweets = Tweet.objects.filter(user=request.user)
    
    # Initialize variables to hold stats
    total_tweets = tweets.count()
    total_likes = 0
    total_comments = 0
    
    tweet_list = []

    # Loop through each tweet to gather the necessary data
    for tweet in tweets:
        # Fetch likes and comments for each tweet
        liked_by = Like.objects.filter(tweet=tweet).select_related('user')
        comments = Comments.objects.filter(tweet=tweet).select_related('user')

        # Add likes and comments count to the totals
        total_likes += liked_by.count()
        total_comments += comments.count()

        # Append tweet data
        tweet_list.append({
            "content": tweet.content,
            "likes": liked_by.count(),
            "liked_by": [{"username": like.user.username} for like in liked_by],
            "comments": comments.count(),
            "comments_details": [{"user": comment.user.username, "text": comment.content} for comment in comments],
        })

    # Prepare stats for rendering
    stats = [{
        "total_tweets": total_tweets,
        "total_likes": total_likes,
        "total_comments": total_comments,
    }]
    
    # Render the dashboard template with the tweets and stats data
    return render(request, "dashboard.html", {"tweets": tweet_list, "stats": stats})



def comment(request,id):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet,pk=id)
        like = Like.objects.filter(tweet=tweet).count()
        print(like)
        if request.method =='POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.tweet = tweet
                comment.user =request.user
                comment.save()
                return redirect('home')
        else:
            form = CommentForm()        
        print(tweet)
        return render(request, "y.html", {'form': form,'tweet':tweet,'like':like})
    else:
       messages.error(request, "Please log in first to like and comment")
       return redirect('home')


def like(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            tweet = get_object_or_404(Tweet,pk=id)
            like,created = Like.objects.get_or_create(tweet=tweet,user=request.user)

            if not created:
                like.delete()
        return redirect('home')
    else:
        messages.error(request,"Please log in first to like and comment")
        return redirect('home')

def Tweetedit(request, id):
    # Fetch the tweet object
    tweet = get_object_or_404(Tweet, pk=id, user=request.user)
    
    if request.method == "POST":
        form = tweet_form(request.POST, instance=tweet)
        if form.is_valid():
            form.save()  # Save the edited tweet
            return redirect('home')  # Redirect to the tweet detail page
    else:
        # Create form instance for GET request
        form = tweet_form(instance=tweet)

    # Render the form on the page
    return render(request, "x.html", {'form': form})

def Tweetcreate(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = tweet_form(request.POST)
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                form.save()
                return redirect('home') 
        else:
            form = tweet_form()  # Initialize an empty form
        return render(request, 'Tweet_home/tweet_create.html', {'form': form})
    else:
        messages.error(request,"Please log in first to create a post")
        return redirect('home')


def Home(request):
    tweets = Tweet.objects.all() 
    tweet_data = []  # Create an empty list to store tweet data along with like count
    
    for tweet in tweets:
        likes = Like.objects.filter(tweet=tweet).count()  # Get like count for each tweet
        comment =  Comments.objects.filter(tweet=tweet).count()
        tweet_data.append({'tweet': tweet, 'like_count': likes,'comments':comment})  # Append tweet and like count as a dictionary
    
    return render(request, "Tweet_home/tweet.html", {'tweet_data': tweet_data})


def Login(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user  = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,'Authentication/login.html',{'error_message':"Invalid username or password"})
    return render(request, 'Authentication/login.html')

def Logout(request):
    if request.method=="POST":
        logout(request)
        return redirect('home')
    return render(request,'Authentication/logout.html')

def Signin(request):
    if request.method=="POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password!=confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signin')
        
        if  User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signin')

        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already registered!")
            return redirect('signin')
      
        user= User.objects.create_user(
                username=username,
                email=email,
                password=make_password(password)
        )
        user.save()
        login(request,user)
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('home')
    return render(request,'Authentication/signin.html')