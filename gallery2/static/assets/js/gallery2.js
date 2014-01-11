'use strict';

$(function () {
    var tags = [];

    // check all thumbs, if 404 then remove
    $.each($('.thumbnail'), function (index, el) {
        var $el = $(el),
            img = $el.find('img');
        $.get(img.attr('src')).fail(function () {
            console.log("REMOVING " + img.attr('src'));
            $el.remove();
        });
    });

    $('input.tags').autocomplete({
        source: function (request, response) {
            if (tags.length > 0) {
                response($.map(tag, function (tag) {
                    if (tag.value.search(request.term) !== -1) {
                        return tag;
                    }
                }));
            } else {
                $.get('/tags', function (data) {
                    response($.map(data.tags, function (item) {
                        var tag = {
                            label: item,
                            value: item
                        };
                        tags.push(tag);
                        if (tag.value.search(request.term) !== -1) {
                            return tag;
                        }
                    }));
                });
            }
        },
        select: function (event, ui) {
            var url = "/search?q=" + ui.item.value;
            window.document.location.href = url;
        }
    });
});
