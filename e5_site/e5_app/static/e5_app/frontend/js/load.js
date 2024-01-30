$(document).ready(function () {

  function updateList(data) {
    console.log(data);
    var ulElement = $("ul.list-group.list-group-flush");
    $.each(data.data_news, function (index, news) {
      var cardInnerHtml = `
  <li class="list-group-item">
      <h5><a href="${news.slug_url}">${news.name}</a></h5>
      <small>${news.created_at}</small>
  </li>
        `;
      // Добавляем карточку в родительский элемент
      ulElement.append(cardInnerHtml);
    });
  }

function buttonCheck(page, totalPage) {
console.log(page);
  if (page >= totalPage) {
    if ($("#More").length) { // Проверить, существует ли кнопка с id="More"
      $("#More").remove(); // Удалить кнопку с id="More" из формы
    }
  }
}

  function ajax_function(pageIn, lastSegIn) {
    $.ajax({
      url: '/site/news/',
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
        buttonCheck(page, totalPage);
      }
    });

  }

  var page = 1;
  var totalPage = 1;
var url = window.location.href.replace(/\/$/, '');
 var lastSeg = url.substr(url.lastIndexOf('/') + 1);
 console.log(lastSeg);
  ajax_function(1, lastSeg);


  $('#More').on('click', function () {
    ajax_function(page+1, lastSeg);
  });

});