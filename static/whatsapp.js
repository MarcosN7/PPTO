document.addEventListener('DOMContentLoaded', function () {
    var whatsappLink = document.querySelector('a[href^="https://wa.me/"]');
    whatsappLink.addEventListener('click', function (event) {
        event.preventDefault();
        window.open(this.href, '_blank');
    });
});