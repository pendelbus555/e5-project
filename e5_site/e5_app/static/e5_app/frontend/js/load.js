$(document).ready(function () {
  var page = 1;
  var totalPage = 1;
  var url = window.location.href.replace(/\/$/, '');
  var lastSeg = url.substr(url.lastIndexOf('/') + 1);

  function updateList(data) {
    var ulElement = $("ul.list-group.list-group-flush");
    $.each(data.data_news, function (index, news) {
      var innerUrl = site_news_url + news.slug_url + '/';
      var InnerHtml = `
        <li class="list-group-item py-3">
          <h5><a class='text-break stretched-link text-black custom-link' href="${innerUrl}">${news.name}</a></h5>
          <small class='text-black'>${news.created_at}</small>
        </li>
      `;
      ulElement.append(InnerHtml);
    });
  }

  function addButton() {
    var Element = $("#newsColumn");
    var InnerHtml = `
      <button type="button" class="btn btn-outline-secondary align-self-center custom-btn my-1" id="More">Показать
      еще</button>
    `;
    Element.append(InnerHtml);
    $('#More').on('click', function () {
      ajax_function(page + 1, lastSeg);
    });
  }

  function ajax_function(pageIn, lastSegIn) {
    $.ajax({
      url: site_news_url,
      type: "get",
      data: {
        'page': pageIn,
        'segment': lastSegIn,
      },
      dataType: 'json',
      success: function (data) {
        totalPage = data.total_pages;
        page = pageIn;
        updateList(data);
        if (page < totalPage) {
          addButton();
        } else {
          $("#More").remove();
        }
      }
    });
  }

  ajax_function(page, lastSeg);
});