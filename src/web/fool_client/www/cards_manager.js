    string_presentation = ''
    bottom_array = Array(0)
    coverings = Array(0)
    top_array = Array(0)
    table = null
    player_cards = null
    dragging = false
    bottom_card = null
    top_card = null
    object_to_drag = null
    saved_cursor = null
    cover_delta_x = 14
    cover_delta_y = 17
function print(text) {
    document.getElementById('txt').innerHTML = text
}

function print0(text) {
    document.getElementById('txt').innerHTML += text
}

function put_to_player_cards(event){
    return coord_in(event.x, event.y, document.getElementById('empty2'))
}

function set_covering_position(bottom) {
    object_to_move.style.position = 'absolute'
    object_to_move.style.top = (getAbsoluteTop(bottom) + cover_delta_y) + 'px'
    object_to_move.style.left = (getAbsoluteLeft(bottom) + cover_delta_x) + 'px'
}

function put_to_table_cards(event) {
    return coord_in(event.x, event.y, document.getElementById('empty'))
}

function set_user_cards_position() {
    object_to_move.style.top = ''
    object_to_move.style.left = ''
    object_to_move.style.position = 'relative'
    parent_id = ''
    if (!document.getElementById('table').contains(object_to_move)) {   
        parent_id = object_to_move.parentElement.id
        object_to_move.parentElement.removeChild(object_to_move)
    } else {                                        
        old_td = object_to_move.parentElement
        parent_id = old_td.parentElement.parentElement.id
        old_td.parentElement.removeChild(old_td)
    }   
    if (parent_id != 'player_cards') {
        td = document.createElement('td')
        td.appendChild(object_to_move)
        player_cards.rows[0].insertBefore(td, player_cards.rows[0].lastChild)  
    }
}

function is_in_player_cards(card) {
    for (var i=0; i<player_cards.rows[0].children.length; ++i) {
        if (player_cards.rows[0].children[i].firstChild.id == card)
            return true
    }
    return false
}

function set_table_card_position() {
    object_to_move.style.top = ''
    object_to_move.style.left = ''
    object_to_move.style.position = 'relative'
    parent_id = ''
    if (!document.getElementById('player_cards').contains(object_to_move)) {
        parent_id = object_to_move.parentElement.id
        object_to_move.parentElement.removeChild(object_to_move)
    } else {
        old_td = object_to_move.parentElement
        parent_id = old_td.parentElement.parentElement.id
        old_td.parentElement.removeChild(old_td)
    }   
    if (parent_id != 'table') {
        td = document.createElement('td')
        td.appendChild(object_to_move)
        table.rows[0].insertBefore(td, table.rows[0].lastChild)  
    }
}   

function init_covering_data() {
    for (i=0; i<table.rows[0].children.length; ++i) {
        id = table.rows[0].children[i].firstChild.id
        if (id != 'empty') {
            bottom_array.push(table.rows[0].children[i].firstChild.id)
            top_array.push(null)
        }
    }
}

function init_coverings() { 
    covering_data = document.getElementById('table_data').value
    splitted = covering_data.substring(1, covering_data.length - 1).split('][')
    bottom_data = Array(0)
    top_data = Array(0)
    for (var i=0; i<splitted.length; ++i) {
        pair = splitted[i].split("<")              
        if (pair.length == 2) {
            bottom_data.push(pair[0].split("'")[0])
            top_data.push(pair[1].split("'")[0])
        }
    }
    for (var i=0; i<bottom_data.length; ++i) {
        tope = document.createElement('img')
        tope.id = top_data[i]
        tope.style.position = 'absolute'
        tope.border = 0
        tope.src = 'img\\' + top_data[i] + '.png'
        place = is_in_bottom(bottom_data[i])
        add_to_top(place, tope.id)
        document.body.appendChild(tope)
        to_coverings(tope)
    } 
    redraw_coverings()
}

function is_covered(bottom_card) {
    for (i=0; i<bottom_array.length; ++i) {
        if (bottom_array[i] == bottom_card) {
            if (top_array[i] != null) 
                return true
            return false
        }
    }
    return false
}

function delete_from_top(top_card) {
    for (i=0; i<top_array.length; ++i)
        if (top_array[i] == top_card)
            top_array[i] = null
}

function delete_from_bottom(bottom_card) {
    for (i=0; i<bottom_array.length; ++i)
        if (bottom_array[i] == bottom_card) {
            bottom_array.splice(i, 1)
            top_array.splice(i, 1)
        }
}

function add_to_top(i, card) {
    top_array[i] = card
}

function add_to_bottom(card) {
    bottom_array.push(card)
    top_array.push(null)
}

function is_in_bottom(card){
    for (i=0; i<bottom_array.length; ++i) {
        if (bottom_array[i] == card)
            return i
    }
    return null
}

function is_in_top(card) {
    for (var i=0; i<top_array.length; ++i)     
        if ( (top_array[i] == card) )
            return i      
    return null    
}

function add_covering_pair(bottom, top) {
    place = is_in_bottom(bottom.id)
    if (place != null)
        add_to_top(place, top.id)
    if (table.contains(top) || player_cards.contains(top)) {
        td = top.parentElement
        td.parentElement.removeChild(td)
        document.body.appendChild(top)
    }
}

function belongs_to_player(id) {
    return document.getElementById(id).border != 0
}

function update_str_presentation() {
    string_presentation = ''
    for (i=0; i<bottom_array.length; ++i) {
        if (belongs_to_player(bottom_array[i])) {
            string_presentation += '[' + bottom_array[i]
            if ((top_array[i] != null) && (belongs_to_player(top_array[i])) )
                string_presentation += '<' + top_array[i]
            string_presentation += ']'
        }
        else
        if ( (top_array[i] != null) && (belongs_to_player(top_array[i])) )
            string_presentation += '[' + bottom_array[i] + '<' + top_array[i] + ']'
    }
    document.getElementById('players_cards').value = string_presentation
}

function redraw_coverings() {
    for (var i=0; i<coverings.length; ++i) {
        covering = coverings[i]
        bottom = document.getElementById(bottom_array[is_in_top(covering.id)])
        if (bottom != null) {
            covering.style.top = (getAbsoluteTop(bottom) + cover_delta_y) + 'px'
            covering.style.left = (getAbsoluteLeft(bottom) + cover_delta_x) + 'px'
            covering.style.visibility = 'visible'
        }
    }
}

function to_coverings(moving) {
    coverings.push(moving)
}

function from_coverings(obj) {
    for (var i=0; i<coverings.length; ++i)
        if (coverings[i].id == obj.id)
            coverings.splice(i, 1)
}
                    
function dragging_mode_off(obj) {
    moving = object_to_move
    if (dragging == true) {
        bottom_card = find_bottom_card(event) 
        if (bottom_card != null) {
            if ( !is_covered(moving.id)  && !is_covered(bottom_card.id)
                    && (moving.id != bottom_card.id) ) {
                set_covering_position(bottom_card)
                delete_from_top(moving.id)
                delete_from_bottom(moving.id)
                add_covering_pair(bottom_card, moving)
                to_coverings(moving)
                update_str_presentation()
            }
        }
        else {    
            put_to_cards = put_to_player_cards(event)
            if ( put_to_cards && (!is_covered(moving.id)) && !is_in_player_cards(moving.id)) { 
                set_user_cards_position()   
                delete_from_top(moving.id)
                delete_from_bottom(moving.id)
                from_coverings(moving)
                update_str_presentation()
            } else {        
                put_to_table = put_to_table_cards(event)
                if (put_to_table && !is_covered(moving.id) && !is_in_bottom(moving.id)) {    
                    set_table_card_position(obj)
                    delete_from_top(moving.id)
                    add_to_bottom(moving.id)
                    from_coverings(moving);
                    update_str_presentation()
                } 
            }                
            moving = null     
        }  
        redraw_coverings()
        object_to_move.src = 'img\\' + object_to_move.id + '.png'
        restore_cursor()
        dragging = false
        object_to_drag = null
        dragging = false
        obj.parentNode.removeChild(obj)
    }
} 

function dragging_mode_on(obj) {
    if (dragging == false) {
        obj.src = 'img\\b1fv.png'
        save_cursor()
        set_grab_cursor()
        object_to_move = obj
        object_to_drag = document.createElement("img")
        object_to_drag.src = "img\\" + obj.id + '.png'
        object_to_drag.visibility = 'visible'
        object_to_drag.style.position = 'absolute'
        object_to_drag.style.left = getAbsoluteLeft(object_to_move)
        object_to_drag.style.top = getAbsoluteTop(object_to_move)
        object_to_drag.onmouseup = function () { dragging_mode_off(this) }
        document.body.appendChild(object_to_drag)
        dragging = true
        top_card = obj.id    
    }       
}  

function restore_cursor() {
    document.body.style.cursor = saved_cursor
}

function set_grab_cursor() {
    document.body.style.cursor = 'move'
}

function save_cursor() {
    saved_cursor = document.body.style.cursor
} 

function drag(obj) {
    if (dragging){
        object_to_drag.style.left = (event.x - 38) + 'px'
        object_to_drag.style.top = (event.y - 48) + 'px'
    }
}

function bodyOnLoad() {
    setInterval("refresher()", 4000)
    table = document.getElementById('table')
    player_cards = document.getElementById('player_cards')
    document.onmousemove = function(){drag(event)}
    if ( (table!=null) & (player_cards!=null) ) {
        init_covering_data()
        init_coverings()
    }
}

function getAbsoluteLeft(obj) {
    if (null != obj.offsetParent)
        return obj.offsetLeft + this.getAbsoluteLeft(obj.offsetParent) 
    return obj.offsetLeft;
}

function getAbsoluteTop(obj) {
    if (null != obj.offsetParent)
        return obj.offsetTop + this.getAbsoluteTop(obj.offsetParent); 
    return obj.offsetTop;
}

function between(value, a, b) {
    return ( ( value >= a ) && (value <= b))
}

function coord_in(x, y, obj) {
    l = getAbsoluteLeft(obj)
    t = getAbsoluteTop(obj)
    delta_x = 71
    delta_y = 96
    if (between(x, l, l + delta_x) && (between(y, t, t + delta_y))) {
        return true
    }
    return false
}

function find_bottom_card(event) {
    for (i=0; i<table.rows[0].children.length; ++i){
        if ( (table.rows[0].children[i].firstChild.id != 'empty') &&
                (coord_in(event.x, event.y, table.rows[0].children[i].children[0])) ) {
            return table.rows[0].children[i].children[0]
        }
    }
    return null
}

function refresher() {
    if (!is_active()) {
        document.getElementById('submitter').submit()
    }
}

function is_active() {
    return document.getElementById('is_active').value == 'True'
}