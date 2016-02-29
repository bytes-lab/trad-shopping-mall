angular.module("shoppingMallApp", ["cart"])
.constant("categoryUrl", "/First/shopping_mall/product_category")
.constant("specProductUrl", "/First/shopping_mall/spec_products/")
.constant("productAllUrl", "/First/shopping_mall/product_all")
.constant("productListPageCount", 8)
.constant("productListRowCount", 4)
.controller("shoppingMallCtrl", function ($scope, $http, categoryUrl, specProductUrl, productAllUrl, productListPageCount, productListRowCount, cart) {
	$scope.data = {"product_all": []};
	
	// for general search
	$scope.data.search_key = '';	
	$scope.data.category = '';
	$scope.data.brand = '';
	
	// Urls for sub views 
	$scope.data.mainUrl = "views/index.html";
	$scope.data.tabBodyUrl = "views/home-special-tab.html";
	$scope.data.rightViewUrl = "views/home-products.html";
	
	// pagination for any page
	$scope.data.pageSize = productListPageCount;	
	$scope.any_pager = {cur:1, max:1};
	
	$scope.hp_page_size = 4;
	$scope.hp_pager = [{cur:1, max:1},{cur:1, max:1},{cur:1, max:1},{cur:1, max:1}];
	
	// for compare box
	$scope.data.compareBox = [];
	
	$http.get(categoryUrl)
		.success(function (data) {
			$scope.data.categories = data;
		})
		.error(function (error) {
			$scope.data.error = error;
		});

	$http.get(specProductUrl+'1')
		.success(function (data) {
			$scope.data.home_products = data;
		})

	$http.get(productAllUrl)
		.success(function (data) {
			$scope.data.product_all = data;
		})
		
	$scope.getAccordId = function(index){
		return '#collapse' + index;
	}
	
	$scope.getIndexUrl = function(){
		return $scope.data.rightViewUrl;
	}
	
	$scope.categoryFilterFn = function (product) {
		return ($scope.data.category == '' || product.category == $scope.data.category) && 
				($scope.data.search_key == '' || product.name.indexOf($scope.data.search_key) >= 0) && 
				($scope.data.brand == '' || product.brand_id == $scope.data.brand);
	}
	
	$scope.selectPage = function (pager, newPage) {
		pager.cur = newPage;
	}
	
	$scope.getPageClass = function (pager, page, d_class) {
		if(!d_class) 
			d_class = "btn-primary";
		return pager.cur == page ? d_class : "";
	}	
	
	$scope.setCategory = function (category) {
		if($scope.data.category != category)
		{
			$scope.data.category = category;
			$scope.data.rightViewUrl = "views/category-products.html";
			$scope.any_pager.cur = 1;		
		}
	}
	
	$scope.showPagination = function(data, pagesize, pager) {
		extra = data.length;
		var num = 0;
		for(i = 0; i < data.length; i++)
			if($scope.categoryFilterFn(data[i]))
				num++;
		pager.max = Math.ceil(num / pagesize);				
		return pager.max > 1;
	}
	
	$scope.prevPage = function(pager) {
		if(pager.cur > 1)
			pager.cur--;
	}

	$scope.nextPage = function(pager) {
		if(pager.cur < pager.max)
			pager.cur++;
	}	
	
	$scope.getPages = function(pager) {
		var result = [];
		start_page = Math.max(pager.cur-2, 1);
		end_page = Math.min(pager.max, start_page+4);
		if(end_page - start_page < 4)
			start_page = Math.max(end_page - 4, 1);
			
		for (var i = start_page; i <= end_page ; i++) {
			result.push(i);
		}
		return result;
	}
	
	$scope.viewProductDetail = function(product) {
		$scope.data.mainUrl = "views/index.html";	
		$scope.data.tabBodyUrl = "views/home-special-tab.html";		
		$scope.data.rightViewUrl = "views/product-detail.html";
		$scope.data.selectedProduct = product;
		
		result = product.upload_check.split(',');
		result.splice(0, 2);
		$scope.data.uploadCheck = result;
	}
	
	$scope.viewLoaded = function() {
		App.init();
		if($scope.data.rightViewUrl == "views/product-detail.html")
			Charts.initPieCharts([{label:'好评', data:32},{label:'中评', data:52},{label:'差评', data:26}]);
		// var element = angular.element(cat_product);  @@jks
		// imgs = element.find("div");
		// alert(imgs.length);				
	}
	
	$scope.addProductToCart = function (product) {
		cart.addProduct(product.id, product.name, product.price_now);
	}	

	$scope.setIndex = function(item, index) {
		item["t_index"] = index;
		return '';
	}
	
	$scope.homePage = function() {
		$scope.data.tabBodyUrl = 'views/home-special-tab.html';
		$scope.data.rightViewUrl = 'views/home-products.html';
		$scope.data.category = '';
		$scope.data.brand = '';
	}
	
	$scope.specialPage = function() {
		$scope.data.tabBodyUrl = 'views/home-special-tab.html';
		$scope.data.rightViewUrl = 'views/special-products.html';
		$scope.data.category = '';
		$scope.data.brand = '';
	}	
	
	$scope.brandPage = function() {
		$scope.data.tabBodyUrl = 'views/brand.html';
	}
	
	$scope.addProductToCompare = function(item) {
        angular.element(compare).css('display','block');
		
        for(i = 0; i < $scope.data.compareBox.length; i++) 
			if($scope.data.compareBox[i].id == item.id) 
				break;
		
		if(i != $scope.data.compareBox.length)
		{
            alert("对不起，您已经选择此商品！");
            return;
		}
		
		if($scope.data.compareBox.length < 3){
			$scope.data.compareBox.push(item);
			$scope.buildCompareDialog();
		}else{
			alert("对不起，最多可以选择三种商品进行对比！");
		}			
	}
	
	$scope.buildCompareDialog = function() {
		$("#comProlist").empty();
		for(i = 0; i < $scope.data.compareBox.length; i++)
		{
			item = $scope.data.compareBox[i];
			str = "<li id='check_" + item.id + "'>" + item.name + "</li>";
			$("#comProlist").append(str);	
		}
	}
	
    $scope.openCompare = function() {
		if($scope.data.compareBox.length < 2)
		{
			alert("对不起，最少选择两种商品进行对比！");
			return;
		}
		
		$scope.data.mainUrl = "views/compare.html";
    }
	
	$scope.clearCompareBox = function() {
		$scope.data.compareBox = [];
		$("#comProlist").empty();
		$("#compare").hide();		
	}
	
	$scope.backToIndex = function() {
		$scope.data.mainUrl = "views/index.html";
	}
});