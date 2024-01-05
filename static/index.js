const join = document.querySelector(".join"),
      faqs = document.querySelectorAll(".faq");

faqs.forEach((faq)=>{
    faq.addEventListener("click", () => {
        faq.classList.toggle("active");
    });
});

function closeMessage(icon) {
    // Find the parent message container and hide it
    var messageContainer = icon.closest('.container#messages');
    messageContainer.style.display = 'none';
}
