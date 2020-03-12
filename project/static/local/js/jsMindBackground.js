var MINDDATA = {}
var JM

//init data
var kClassId = $("#jsmind_container").attr('kClassId')
$("#div-loading").addClass('d-block')
$.ajax({
    type: "get",
    url: '/kadmin/kispowerGetMindData/' + kClassId,
    success: function (ret) {
        if (ret.status) {
            MINDDATA = ret.data;
            jm_creatMind();
            setVersionSaveTime(MINDDATA['meta']['version'], MINDDATA['meta']['saveTime'])
            $("#div-loading").removeClass('d-block')
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
        editable: true,
        mode: mode,           // 显示模式
        view: {
            engine: 'svg',   // 思维导图各节点之间线条的绘制引擎
            line_width: 2.5,       // 思维导图线条的粗细
            line_color: lineColor   // 思维导图线条的颜色
        },
        shortcut: {
            enable: true,
            handles: {
                'handle_editnode' : function(jm,e){
                    jm_editNode()
                },
                'handle_moveUp' : function(jm,e){
                    jm_nodeUpOrDown('nodeUp')
                },
                'handle_moveDown' : function(jm,e){
                    jm_nodeUpOrDown('nodeDown')
                },
                'handle_saveData' : function(jm,e){
                    jm_saveData()
                },
                'handle_expand1' : function(jm,e){
                    jm_expand1()
                },
                'handle_expand2' : function(jm,e){
                    jm_expand2()
                },
                'handle_expand3' : function(jm,e){
                    jm_expand3()
                },
                'handle_expand4' : function(jm,e){
                    jm_expand4()
                },
                'handle_expand5' : function(jm,e){
                    jm_expand5()
                },
                'handle_expand6' : function(jm,e){
                    jm_expand6()
                },
                'handle_zoomIn' : function(jm,e){
                    jm_setZoom('zoom-in')
                },
                'handle_zoomOut' : function(jm,e){
                    jm_setZoom('zoom-out')
                },
            },
            mapping: {
                addchild: 70, // F
                addbrother: 68, // D
                handle_editnode: 69,// E
                delnode: 46, // Delete
                toggle: 32, // Space
                left: 37, // Left
                up: 38, // Up
                right: 39, // Right
                down: 40, // Down
                handle_moveUp: 87,// W node move up
                handle_moveDown: 83,// S node move down
                //全局快捷键
                handle_saveData: jsMind.key.alt + 83, //alt+S
                //handle_displayRight: jsMind.key.alt + 82, //alt+r
                //handle_displayFull: jsMind.key.alt + 70, //alt+f
                handle_expand1: jsMind.key.alt + 49, //alt+1
                handle_expand2: jsMind.key.alt + 50, //alt+2
                handle_expand3: jsMind.key.alt + 51, //alt+3
                handle_expand4: jsMind.key.alt + 52, //alt+4
                handle_expand5: jsMind.key.alt + 53, //alt+5
                handle_expand6: jsMind.key.alt + 54, //alt+6
                handle_zoomIn: jsMind.key.alt + 73, //alt+i
                handle_zoomOut: jsMind.key.alt + 79, //alt+o
            }
        },
        default_event_handle: {
            enable_dblclick_handle: true,
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

//set text:version,savetime
var setVersionSaveTime = function (version, saveTime) {
    $("#versionSaveTime").text('v' + version + ' / ' + saveTime)
}

//add node
var jm_addNode = function (key, e) {
    if (key.indexOf("children") != -1) {
        JM.shortcut.handles['addchild'](JM, e);
    } else if (key.indexOf("brother") != -1) {
        JM.shortcut.handles['addbrother'](JM, e);
    }
}
//添加节点时,一级节点随机颜色，二级以上节点固定颜色颜色
var jm_getNodeColor = function (addType) {
    node = JM.get_selected_node()
    if(addType=='child'){
        if(node.id=='root'){
            return getRandomColor()
        }else{
            //return [node.data['background-color'],node.data['foreground-color']]
            return ['#f0f0f4','#000000']
        }
    }else{
        if(node.parent.id=='root'){
            return getRandomColor()
        }else{
            //return [node.parent.data['background-color'],node.parent.data['foreground-color']]
            return ['#f0f0f4','#000000']
        }
    }

}

//edit node title
var jm_editNode = function () {
    // set val empty
    $("#ordinaryTextTitle").val('')
    $(".simditor-body").html('')
    $("#edit-title-Modal").modal('show');
    var currentNode = JM.get_selected_node()
    if (currentNode.data.topicType == 'ordinary') {
        $("#selectTextType").val('ordinary')
        var title = currentNode.topic.replace('<div class="ordinary-title">', '').replace('</div>', '')
        if(title=='New Node'){
            title = ''
        }
        $("#ordinaryTextTitle").val(title)
        $("#objOrdinaryText").removeClass('d-none')
        $("#objRichText").addClass('d-none')
        var t = $('#ordinaryTextTitle').val();
        setTimeout(function () {
            if(t==''){
                $('#ordinaryTextTitle').focus();
            }else{
                $('#ordinaryTextTitle').val("").focus().val(t);
            }
        }, 700);
    } else if (currentNode.data.topicType == 'rich') {
        $("#selectTextType").val('rich')
        var title = currentNode.topic.replace('<div class="rich-title">', '').replace('</div>', '')
        $(".simditor-body").html(title)
        $("#objRichText").removeClass('d-none')
        $("#objOrdinaryText").addClass('d-none')
    }

}
$('#ordinaryTextTitle').bind('keypress', function (event) {
    if (event.keyCode == "13") {
        jm_setTitle()
    }
});
$("#postEditTitle").on('click', function () {
    jm_setTitle()
});
var jm_setTitle = function () {
    var currentNode = JM.get_selected_node()
    var textType = $('#selectTextType').val();
    if (textType == 'ordinary') {
        var title = $("#ordinaryTextTitle").val().trim();
        if (typeof title == "undefined" || title == null || title == "") {
            alert('请输入普通标题内容')
        } else {
            if (title.indexOf('class="ordinary-title"') == -1) {
                title = '<div class="ordinary-title">' + title + '</div>'
            }
            JM.update_node(currentNode.id, title)
            currentNode.data.topicType = 'ordinary'
            JM.update_node(currentNode)
            $("#edit-title-Modal").modal('hide');
        }
    } else if (textType == 'rich') {
        var title = $(".simditor-body").html();
        if (typeof title == "undefined" || title == null || title == "") {
            alert('请输入富文本标题内容')
        } else {
            if (title.indexOf('class="rich-title"') == -1) {
                title = '<div class="rich-title">' + title + '</div>'
            }
            var currentNode = JM.get_selected_node()
            JM.update_node(currentNode.id, title)
            currentNode.data.topicType = 'rich'
            JM.update_node(currentNode)
            $("#edit-title-Modal").modal('hide');
        }
    }
    JM.select_node(currentNode);
}

// delete node
var jm_deleteNode = function () {
    var currentNode = JM.get_selected_node()
    if (currentNode.isroot) {
        alert('根节点不能删除')
    } else {
        if (confirm('确定要删除该节点吗，没有后悔功能哦') == true) {
            JM.remove_node(currentNode)
        }
    }
}

//set node color
var COLORDIC = {
    '精白': ['#ffffff', '#000000'],
    '铅白': ['#f0f0f4', '#000000'],
    '雪白': ['#f0fcff', '#000000'],
    '月白': ['#d6ecf0', '#000000'],
    '象牙白': ['#fffbf0', '#000000'],
    '青白': ['#c0ebd7', '#000000'],
    '灰色': ['#808080', '#000000'],
    '黝': ['#6b6882', '#ffffff'],
    '玄青': ['#3d3b4f', '#ffffff'],
    '黧': ['#5d513c', '#ffffff'],
    '缁色': ['#493131', '#ffffff'],
    '漆黑': ['#161823', '#ffffff'],
    '黑色': ['#000000', '#ffffff'],
    '鹅黄': ['#fff143', '#000000'],
    '橙黄': ['#ffa400', '#000000'],
    '橘红': ['#ff7500', '#000000'],
    '秋香色': ['#d9b611', '#000000'],
    '枯黄': ['#d3b17d', '#000000'],
    '茶色': ['#b35c44', '#ffffff'],
    '豆青': ['#96ce54', '#000000'],
    '油绿': ['#00bc12', '#ffffff'],
    '松花绿': ['#057748', '#ffffff'],
    '铜绿': ['#549688', '#000000'],
    '竹青': ['#789262', '#000000'],
    '粉红': ['#ffb3a7', '#000000'],
    '桃红': ['#f47983', '#000000'],
    '樱桃红': ['#c93756', '#ffffff'],
    '洋红': ['#ff4777', '#000000'],
    '品红': ['#f00056', '#ffffff'],
    '大红': ['#ff2121', '#ffffff'],
    '胭脂': ['#9d2933', '#ffffff'],
    '栗色': ['#60281e', '#ffffff'],
    '蔚蓝': ['#70f3ff', '#000000'],
    '蓝色': ['#44cef6', '#000000'],
    '靛蓝': ['#065279', '#ffffff'],
    '宝蓝': ['#4b5cc4', '#ffffff'],
    '藏蓝': ['#3b2e7e', '#ffffff'],
    '黛紫': ['#574266', '#ffffff'],
    '紫色': ['#8d4bbb', '#ffffff'],
    '酱紫': ['#815476', '#ffffff'],
    '紫棠': ['#56004f', '#ffffff'],
    '丁香': ['#cca4e3', '#000000'],
    '藕色': ['#edd1d8', '#000000']
};
var getRandomColor = function () {
    var newObj = {}, total = 0;
    for (var key in COLORDIC) {
        if (COLORDIC.hasOwnProperty(key)) {
            newObj[total++] = key;
        }
    }
    var _index = ~~(Math.random() * total);
    var randomVal = COLORDIC[newObj[_index]]
    return randomVal
}
var jm_creatMenuColorItems = function (useFor) {
    var items = {}
    var i = 1
    var keyword = ''
    if (useFor == 'node') {
        keyword = 'color-node-'
    } else if (useFor == 'system-bk') {
        keyword = 'color-system-bk-'
    } else if (useFor == 'system-line') {
        keyword = 'color-system-line-'
    }
    for (var key in COLORDIC) {
        items[keyword + key] = {name: key, icon: 'fa-color-' + i}
        i = i + 1
    }
    return items
}
var jm_creatMenuColorCss = function () {
    var i = 1
    for (var key in COLORDIC) {
        var str = '.fa-color-' + i + '{background-color:' + COLORDIC[key][0] + ';}'
        console.log(str);
        i = i + 1
    }
}
var jm_setNodeColor = function (key) {
    var color = COLORDIC[key.split('-')[2]]
    var currentNode = JM.get_selected_node()
    JM.set_node_color(currentNode.id, color[0], color[1])
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
//expand全局
var jm_expand1 = function () {
    JM.collapse_all();
}
var jm_expand2 = function () {
    JM.expand_to_depth(2);
}
var jm_expand3 = function () {
    JM.expand_to_depth(3);
}
var jm_expand4 = function () {
    JM.expand_to_depth(4);
}
var jm_expand5 = function () {
    JM.expand_to_depth(5);
}
var jm_expand6 = function () {
    JM.expand_to_depth(6);
}


//node up/down
var jm_getAdjacentNodeId = function (node, beforeOrafter) {
    var parent = node.parent
    if (parent.id == 'root' && JM.get_meta().displayMode == 'full') {
        alert('在两边显示模式下，一级节点暂不支持上下移动，如要移动请切换到：右边显示模式')
        return null
    }
    if (parent) {
        var children = parent.children
        for (var i = 0; i < children.length; i++) {
            if (node.id == children[i].id) {
                if (beforeOrafter == 'before') {
                    if (i == 0) {
                        return null
                    } else {
                        return children[i - 1].id
                    }
                } else if (beforeOrafter == 'after') {
                    if (i + 1 == children.length) {
                        return null
                    } else {
                        return children[i + 1].id
                    }
                }
            }
        }
    } else {
        return null
    }
}
var jm_nodeUpOrDown = function (key) {
    var currentNode = JM.get_selected_node()
    if (key == 'nodeUp') {
        deforeNodeId = jm_getAdjacentNodeId(currentNode, 'before')
        if (deforeNodeId) {
            JM.move_node(currentNode, deforeNodeId)
        }
    } else if (key == 'nodeDown') {
        afterNodeId = jm_getAdjacentNodeId(currentNode, 'after')
        if (afterNodeId) {
            JM.move_node(afterNodeId, currentNode.id)
        }
    }
    JM.select_node(currentNode)
}

//set zoom
var jm_setZoom = function (key) {
    if (key.indexOf("in") != -1) {
        JM.view.zoomIn()
    } else if (key.indexOf("out") != -1) {
        JM.view.zoomOut()
    }
}

//set background color
var jm_setBackgroundColor = function (key) {
    var color = COLORDIC[key.split('-')[3]]
    JM.mind.backgroundColor = color[0]
    jm_reloadPage()
}

//set line color
var jm_setLineColor = function (key) {
    var color = COLORDIC[key.split('-')[3]]
    JM.mind.lineColor = color[0]
    jm_reloadPage()
}

//set display mode
var jm_setDisplayMode = function (key) {
    var mode = key.split('-')[2]
    if (mode != JM.options.mode) {
        if (mode == 'full') {
            JM.mind.displayMode = 'full'
        } else if (mode == 'side') {
            JM.mind.displayMode = 'side'
        }
        jm_reloadPage()
    }
}

//reload page
var jm_reloadPage = function () {
    var data = JM.get_data()
    $.ajax({
        url: '/kadmin/kispowerPostMindData/' + kClassId,
        type: 'POST',
        data: {"data": JSON.stringify(data), "action": 'reload'},
        success: function (ret) {
            if (ret.status) {
                window.location.href = "/kadmin/kispowerKClassShow/" + kClassId;
            } else {
                alert(ret.msg)
            }
        },
        error: function () {
            alert('请求数据失联了！');
        },
    });
}

//save data
$("#kLabel").on("click", function () {
    jm_saveData()
})
// save data / 60s
window.setInterval(function() {
    jm_saveData()
},1000*60)
var jm_saveData = function () {
    $("#div-loading").addClass('d-block')
    var data = JM.get_data()
    $.ajax({
        url: '/kadmin/kispowerPostMindData/' + kClassId,
        type: 'POST',
        data: {"data": JSON.stringify(data), "action": 'save'},
        success: function (ret) {
            $("#div-loading").removeClass('d-block')
            if(ret.hasOwnProperty('data')){
                $("#versionSaveTime").text(ret.data)
                $("#versionSaveTime").css('color',getRandomColor()[0])
            }
        },
        error: function () {
            alert('请求数据失联了！');
        },
    });
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
$('#exportNodeFileName').bind('keypress', function (event) {
    if (event.keyCode == "13") {
        jm_exportNodeDo()
    }
});
$("#postExportNodeFileName").on("click", function () {
    jm_exportNodeDo()
});
var jm_exportNodeDo = function () {
    var fileName = $("#exportNodeFileName").val()
    if (typeof fileName == "undefined" || fileName == null || fileName == "") {
        alert('请输入文件名')
    } else {
        var currentNode = JM.get_selected_node()
        var nodeData = JM.get_nodeData(currentNode)
        var meta = JM.get_meta()
        var exportData = {
            "meta": {
                "name": fileName,
                "author": meta.author,
                "version": meta.version,
                "website": window.location.href.split('/')[2]
            },
            "format": "node_tree",
            "data": nodeData
        }
        var mindStr = jsMind.util.json.json2string(exportData);
        jsMind.util.file.save(mindStr, 'text/jsmind', fileName + '.kispower');
        $("#export-node-Modal").modal('hide');
        $("#exportNodeFileName").val('')
    }
}
var jm_importNode = function () {
    $("#import-node-Modal").modal('show');
}
$("#postImportNodeFile").on("click", function () {
    var tempThis = $(this)
    tempThis.addClass('d-none')
    var fileInput = document.getElementById('importFile');
    var files = fileInput.files;
    if (files.length > 0) {
        var fileData = files[0];
        jsMind.util.file.read(fileData, function (jsmind_data, jsmind_name) {
            var mind = jsMind.util.json.string2json(jsmind_data);
            if (!!mind) {
                alert('节点知识：' + mind.meta.name + '，版本号：' + mind.meta.version + '，来自：' + mind.meta.author + '_' + mind.meta.website + '的知识分享')
                nodeData = mind.data;
                var currentNode = JM.get_selected_node()
                var allData = JM.get_data()
                var postData = {
                    "allData": allData,
                    "currentNodeId": currentNode.id,
                    "importNode": nodeData
                }
                $.ajax({
                    url: '/kadmin/kispowerPostMindData/' + kClassId,
                    type: 'POST',
                    data: {"data": JSON.stringify(postData), "action": 'import'},
                    success: function (ret) {
                        if (ret.status) {
                            alert(ret.msg)
                            $("#import-node-Modal").modal('hide');
                            window.location.href = "/kadmin/kispowerKClassShow/" + kClassId;
                        }
                        tempThis.removeClass('d-none')
                    },
                    error: function () {
                        alert('请求数据失联了！');
                        tempThis.removeClass('d-none')
                    },
                });
            } else {
                alert('文件内容有误，请导入.kispower文件');
                tempThis.removeClass('d-none')
            }
        });
    } else {
        alert('请选择文件')
        tempThis.removeClass('d-none')
    }
});
var jm_shareNode = function () {
    $("#share-node-Modal").modal('show');
    //获取是否已经分享过
    var currentNode = JM.get_selected_node()
    $.ajax({
        url: '/kadmin/kispowerGetIsSharedNode',
        type: 'POST',
        data: {"kClassId": kClassId, "nodeId": currentNode.id},
        success: function (ret) {
            if (ret.status) {
                $("#shareTitle").val(ret.data.title);
                $("#shareTag").val(ret.data.tag);
                $("#shareMode").val(ret.data.mode);
                $("#shareIntroduction").val(ret.data.introduction);
            } else {
                $("#shareTitle").val('');
                $("#shareTag").val('');
                $("#shareIntroduction").val('');
            }
        },
        error: function () {
            alert('请求数据失联了！');
        },
    });
}
$("#postShareNode").on("click", function () {
    var tempThis = $(this)
    tempThis.addClass('d-none')
    var shareTitle = $("#shareTitle").val()
    var shareTag = $("#shareTag").val()
    var shareMode = $("#shareMode").val()
    var shareIntroduction = $("#shareIntroduction").val()
    if (typeof shareTitle == "undefined" || shareTitle == null || shareTitle == "") {
        alert('请输入标题')
        tempThis.removeClass('d-none')
    }
    if (typeof shareTag == "undefined" || shareTag == null || shareTag == "") {
        alert('请输入标签')
        tempThis.removeClass('d-none')
    } else if (typeof shareIntroduction == "undefined" || shareIntroduction == null || shareIntroduction == "") {
        alert('请输入简介')
        tempThis.removeClass('d-none')
    } else {
        var currentNode = JM.get_selected_node()
        var nodeData = JM.get_nodeData(currentNode)
        var meta = JM.get_meta()
        meta.name = shareTitle
        var shareData = {
            "meta": meta,
            "format": "node_tree",
            "data": nodeData
        }
        $("#div-loading").addClass('d-block')
        $.ajax({
            url: '/kadmin/kispowerPostShareData/' + kClassId,
            type: 'POST',
            data: {
                "shareData": JSON.stringify(shareData),
                "shareTitle": shareTitle,
                "shareTag": shareTag,
                "shareMode":shareMode,
                "shareIntroduction": shareIntroduction
            },
            success: function (ret) {
                alert(ret.msg)
                tempThis.removeClass('d-none')
                if (ret.status) {
                    $("#share-node-Modal").modal('hide');
                    $("#shareTitle").val('');
                    $("#shareTag").val('');
                    $("#shareIntroduction").val('');
                    $("#div-loading").removeClass('d-block')
                }
            },
            error: function () {
                alert('请求数据失联了！');
                tempThis.removeClass('d-none')
            },
        });
    }
});

//move
// var drag = $('#jsmind_container');
// var moveMark = 0;
// var mouseX = 0;
// var mouseY = 0;
// drag.mousedown(function(e){
//     if(e.target.localName == 'jmnodes'){
//         moveMark = 1
//         mouseX = e.pageX
//         mouseY = e.pageY
//     }
// })
// drag.mousemove(function(e){
//     if(moveMark == 1){
//         //$('body,html').animate({'scrollTop':0},'slow')
//         var x = e.pageX-mouseX
//         var y = e.pageY-mouseY
//         //$('html,body').animate({scrollTop:y},'slow');
//         //$('html,body').animate({scrollLeft:x},'slow');
//         mouseX = e.pageX
//         mouseY = e.pageY
//     }
// })
// drag.mouseup(function(e){
//     moveMark = 0
//     mouseX = 0
//     mouseY = 0
// })


