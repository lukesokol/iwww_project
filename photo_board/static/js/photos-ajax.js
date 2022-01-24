$(document).ready(function() {
    $('.like_btn').click(function() {
        var photo_id_var;
        var index;
        photo_id_var = $(this).attr('data-photoid');
        index = photo_id_var - 1;
        $.get('like_photo/',
            {'photo_id': photo_id_var},
            function(data) {
                $('#like_count'+photo_id_var).html(data);
                $('#like_btn'+photo_id_var).attr('disabled','disabled');
        })
    });
    $('#search-input').keyup(function() {
        var query;
        query = $(this).val();

        $.get('suggest/',
            {'suggestion': query},
            function(data) {
            $('#categories-listing').html(data);
        })
    });
    $('.nav-link').click(function() {
        var active_btn;
        var clicked_btn;
        active_btn = $('.active');
        clicked_btn = $(this);
        clicked_btn.classList.add('active');
        active_btn.classList.remove('active');
    })
});