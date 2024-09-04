from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import update_session_auth_hash
from .models import Post, PostInteraction, Comment
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.contrib.auth import logout, authenticate, login
from .forms import LoginForm 
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import json
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, UserSignupSerializer, PostSerializer, CommentSerializer
from openpyxl.utils import get_column_letter
from django.utils.timezone import make_naive
from PIL import Image as PILImage
from openpyxl.drawing.image import Image as OpenpyxlImage
import os
import openpyxl
import openpyxl.workbook
from openpyxl.drawing.image import Image as XLSXImage
from  io import BytesIO

import io
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.drawing.image import Image as xlImage
from django.core.files.base import ContentFile
from openpyxl.styles import Alignment, Border, Side


class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print(request.data)
    

        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)


class userbloglist(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user_id= request.data.get('user_id')

        if not user_id or not str(user_id).isdigit():
            return Response({"detail": "INVAILD USER ID. ONLY INTEGERS ARE ALLOWED."})
        
        if User.objects.filter(id= user_id).exists():
            blog = Post.objects.filter(author__id=user_id).values()
            return Response({"blog": blog}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"detail": "user id is not valid"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def update_passwordapi(request):
    username = request.data.get('username')
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not username:
        return Response({"detail": "username is require"})
    
    try:
        user = User.objects.get(username = username)
    except user.DoesNotExist:
        return Response({"detail": "user not found"})
    

    if not user.check_password(old_password):
        return Response({"detail": "old password incorrect"})
    
    try:
        validate_password(new_password, user)

    except Exception as e:
        return Response({"detail": str(e)})
    
    user.set_password(new_password)
    user.save()

    return Response ({"detail": "password updated"})

@api_view(['GET'])
@permission_classes([AllowAny])
def allBlogPostApi(request):
    post = Post.objects.all()
    serializer = PostSerializer(post, many=True)
    return Response({"post": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def createPostApi(request):  
    author_id = request.data.get('author_id')  
    
    try:
        author = User.objects.get(id=author_id)
    except User.DoesNotExist:
        return Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)
    print(author)
    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
        post = serializer.save()
        post.author = author
        post.save()
        return Response({"post":serializer.data})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['PUT'])
@permission_classes([AllowAny])
def updatePostApi(request, post_id):  
    
    try:
        post =  Post.objects.get(id = post_id)

    except Post.DoesNotExist:
        return Response({"detail": "post not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PostSerializer(post, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"Post": serializer.data})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def commentApi(request, post_id):  
    
    try:
        post =  Post.objects.get(id = post_id)

    except Post.DoesNotExist:
        return Response({"detail": "post not found"}, status=status.HTTP_404_NOT_FOUND)
    
    content =  request.data.get('content')
    user_id =  request.data.get('user_id')

    if not content:
        return Response({"detail":"content required"})
    
    comment = Comment.objects.create(

        content = content,
        post = post,
        user_id = user_id
    )
    
    serializer = CommentSerializer(comment)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)  


@api_view(['POST'])
@permission_classes([AllowAny])
def InteractionApi(request): 
    post_id = request.data.get('post_id')
    user_id = request.data.get('user_id')
    interaction_type = request.data.get('interaction_type')

    try:
        post =  Post.objects.get(id = post_id)
        user = User.objects.get(id=user_id)
    except Post.DoesNotExist or User.DoesNotExist :
        return Response({"detail": "post or user or interecation type not found"})

 

    if PostInteraction.objects.filter(post=post, user=user).exists():
        PostInteraction.objects.filter(post= post, user = user).update(interaction_type=interaction_type)
        return Response({"detail": "your interaction is updated"})


    else: 
        PostInteraction.objects.filter(post= post, user = user).create(interaction_type=interaction_type)
        return JsonResponse({"message": "Interaction created successfully"})        

     
            

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def dislikePostApi(request):
#     post_id = request.data.get('post_id')
#     user_id = request.data.get('user_id')
#     try:
#         post = Post.objects.get(id=post_id)
#         user = User.objects.get(id=user_id)
    
#     except Post.DoesNotExist or User.DoesNotExist:
#         return Response({"detail": "post or user not found"})
    
#     interaction, created = PostInteraction.objects.update_or_create(
#             post = post,
#             user = user,
#             interaction_type = 'dislike'
#         )
#     if not created:
#         return Response({"message": "Already disliked"})
#     return Response({"message": "post dislike successfully"})


@api_view(['PUT'])
@permission_classes([AllowAny])
def updateCommentApi(request, comment_id):
    post_id = request.data.get('post_id')
    try:
        post =  Post.objects.get(id = post_id)
        comment_id = Comment.objects.get(id=comment_id)

    except Post.DoesNotExist or Comment.DoesNotExist:
        return Response({"detail": "post or comment not found"}, status=status.HTTP_404_NOT_FOUND)


    serializer = CommentSerializer(comment_id, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"Comment": serializer.data})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
  
   
@api_view(['DELETE'])
@permission_classes([AllowAny])
def deleteCommentApi(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return Response({"detail": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Comment.DoesNotExist:
        return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)




def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    message = '' 

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = '!Invalid username or password.' 
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'message': message})

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        user = request.user

        
        if not user.check_password(old_password):
            messages.error(request, 'Old password is incorrect.')
        elif new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
        elif len(new_password1) < 8:  
            messages.error(request, 'New password must be at least 8 characters long.')
        else:
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')

    return render(request, 'change_password.html')

@login_required
def logout_view(request):
    logout(request) 
    return render(request, 'logout.html')


def home(request):
    posts = Post.objects.prefetch_related('comments').all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

@login_required
def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    return render(request, 'user_posts.html', {'user': user, 'posts': posts})

@login_required
@require_POST
def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = request.user

   
    interaction, created = PostInteraction.objects.get_or_create(
        post=post, 
        user=user,
        defaults={'interaction_type': 'like'}
    )
    
    if not created:
        if interaction.interaction_type == 'like':
            interaction.delete()  
        else:
            interaction.interaction_type = 'like'  
            interaction.save()
    else:
        PostInteraction.objects.filter(post=post, user=user, interaction_type='dislike').delete()

    
    return JsonResponse({
        'success': True,
        'likes': post.get_like_count(),
        'dislikes': post.get_dislike_count()
    })


@login_required
@require_POST
def dislike_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = request.user

    interaction, created = PostInteraction.objects.get_or_create(
        post=post, 
        user=user,
        defaults={'interaction_type': 'dislike'}
    )
    
    if not created:
        if interaction.interaction_type == 'dislike':
            interaction.delete()  
        else:
            interaction.interaction_type = 'dislike' 
            interaction.save()
    else:
        PostInteraction.objects.filter(post=post, user=user, interaction_type='like').delete()

    return JsonResponse({
        'success': True,
        'likes': post.get_like_count(),
        'dislikes': post.get_dislike_count()
    })


@login_required
def download_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not post.image:
        raise Http404("Image not found")

    image_path = post.image.path
    with open(image_path, 'rb') as image_file:
        response = HttpResponse(image_file.read(), content_type='image/jpeg')  # Change content_type based on image type
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(image_path)}"'
        return response
    
    
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()  
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})




@login_required
def profile(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'user': request.user, 'posts': user_posts})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post.objects.filter(author=request.user), pk=pk)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post.objects.filter(author=request.user), pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES or None, instance=post)  
        if form.is_valid():
            post = form.save(commit=False)
            # post.image = request.FILES.get('image', None)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post.objects.filter(author=request.user), pk=pk)   
    if request.method == 'GET':
        post.delete()
        return JsonResponse({'message': 'Post deleted successfully.'})    
    return JsonResponse({'error': 'Invalid request'}, status=400)







# ----------------comment section --------

@login_required
@csrf_exempt
def add_comment(request, post_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content')
            post = get_object_or_404(Post, id=post_id)
            
            if content:
                Comment.objects.create(post=post, user=request.user, content=content)
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failure', 'error': 'No content provided'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'failure', 'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'failure', 'error': 'Invalid request method'}, status=405)


@csrf_exempt
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)








# @csrf_exempt
# @login_required
# def edit_comment(request, comment_id):
#     if request.method == 'POST':
#         comment = get_object_or_404(Comment, id=comment_id, user=request.user)
#         data = json.loads(request.body)
#         new_content = data.get('content')

#         if new_content:
#             comment.content = new_content
#             comment.save()
#             return JsonResponse({'success': True})
#         return JsonResponse({'success': False, 'error': 'No content provided'}, status=400)

#     return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@csrf_exempt
@login_required
def edit_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        data = json.loads(request.body)
        new_content = data.get('content')

        if new_content:
            comment.content = new_content
            comment.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'No content provided'}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)




@login_required
def exportData(request):

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Posts'


    headers = ['ID','Title', 'Content', 'created at', 'image']
    sheet.append(headers)

#colm width
    sheet.column_dimensions['A'].width = 10
    sheet.column_dimensions['B'].width = 30
    sheet.column_dimensions['C'].width = 50
    sheet.column_dimensions['D'].width = 20
    sheet.column_dimensions['E'].width = 30
    
    header_alignment = Alignment(horizontal="center", vertical="center")
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))

    for cell in sheet[1]: 
        cell.alignment = header_alignment
        cell.border = thin_border


    posts = Post.objects.all()


    for index, post in enumerate(posts, start=2):
        sheet[f'A{index}']= post.id
        sheet[f'B{index}']= post.title
        sheet[f'C{index}']= post.content
        sheet[f'D{index}']= post.created_at.strftime('%Y-%m-%d %H:%M:%S')

        for col in 'ABCDE':
            sheet[f'{col}{index}'].alignment = Alignment(horizontal="left", vertical="center")
            sheet[f'{col}{index}'].border = thin_border

        if post.image:
            image_path = post.image.path
            img = OpenpyxlImage(image_path)
            img.height = 100
            img.width = 200
            sheet.add_image(img, f'E{index}')

            sheet.row_dimensions[index].height = 80

    excel_file = BytesIO()
    workbook.save(excel_file)
    excel_file.seek(0)




    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=posts.xlsx'
    workbook.save(response)

    return response


