$(document).ready(function () {

  function updatePagination(page, totalPage) {


    // Дополнительная логика пагинации, если нужно
    console.log('pag_page', page);
    console.log('pag_total', totalPage);
    if (page == 1) {
      $('#news_1').text(page);
      $('#news_2').text(page + 1);
      $('#news_3').text(page + 2);

    }

    else if (page == totalPage) {
      $('#news_1').text(page - 2);
      $('#news_2').text(page - 1);
      $('#news_3').text(page);

    }

    else {
      $('#news_1').text(page - 1);
      $('#news_2').text(page);
      $('#news_3').text(page + 1);

    }
  }


  function updateCards(data) {
    var data_news = JSON.parse(data['data_news']);

    // Находим элемент "row g-4" для добавления карточек
    var rowElement = $('.row.g-4');

    // Очищаем содержимое элемента, чтобы избежать дублирования карточек
    rowElement.empty();

    // Проходим по каждой новости и создаем карточку
    $.each(data_news, function (index, news) {
      // Создаем HTML для карточки
      var cardInnerHtml = `
            <div class="col-xl-3 col-sm-6">
                <div class="card custom-card mx-auto h-100">
                    <img src="${news.fields.picture ? news.fields.picture.url : '{% static "e5_app/frontend/images/news_default.png" %}'}" class="card-img-top card-img-top-custom" alt="...">
                    <div class="card-body">
                        <h5 class="card-title">${news.fields.name}</h5>
                        <p class="card-text">${news.fields.description}</p>
                        <a href="#" class="btn btn-primary">Go somewhere</a>
                    </div>
                    <div class="card-footer">
                        <small class="text-body-secondary">${news.fields.created_at}</small>
                    </div>
                </div>
            </div>
        `;

      // Добавляем карточку в родительский элемент
      rowElement.append(cardInnerHtml);
    });
  }



  function ajax_function(pageIn) {
    console.log('start', pageIn);
    $.ajax({
      url: '/site',
      type: "get",
      data: {
        'page': pageIn,
      },
      dataType: 'json',
      success: function (data) {
        console.log('succes', pageIn);
        //console.log(data);
        //console.log(data.total_pages);
        totalPage = parseInt(data.total_pages);
        page = parseInt(pageIn);
        //console.log(data_news[0].fields.name);
        updateCards(data);
        updatePagination(page, totalPage);
      }
    });
    console.log('end', pageIn);

  }

  var page = 1;
  var totalPage = 3;
  ajax_function(1);


  // Обработчик события для кнопки "new_left"
  $('#news_left').on('click', function () {
    ajax_function(1);
  });

  // Обработчик события для кнопки "new_right"
  $('#news_right').on('click', function () {
    ajax_function(totalPage);
  });

  // Обработчик события для кнопок выбора страницы
  $('#news_1, #news_2, #news_3').on('click', function () {
    ajax_function(parseInt($(this).text()));
  });
});