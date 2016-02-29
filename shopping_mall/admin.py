# -*- coding: utf-8 -*-
from django.contrib import admin
from shopping_mall.models import ProductCategory, Brand, Product, ProductSelect, ProductSelectLimit, BrandSelect
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns
from django.shortcuts import render
from shopping_mall.views import ProductSelectForm
from django.http import HttpResponse
import csv
from django.template import loader, Context


class ProductCategoryListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('upper category')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'up_category'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        qs = model_admin.get_queryset(request)
        categories = qs.filter(code__regex=r'^\d{7}$')
        return [(pp.code + '0', pp.title) for pp in categories]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        code = self.value() or '0000'

        return queryset.filter(code__startswith=code)


class ProductBrandSelectFilter(admin.SimpleListFilter):
    title = _('Brand')
    template = "util/select_filter.html"
    parameter_name = 'brand'

    def lookups(self, request, model_admin):
        return [(pp.id, pp.chinese_name) for pp in Brand.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(brand__id=self.value())
        else:
            return queryset.all()


class ProductCategorySelectFilter(admin.SimpleListFilter):
    title = _('Category')
    template = "util/select_filter.html"
    parameter_name = 'cate'

    def lookups(self, request, model_admin):
        return [(pp.code, '.' * ((len(pp.code) - 4) / 3 * 2) + pp.title) for pp in
                ProductCategory.objects.all().order_by('code')]

    def queryset(self, request, queryset):
        cate = self.value() or '0000'
        return queryset.filter(category__code__startswith=cate)


class ProductPeanutsSelectFilter(admin.SimpleListFilter):
    title = _('Peanuts')
    template = "util/select_filter.html"
    parameter_name = 'peanuts'

    def lookups(self, request, model_admin):
        return [(0, '没单'), (1, '凑单')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(peanuts=self.value())
        else:
            return queryset.all()


class ProductOnShelfSelectFilter(admin.SimpleListFilter):
    title = _('On Shelf')
    template = "util/select_filter.html"
    parameter_name = 'shelf'

    def lookups(self, request, model_admin):
        return [(0, '上架'), (1, '下架')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(visible_status=self.value())
        else:
            return queryset.all()


class ProductAdmin(admin.ModelAdmin):
    list_display = ['ch_name_of_category', 'brand', 'code', 'ch_name_of_name', 'type', 'color', 'ch_name_of_reg_date',
                    'ch_name_of_price_now', 'ch_name_of_limit_amount', 'ch_name_of_remain_amount',
                    'ch_name_of_schedule', 'ch_name_of_peanuts']
    list_display_links = ['ch_name_of_name']
    list_per_page = 15
    list_filter = [ProductCategorySelectFilter, ProductBrandSelectFilter, ProductOnShelfSelectFilter,
                   ProductPeanutsSelectFilter]
    search_fields = ['name', 'type']
    actions = ['export_csv', 'make_on_self', 'make_off_self', 'make_schedule', 'make_unschedule', 'make_peanuts',
               'make_uot_peanuts']
    fieldsets = (
        (None, {
            'fields': (('code', 'category', 'brand'), ('name', 'type'), ('color', 'origin_place', 'barcode'))
        }),
        ('Price Information', {
            'fields': (
            ('price_now', 'market_price'), ('weight', 'weight_unit', 'carriage_charge'), ('discount_rate', 'point_num'),
            ('remain_amount', 'limit_amount', 'sell_amount'), ('receipt_general_rate', 'chk_ticket'))
        }),
        ('Detail Information', {
            'classes': ('collapse',),
            'fields': ('package', 'service', 'detail_info')
        }),
        ('Image Information', {
            #            'classes': ('collapse',),
            'fields': ('upload_check',)
        })
    )
    exclude = ['kind_index', 'price_old', 'point_price', 'point_low_price', 'related_info', 'request_amount',
               'visible_status', 'del_status', 'sel_date_promotion', 'schedule', 'peanuts', 'order_num_promotion',
               'sel_date_best_sells', 'order_num_best_sells', 'sel_date_news', 'order_num_news', 'sel_date_discount',
               'order_num_discount', 'sel_date_bargain', 'order_num_bargain', 'reg_date', 'master_index',
               'receipt_vat_rate']
    change_form_template = 'admin/shopping_mall/extras/product_change_form.html'

    def get_urls(self):
        urls = super(ProductAdmin, self).get_urls()
        #        my_urls = patterns('',
        #            (r'^image_spec/$', self.admin_site.admin_view(self.image_spec))
        #        )
        return urls

    def make_on_self(self, request, queryset):
        rows_updated = queryset.update(visible_status=0)
        if rows_updated == 1:
            message_bit = "1 product was"
        else:
            message_bit = "%s products were" % rows_updated
        self.message_user(request, "%s successfully put on shelf." % message_bit)

    make_on_self.short_description = '上架'

    def make_off_self(self, request, queryset):
        rows_updated = queryset.update(visible_status=1)
        if rows_updated == 1:
            message_bit = "1 product was"
        else:
            message_bit = "%s products were" % rows_updated
        self.message_user(request, "%s successfully put off shelf." % message_bit)

    make_off_self.short_description = '下架'

    def make_schedule(self, request, queryset):
        queryset.update(schedule=1)

    make_schedule.short_description = '预定'

    def make_unschedule(self, request, queryset):
        queryset.update(schedule=0)

    make_unschedule.short_description = '没预定'

    def make_peanuts(self, request, queryset):
        queryset.update(peanuts=1)

    make_peanuts.short_description = '凑单'

    def make_uot_peanuts(self, request, queryset):
        queryset.update(peanuts=0)

    make_uot_peanuts.short_description = '没凑单'

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="good-products.csv"'

        #    This is the case for csv library

        #        writer = csv.writer(response)
        #        writer.writerow(['Name', 'Brand', 'Type', 'Code', 'Color', 'Origin_place'])
        #        for qs in queryset:
        #            writer.writerow([qs.name, qs.brand, qs.type, qs.code, qs.color, qs.origin_place])
        #            writer.writerow([qs.code, qs.code, qs.code, qs.code, qs.color, qs.code])

        t = loader.get_template('admin/shopping_mall/extras/csv-template.html')
        c = Context({
            'data': queryset,
        })
        response.write(t.render(c))
        return response

    export_csv.short_description = 'Export selected products as CSV'


class ProductCategoryAdmin(admin.ModelAdmin):
    fields = ['code', 'title', 'order_num']
    list_display = ['get_up_category', 'title']
    list_display_links = ['get_up_category', 'title']
    search_fields = ['title', 'code']
    list_per_page = 10
    list_filter = (ProductCategoryListFilter,)

    change_form_template = 'admin/shopping_mall/extras/product_category_change_form.html'

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['up_category'] = ProductCategory().get_up_category_map()
        return super(ProductCategoryAdmin, self).add_view(request, form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['up_category'] = ProductCategory().get_up_category_map()
        return super(ProductCategoryAdmin, self).change_view(request, object_id,
                                                             form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        parent_code = request.POST['up_code']
        old_code = obj.code

        qs = ProductCategory.objects.extra(where=['code like %s'], params=[parent_code + '___'])
        new_code = '000'
        if qs:
            new_code = qs.extra(select={'max_code': 'max(code)'})[0].max_code[-3:]

        obj.code = parent_code + format('%03d' % (int(new_code) + 1))
        obj.save()
        if change:
            ProductCategory.objects.get(code=old_code).delete()


class TestManyToManyAdmin(admin.ModelAdmin):
    raw_id_fields = ("ref_many",)


class ProductSelectAdmin(admin.ModelAdmin):
    fields = ['page_type']
    change_list_template = "admin/shopping_mall/productselect/index.html"

    def get_urls(self):
        urls = super(ProductSelectAdmin, self).get_urls()
        my_urls = patterns('',
                           (r'^list_item/$', self.admin_site.admin_view(self.list_view)),
                           (r'^removeAll/$', self.admin_site.admin_view(self.remove_all)),
                           (r'^update_selection/$', self.admin_site.admin_view(self.update_selection)),
                           (r'^reorder/$', self.admin_site.admin_view(self.reorder))
                           )
        return my_urls + urls

    def reorder(self, request):
        ps_form = ProductSelectForm(request.GET)
        ps = ps_form.save(commit=False)
        order_str = request.GET.get('order_str')
        ps.reorder(order_str)
        return HttpResponse('success')

    def update_selection(self, request):
        ps_form = ProductSelectForm(request.GET)
        ps = ps_form.save(commit=False)
        selected = request.GET.get('selected')
        deselected = request.GET.get('deselected')

        if selected:
            ps.select(selected)
        if deselected:
            ps.deselect(deselected)

        return HttpResponse('success')

    def remove_all(self, request):
        ps_form = ProductSelectForm(request.GET)
        ps = ps_form.save(commit=False)
        page_detail = request.GET.get('page_detail')
        ps.deselect_all(page_detail)
        return HttpResponse('success')

    def list_view(self, request):
        ps_form = ProductSelectForm(request.GET)
        ps = ps_form.save(commit=False)
        page_detail = request.GET.get('page_detail') or '0000'
        page = request.GET.get('page')

        list_id = request.GET.get('listId')
        is_up = request.GET.get('is_up')

        if is_up == '1':
            data = ps.get_up_data_spec(page)
            extra_data = [ps.page_type, 1]
        else:
            sort_direction = int(request.GET.get('sort_direction'))
            product_name = request.GET.get('product_name') or ''
            order_by = request.GET.get('order_by')

            data = ps.get_down_data_spec(page_detail, product_name, order_by, sort_direction, page)
            extra_data = [ps.page_type, 0]

        return render(request, 'admin/shopping_mall/productselect/list_view_item.html',
                      {'list_id': list_id, 'data': data, 'extra_data': extra_data})

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['page_details'] = {2: '   分类名   ', 3: '   品牌名   '}
        extra_context['sel_kind_select'] = ProductSelect().get_sel_kind_title()
        brands = [(pp.id, pp.chinese_name) for pp in Brand.objects.all()]
        brands.insert(0, ('0', '所有'))
        extra_context['page_detail_select'] = {2: ProductCategory().get_up_category_map(parent_level=2), 3: brands}
        extra_context['limit_select'] = [
            [(0, '无限制'), (10, '   10个'), (20, '   20个'), (30, '   30个'), (40, '   40个'), (50, '   50个'), (80, '   80个'),
             (120, '   120个')],
            [(0, '无限制'), (1, '   1个'), (2, '   2个'), (3, '   3个'), (4, '   4个'), (5, '   5个'), (8, '   8个'),
             (12, '   12个')]]
        extra_context['limits'] = ProductSelectLimit().get_general_limits()

        return super(ProductSelectAdmin, self).changelist_view(request, extra_context=extra_context)


# register admin pages to the admin.site
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Brand)
# admin.site.register(BrandSelect)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSelect, ProductSelectAdmin)
# admin.site.register(ProductSelectLimit)
