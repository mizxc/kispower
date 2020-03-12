function postDataToUrl(postData, url) {
    $("#div-loading").addClass('d-block')
    $.ajax({
        type: "POST",
        url: url,
        data:postData,
        success: function (ret) { //ret={'status':true,'info':'.....'}
            alert(ret.info)
            $("#div-loading").removeClass('d-block')
        },
        error:function () {
            alert('提交数据服务出错了，请联系开发人员!')
        }
    });
}