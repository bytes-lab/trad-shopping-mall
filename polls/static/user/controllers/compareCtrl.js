angular.module("shoppingMallApp")
.controller("compareCtrl", function ($scope) {
	$scope.data.main_option = [["商品名称", "name"], ["商品图片", "id"], ["商城价", "price_now"], ["产品毛重", "weight"], ["产地", "origin_place"], ["品牌", "brand"]];
});
