// Navbar functionality

function hideIconBar(){
    var iconBar = document.getElementById("iconBar");
    var navigation = document.getElementById("navigation");
    iconBar.setAttribute("style", "display: none;");
    navigation.classList.remove("hide");
}

function hideNav(){
    var iconBar = document.getElementById("iconBar");
    var navigation = document.getElementById("navigation");
    iconBar.setAttribute("style", "display: block;");
    navigation.classList.add("hide");
}

// comment

function showComment(){
    var commentArea = document.getElementById("comment-area")
    commentArea.setAttribute("style", "display: block;")
}

function showReply(){
    var replyArea = document.getElementById("reply-area")
    replyArea.setAttribute("style", "display: block;")
}