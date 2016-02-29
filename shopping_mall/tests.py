# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User

from shopping_mall.models import ProductSelect, Product, ProductCategory, Brand

def create_product_category(code, title):
    return ProductCategory.objects.create(code = code, title = title)

def create_brand(name):
    return Brand.objects.create(chinese_name = name, name = name, path1 = name, path2 = name)

def create_product(brand_id, category_id, name):
    return Product.objects.create(category_id = category_id, brand_id = brand_id, code = name, name = name, type = name, related_info = name, color = name, origin_place = name)

def create_product_select(page_type, sel_kind, product_id):
    return ProductSelect.objects.create(page_type = page_type, sel_kind = sel_kind, product_id = product_id)

class ProductCategoryModelTests(TestCase):
    def setUp(self):
        create_product_category('0000001', 'A')
        create_product_category('0000001001', 'AA')
        create_product_category('0000001002', 'AB')
        create_product_category('0000002', 'B')
        create_brand('Test Brand')

        create_product(1, '0000001001', 'product A')
        create_product(1, '0000001001', 'product B')
        create_product(1, '0000001002', 'product C')
        create_product(1, '0000001002', 'product D')


    def test_get_up_category_with_0000(self):
        pc = ProductCategory.objects.get(code='0000001')
        self.assertEqual(pc.get_up_category(), '大分类')

    def test_get_up_category_with_other(self):
        pc = ProductCategory.objects.get(code='0000001002')
        self.assertEqual(pc.get_up_category(), 'A')

    def test_get_up_category_map_with_parent_level_0(self):
        pc = ProductCategory.objects.get(code='0000001002')
        self.assertListEqual(pc.get_up_category_map(parent_level=0, include_root=False), [])

    def test_get_up_category_map_with_parent_level_1(self):
        self.assertListEqual(ProductCategory().get_up_category_map(parent_level=1, include_root=False), [('0000001','....A'),('0000002','....B')])

    def test_get_up_category_map_with_parent_level_2(self):
        self.assertListEqual(ProductCategory().get_up_category_map(parent_level=2, include_root=False), [
            ('0000001','....A'),
            ('0000001001', '........AA'),
            ('0000001002', '........AB'),
            ('0000002','....B')
        ])

    def test_get_cate_statistics(self):
        self.assertJSONEqual(ProductCategory().get_cate_statistics(),'[{"label":"AA", "data":[[1,2]]},{"label":"AB", "data":[[2,2]]}]')

class ProductSelectMethodTests(TestCase):
    def test_get_up_data_spec(self):
        """
        get_up_data_spec() should return the same number of products from the raw database
        """
        create_brand('Test Brand')

        create_product_category('0000001', 'A')
        create_product_category('0000001001', 'AA')
        create_product_category('0000001002', 'AB')

        create_product(1, '0000001001', 'product A')
        create_product(1, '0000001001', 'product B')
        create_product(1, '0000001002', 'product C')
        create_product(1, '0000001002', 'product D')

        create_product_select(1,1,2)
        create_product_select(2,1,2)
        create_product_select(3,1,2)
        create_product_select(4,1,1)
        create_product_select(5,1,2)
        create_product_select(6,1,3)
        create_product_select(7,1,4)

        for i in [1, 4, 5, 6, 7]:
            ps = ProductSelect.objects.filter(page_type=i, sel_kind=1).count()
            test_ps = ProductSelect(page_type=i, sel_kind=1).get_up_data_spec(page_size=10000)
            t_ps = test_ps.paginator.count
            self.assertEqual(ps, t_ps)


class ProductSelectAdminViewTest(TestCase):
    def test_list_view(self):
        User.objects.create_user(username='jks', password='jksfirst')

        c = self.client
        if c.login(username='jks', password='jksfirst'):
#        response = c.post('/admin/', {'username': 'test', 'password': 'jks'})
#        print response.status_code
#        print response.content
#        print '@@@@@'
#        response = self.client.post('/admin/shopping_mall')
#        print response.status_code
            print '@@@@@'