$(document).ready(function(){
    $('#search_input').on('input', function() {
        if ($(this).val().length > 0) {
            $('#search_button').prop('disabled', false);
        } else {
            $('#search_button').prop('disabled', true);
        }
    });
});