$(document).ready(function(){
    $('paper-fab').click(function(e) {
        var button = this;
        button.disabled = true;
        var action = button.getAttribute('icon') == 'check' ? 'accept' : 'decline';
        
        $.post('/requests/' + button.getAttribute('value') + '/' + action)
        .done(function(){
            $(button).parents('.join_request').fadeOut('slow');
        })
        .fail(function(){
            alert("Error");
            button.disabled = false;
        });
    });
});