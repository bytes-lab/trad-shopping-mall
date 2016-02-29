angular.module("shoppingMallApp")
.controller("specialProductCtrl", function ($scope, $http, specProductUrl) {
	$scope.data.sel_kind = 0;
	$http.get(specProductUrl+'4')
		.success(function (data) {
			$scope.data.special_products = data;
		})
	
});
