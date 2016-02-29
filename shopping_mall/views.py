# -*- coding: utf-8 -*-
import json
from django.forms import ModelForm
from django.http import HttpResponse

from shopping_mall.models import ProductSelect
from shopping_mall.models import ProductCategory
from shopping_mall.models import BrandSelect
from shopping_mall.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from PIL import Image
from django.conf import settings


class ProductSelectForm(ModelForm):
    class Meta:
        model = ProductSelect
        exclude = ['product', 'order_num']


def product_category(request):
    categories = ProductCategory.objects.extra(where=['length(code)=7'])
    f_categories = [{'code': pp.code, 'title': pp.title} for pp in categories]
    for up_cate in f_categories:
        sub_cate = ProductCategory.objects.filter(code__startswith=up_cate["code"]).extra(where=['length(code)=10'])
        f_sub_cate = [{'code': pp.code, 'title': pp.title} for pp in sub_cate]
        up_cate["sub_cate"] = f_sub_cate

    return HttpResponse(json.dumps(f_categories))


def spec_products(request, page_type=1):
    page_type = int(page_type)
    sel_kinds = ProductSelect().get_sel_kind_title()[page_type]
    results = []

    for sel_kind, sel_title in sel_kinds:
        ps = ProductSelect.objects.filter(page_type=page_type, sel_kind=sel_kind).order_by('order_num')
        product_ids = [pp.product_id for pp in ps]
        products = [Product.objects.get(id=pp) for pp in product_ids]
        products = get_formatted_products(products)
        element = {"type": sel_title, "products": products}
        results.append(element)
    return HttpResponse(json.dumps(results))


def get_product_all(request):
    products = get_formatted_products(Product.objects.all())
    return HttpResponse(json.dumps(products))


def get_formatted_products(products):
    products = [{
                    "id": pp.id,
                    "name": pp.name,
                    "type": pp.type,
                    "price_now": pp.price_now,
                    "category": pp.category_id,
                    "category_title": pp.category.title,
                    "upload_check": pp.upload_check,
                    "code": pp.code,
                    "market_price": pp.market_price,
                    "package": unicode(pp.package),
                    "service": unicode(pp.service),
                    "detail_info": unicode(pp.detail_info),
                    "origin_place": pp.origin_place,
                    "weight_unit": pp.weight_unit,
                    "weight": pp.weight,
                    "reg_date": str(pp.reg_date),
                    "discount_rate": pp.discount_rate,
                    "brand": pp.brand.name,
                    "brand_id": pp.brand.id,
                    "sell_amount": pp.sell_amount
                } for pp in products]

    return products


def get_brands(request):
    results = {}
    ads = BrandSelect().get_recommended_brands(2)
    results["ads"] = ads
    results["recommended"] = {}
    results["other"] = {}

    categories = ProductCategory.objects.extra(where=['length(code)=7'])
    for category in categories:
        rec_brands = BrandSelect().get_recommended_brands(3, category.code)
        oth_brands = BrandSelect().get_other_brands(category.code, rec_brands)
        results["recommended"][category.code] = rec_brands
        results["other"][category.code] = oth_brands

    return HttpResponse(json.dumps(results))


@csrf_exempt
def image_spec(request, product_id):
    if product_id == '0':
        product_id = Product.objects.extra(select={'max_id': 'max(id)'})[0].max_id
        product_id = str(int(product_id) + 1)

    return render(request, 'admin/shopping_mall/product/image_spec.html',
                  {'product_id': product_id, 'upload_check': request.GET.get('upload_check')})


@csrf_exempt
def image_upload(request, product_id):
    print '################'
    if len(request.FILES) > 0:
        print '@@@@@@@@@@@'
        im = Image.open(request.FILES['product_image'])
        sub_idx = request.POST.get('upload_check')

        if product_id == '0':
            product_id = Product.objects.extra(select={'max_id': 'max(id)'})[0].max_id
            product_id = str(int(product_id) + 1)

        saveProductImage(im, product_id, sub_idx)
        return HttpResponse('success')


def saveProductImage(sourceImg, id, s_idx):
    widths = [50, 70, 100, 130, 160, 300, 350, 700]
    static_url = settings.STATIC_ROOT + 'images/productImages/' + id + '_'

    print '@@@@@@@@@@@', id, s_idx
    for width in widths:
        image = sourceImg.resize((width, width))
        image.save(static_url + str(s_idx) + '_' + str(width) + '.jpg')
    image = sourceImg.resize((700, 700))
    image.save(static_url + str(s_idx) + '_t.jpg')
