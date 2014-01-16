<%def name="pagination_links(page)">
% if page.page_count > 1:
<ul class="pagination">
    % if page.previous_page:
    <li><a href="${page.url_maker(page.first_page)}">&laquo;&laquo;</a></li>
    <li><a href="${page.url_maker(page.previous_page)}">&laquo;</a></li>
    % else:
    <li class="disabled"><a href="#">&laquo;&laquo;</a></li>
    <li class="disabled"><a href="#">&laquo;</a></li>
    % endif
    % for curpage in page.window:
    <li${' class="active"' if page.page == curpage else '' | n}><a href="${page.url_maker(curpage)}">${curpage}</a></li>
    % endfor
    % if page.next_page:
    <li><a href="${page.url_maker(page.next_page)}">&raquo;</a></li>
    <li><a href="${page.url_maker(page.last_page)}">&raquo;&raquo;</a></li>
    % else:
    <li class="disabled"><a href="#">&raquo;</a></li>
    <li class="disabled"><a href="#">&raquo;&raquo;</a></li>
    % endif
</ul>
% endif
</%def>

