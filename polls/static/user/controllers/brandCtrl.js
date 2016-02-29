angular.module("shoppingMallApp")
.constant("brandUrl", "/First/shopping_mall/get_brand_select")
.controller("brandCtrl", function ($scope, $http, brandUrl) {
	$scope.data.brandBodyUrl = 'views/brand-index.html';
	$scope.data.brandAccordionUrl = 'views/brand-index-accordion.html';

	$scope.data.sortkey = 'sell_amount';
	
	$scope.data.brandCategoryHash = {};
	$scope.data.selectedBrandCategories = {};
	
	$scope.any_pager = {cur:1, max:1};
	
	$http.get(brandUrl)
		.success(function (data) {
			$scope.data.brands = data;
		})

	$scope.setBrandCategory = function(category) {
		$scope.data.brandCategory = category;
		$scope.data.brandBodyUrl = 'views/brand-category.html';
	}
	
	$scope.setBrand = function(brand_id) {
		if(!$scope.data.brandCategoryHash[brand_id])
		{
			sbrandCategory = {'0000':{'全部查看':0}};
			for(i = 0; i < $scope.data.product_all.length; i++)
			{
				product = $scope.data.product_all[i];
				if(product.brand_id == brand_id)
				{
					sbrandCategory['0000']['全部查看']++;
					if(sbrandCategory[product.category])
					{
						sbrandCategory[product.category][product.category_title]++;
					} else {
						item = {};
						item[product.category_title] = 1;
						sbrandCategory[product.category] = item;
					}
				}
			}
			
			$scope.data.brandCategoryHash[brand_id] = sbrandCategory;
		}
		
		$scope.data.brand = brand_id;
		$scope.setSelectBrandCategory('0000');
		
		$scope.data.selectedBrandCategories = $scope.data.brandCategoryHash[brand_id];
		$scope.data.brandAccordionUrl = 'views/brand-category-accordion.html';		
		$scope.data.brandBodyUrl = 'views/product-brand-category.html';
	}
	
	$scope.setSelectBrandCategory = function(category) {
		$scope.data.category = '';
		if(category != '0000')
			$scope.data.category = category;
	}
});
