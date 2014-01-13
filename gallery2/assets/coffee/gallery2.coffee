$ ->
  thumbnails = $ '.thumbnail'

  $.each thumbnails, (index, el) ->
    el = $(el)
    img = el.find 'img'
    src = img.attr 'data-src'

    $.get(src)
      .success ->
        img.attr 'src', src
        el.show()
      .fail ->
        el.remove()

  $('input.tags').autocomplete
     source: (req, res) ->

       $.get '/tags', (data) ->

         res $.map data.tags, (item) ->

           tag =
             label: item
             value: item

            if tag.value.search(req.term) != -1
              return tag
         
     select: (event, ui) ->
       window.document.location.href = "/search?q=#{ui.item.value}"
