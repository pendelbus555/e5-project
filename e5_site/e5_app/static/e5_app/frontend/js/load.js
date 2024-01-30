$(document).ready(function () {

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
      }
    });

  }

  var page = 1;
  var totalPage = 1;
  ajax_function(1);


  $('#More').on('click', function () {
    ajax_function(1);
  });

});