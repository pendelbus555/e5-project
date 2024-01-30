$(document).ready(function () {

  function updatePagination(page, totalPage) {


    // Дополнительная логика пагинации, если нужно
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
    // Находим элемент "row g-4" для добавления карточек
    var rowElement = $('.row.g-4');

    // Очищаем содержимое элемента, чтобы избежать дублирования карточек
    rowElement.empty();

    // Проходим по каждой новости и создаем карточку
    $.each(data.data_news, function (index, news) {
      // Создаем HTML для карточки
      var cardInnerHtml = `
            <div class="col-xl-3 col-sm-6">
                <div class="card custom-card mx-auto h-100">
                    <img src="${news.picture_url}" class="card-img-top card-img-top-custom" alt="...">
                    <div class="card-body">
                        <h5 class="card-title">${news.name}</h5>
                        <p class="card-text">${news.description}</p>
                        <a href="#" class="btn btn-primary">Go somewhere</a>
                    </div>
                    <div class="card-footer">
                        <small class="text-body-secondary">${news.created_at}</small>
                    </div>
                </div>
            </div>
        `;

      // Добавляем карточку в родительский элемент
      rowElement.append(cardInnerHtml);
    });
  }



  function ajax_function(pageIn) {
    $.ajax({
      url: '/site/',
      type: "get",
      data: {
        'page': pageIn,
      },
      dataType: 'json',
      success: function (data) {
        totalPage = data.total_pages;
        page = pageIn;
        updateCards(data);
        updatePagination(page, totalPage);
      }
    });

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