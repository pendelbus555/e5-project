$(document).ready(function () {
document.querySelectorAll('.dropdown-item').forEach(function(button) {
    button.addEventListener('click', function() {
        $('.dropdown-item').removeClass('active');
        var selectedType = this.dataset.type;
        filterEvents(selectedType);
        $(this).addClass('active');
    });
});
});
function filterEvents(selectedType) {
    var events = document.querySelectorAll('.accordion-item');
    events.forEach(function(event) {
        var eventType = event.dataset.type;
        if (selectedType === 'all' || selectedType === eventType) {
            event.style.display = 'block';
        } else {
            event.style.display = 'none';
        }
    });
}