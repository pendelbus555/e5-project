$(document).ready(function() {

function updatePagination(page , totalPage) {
    //var $pagination = $('ul.pagination');
    //$pagination.find('.active').removeClass('active');
    //$pagination.find('#news_' + page).addClass('active');



    // Дополнительная логика пагинации, если нужно
    console.log('pag_page', page);
    console.log('pag_total', totalPage);
    if (page == 1) {
                       $('#news_1').text(page);
                       $('#news_2').text(page+1);
                       $('#news_3').text(page+2);

    }

    else if (page == totalPage) {
                       $('#news_1').text(page-2);
                       $('#news_2').text(page-1);
                       $('#news_3').text(page);

    }

    else {
                       $('#news_1').text(page-1);
                       $('#news_2').text(page);
                       $('#news_3').text(page+1);

    }
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
                       var data_news = JSON.parse(data['data_news']);
                       totalPage = parseInt(data.total_pages);
                       page = parseInt(pageIn);
                       //console.log(data_news[0].fields.name);

                      updatePagination(page , totalPage)
                  }
              });
                       console.log('end', pageIn);

          }

        var page = 1;
        var totalPage = 3;
        ajax_function(1);


            // Обработчик события для кнопки "new_left"
  $('#news_left').on('click', function() {
    ajax_function(1);
  });

  // Обработчик события для кнопки "new_right"
  $('#news_right').on('click', function() {
    ajax_function(totalPage);
  });

  // Обработчик события для кнопок выбора страницы
  $('#news_1, #news_2, #news_3').on('click', function() {
    ajax_function(parseInt($(this).text()));
  });
});