from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from .middleware import *
from rest_framework.response import Response
from .json_blog import *
from .models import *
from django.shortcuts import redirect
from seartz.mongoDBConnection import *
from bson.json_util import dumps
import json
from datetime import datetime
blog_db = database['blog_blog']


@api_view(['POST', ])
@decorator_from_middleware(CreateBlogMiddleware)
def create_blog_view(request, form=None):
    try:
        form.cleaned_data['user_id'] = request.user.id
        Blog(**form.cleaned_data).save()
        blog_obj = Blog.objects.last()
        if 'blog_image' in request.FILES:
            for i in request.FILES.getlist('blog_image'):
                BlogImage(blog_id=blog_obj.id, user_id=request.user.id, blog_image=i).save()
        blog_json = blog_to_json(blog_obj)
        return Response({'data': blog_json, 'message': 'Successfully Create Blog', 'status': 200})
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return JsonResponse({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)


@api_view(['PUT', ])
@decorator_from_middleware(CreateBlogMiddleware)
def edit_blog_view(request, form=None, pk=None):
    if pk:
        if Blog.objects.filter(id=pk).exists():
            Blog.objects.filter(id=pk).update(**form.cleaned_data)
            blog_obj = Blog.objects.get(id=pk)
            if 'blog_image' in request.FILES:
                for i in request.FILES.getlist('blog_image'):
                    BlogImage(blog_id=blog_obj.id, user_id=request.user.id, blog_image=i).save()
            blog_json = blog_to_json(blog_obj)
            return Response({'data': blog_json, 'message': 'Successfully Update Blog', 'status': 200}, status=200)
        else:
            return Response({'data': None, 'message': 'Blog Unique key is not exists', 'status': 404}, status=200)
    else:
        return Response({'data': None, 'message': 'Blog Unique key is required', 'status': 404}, status=200)


@api_view(['GET', ])
def get_blog_view(request, pk=None):
    if pk:
        if Blog.objects.filter(id=pk).exists():
            blog_obj = Blog.objects.get(id=pk)
            blog_json = blog_to_json(blog_obj)
            return Response({'data': blog_json, 'message': 'Successfully Update Blog', 'status': 200}, status=200)
        else:
            return Response({'data': None, 'message': 'Blog Unique key is not exists', 'status': 404}, status=200)
    else:
        if 'page' in request.GET and request.GET['page']:
            page = request.GET['page']
        else:
            page = 1
        blog_obj = blog_db.aggregate([
            {'$match': {'is_approved': True, 'is_delete': False}},
            {
                "$lookup": {
                    "from": "blog_blogimage",
                    "localField": "id",
                    "foreignField": "blog_id",
                    "as": "blog_images"
                }
            },
            {'$skip': (page-1)*10},
            {'$limit': 10}
        ])
        blog_data = json.loads(dumps(list(blog_obj), indent=2))
        for index, i in enumerate(blog_data):
            blog_data[index].pop("_id")
            blog_data[index]['created_at'] = datetime.fromtimestamp(int(i['created_at']['$date']/1000))
            blog_data[index]['updated_at'] = datetime.fromtimestamp(int(i['updated_at']['$date']/1000))
            for img_index, j in enumerate(blog_data[index]['blog_images']):
                blog_data[index]['blog_images'][img_index].pop("_id")
                blog_data[index]['blog_images'][img_index]['blog_image'] = '/media/' + j['blog_image']
                blog_data[index]['blog_images'][img_index]['created_at'] = datetime.fromtimestamp(int(j['created_at']['$date']/1000))
                blog_data[index]['blog_images'][img_index]['updated_at'] = datetime.fromtimestamp(int(j['updated_at']['$date']/1000))
        return Response({'data': blog_data, 'message': 'Successfully Update Blog', 'status': 200}, status=200)


@api_view(['DELETE', ])
def delete_blog_view(request, pk=None):
    if pk:
        if Blog.objects.filter(id=pk).exists():
            blog_obj = Blog.objects.filter(id=pk).update(is_delete=True)
            return Response({'data': None, 'message': 'Successfully Delete Blog', 'status': 200}, status=200)
        else:
            return Response({'data': None, 'message': 'Blog Unique key is not exists', 'status': 404}, status=200)
    else:
        return Response({'data': None, 'message': 'Blog Unique key is required', 'status': 404}, status=200)


@api_view(['GET', ])
def users_blog_view(request, pk=None):
    if 'page' in request.GET and request.GET['page']:
        page = request.GET['page']
    else:
        page = 1
    blog_obj = blog_db.aggregate([
        {'$match': {'is_approved': True, 'is_delete': False, 'user_id': request.user.id}},
        {
            "$lookup": {
                "from": "blog_blogimage",
                "localField": "id",
                "foreignField": "blog_id",
                "as": "blog_images"
            }
        },
        {'$skip': (page - 1) * 10},
        {'$limit': 10}
    ])
    blog_data = json.loads(dumps(list(blog_obj), indent=2))
    for index, i in enumerate(blog_data):
        blog_data[index].pop("_id")
        blog_data[index]['created_at'] = datetime.fromtimestamp(int(i['created_at']['$date'] / 1000))
        blog_data[index]['updated_at'] = datetime.fromtimestamp(int(i['updated_at']['$date'] / 1000))
        for img_index, j in enumerate(blog_data[index]['blog_images']):
            print(" iiiiiiiiiiiiiiiiiiii ", j['blog_image'])
            blog_data[index]['blog_images'][img_index].pop("_id")
            blog_data[index]['blog_images'][img_index]['blog_image'] = '/media/' + j['blog_image']
            blog_data[index]['blog_images'][img_index]['created_at'] = datetime.fromtimestamp(int(j['created_at']['$date'] / 1000))
            blog_data[index]['blog_images'][img_index]['updated_at'] = datetime.fromtimestamp(int(j['updated_at']['$date'] / 1000))
    return Response({'data': blog_data, 'message': 'Successfully Update Blog', 'status': 200}, status=200)


@api_view(['POST', ])
def create_blog_heart_view(request, blog_id=None):
    try:
        if Blog.objects.filter(id=blog_id).exists():
            blog_obj = Blog.objects.get(id=blog_id)
            if BlogHeart.objects.filter(user_id=request.user.id, blog_id=blog_id).exists():
                BlogHeart.objects.get(user_id=request.user.id, blog_id=blog_id).delete()
                blog_obj.heart = blog_obj.heart - 1
                blog_obj.save()
                msg = f'We Are Sorry, you remove heart from {blog_obj.title} Product'
            else:
                BlogHeart(user_id=request.user.id, blog_id=blog_id).save()
                blog_obj.heart = blog_obj.heart + 1
                blog_obj.save()
                msg = 'Thank you for giving heart'
            blog_json = blog_to_json(Blog.objects.get(id=blog_id))
            return Response({'data': blog_json, 'message': msg, 'status': 200})
        return Response({'data': None, 'message': "Blog Not Found", 'status': 404})
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return JsonResponse({'data': None, 'message': f"{e}, {f_name}, {exc_tb.tb_lineno}", 'status': 500}, status=200)


@api_view(['POST', ])
def create_blog_view_view(request, blog_id=None):
    try:
        if Blog.objects.filter(id=blog_id).exists():
            if not BlogView.objects.filter(user_id=request.user.id, blog_id=blog_id).exists():
                blog_obj = Blog.objects.get(id=blog_id)
                BlogView(user_id=request.user.id, blog_id=blog_id).save()
                blog_obj.view = blog_obj.view + 1
                blog_obj.save()
                msg = 'Thank you for View'
                blog_json = blog_to_json(Blog.objects.get(id=blog_id))
                return Response({'data': blog_json, 'message': msg, 'status': 200})
            return Response({'data': None, 'message': "User Already Viewwd the Blog", 'status': 200})
        return Response({'data': None, 'message': "Blog Not Found", 'status': 404})
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return JsonResponse({'data': None, 'message': f"{e}, {f_name}, {exc_tb.tb_lineno}", 'status': 500}, status=200)


@api_view(['POST', ])
@decorator_from_middleware(CreateBlogCommentMiddleware)
def create_blog_comment_view(request, form=None, blog_id=None):
    try:
        if Blog.objects.filter(id=blog_id).exists():
            form.cleaned_data['user_id'] = request.user.id
            form.cleaned_data['blog_id'] = blog_id
            BlogComment(**form.cleaned_data).save()
            blog_comment_obj = None
            if BlogComment.objects.filter(blog_id=blog_id, is_approved=True).exists():
                blog_comment_obj = blog_comment_json(BlogComment.objects.filter(blog_id=blog_id, is_approved=True))
            return Response({'data': blog_comment_obj, 'message': "Thank You For Commet, Please Wait for Approval", 'status': 200})
        return Response({'data': None, 'message': "Blog Not Found", 'status': 404})
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return JsonResponse({'data': None, 'message': f"{e}, {f_name}, {exc_tb.tb_lineno}", 'status': 500}, status=200)


@api_view(['POST', ])
def create_blog_comment_like_view(request, blog_id=None, blog_comment_id=None):
    try:
        if Blog.objects.filter(id=blog_id).exists():
            if BlogComment.objects.filter(id=blog_comment_id).exists():
                if not BlogCommentLike.objects.filter(user_id=request.user.id, blog_id=blog_id, blog_comment_id=blog_comment_id).exists():
                    blog_comment_obj = BlogComment.objects.get(id=blog_id)
                    BlogCommentLike(user_id=request.user.id, blog_id=blog_id, blog_comment_id=blog_comment_id).save()
                    blog_comment_obj.likes_count = blog_comment_obj.likes_count + 1
                    blog_comment_obj.save()
                    blog_json = blog_to_json(Blog.objects.get(id=blog_id))
                    return Response({'data': blog_json, 'message': 'Thank you for like Comment', 'status': 200})
            return Response({'data': None, 'message': "User Already Viewwd the Blog", 'status': 200})
        return Response({'data': None, 'message': "Blog Not Found", 'status': 404})
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return JsonResponse({'data': None, 'message': f"{e}, {f_name}, {exc_tb.tb_lineno}", 'status': 500}, status=200)


@api_view(['GET', ])
def approval_blog_comment_view(request, comment_id=None):
    if request.user.is_authenticated:
        if comment_id and BlogComment.objects.filter(id=comment_id).exists():
            comment_obj = BlogComment.objects.get(id=comment_id)
            if comment_obj.is_approved:
                comment_obj.is_approved = False
                comment_obj.unapproved_by = request.user.id
                comment_obj.approved_by = None
            else:
                comment_obj.is_approved = True
                comment_obj.approved_by = request.user.id
                comment_obj.unapproved_by = None
            comment_obj.save()
            return redirect('/admin/blog/blogcomment/')
    else:
        return redirect('/admin/login/')


@api_view(['GET', ])
def approval_blog_view(request, blog_id=None):
    if request.user.is_authenticated:
        if blog_id and Blog.objects.filter(id=blog_id).exists():
            blog_obj = Blog.objects.get(id=blog_id)
            if blog_obj.is_approved:
                Blog.objects.filter(id=blog_id).update(is_approved=False, approved_by=None)
            else:
                Blog.objects.filter(id=blog_id).update(is_approved=True, approved_by=request.user.id)
            return redirect('/admin/blog/blog/')
        else:
            return redirect('/admin/blog/blog/')
    else:
        return redirect('/admin/login/')
