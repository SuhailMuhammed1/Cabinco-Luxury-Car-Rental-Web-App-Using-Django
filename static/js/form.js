// JavaScript code to display the notification
const contactForm = document.getElementById('contactForm');
contactForm.addEventListener('submit', function () {
    displayNotification();
});

function displayNotification() {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = 'Thank you for contacting us! We will get back to you soon.';
    document.body.appendChild(notification);

    setTimeout(function () {
        notification.style.opacity = '0';
        setTimeout(function () {
            notification.style.display = 'none';
        }, 1000);
    }, 5000);
}
