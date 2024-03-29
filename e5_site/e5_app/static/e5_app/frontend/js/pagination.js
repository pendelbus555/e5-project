$(document).ready(function () {
  function updatePagination(page, totalPage) {
    if (totalPage <= 3) {
      $('#news_left').remove();
      $('#news_right').remove();
    }
    if (totalPage < 3) {
      $('#news_3').remove();
    }
    if (totalPage < 2) {
      $('#news_2').remove();
      $('#news_1').remove();
    }
    if (page == 1) {
      $('#news_1').text(page);
      $('#news_2').text(page + 1);
      $('#news_3').text(page + 2);

    }
    else if (totalPage > 3) {
        if (page == totalPage){
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
  }

  function updateCards(data) {
    var rowElement = $('#news_row');
    rowElement.empty();
    $.each(data.data_news, function (index, news) {
      var innerUrl = site_news_url + news.slug_url + '/';
      var cardInnerHtml = `
            <div class="col-xl-3 col-lg-4 col-sm-6">
                <div class="card custom-card mx-auto h-100">
                    <img src="${news.picture_url}" class="card-img-top card-img-top-custom" alt="...">
                    <div class="card-body">
                        <h5 class="card-title">${news.name}</h5>
                        <p class="card-text">${news.description}</p>
                        <a href="${innerUrl}" class="btn btn-primary stretched-link">Подробнее</a>
                    </div>
                    <div class="card-footer">
                        <small class="text-body-secondary">${news.created_at}</small>
                    </div>
                </div>
            </div>
        `;
      rowElement.append(cardInnerHtml);
    });
  }

  function ajax_function(pageIn) {
    $.ajax({
      url: '/site/',
      type: "get",
      data: {
        'from': from,
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
  var from = 'news';
  var page = 1;
  var totalPage = 3;
  ajax_function(1);

  $('#news_left').on('click', function () {
    ajax_function(1);
  });

  $('#news_right').on('click', function () {
    ajax_function(totalPage);
  });

  $('#news_1, #news_2, #news_3').on('click', function () {
    ajax_function(parseInt($(this).text()));
  });
});

//-------------------------------------------------------

$(document).ready(function () {
  function updatePagination(page, totalPage) {
    if (totalPage <= 3) {
      $('#vacancy_left').remove();
      $('#vacancy_right').remove();
    }
    if (totalPage < 3) {
      $('#vacancy_3').remove();
    }
    if (totalPage < 2) {
      $('#vacancy_2').remove();
      $('#vacancy_1').remove();
    }
    if (page == 1) {
      $('#vacancy_1').text(page);
      $('#vacancy_2').text(page + 1);
      $('#vacancy_3').text(page + 2);

    }
    else if (totalPage > 3) {
        if (page == totalPage){
          $('#vacancy_1').text(page - 2);
          $('#vacancy_2').text(page - 1);
          $('#vacancy_3').text(page);

        }
        else {
          $('#vacancy_1').text(page - 1);
          $('#vacancy_2').text(page);
          $('#vacancy_3').text(page + 1);
        }
    }
  }

  function updateCards(data) {
    var rowElement = $('#vacancy_row');
    rowElement.empty();
    $.each(data.data_vacancy, function (index, vacancy) {
      var innerUrl = site_vacancy_url + vacancy.slug_url + '/';
      var salaryTitle = vacancy.salary !== null ? `<h5 class="card-title">${vacancy.salary}</h5>` : '';
      var cardInnerHtml = `
            <div class="col-xl-3 col-lg-4 col-sm-6">
                <div class="card custom-card mx-auto h-100">
                      <div class="card-header">${vacancy.name}</div>
                      <div class="card-body">
                        ${salaryTitle}
                        <p class="card-text">${vacancy.company_name}</p>
                        <a href="${innerUrl}" class="btn btn-primary stretched-link">Подробнее</a>
                      </div>
                </div>
            </div>
        `;
      rowElement.append(cardInnerHtml);
    });
  }

  function ajax_function(pageIn) {
    $.ajax({
      url: '/site/',
      type: "get",
      data: {
        'from': from,
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

  var from = 'vacancy';
  var page = 1;
  var totalPage = 3;
  ajax_function(1);

  $('#vacancy_left').on('click', function () {
    ajax_function(1);
  });

  $('#vacancy_right').on('click', function () {
    ajax_function(totalPage);
  });

  $('#vacancy_1, #vacancy_2, #vacancy_3').on('click', function () {
    ajax_function(parseInt($(this).text()));
  });
});