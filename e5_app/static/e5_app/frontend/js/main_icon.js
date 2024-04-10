$(document).ready(function () {
    document.querySelector('.navbar-brand').addEventListener('mouseenter', function() {
      document.querySelector('#custom_icon_2').classList.remove('custom_icon_2_out');
      document.querySelector('#custom_icon_2').classList.add('custom_icon_2_in');
      document.querySelector('#custom_icon_1').classList.remove('custom_icon_1_out');
      document.querySelector('#custom_icon_1').classList.add('custom_icon_1_in');
    });

    document.querySelector('.navbar-brand').addEventListener('mouseleave', function() {
      document.querySelector('#custom_icon_2').classList.remove('custom_icon_2_in');
      document.querySelector('#custom_icon_2').classList.add('custom_icon_2_out');
      document.querySelector('#custom_icon_1').classList.remove('custom_icon_1_in');
      document.querySelector('#custom_icon_1').classList.add('custom_icon_1_out');
    });
});