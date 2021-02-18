from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from .middleware import *
from .product_json import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from categories.models import *
from django.db.models import Avg
from .serializers import *
from admin_users.models import *
from django.core.files.storage import FileSystemStorage


@api_view(['GET', ])
def get_product_view(request):
    if Product.objects.filter().exists():
        products = Product.objects.filter()
        page = request.GET.get('page', 1)

        paginator = Paginator(products, 10)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        page = products.paginator.num_pages
        products = json_product(products)
        return Response({'data': products, 'message': 'Successfully Get Product', 'page': page, 'status': 200},
                        status=200)
    else:
        return Response({'data': None, 'message': 'Product not found', 'status': 404}, status=200)


@api_view(['GET', ])
def get_one_product_view(request, pk):
    if pk:
        if Product.objects.filter(id=pk).exists():
            products = one_product_json(Product.objects.get(id=pk))
            return Response({'data': products, 'message': 'Successfully Get Product', 'status': 200}, status=200)
        else:
            return Response({'data': None, 'message': 'Product Id Invalid', 'status': 404}, status=200)
    else:
        return Response({'data': None, 'message': 'Product Id Cannot Be NULL', 'status': 404}, status=200)


@api_view(['GET', ])
def get_one_slug_product_view(request, slug):
    if slug:
        if Product.objects.filter(slug=slug).exists():
            products = one_product_json(Product.objects.get(slug=slug))
            return Response({'data': products, 'message': 'Successfully Get Product', 'status': 200}, status=200)
        else:
            return Response({'data': None, 'message': 'Product Id Invalid', 'status': 404}, status=200)
    else:
        return Response({'data': None, 'message': 'Product Id Cannot Be NULL', 'status': 404}, status=200)


@api_view(['GET', ])
def get_product_category_view(request, category=None):
    if category:
        if Categories.objects.filter(category_name=category).exists():
            category = Categories.objects.filter(category_name=category)
            if Product.objects.filter(category_id=category.id).exists():
                products = Product.objects.filter(category_id=category.id)
                page = request.GET.get('page', 1)
                paginator = Paginator(products, 10)
                try:
                    products = paginator.page(page)
                except PageNotAnInteger:
                    products = paginator.page(1)
                except EmptyPage:
                    products = paginator.page(paginator.num_pages)
                page = products.paginator.num_pages
                products = json_product(products)
                return Response({'data': products, 'message': 'Successfully Get Product', 'page': page,
                                 'status': 200}, status=200)
            else:
                return Response({'data': None, 'message': 'Product not found', 'status': 404}, status=200)
        else:
            return Response({'data': None, 'message': 'Category not found', 'status': 404}, status=200)
    else:
        return Response({'data': None, 'message': 'Category Valid Category', 'status': 404}, status=200)


@api_view(['POST', ])
def create_product_heart_view(request, prodid=None):
    prod_obj = Product.objects.get(pk=prodid)
    if not ProductHeart.objects.filter(user_id=request.user.id, product_id=prod_obj.id).exists():
        ProductHeart(user_id=request.user.id, product_id=prod_obj.id).save()
        prod_obj.heart = prod_obj.heart + 1
        prod_obj.save()
        return Response({'data': prod_obj.product_name, 'message': 'Thank you for give heart', 'status': 200},
                        status=200)
    else:
        ProductHeart.objects.get(user_id=request.user.id, product_id=prod_obj.id).delete()
        prod_obj.heart = prod_obj.heart - 1
        prod_obj.save()
        return Response({'data': prod_obj.product_name,
                         'message': f'We Are Sorry, you remove heart from {prod_obj.product_name} Product',
                         'status': 200}, status=200)


@api_view(['POST', ])
def create_product_view_view(request, prodid=None):
    prod_obj = Product.objects.get(pk=prodid)
    if not ProductView.objects.filter(user_id=request.user.id, product_id=prod_obj.id).exists():
        ProductView(user=request.user, product=prod_obj).save()
        prod_obj.view += prod_obj.view + 1
        prod_obj.save()
        return Response({'data': prod_obj.product_name, 'message': 'Thank you for view', 'status': 200}, status=200)
    else:
        return Response({'data': None, 'message': 'User already Viewed', 'status': 200}, status=200)


@api_view(['POST', ])
def create_product_total_comment_view(request, prodid=None):
    prod_obj = Product.objects.get(pk=prodid)
    comment = request.POST.get('comment')
    sub_comment = None
    if 'sub_comment' in request.POST and request.POST['sub_comment'] is not None and request.POST['sub_comment'] != '':
        if ProductComment.objects.filter(id=request.POST['sub_comment']).exists():
            sub_comment = ProductComment.objects.get(id=request.POST['sub_comment'])
    ProductComment(user_id=request.user.id, product_id=prod_obj.id, comment=comment, sub_comment=sub_comment).save()
    prod_obj.total_comment += prod_obj.total_comment + 1
    prod_obj.save()
    return Response({'data': prod_obj.product_name, 'message': 'Thank you for give comment', 'status': 200}, status=200)


@api_view(['POST', ])
def create_product_size_view(request, form=None, prodid=None):
    if request.user.user_role.role in ['Admin', 'Artist']:
        prod_obj = Product.objects.get(pk=prodid)
        size = form.cleaned_data['size']
        size_image = form.cleaned_data['size_image']
        price = form.cleaned_data['price']
        ProductSize(user_id=request.user.id, product_id=prod_obj.id, size=size, size_image=size_image, price=price).save()
        return Response({'data': ProductSize.objects.last(), 'message': 'Successfully create Product Size',
                         'status': 200}, status=200)
    else:
        return Response({'data': None, 'message': 'User must be Admin or Artist', 'status': 200}, status=200)


@api_view(['POST', ])
def create_product_total_review_view(request, prodid=None):
    try:
        review = int(request.POST.get('review'))
        if review not in [1, 2, 3, 4, 5]:
            return Response({'data': None, 'message': 'Review must be 1, 2, 3, 4, 5', 'status': 200},
                            status=200)
        prod_obj = Product.objects.get(pk=prodid)
        ProductReview(user_id=request.user.id, product_id=prod_obj.id, review=review).save()
        prod_review = ProductReview.objects.filter(product_id=prod_obj.id).aggregate(Avg('review'))
        prod_obj.total_review = prod_review['review__avg']
        prod_obj.save()
        return Response({'data': prod_obj.product_name, 'message': 'Thank you for give review', 'status': 200},
                        status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return Response({'data': None, 'message': f"{e}, {f_name}, {exc_tb.tb_lineno}", 'status': 200}, status=200)


@api_view(['GET', ])
def update_feature_product_view(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            prod = Product.objects.get(id=pk)
            if prod.is_feature:
                prod.is_feature = False
            else:
                prod.is_feature = True
            prod.save()
        return redirect('/admin/product/product/')
    return redirect('/admin/login/')


@api_view(['GET', ])
def get_users_product_view(request, pk=None):
    if pk:
        if User.objects.filter(id=int(pk)).exists():
            product_obj = ProductSerializer(instance=Product.objects.filter(user_id=int(pk)), many=True)
            return Response({'data': product_obj.data, 'message': 'Successfully Get User`s Product', 'status': 200}, status=200)
        else:
            return Response({'data': None, 'message': 'User Not Found', 'status': 404}, status=200)
    else:
        product_obj = ProductSerializer(instance=Product.objects.filter(), many=True)
        return Response({'data': product_obj.data, 'message': 'Successfully Get User`s Product', 'status': 200}, status=200)


@api_view(['POST', ])
@decorator_from_middleware(ProductMiddleware)
def create_product_view(request, form=None):
    try:
        if request.user.is_superuser or UserRole.objects.filter(id=request.user.user_role, role="Artist").exists():
            form.cleaned_data['user_id'] = request.user.id
            product_gallery_image = None
            if 'product_gallery_image' in request.FILES:
                product_gallery_image = request.FILES.getlist('product_gallery_image')
                form.cleaned_data.pop('product_gallery_image')
            Product(**form.cleaned_data).save()
            prod_obj = Product.objects.last()
            if product_gallery_image:
                for file in product_gallery_image:
                    ProductGalleryImage(user_id=request.user.id, product_id=prod_obj.id, product_gallery_image=file).save()
            product_obj = ProductSerializer(instance=prod_obj, many=False)

            return Response({'data': product_obj.data, 'message': 'Successfully Get User`s Product', 'status': 200}, status=200)
        else:
            return Response({'data': None, 'message': 'Please Register as Artist', 'status': 404}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return Response({'data': None, 'message': f"{e}, {f_name}, {exc_tb.tb_lineno}", 'status': 200}, status=200)


@api_view(['PUT', ])
@decorator_from_middleware(ProductMiddleware)
def edit_product_view(request, form=None, pk=None):
    try:
        product_gallery_image = None
        if 'product_gallery_image' in request.FILES:
            product_gallery_image = request.FILES.getlist('product_gallery_image')
            form.cleaned_data.pop('product_gallery_image')
        year, month, date = datetime.now().strftime("%Y"), datetime.now().strftime("%B"), datetime.now().strftime("%d")
        if 'product_home_image' in form.cleaned_data and form.cleaned_data['product_home_image']:
            product_home_image_fs = FileSystemStorage('Product/' + f"{year}/{month}/{date}/{request.user.account_id}")
            product_home_image_file = product_home_image_fs.save(form.cleaned_data['product_home_image'].name, form.cleaned_data['product_home_image'])
            form.cleaned_data['product_home_image'] = 'Product/' + f"{year}/{month}/{date}/{request.user.account_id}/" + product_home_image_file
        Product.objects.filter(id=pk).update(**form.cleaned_data)

        prod_obj = Product.objects.get(id=pk)
        if product_gallery_image:
            for file in product_gallery_image:
                ProductGalleryImage(user_id=request.user.id, product_id=prod_obj.id, product_gallery_image=file).save()
        product_obj = ProductSerializer(instance=prod_obj, many=False)
        return Response({'data': product_obj.data, 'message': 'Successfully Get User`s Product', 'status': 200}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return Response({'data': None, 'message': f"{e}, {f_name}, {exc_tb.tb_lineno}", 'status': 200}, status=200)
