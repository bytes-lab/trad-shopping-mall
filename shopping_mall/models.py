# -*- coding: utf-8 -*-

from django.db import models
from django.core.paginator import Paginator
import json


class ProductCategory(models.Model):
    """
    This is the model for product category in the shopping mall
    """
    code = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=200)
    recommended_product = models.CharField(max_length=100, null=True)
    order_num = models.IntegerField(default=0)

    def get_up_category(self):
        up_category_code = self.code[:-3]
        if up_category_code == '0000':
            return '大分类'
        else:
            return ProductCategory.objects.get(code=up_category_code).title

    def get_up_category_map(self, parent_level=1, include_root=True):
        depth = 4 + parent_level * 3
        categories = ProductCategory.objects.extra(where=['length(code)<=%s'], params=[depth])
        categories = categories.order_by('code')
        up_category = [(pp.code, '.' * ((len(pp.code) - 4) / 3 * 4) + pp.title) for pp in categories]
        if include_root:
            up_category.insert(0, (u'0000', '大分类'))

        return up_category

    #@staticmethod
    def get_cate_statistics(self):
        categories = ProductCategory.objects.all()
        result = []
        index = 0
        for pp in categories:
            num_products = len(Product.objects.filter(category__code=pp.code))
            if num_products > 0:
                index += 1
                result.append({'label': pp.title, 'data': [[index, num_products]]})
        return json.dumps(result)

    def __unicode__(self):
        return self.title

    get_up_category.short_description = '上分类'
    get_up_category.admin_order_field = 'code'


class Brand(models.Model):
    chinese_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    path1 = models.CharField(max_length=150)
    path2 = models.CharField(max_length=150)
    order_num = models.IntegerField(default=0)
    recommended = models.TextField(blank=True)

    def __unicode__(self):
        return self.chinese_name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory)
    brand = models.ForeignKey(Brand)
    kind_index = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=150)
    color = models.CharField(max_length=30)
    origin_place = models.CharField(max_length=50)
    reg_date = models.DateTimeField(blank=True, null=True)
    market_price = models.FloatField(blank=True, null=True)
    price_now = models.FloatField(blank=True, null=True)
    price_old = models.FloatField(blank=True, null=True)
    point_price = models.IntegerField(blank=True, null=True)
    point_low_price = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    weight_unit = models.FloatField(blank=True, null=True)
    package = models.CharField(max_length=200, blank=True, null=True)
    service = models.TextField(blank=True, null=True)
    detail_info = models.TextField(blank=True, null=True)
    related_info = models.TextField(null=True)
    upload_check = models.CharField(max_length=50, blank=True, null=True)
    remain_amount = models.IntegerField(blank=True, null=True)
    request_amount = models.IntegerField(blank=True, null=True)
    limit_amount = models.IntegerField(blank=True, null=True)
    sell_amount = models.IntegerField(blank=True, null=True)
    visible_status = models.IntegerField(blank=True, null=True)
    del_status = models.IntegerField(blank=True, null=True)
    discount_rate = models.IntegerField(blank=True, null=True)
    point_num = models.IntegerField(blank=True, null=True)
    carriage_charge = models.FloatField(blank=True, null=True)
    receipt_general_rate = models.IntegerField(blank=True, null=True)
    receipt_vat_rate = models.IntegerField(blank=True, null=True)
    sel_date_promotion = models.DateTimeField(blank=True, null=True)
    order_num_promotion = models.IntegerField(blank=True, null=True)
    sel_date_best_sells = models.DateTimeField(blank=True, null=True)
    order_num_best_sells = models.IntegerField(blank=True, null=True)
    sel_date_news = models.DateTimeField(blank=True, null=True)
    order_num_news = models.IntegerField(blank=True, null=True)
    sel_date_discount = models.DateTimeField(blank=True, null=True)
    order_num_discount = models.IntegerField(blank=True, null=True)
    sel_date_bargain = models.DateTimeField(blank=True, null=True)
    order_num_bargain = models.IntegerField(blank=True, null=True)
    schedule = models.IntegerField(blank=True, null=True)
    peanuts = models.IntegerField(blank=True, null=True)
    master_index = models.IntegerField(blank=True, null=True)
    chk_ticket = models.IntegerField(blank=True, null=True)
    barcode = models.CharField(max_length=30, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def ch_name_of_category(self):
        return self.category

    def ch_name_of_name(self):
        return self.name

    def ch_name_of_reg_date(self):
        return self.reg_date

    def ch_name_of_price_now(self):
        return self.price_now

    def ch_name_of_remain_amount(self):
        return self.remain_amount

    def ch_name_of_limit_amount(self):
        return self.remain_amount

    def ch_name_of_schedule(self):
        return self.schedule

    def ch_name_of_peanuts(self):
        return self.peanuts

    ch_name_of_category.short_description = " 分 类 "
    ch_name_of_name.short_description = " 商 品 名 称 "
    ch_name_of_reg_date.short_description = " 上 架 时 间 "
    ch_name_of_price_now.short_description = "商品价格"
    ch_name_of_remain_amount.short_description = "现在"
    ch_name_of_limit_amount.short_description = "限度"
    ch_name_of_schedule.short_description = "预定"
    ch_name_of_schedule.boolean = True
    ch_name_of_peanuts.short_description = "凑单"
    ch_name_of_peanuts.boolean = True


class BrandSelect(models.Model):
    page_type = models.IntegerField()
    category = models.ForeignKey(ProductCategory, null=True, blank=True)
    brand = models.ForeignKey(Brand)
    order_num = models.IntegerField(default=1)

    def get_recommended_brands(self, page_type, category_id=''):
        brands = BrandSelect.objects.filter(page_type=page_type)
        if category_id:
            brands = BrandSelect.objects.filter(page_type=page_type, category=category_id)

        return [pp.brand_id for pp in brands]

    def get_other_brands(self, category_id, rec_brands):
        products = Product.objects.filter(category__code__startswith=category_id).exclude(brand__in=rec_brands)
        brands = set([pp.brand.id for pp in products])
        return [pp for pp in brands]


class ProductSelect(models.Model):
    page_type = models.IntegerField()
    sel_kind = models.IntegerField()
    product = models.ForeignKey(Product)
    order_num = models.IntegerField(default=0)

    def get_up_data_spec(self, page=1, page_size=5):
        rp = ProductSelect.objects.filter(page_type=self.page_type, sel_kind=self.sel_kind).order_by('order_num')
        limit = self.product_id
        if limit != '0':
            rp = rp[:limit]

        product_ids = [pp.product_id for pp in rp]
        order_nums = [pp.order_num for pp in rp]

        data = [[Product.objects.get(id=product_ids[i]), order_nums[i]] for i in range(len(order_nums))]
        paginator = Paginator(data, page_size)
        return paginator.page(page)

    def get_down_data_spec(self, page_detail, product_name, order_by, sort_direction, page, page_size=5):
        # update limit information
        exclude_products = [pp[0].id for pp in self.get_up_data_spec(page_size=1000)]

        if self.page_type == 1 or self.page_type == 4:
            ps = ProductSelect.objects.filter(page_type=self.page_type)
        else:
            ps = ProductSelect.objects.all()
        all_products = [pp.product_id for pp in ps]

        order_by = '-' * sort_direction + order_by

        if self.page_type == 3 and page_detail != '0':
            products = Product.objects.exclude(id__in=exclude_products) \
                .filter(del_status=0, visible_status=0, name__icontains=product_name,
                        brand__id=page_detail, id__in=all_products).order_by(order_by)
        else:
            products = Product.objects.exclude(id__in=exclude_products). \
                filter(del_status=0,
                       visible_status=0,
                       name__icontains=product_name,
                       category__code__startswith=page_detail,
                       id__in=all_products).order_by(order_by)

        data = [[pp, 0] for pp in products]
        paginator = Paginator(data, page_size)

        return paginator.page(page)

    def get_sel_kind_title(self):
        return {
            1: [(1, '新品上市'), (2, '疯狂抢购 (上)'), (5, '特价专区'), (6, '疯狂抢购 (下)')],
            2: [(1, '新品市场'), (2, '热销'), (3, 'HOT促销'), (4, '打折'), (5, '特价专区')],
            4: [(1, '新品'), (3, '促销'), (4, '打折'), (5, '特价')]
        }

    def deselect_all(self, page_detail):
        if self.page_type == 2:
            selection = ProductSelect.objects. \
                filter(page_type=self.page_type,
                       sel_kind=self.sel_kind,
                       product__category__code__startswith=page_detail)
        elif self.page_type == 3 and page_detail != '0':
            selection = ProductSelect.objects. \
                filter(page_type=self.page_type,
                       sel_kind=self.sel_kind,
                       product__brand__id=page_detail)
        else:
            selection = ProductSelect.objects. \
                filter(page_type=self.page_type,
                       sel_kind=self.sel_kind)

        selection.delete()

    def deselect(self, deselection):
        ids = deselection.split(',')
        ids = [int(pp) for pp in ids]
        ProductSelect.objects.filter(page_type=self.page_type,
                                     sel_kind=self.sel_kind,
                                     product__id__in=ids).delete()

    def select(self, selection):
        ids = selection.split(',')
        order_num = 0
        for p_id in ids:
            order_num += 1
            ProductSelect.objects.create(page_type=self.page_type,
                                         sel_kind=self.sel_kind,
                                         product_id=int(p_id),
                                         order_num=order_num)

    def reorder(self, order_str):
        id_order = order_str.split('@')
        for i in range(len(id_order) / 2):
            product_id = int(id_order[2 * i])
            order_num = int(id_order[2 * i + 1])
            ProductSelect.objects.filter(page_type=self.page_type, sel_kind=self.sel_kind,
                                         product__id=product_id).update(order_num=order_num)


class ProductSelectLimit(models.Model):
    page_type = models.IntegerField()
    sel_kind = models.IntegerField()
    sel_limit = models.IntegerField(default=0)

    def get_limit(self):
        return ProductSelectLimit.objects.filter(page_type=self.page_type, sel_kind=self.sel_kind)[0].sel_limit

    def get_general_limits(self):
        result = {}
        self.sel_kind = 1
        for i in range(1, 8):
            self.page_type = i
            result[i] = self.get_limit()
        return result
