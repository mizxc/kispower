$.contextMenu({
    selector: 'jmnodes',
    autoHide: false,
    className: 'css-title-jmnodes',
    callback: function (key, options) {
        if (key == 'saveData') {
            jm_saveData();
        } else if (key == 'screenshot') {
            jm_screenshot();
        }else if (key == 'expand1') {
            jm_expand1();
        }else if (key == 'expand2') {
            jm_expand2();
        }else if (key == 'expand3') {
            jm_expand3();
        }else if (key == 'expand4') {
            jm_expand4();
        } else if (key == 'expand5') {
            jm_expand5();
        } else if (key == 'expand6') {
            jm_expand6();
        } else if (key.indexOf("zoom") != -1) {
            jm_setZoom(key);
        } else if (key.indexOf("system-display") != -1) {
            jm_setDisplayMode(key);
        } else if (key.indexOf("color-system-bk") != -1) {
            jm_setBackgroundColor(key);
        } else if (key.indexOf("color-system-line") != -1) {
            jm_setLineColor(key);
        }
    },
    items: {
        "saveData": {name: "保存数据", icon: "fa-save"},
        "screenshot": {name: "屏幕截图", icon: "fa-desktop"},
        "sep1": "---------",
        "system-display": {
            name: "显示模式", icon: "fa-play", "items": {
                "system-display-side": {name: "节点分布在右侧", icon: "fa-chevron-right"},
                "system-display-full": {name: "节点分布在两侧", icon: "fa-bars"},
            }
        },
        "system-bk": {name: "屏幕背景色", icon: "fa-square", "items": jm_creatMenuColorItems('system-bk')},
        "system-line": {name: "连接线颜色", icon: "fa-arrows-h", "items": jm_creatMenuColorItems('system-line')},
        "sep2": "---------",
        "expandCollapse": {
            name: "展开", icon: "fa-hand-spock-o", "items": {
                "expand1": {name: "展开1级", icon: "fa-hand-paper-o"},
                "expand2": {name: "展开2级", icon: "fa-hand-paper-o"},
                "expand3": {name: "展开3级", icon: "fa-hand-paper-o"},
                "expand4": {name: "展开4级", icon: "fa-hand-paper-o"},
                "expand5": {name: "展开5级", icon: "fa-hand-paper-o"},
                "expand6": {name: "展开6级", icon: "fa-hand-paper-o"},
            }
        },
        "zoom": {
            name: "缩放", icon: "fa-exchange", "items": {
                "zoom-in": {name: "放大", icon: "fa-search-plus"},
                "zoom-out": {name: "缩小", icon: "fa-search-minus"},
            }
        },
        "sep3": "---------",
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
        if (!JM.get_selected_node() || JM.get_selected_node().id != nodeId) {
            JM.select_node(nodeId);
        }
        if (key.indexOf("plus") != -1) {
            jm_addNode(key);
        } else if (key == 'edit') {
            jm_editNode();
        } else if (key.indexOf("color-node") != -1) {
            jm_setNodeColor(key);
        } else if (key == 'expandNode') {
            jm_expandNode();
        } else if (key == 'collapseNode') {
            jm_collapseNode();
        } else if (key == 'nodeUp') {
            jm_nodeUpOrDown(key);
        } else if (key == 'nodeDown') {
            jm_nodeUpOrDown(key);
        } else if (key == 'share') {
            jm_shareNode();
        } else if (key == 'export') {
            jm_exportNode();
        } else if (key == 'import') {
            jm_importNode();
        } else if (key == 'delete') {
            jm_deleteNode();
        }
    },
    items: {
        "plus-children": {name: "添加子节点", icon: "fa-plus"},
        "plus-brother": {name: "添加兄弟节点", icon: "fa-plus-circle"},
        "sep1": "---------",
        "edit": {name: "修改节点标题", icon: "fa-edit"},
        "color": {name: "修改节点颜色", icon: "fa-adjust", "items": jm_creatMenuColorItems('node')},
        "sep2": "---------",
        "expandNode": {name: "展开节点", icon: "fa-hand-paper-o"},
        "collapseNode": {name: "收起节点", icon: "fa-hand-grab-o"},
        "sep3": "---------",
        "nodeUp": {name: "节点上移", icon: "fa-arrow-up"},
        "nodeDown": {name: "节点下移", icon: "fa-arrow-down"},
        "sep4": "---------",
        "kShare": {
            name: "知识分享", icon: "fa-share-alt", "items": {
                "share": {name: "分享节点知识", icon: "fa-share"},
                "export": {name: "导出节点知识", icon: "fa-arrow-down"},
                "import": {name: "导入节点知识", icon: "fa-arrow-up"},
            }
        },
        "sep5": "---------",
        "delete": {name: "删除节点", icon: "fa-trash"},
        "quit": {
            name: "退出", icon: function () {
                return 'context-menu-icon context-menu-icon-quit';
            }
        }
    }
});
