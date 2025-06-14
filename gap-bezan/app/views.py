from itertools import chain
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib import auth
from .documents import PostDocument
from .models import Profile, Post, Comment, Reply, LikedPost, Followercount, PostReport
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
import random




@login_required
def home(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    posts = list(Post.objects.all())  
    random.shuffle(posts)

    posts_with_profiles = []
    for post in posts:
        post_user_profile = Profile.objects.get(user__username=post.user)
        posts_with_profiles.append({
            'post': post,
            'profile_image': post_user_profile.profileimg
        })

    return render(request, 'app/home.html', {'user_profile': user_profile, 'posts_with_profiles': posts_with_profiles})


@login_required
def following(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)

    # Get usernames of users the current user is following
    following_users = Followercount.objects.filter(follower=user.username).values_list('user', flat=True)

    # Get posts only from followed users
    posts = Post.objects.filter(user__in=following_users).order_by('-crated_at')

    # Attach profile image for each post
    posts_with_profiles = []
    for post in posts:
        try:
            post_user_profile = Profile.objects.get(user__username=post.user)
            posts_with_profiles.append({
                'post': post,
                'profile_image': post_user_profile.profileimg
            })
        except Profile.DoesNotExist:
            pass  # skip if profile not found

    return render(request, 'app/home.html', {
        'user_profile': user_profile,
        'posts_with_profiles': posts_with_profiles
    })

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('name', '')

        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'user name exist')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'this email is tekan')
                return redirect('signup')
            elif len(password) < 5:
                messages.error(
                    request, 'Password must be at least 5 characters long')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                user_login = auth.authenticate(
                    username=username, password=password)
                auth.login(request, user_login)
                user_model = User.objects.get(username=username)
                profile = Profile.objects.create(
                    user=user_model, id_user=user_model.id)
                profile.save()

                messages.success(request, 'Account created successfully. Please log in.')
                return redirect('editprofile')

        else:
            messages.error(request, 'password dosnt match')
    return render(request, 'app/signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('name', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'credential invalid')

    return render(request, 'app/login.html')


@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    if request.method == 'POST':
        post_id = request.POST.get('post_id')

        post = Post.objects.get(id=post_id)

        like_filter = LikedPost.objects.filter(post_id=post_id, username=username).first()
        
        if like_filter == None:
            new_like = LikedPost.objects.create(post_id=post_id, username=username, vote_type='up')
            new_like.save
            post.no_of_like += 1
            post.save()

        elif like_filter.vote_type == 'up':
            like_filter.delete()
            post.no_of_like -= 1
            post.save()
        
        elif like_filter.vote_type == 'down':
            like_filter.vote_type = 'up'
            like_filter.save()
            post.no_of_like -= 2
            post.save()
                                                                                                                                                                                                                                 
        
        # Redirect to the previous page
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect('/')



@login_required
def most_liked(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    posts = Post.objects.all().order_by('-no_of_like')[0:4]

    posts_with_profiles = []
    for post in posts:
        post_user_profile = Profile.objects.get(user__username=post.user)
        posts_with_profiles.append({
            'post': post,
            'profile_image': post_user_profile.profileimg
        })

    return render(request, 'app/most_liked.html', {'user_profile': user_profile, 'posts_with_profiles': posts_with_profiles})

@login_required
def most_trending(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    posts = Post.objects.all().order_by('-no_of_like', '-crated_at')[0:4]

    posts_with_profiles = []
    for post in posts:
        post_user_profile = Profile.objects.get(user__username=post.user)
        posts_with_profiles.append({
            'post': post,
            'profile_image': post_user_profile.profileimg
        })

    return render(request, 'app/most_trending.html', {'user_profile': user_profile, 'posts_with_profiles': posts_with_profiles})
















@login_required
def changepassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('oldpassword')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')
        
        if not request.user.check_password(old_password):
            messages.error(request, 'old password in incorect')
            return redirect('chnagepassword')
        elif new_password != new_password2:
            messages.error(request, 'passwords dosnt match')
            return redirect('chnagepassword')
        
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Password changed successfuly')
        return redirect('home')

    return render(request, 'app/change_password.html')

@login_required
def profile(request, pk):
    user_object = User.objects.get(username=request.user.username)
    user_profileo = Profile.objects.get(user=user_object)
    user = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user)
    user_post = Post.objects.filter(user=user)
    user_post_lens = len(user_post)
    follower = request.user.username

    if Followercount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = Followercount.objects.filter(user=user).count()
    user_following = Followercount.objects.filter(follower=user).count()

    context = {
        'user_object': user,
        'user_profile': user_profileo,
        'user_profileo': user_profile,
        'user_posts': user_post,
        'user_post_length': user_post_lens,
        'user_followers': user_followers,
        'user_following': user_following,
        'button_text': button_text,
    }
    return render(request, 'app/profile.html', context)

@login_required
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if Followercount.objects.filter(follower=follower, user=user).first():
            delete_follower = Followercount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = Followercount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
            
    else:
        return redirect('/')



@login_required
def create_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        user = request.user
        comment = Comment.objects.create(
            post=post,
            user=user,
            content=content
        )
        comment.save()
        messages.success(request, 'your comment has been added')
        request.META.get('HTTP_REFERER', '/')
    return redirect('home')

@login_required
def create_replay(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        content = request.POST.get('replay_content')
        user = request.user
        replay = Reply.objects.create(
            comment=comment,
            user=user,
            content=content,
            )
        replay.save()
        messages.success(request, 'Your reply has been added.')
        request.META.get('HTTP_REFERER', '/')
    return redirect('home')



@login_required
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('profile', pk=str(request.user.username))  # You redirect here

@login_required
def report(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        reported_by = request.user
        post = PostReport.objects.create(
            post=post,
            reported_by=reported_by,
            reason=reason
        )
        post.save()
        messages.success(request, 'your you report has been added')
        return redirect('home') 

    return render(request, 'app/report.html')



@login_required
def settings(request):
    return render(request, 'app/settings.html')

@login_required
def edit_profile(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            gender = request.POST.get('gender')

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.gender = gender
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            gender = request.POST.get('gender')

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.gender = gender
            user_profile.save()
        return redirect('profile', pk=request.user.username)
    return render(request, 'app/edit_profile.html', {'user_profile':user_profile, 'user_objects':user_object})


@login_required
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)
    query = request.GET.get('searcho', '')
    results = PostDocument.search().query("match", caption=query)

    posts_with_profiles = []
    for result in results:
        post = Post.objects.get(id=result.meta.id)  
        profile = Profile.objects.get(user__username=post.user)
        posts_with_profiles.append({
            'post': post,
            'profile_image': profile.profileimg,
            
        })

    return render(request, 'app/search.html', {'posts_with_profiles': posts_with_profiles,  'user_profile':user_profile})













def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required
def create_post(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image')
        caption = request.POST.get('caption')
        user_post = Post.objects.create(
            user=user, image=image, caption=caption)
        user_post.save()
        return redirect('profile', pk=request.user.username)
    return render(request, 'app/create_post.html', {'user_profile': user_profile})

