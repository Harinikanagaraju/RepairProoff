
document.addEventListener("DOMContentLoaded", function () {

    // Automatically hide success messages
    const messages = document.querySelectorAll(".message");

    messages.forEach(function (message) {
        setTimeout(function () {
            message.style.opacity = "0";
            message.style.transition = "opacity 0.5s";

            setTimeout(function () {
                message.remove();
            }, 500);

        }, 3500);
    });

});