django.jQuery(function() {
    
    var $ = django.jQuery;

    $('input[id$="override"]').change(function() {
        // If "override" is true, target field is set enabled, otherwise - disabled and empty.
        var field_name = String(this.name).replace('_override', ''),
            field      = $('#id_' + field_name);

        field.attr('disabled', !this.checked);
    });

    $('#override_all').click(function() {
        $('input[id$="override"]').each(function() {
            this.checked = true;
            $(this).change();
        });
        return false;
    })

    $('.inheritable').dblclick(function() {
        var input = $(this).find('input[type="text"]');

        if (input.attr('disabled')) {
            input.removeAttr('disabled');
            input.focus();

            var checkbox = $('[name="%s"]'.replace('%s', input.attr('name') + '_override'));
            checkbox.attr('checked', true);
        }
    });


});