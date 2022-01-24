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
                $('#like_btn'+photo_id_var).hide();
        })
    });
    $('#search-input').keyup(function() {
        var query;
        query = $(this).val();

        $.get('photos/suggest/',
            {'suggestion': query},
            function(data) {
            $('#categories-listing').html(data);
        })
    });
});