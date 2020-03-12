var MINDDATA = {}
var JM

//init data
var kClassId = $("#jsmind_container").attr('kClassId')
$.ajax({
    type: "get",
    url: '/kispowerGetKShareData/' + kClassId,
    success: function (ret) {
        if (ret.status) {
            MINDDATA = ret.data;
            jm_creatMind();
            var url = location.href.split('/')
            setShareTitle(MINDDATA['meta']['name'])
        } else {
            alert(ret.msg)
        }
    },
    error: function () {
        alert('请求数据失联了！');
    },
});

//creat node
var setOptions = function (mode, lineColor) {
    var options = {
        container: 'jsmind_container',
        theme: 'clouds',
        editable: false,
        mode: mode,           // 显示模式
        view: {
            engine: 'svg',   // 思维导图各节点之间线条的绘制引擎
            line_width: 3,       // 思维导图线条的粗细
            line_color: lineColor   // 思维导图线条的颜色
        },
        shortcut: {
            enable: false,        // 是否启用快捷键
        },
        default_event_handle: {
            enable_dblclick_handle: false,
        },
    };
    return options;
}
var jm_creatMind = function () {
    $("#jsmind_container").height($(window).height());
    $("#jsmind_container").width($(window).width());
    $("#jsmind_container").css('background-color', MINDDATA['meta']['backgroundColor']);
    var options = setOptions(MINDDATA['meta']['displayMode'], MINDDATA['meta']['lineColor']);
    JM = new jsMind(options);
    JM.show(MINDDATA);
}

//set title
var setShareTitle = function (name) {
    $("#shareTitle").text(name)
    $("title").text(name)
}

//expand/collapse
var jm_expandNode = function () {
    var currentNode = JM.get_selected_node()
    JM.expand_node(currentNode.id);
}
var jm_collapseNode = function () {
    var currentNode = JM.get_selected_node()
    JM.collapse_node(currentNode.id);
}
var jm_expand3 = function () {
    JM.expand_to_depth(2);
}
var jm_expand4 = function () {
    JM.expand_to_depth(3);
}
var jm_expandAll = function () {
    JM.expand_all();
}
var jm_collapseAll = function () {
    JM.collapse_all();
}

//set zoom
var jm_setZoom = function (key) {
    if (key.indexOf("in") != -1) {
        JM.view.zoomIn()
    } else if (key.indexOf("out") != -1) {
        JM.view.zoomOut()
    }
}

//screenshot
var jm_screenshot = function () {
    alert('请使用谷歌浏览器，安装“Full Page Screen Capture”插件，实现全屏幕截图，安装参考教程http://www.kispower.cn/blogShow/5e45fa24fadb6730d6d332de')
    //JM.screenshot.shootDownload();
}

//share
var jm_exportNode = function () {
    $("#export-node-Modal").modal('show');
}
$("#postExportNodeFileName").on("click", function () {
    var fileName = $("#exportNodeFileName").val()
    if (typeof fileName == "undefined" || fileName == null || fileName == "") {
        alert('请输入文件名')
    }else{
        var currentNode = JM.get_selected_node()
        var nodeData = JM.get_nodeData(currentNode)
        var meta = JM.get_meta()
        var exportData = {
            "meta":{"name":fileName,"author":meta.author,"version":meta.version,"website":window.location.href.split('/')[2]},
            "format":"node_tree",
            "data":nodeData
        }
        var mindStr = jsMind.util.json.json2string(exportData);
        jsMind.util.file.save(mindStr,'text/jsmind',fileName+'.kispower');
        $("#export-node-Modal").modal('hide');
        $("#exportNodeFileName").val('')
    }
});
