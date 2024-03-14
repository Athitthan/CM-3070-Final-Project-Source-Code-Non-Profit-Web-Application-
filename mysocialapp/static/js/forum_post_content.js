
const replyForms = document.querySelectorAll(".reply_form");
const addReplyButtons = document.querySelectorAll(".add_reply");
const replyContainers = document.querySelectorAll(".reply_container");
const seeReplyButtons = document.querySelectorAll(".see_reply_button");
const noseeReplyButtons = document.querySelectorAll(".nosee_reply_button");



const replyFormsArray = Array.from(replyForms);
const addReplyButtonsArray = Array.from(addReplyButtons);
const replyContainersArray = Array.from(replyContainers);
const seeReplyButtonsArray = Array.from(seeReplyButtons);
const noseeReplyButtonsArray = Array.from(noseeReplyButtons);




// Add click event listener to the document
document.addEventListener("click", function (event) {
  // Iterate through reply forms
  replyFormsArray.forEach((form) => {
    if (form.style.display === "block") {
      // Check if the clicked element is not the form or the corresponding add_reply button
      if (
        !form.contains(event.target) &&
        !addReplyButtonsArray.includes(event.target)
      ) {
        form.style.display = "none"; // Close the form if click is outside
      }
    }
  });
});

addReplyButtonsArray.forEach((replyButton) => {
  replyButton.addEventListener("click", (elem) => {
    elem.preventDefault();
    replyFormsArray.forEach((form) => {
      if (
        form.getAttribute("comment_id") ==
        replyButton.getAttribute("comment_id")
      ) {
        form.style.display = "block";
        
      }
    });
  });
});


seeReplyButtonsArray.forEach((seeReplyButton) => {
  seeReplyButton.addEventListener("click", (elem) => {
    elem.preventDefault();
    replyContainersArray.forEach((replyContainer) => {
      if (
        replyContainer.getAttribute("comment_id") ==
        seeReplyButton.getAttribute("comment_id")
      ) {
        replyContainer.style.display = "block";
        seeReplyButton.style.display= "none"
        noseeReplyButtonsArray.forEach(noseeReplyButton=>{
            if (
        replyContainer.getAttribute("comment_id") ==
        noseeReplyButton.getAttribute("comment_id")
      ){
        noseeReplyButton.style.display="block"
      }
        });
      }
    });
  });
});




noseeReplyButtonsArray.forEach((noseeReplyButton) => {
  noseeReplyButton.addEventListener("click", (elem) => {
    elem.preventDefault();
    replyContainersArray.forEach((replyContainer) => {
      if (
        replyContainer.getAttribute("comment_id") ==
        noseeReplyButton.getAttribute("comment_id")
      ) {
        replyContainer.style.display = "none";
        noseeReplyButton.style.display = "none";
        seeReplyButtonsArray.forEach((seeReplyButton) => {
          if (
            replyContainer.getAttribute("comment_id") ==
            seeReplyButton.getAttribute("comment_id")
          ) {
            seeReplyButton.style.display = "block";
          }
        });
      }
    });
  });
});



