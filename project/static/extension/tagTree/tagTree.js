///////////////////////////////////////////////
/// 树型标签
/// V 1.0
/// creat by lee
/// https://github.com/miracleren/tagTree
/// 20190529
/// 运行库 juqery
/// //////////////////////////////////////////


;(function($){

	var defaults ={
		id:"",
		data:[],
		fold:true,
		multiple:false,
		check:function(){},
		done:function(){}
	};

	$.fn.tagTree = function(options){
		var that = $(this);
		options.id = "#" + that.attr("id");
        var opts = $.extend(defaults, options);

        that.addClass("tagtree");
        setTree(defaults.data,that);

        $(defaults.id+' li:has(ul)').addClass('li-top');
        if(defaults.fold)
        	$(defaults.id+" .li-top li").hide('fast');
	    $(defaults.id+' li.li-top > span').on('click', function (e) {
	        var children = $(this).parent('li.li-top').find(' > ul > li');
	        if (children.is(":visible")) {
	            children.hide('fast');
	        } else {
	            children.show('fast');
	        }
	        return false;
	    });
	    $(defaults.id+' li span').hover(function() {
	    	if (!$(this).find('i').hasClass('i-check'))
	    		$(this).find('i').show(200);
	    }, function() {
	    	if (!$(this).find('i').hasClass('i-check'))
	    		$(this).find('i').hide(100);
	    });
	    $(defaults.id+' li span i').click(function(event) {
	    	if(!defaults.multiple)
	    	{
	    		$(defaults.id +" .i-check").removeClass('i-check').hide(100);
	    	}

	    	if($(this).hasClass('i-check'))
	    		$(this).removeClass('i-check');
	    	else
	    		$(this).addClass('i-check');
	    	defaults.check($(this).attr("data-val"));
	    	return false;
	    });

	    defaults.done();
	}

	$.fn.tagTreeValues =function(){
		var vals = [];
		$(defaults.id +" .i-check").each(function(index, el) {
			vals.push($(el).attr('data-val'));
		});
		return vals;
	}

	//递归生成树
	function setTree(data,that)
	{
		var ul = $('<ul></ul>');
		that.append(ul);
		$.each(data,function(index,value){
			var li = $('<li><span class="span-item" style="background-color:'+value['background-color']+';color:'+value['foreground-color']+'">'+value.topic+'<i data-val="'+value.value+'" class="fa fa-check" style="display:none;"></i></span></li>');
			ul.append(li);
		    if(value.hasOwnProperty("children") && value.children.length > 0)
		    {
		    	li.append('<div class="node-count">'+value.children.length+'</div>');
		    	setTree(value.children,li);
		    }
		});
	}
})(jQuery);