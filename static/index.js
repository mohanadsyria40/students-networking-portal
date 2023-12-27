const join = document.querySelector(".join"),
      overlay = document.querySelector(".overlay"),
      closeBtn = document.querySelector(".overlay .close"),
      faqs = document.querySelectorAll(".faq");

faqs.forEach((faq)=>{
    faq.addEventListener("click", () => {
        faq.classList.toggle("active");
    });
});


