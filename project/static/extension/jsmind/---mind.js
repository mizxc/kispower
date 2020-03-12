(function($,$w){
    var CONTAINER_ID = 'jsmind_container';

    var $d = $w.document;
    var $container = $d.getElementById(CONTAINER_ID);

    var _h_header = $d.getElementsByTagName('nav')[0].clientHeight;

    var _jm = new jsMind({
            container:CONTAINER_ID,
            editable:true,
            theme:'asphalt'
    });

    var get_mind_id = function(){
        return location.href.match(/([a-zA-Z0-9]{32})(#.*)?$/)[1];
    };

    var get_mind_url = function(){
        return location.href.split('#')[0] + '.jm';
    };

    var load_ajax_mind = function(url){
        jsMind.util.ajax.get(url,function(mind){
            _jm.show(mind);
        });
    };

    var on_mind_saved = function(data){
        if(data.success){
            $('#save_map_btn').popover({
                delay: {'hide': 1000},
                content: '保存成功',
                placement: 'bottom',
                trigger: 'focus',
                container: 'body'
            }).popover('show');
        }
    };

    var on_mind_name_changed = function(data){
        if(data.success){
            var mind_name = $('#mind_name_input').val();
            $('#mind_name_link').text(mind_name);
        }
        toggle_edit_mind_name();
    };

    var on_mind_deleted = function(data){
        if(data.success){
            back_to_list();
        }
    };

    var toggle_edit_mind_name = function(e){
        $('#mind_name_link, #mind_name_edit_panel').toggleClass('hidden');
        return false;
    };

    var change_mind_name = function(e){
        var mind_id = get_mind_id();
        var origin_mind_name = $('#mind_name_link').text();
        var mind_name = $('#mind_name_input').val();
        if(origin_mind_name == mind_name){
            toggle_edit_mind_name();
            return false;
        }
        $.ajax({
            url : '/mind/rename',
            type : 'POST',
            data: {"mind-id":mind_id,"mind-name":mind_name},
            success : on_mind_name_changed
        });
        return false;
    };

    var save_map = function(e){
        $.ajax({
            url  : get_mind_url(),
            type : 'PUT',
            data: JSON.stringify(_jm.get_data()),
            contentType: "application/json; charset=utf-8",
            dataType   : "json",
            success : on_mind_saved
        });
        return false;
    };

    var add_sibling_node = function(e){
        _jm.shortcut.handles['addbrother'](_jm, e);
        return false;
    };

    var add_child_node = function(e){
        _jm.shortcut.handles['addchild'](_jm, e);
        return false;
    };

    var remove_node = function(e){
        _jm.shortcut.handles['delnode'](_jm, e);
        return false;
    };

    var clear_map = function(e){
        curr_mind = _jm.mind;
        _jm.show();
        _jm.mind.author = curr_mind.author;
        _jm.begin_edit(_jm.mind.root);
        return false;
    };

    var destory_map = function(e){
        $.ajax({
            url  : get_mind_url(),
            type : 'DELETE',
            contentType: "application/json; charset=utf-8",
            dataType   : "json",
            success : on_mind_deleted
        });
        return false;
    };

    var back_to_list = function(e){
        location.href='/mind/';
        return false;
    };

    var set_container_size = function(){
        var ch = $w.innerHeight-_h_header;
        var cw = $w.innerWidth;
        $container.style.height = ch+'px';
        $container.style.width = cw+'px';
    };

    var _resize_timeout_id = -1;
    var reset_container_size = function(){
        if(_resize_timeout_id != -1){
            clearTimeout(_resize_timeout_id);
        }
        _resize_timeout_id = setTimeout(function(){
            _resize_timeout_id = -1;
            set_container_size();
            _jm.resize();
        },300);
    };

    var register_event = function(){
        jsMind.util.dom.add_event($w,'resize',reset_container_size);
    };

    var init_action_menu = function(){
        $('#mind_name_link').click(toggle_edit_mind_name);
        $('#change_mind_name_btn').click(change_mind_name);
        $('#save_map_btn').click(save_map);
        $('#add_sibling_node_btn').click(add_sibling_node);
        $('#add_child_node_btn').click(add_child_node);
        $('#remove_node_btn').click(remove_node);
        $('#clear_map_btn').click(clear_map);
        $('#destory_map_btn').click(destory_map);
        $('#back_to_list_btn').click(back_to_list);
    };

    var page_load = function(){
        register_event();
        set_container_size();
        load_ajax_mind(get_mind_url());
        init_action_menu();
    };

    page_load();
})(jQuery,window);
