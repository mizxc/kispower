$.contextMenu({
    selector: 'jmnodes',
    autoHide: false,
    className: 'css-title-jmnodes',
    callback: function (key, options) {
        if (key == 'screenshot') {
            jm_screenshot();
        } else if (key == 'expand3') {
            jm_expand3();
        } else if (key == 'expand4') {
            jm_expand4();
        } else if (key == 'expandAll') {
            jm_expandAll();
        } else if (key == 'collapseAll') {
            jm_collapseAll();
        } else if (key.indexOf("zoom") != -1) {
            jm_setZoom(key);
        }
    },
    items: {
        "screenshot": {name: "屏幕截图", icon: "fa-desktop"},
        "sep1": "---------",
        "expandCollapse": {
            name: "展开&收起", icon: "fa-hand-spock-o", "items": {
                "expandAll": {name: "全部展开", icon: "fa-hand-paper-o"},
                "collapseAll": {name: "全部收起", icon: "fa-hand-grab-o"},
                "expand3": {name: "展开3级", icon: "fa-hand-paper-o"},
                "expand4": {name: "展开4级", icon: "fa-hand-paper-o"},
            }
        },
        "zoom": {
            name: "缩放", icon: "fa-exchange", "items": {
                "zoom-in": {name: "放大", icon: "fa-search-plus"},
                "zoom-out": {name: "缩小", icon: "fa-search-minus"},
            }
        },
        "sep2": "---------",
        "quit": {
            name: "退出", icon: function () {
                return 'context-menu-icon context-menu-icon-quit';
            }
        }
    }
});

$.contextMenu({
    selector: 'jmnode',
    autoHide: false,
    className: 'css-title-jmnode',
    callback: function (key, options) {
        //rich文本获取不到节点/右键菜单的节点不与当前选择的节点一样
        var nodeId = $(options.$trigger.parents('jmnode').prevObject[0]).attr('nodeid');
        if(!JM.get_selected_node() || JM.get_selected_node().id!=nodeId){
            JM.select_node(nodeId);
        }
        if(key == 'expandNode'){
            jm_expandNode();
        }else if(key == 'collapseNode'){
            jm_collapseNode();
        }else if(key == 'export'){
            jm_exportNode();
        }
    },
    items: {
        "expandNode": {name: "展开节点", icon: "fa-hand-paper-o"},
        "collapseNode": {name: "收起节点", icon: "fa-hand-grab-o"},
        "sep1": "---------",
        "export": {name: "导出节点知识", icon: "fa-arrow-down"},
        "sep2": "---------",
        "quit": {
            name: "退出", icon: function () {
                return 'context-menu-icon context-menu-icon-quit';
            }
        }
    }
});
