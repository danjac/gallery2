<%!
    active_tab = "tags"
%>
<%inherit file="/base.mako" />
<%namespace name="navigate" file="/navigate.mako" />

<% page = paginate(images) %>
<div class="row">
% for image in page.items:
<div class="col-xs-3">
<a class="thumbnail" data-toggle="tooltip" title="${image.title}" href="${route_url('detail', image)}">
    <img src="${static_url('gallery2:static/img/ajax-loader.gif')}" data-src="${storage_url(image.thumbnail)}" alt="${image.title}">
</a>
</div>
% endfor 
</div>
${navigate.pagination_links(page)}
<div class="text-center"><small>${_("Images:")} ${page.item_count}</small></div>
