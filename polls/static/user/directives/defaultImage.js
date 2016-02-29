angular.module("shoppingMallApp")
.directive("defaultImage", function ($http) {
	return function (scope, element, attrs) {
		var url = attrs["src"];
		$http.get(url)
			.error(function (error) {
				element.attr("src", "/static/images/productImages/3_1_160.jpg");
			});
	}
})
