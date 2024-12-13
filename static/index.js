const faqs = document.querySelectorAll(".faq"),
    dropdownBtn = document.querySelectorAll(".dropdown-btn"),
    dropdown = document.querySelectorAll(".dropdown");
    links = document.querySelectorAll(".dropdown a");


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

function setAriaExpandedFalse() {
    dropdownBtn.forEach((btn) => btn.setAttribute("aria-expanded", "false"));
  }


function closeDropdownMenu() {
dropdown.forEach((drop) => {
    drop.classList.remove("active");
    drop.addEventListener("click", (e) => e.stopPropagation());
});
}

dropdownBtn.forEach((btn) => {
    btn.addEventListener("click", function (e) {
      const dropdownIndex = e.currentTarget.dataset.dropdown;
      const dropdownElement = document.getElementById(dropdownIndex);
  
      dropdownElement.classList.toggle("active");
      dropdown.forEach((drop) => {
        if (drop.id !== btn.dataset["dropdown"]) {
          drop.classList.remove("active");
        }
      });
      e.stopPropagation();
    });
  });