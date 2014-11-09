var PolymerForm;
$(document).ready(function(){
    PolymerForm = function(init_obj) {
        if (!init_obj.formId || !init_obj.submitButtonId) {
            throw "PolymerForm: Arguments error";
        }
        var form =  $('form#' + init_obj.formId);
        var submitButton = $('#' + init_obj.submitButtonId);
        
        // prevent normal submit
        form.submit(function(e) {
            e.preventDefault();
        });
        
        submitButton.click(function(e) {
            var inputs = form.find('[name]');
            var button = this;
            button.disabled = true;
            // client side validation
            // for (var i = 0, l = inputs.length; i < l; ++i) {
            //     if (inputs[i].invalid) {
            //         return;
            //     }
            // }
            // form data
            var data = {};
            inputs.each(function(i) {
                var name = this.getAttribute('name');
                switch(this.tagName.toLowerCase()) {
                    case 'paper-input':
                        if (this.value !== null) {
                            data[name] = this.value;
                        }
                        break;
                    case 'paper-dropdown-menu':
                        if (this.selected !== null) {
                            data[name] = this.selected;
                        }
                        break;
                    case 'paper-toggle-button':
                        data[name] = this.checked;
                        break;
                    case 'paper-checkbox':
                        if (this.checked) {
                            data[name] = data[name] || [];
                            data[name].push(this.getAttribute('value'));
                        }
                        break;
                    case 'paper-radio-group':
                        if (this.selected !== null) {
                            data[name] = this.selected;
                        }
                        break;
                    case 'paper-item':
                    case 'paper-radio-button':
                        console.log("Do not use 'name' attribute on paper-item or paper-radio-button, instead use 'value' attribute and on parent paper-dropdown-menu or paper-radio-group set valueattr=value");
                        break;
                    default:
                        $this = $(this);
                        if ($this.val() !== null) {
                            data[name] = $(this).val();
                        }
                }
            });
            
            $.ajax({
                url: form.attr('action'),
                data: JSON.stringify(data),
                contentType: 'application/json;charset=UTF-8',
                type: 'post',
            }).done(function(data) {
                if (data.redirect) {
                    window.location.replace(data.redirect);
                }
            }).fail(function(resp) {
                var errors = JSON.parse(resp.responseText);
                for(var field in errors) {
                    var input = $('[name=' + field + ']')[0];
                    if ('invalid' in input && 'error' in input) {
                        input.invalid = true;
                        input.error = $.isArray(errors[field]) ? errors[field].join() : errors[field];
                    } else {
                        // in some polymer elements errors are not implemented yet
                        $(input).css({
                            padding: '5px',
                            border: '1px solid red'
                        });
                    }
                }
                button.disabled = false;
            });
        });
        
        form.on('keyup', function(e) {
            if (e.keyCode == 13) {    // Enter
                submitButton.click();
            }
        });
    }
});