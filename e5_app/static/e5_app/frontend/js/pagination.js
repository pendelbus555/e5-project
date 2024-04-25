$(document).ready(function () {
  function updatePagination(page, totalPage, prefix) {
    if (totalPage <= 3) {
      $(`#${prefix}_left, #${prefix}_right`).remove();
    }
    if (totalPage < 3) {
      $(`#${prefix}_3`).remove();
    }
    if (totalPage < 2) {
      $(`#${prefix}_2, #${prefix}_1`).remove();
    }
    if (page == 1) {
      $(`#${prefix}_1`).text(page);
      $(`#${prefix}_2`).text(page + 1);
      $(`#${prefix}_3`).text(page + 2);
    } else if (totalPage > 3) {
      if (page == totalPage) {
        $(`#${prefix}_1`).text(page - 2);
        $(`#${prefix}_2`).text(page - 1);
        $(`#${prefix}_3`).text(page);
      } else {
        $(`#${prefix}_1`).text(page - 1);
        $(`#${prefix}_2`).text(page);
        $(`#${prefix}_3`).text(page + 1);
      }
    }
  }

  function updateCards(data, prefix) {
    var rowElement = $(`#${prefix}_row`);
    rowElement.empty();
    $.each(data[`data`], function (index, item) {
      var additionalInfo = "";
      if (prefix === "news") {
        var innerUrl = site_news_url + item.slug_url + "/";
        additionalInfo = `
          <img src="${item.picture_url}" class="card-img-top" alt="Новость">
          <div class="card-body">
            <h5 class="card-title">${item.name}</h5>
            <p class="card-text">${item.description}</p>
            <a href="${innerUrl}" class="btn btn-primary stretched-link">Подробнее</a>
          </div>
          <div class="card-footer">
            <small class="text-body-secondary">${item.created_at}</small>
          </div>
        `;
      } else if (prefix === "vacancy") {
        var innerUrl = site_vacancy_url + item.slug_url + "/";
        var salaryTitle = item.salary !== null ? `<h5 class="card-title">${item.salary}</h5>` : "";
        additionalInfo = `
          <div class="card-header">${item.name}</div>
          <div class="card-body">
            ${salaryTitle}
            <p class="card-text">${item.company_name}</p>
            <a href="${innerUrl}" class="btn btn-primary stretched-link">Подробнее</a>
          </div>
        `;
      }
      var cardInnerHtml = `
        <div class="col-xl-3 col-lg-4 col-sm-6">
          <div class="card custom-card mx-auto h-100">
            ${additionalInfo}
          </div>
        </div>
      `;
      rowElement.append(cardInnerHtml);
    });
  }

  function ajax_function(pageIn, prefix) {
    $.ajax({
      url: "/site/",
      type: "get",
      headers: {
        From: prefix,
      },
      data: {
        from: prefix,
        page: pageIn,
      },
      dataType: "json",
      success: function (data) {
        totalPage = data.total_pages;
        if (prefix === "news") {
          totalPage_news = totalPage;
        } else if (prefix === "vacancy") {
          totalPage_vacancy = totalPage;
        }
        page = pageIn;
        updateCards(data, prefix);
        updatePagination(page, totalPage, prefix);
      },
      complete: function (data) {
        AOS.refresh();
      },
    });
  }

  var page_news = 1;
  var totalPage_news = 3;
  var page_vacancy = 1;
  var totalPage_vacancy = 3;

  ajax_function(1, "news");
  ajax_function(1, "vacancy");

  $("#news_left").on("click", function () {
    ajax_function(1, "news");
  });

  $("#news_right").on("click", function () {
    ajax_function(totalPage_news, "news");
  });

  $("#news_1, #news_2, #news_3").on("click", function () {
    ajax_function(parseInt($(this).text()), "news");
  });

  $("#vacancy_left").on("click", function () {
    ajax_function(1, "vacancy");
  });

  $("#vacancy_right").on("click", function () {
    ajax_function(totalPage_vacancy, "vacancy");
  });

  $("#vacancy_1, #vacancy_2, #vacancy_3").on("click", function () {
    ajax_function(parseInt($(this).text()), "vacancy");
  });
});
