'use strict';

$(function () {
    var thumbnails = $('.thumbnail');

    thumbnails.hide();
    // check all thumbs, if 404 then remove
    $.each(thumbnails, function (index, el) {
        var $el = $(el),
            img = $el.find('img'),
            src = img.attr('data-src');
        $.get(src)
            .success(function () {
                img.attr('src', src);
                $el.show();
            })
            .fail(function () {
                $el.remove();
            });
    });

    $('input.tags').autocomplete({
        source: function (request, response) {
            $.get('/tags', function (data) {
                response($.map(data.tags, function (item) {
                    var tag = {
                        label: item,
                        value: item
                    };
                    if (tag.value.search(request.term) !== -1) {
                        return tag;
                    }
                }));
            });
        },
        select: function (event, ui) {
            var url = "/search?q=" + ui.item.value;
            window.document.location.href = url;
        }
    });
});
