function  ajaxFunc(method, url, tagId, jsData){
    $.ajax({
        type: method,
        url: url,
        data: jsData,
        
        //dataType: "json",
        async: true,
        cache: false,
        success: function (msg) {
            $(tagId).html(msg);
        },
        error: function (x, e) {
            alert("The call to the server side failed. " + x.responseText);
        }
    });
}

function addValidation(formID, tagID, errorID, actionName, baseurl)
{
    
    $(formID).validateDelegate(tagID, actionName, function(event) {
         if(event.keyCode > 36 && event.keyCode < 41) return;
         //alert(event.keyCode);
         if($(tagID).attr("value", $(tagID).attr("value")).valid())
            $(errorID).html("<img src='"+ baseurl +"/images/success.jpg'>");
         else
            $(errorID).html("<img src='"+ baseurl +"/images/warnning.png'>");
            
    });
}

function isValid(tagID, errorID, baseurl)
{
     if($(tagID).attr("value", $(tagID).attr("value")).valid())
        $(errorID).html("<img src='"+ baseurl +"/images/success.jpg'>");
     else
        $(errorID).html("<img src='"+ baseurl +"/images/warnning.png'>");
    
    return $(tagID).attr("value", $(tagID).attr("value")).valid();
}

function uploadFile(tagID, actionUrl, baseUrl)
{
	new AjaxUpload($(tagID), 
	{
		action: actionUrl,
		data: {                                         
			route: baseUrl,
		},
		name: 'uploadfile',
		onChange: function (file, ext){
			
		},
		onComplete: function(file, ext){
			imgSrc = baseUrl+"/images/uploads/"+file;
			editor.insertHtml('<img src="'+ imgSrc +'">');
		}
	}); 
}