from rest_framework.decorators import api_view
from .models import *
from rest_framework.response import Response
from .in_json import *
from django.shortcuts import redirect
from seartz.mongoDBConnection import *
from bson.json_util import dumps
from django.utils.decorators import decorator_from_middleware
from .middleware import *
import json
from admin_users.models import User
order_db = database['order_order']
gallery_db = database['projectconfig_gallery']
gallery_category_db = database['projectconfig_gallerycategory']
contact_us_content_db = database['projectconfig_contactuscontent']
testimonial_db = database['projectconfig_testimonial']


@api_view(['GET', ])
def home_slider_view(request):
    home_slider_obj = json_product(HomeSlider.objects.filter())
    return Response({'data': home_slider_obj, 'message': 'Successfully Get Product', 'status': 200}, status=200)


@api_view(['GET', ])
def update_feature_home_slider_view(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            home_slider_obj = HomeSlider.objects.get(id=pk)
            feature_slider_obj = HomeSlider.objects.filter(id=pk).update(is_featured=False if home_slider_obj.is_featured else True)
        return redirect('/admin/projectconfig/homeslider/')
    return redirect('/admin/login/')


@api_view(['GET', ])
def dashboard_view(request):
    if 'page' in request.GET and request.GET['page']:
        page = int(request.GET['page'])
    else:
        page = 1
    order_obj = order_db.find({'$and': [{"product.status": {'$ne': None}}, {"product.status": {'$ne': 'Cancelled'}}]})
    blog_data = json.loads(dumps(list(order_obj.skip((page-1)*10).limit(10)), indent=2))
    pages = order_obj.count()/10
    pages = round(pages)+1 if isinstance(pages, float) else pages
    return Response({'data': blog_data, 'pages': pages, 'count': order_obj.count(),  'message': 'Successfully Get Order', 'status': 200}, status=200)


@api_view(['GET', ])
def gallery_category_view(request, pk=None):
    if pk:
        pk = int(pk)
        if GalleryCategory.objects.filter(id=pk).exists():
            gallery_category_obj = GalleryCategory.objects.get(id=pk)
            gallery_obj = Gallery.objects.filter(category_id=gallery_category_obj.id)
            if gallery_obj.exists():
                gallery_category_data = model_to_dict(gallery_category_obj)
                galleries_list = []
                for i in gallery_obj:
                    k = model_to_dict(i)
                    k['image'] = i.image.url if i.image.name else i.image.name
                    galleries_list.append(k)
                gallery_category_data['galleries'] = galleries_list
                return Response({'data': gallery_category_data, 'message': 'Successfully Get Gallery Category', 'status': 200}, status=200)
    else:
        if 'page' in request.GET and request.GET['page']:
            page = request.GET['page']
        else:
            page = 1
        gallery_category_obj = gallery_category_db.aggregate([
            {'$match': {'status': True}},
            {
                "$lookup": {
                    "from": "projectconfig_gallery",
                    "localField": "id",
                    "foreignField": "category_id",
                    "as": "galleries"
                }
            },
            {'$skip': (page-1)*10},
            {'$limit': 10}
        ])
        blog_data = json.loads(dumps(list(gallery_category_obj), indent=2))
        for index, i in enumerate(blog_data):
            for g_index, k in enumerate(i['galleries']):
                blog_data[index]['galleries'][g_index]['image'] = '/media/' + k['image']
        return Response({'data': blog_data, 'message': 'Successfully Get Gallery Category', 'status': 200}, status=200)


@api_view(['GET', ])
def contact_us_view(request):
    contact_us_content_obj = contact_us_content_db.aggregate([
            {
                "$lookup": {
                    "from": "projectconfig_contactusicons",
                    "localField": "id",
                    "foreignField": "contact_us_content",
                    "as": "contactusicons"
                }
            },
        ])
    contact_us_content_json = json.loads(dumps(list(contact_us_content_obj), indent=2))

    for index, i in enumerate(contact_us_content_json):
        contact_us_content_json[index].pop('_id')
        contact_us_content_json[index]['created_at'] = datetime.fromtimestamp(i['created_at']['$date']/1000)
        contact_us_content_json[index]['updated_at'] = datetime.fromtimestamp(i['updated_at']['$date']/1000)
        if i['banner_image']:
            contact_us_content_json[index]['banner_image'] = '/media/' + i['banner_image']
        for row_index, k in enumerate(i['contactusicons']):
            contact_us_content_json[index]['contactusicons'][row_index].pop('_id')
            contact_us_content_json[index]['contactusicons'][row_index]['created_at'] = datetime.fromtimestamp(k['created_at']['$date']/1000)
            contact_us_content_json[index]['contactusicons'][row_index]['updated_at'] = datetime.fromtimestamp(k['updated_at']['$date']/1000)
    return Response({'data': contact_us_content_json, 'message': 'Successfully Get Contact Us Content', 'status': 200}, status=200)


@api_view(['POST', ])
@decorator_from_middleware(ContactUsFormModelMiddleware)
def create_contact_us_view(request, form):
    if request.user.is_authenticated:
        form.cleaned_data['user_id'] = request.user.id
    ContactUsFormModel(**form.cleaned_data).save()
    return Response({'data': None, 'message': 'Thank You for your Interest, we will reach you soon', 'status': 200}, status=200)


@api_view(['GET', ])
def testimonial_view(request):
    testimonial_obj = testimonial_db.find({'is_featured': True})
    testimonial_json = json.loads(dumps(list(testimonial_obj), indent=2))
    for index, i in enumerate(testimonial_json):
        testimonial_json[index].pop('_id')
        testimonial_json[index]['profile_image'] = '/media/' + i['profile_image']
        testimonial_json[index]['banner_image'] = '/media/' + i['banner_image']
        testimonial_json[index]['created_at'] = datetime.fromtimestamp(i['created_at']['$date']/1000)
        testimonial_json[index]['updated_at'] = datetime.fromtimestamp(i['updated_at']['$date']/1000)
    return Response({'data': testimonial_json, 'message': 'Successfully Get Testimonial', 'status': 200}, status=200)


@api_view(['GET', ])
def update_feature_testimonial_view(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            testimonial_obj = Testimonial.objects.get(id=pk)
            if testimonial_obj.is_featured:
                is_featured = False
            else:
                is_featured = True
            Testimonial.objects.filter(id=pk).update(is_featured=is_featured)
        return redirect('/admin/projectconfig/testimonial/')
    return redirect('/admin/login/')


@api_view(['GET', ])
def about_us_view(request):
    about_us_obj = AboutUs.objects.filter()
    about_us_list = []
    for i in about_us_obj:
        about_us_json = model_to_dict(i)
        about_us_json['banner_image'] = i.banner_image.url if i.banner_image.name else i.banner_image.name
        about_us_list.append(about_us_json)
    return Response({'data': about_us_list, 'message': 'Successfully Get About Us', 'status': 200}, status=200)
