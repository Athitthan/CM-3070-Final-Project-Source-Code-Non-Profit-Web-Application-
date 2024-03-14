var username = JSON.parse(document.getElementById("username").textContent);
var id = JSON.parse(document.getElementById("id").textContent);
var contact_username = JSON.parse(
  document.getElementById("contact_username").textContent
);
var contact_id = JSON.parse(document.getElementById("contact_id").textContent);
var backgroundImgElem = document.querySelector("#background_image");
var profileImgElem = document.querySelector("#profile_image");
var profileNameElem = document.querySelector("#profile_name");
var emailElem = document.querySelector("#email");
var bioElem = document.querySelector("#bio");
var searchInputElem = document.querySelector("#search_input");
var searchListElem = document.querySelector("#search_list");
var searchListContainerElem = document.querySelector("#search_list>ul");
var followButton = document.querySelector("#follow_button");
var addFriendElem = document.querySelector("#add_friend");
var friendListContainerElem = document.querySelector("#friend_list_container");
var requestListContainerElem = document.querySelector(
  "#request_list_container"
);
var link = document.querySelector("#friend_list_container a");
var chatButton = document.querySelector("#friend_list_container button");
var likesElem = document.querySelector("#likes");

var postContainerElem = document.querySelector("#post_container");
var statusTextElem = document.querySelector("#status_text");
var statusCreatedAtElem = document.querySelector("#status_createdAt span");
var statusElem = document.querySelector("#status");
var emptyRequestListDisplay = document.querySelector(
  "#empty_request_list_display"
);
var emptyFriendListDisplay = document.querySelector(
  "#empty_friend_list_display"
);

//---I WROTE THIS CODE---
//Execute all functions
getAllUsers();
allFriendsList();
allRequestList();

if (contact_username) {
  checkIfFriend();
}
galleryList();
getStatus();
// End
//---END OF CODE THAT I WROTE---

//---I WROTE THIS CODE---
// This section makes an XMLHttpRequest to fetch a list of all users.
function getAllUsers() {
  var request = new XMLHttpRequest();

  request.onreadystatechange = function () {
    if (this.readyState == 4 && this.status >= 200 && this.status < 400) {
      console.log(this.status);
      var data = JSON.parse(this.responseText);
      // Call functions to process the received data
      searchUsers(data);
      fillProfileElems(data);

      console.log(data);
    } else if (this.status > 400 || (this.status > 0 && this.status < 200)) {
      console.error("Request failed with status: " + this.status);
    }
  };

  request.open("GET", "/api/users", true);

  request.send();
}
//---END OF CODE THAT I WROTE---

//---I WROTE THIS CODE---
// This function updates the user's profile information on the webpage.
function fillProfileElems(data) {
  // Iterate through the data to find the current user's information.
  data.forEach((elem) => {
    let currentUser = contact_username ? contact_username : username;
    if (elem.user.username == currentUser) {
      // Update profile elements with user information.
      // (e.g., profile image, email, bio, etc.)
      if (elem.background_image) {
        backgroundImgElem.setAttribute("src", `${elem.background_image}`);
      } else {
        backgroundImgElem.setAttribute(
          "src",
          "../../static/assets/blank-profile.jpeg"
        );
      }

      if (elem.profile_image) {
        profileImgElem.setAttribute("src", `${elem.profile_image}`);
      } else {
        profileImgElem.setAttribute(
          "src",
          "../../static/assets/blank-profile.jpeg"
        );
      }

      if (elem.email) {
        emailElem.firstElementChild.textContent =elem.email;
      } else {
        emailElem.textContent = "no email";
      }

      if (elem.bio) {
        bioElem.textContent = elem.bio;
      } else {
        bioElem.textContent = "no bio";
      }

      if (elem.name) {
        profileNameElem.textContent = elem.name;
      } else {
        profileNameElem.textContent = elem.user.username;
      }
    }
  });
}
//---END OF CODE THAT I WROTE---

//---I WROTE THIS CODE---
// This function filters and displays user search results as the user types in a search input field.
function searchUsers(data) {
  // Add an event listener to the search input field.
  // It dynamically updates the search results based on user input.
  searchInputElem.addEventListener("input", (e) => {
    const inputValue = searchInputElem.value.toLowerCase();
    searchListContainerElem.innerHTML = "";

    data.forEach((elem) => {
      if (elem.user.username != username) {
        if (elem.name.toLowerCase().startsWith(inputValue)) {
          searchListContainerElem.innerHTML += `
          
          <li id="list_user">
             <a href="../user_profile/${elem.user.username}">
              <img
                src=${
                  elem.profile_image
                    ? elem.profile_image
                    : "../../static/assets/blank-profile.jpeg"
                }
                alt=""
              />
              <p>${elem.name}</p>
              </a>

              </li>
             
                `;
        }
      }
    });
    if (inputValue) {
      searchListElem.style.display = "block";
    } else {
      searchListElem.style.display = "none";
    }

    document.body.addEventListener("click", function (event) {
      // Check if the click event did not originate from the input or results
      if (
        event.target !== searchListElem &&
        event.target !== searchInputElem &&
        !searchListContainerElem.contains(event.target)
      ) {
        searchListElem.style.display = "none"; // Hide the results
        searchInputElem.value = "";
      }
    });
  });
}
//---END OF CODE THAT I WROTE---

//---I WROTE THIS CODE---
// This function checks if a user is a friend of the current user.
function checkIfFriend() {
  // Makes an XMLHttpRequest to check if a user is a friend of the current user.
  // If they are friends, a "unFriend" button is displayed; otherwise, a "Friend" button is displayed.
  var request = new XMLHttpRequest();
  var url = "/api/checkRowExists/"; // Correct URL

  // Construct the URL with query parameters
  url += `?current_username=${encodeURIComponent(
    username
  )}&contact_username=${encodeURIComponent(contact_username)}`;

  request.open("GET", url, true);
  console.log(typeof id, typeof contact_id);

  request.onreadystatechange = function () {
    if (this.readyState == 4 && this.status >= 200 && this.status < 400) {
      console.log(this.status);
      var data = JSON.parse(this.responseText);
      var exists = data.exists;
      console.log(exists);
      if (exists) {
        addFriendElem.setAttribute(
          "href",
          `../follow/?following=${contact_username}`
        );
        addFriendElem.innerHTML += `
       
          <button id="follow_button">
          UnFriend
        </button>
        
        `;
      } else {
        checkIfRequestExist()
          .then((exists) => {
            if (exists) {
              console.log(exists);
              addFriendElem.setAttribute(
                "href",
                `../request/?requestedUserId=${contact_id}&requesterId=${id}`
              );
              addFriendElem.innerHTML += `
       
          <button style="background-color: grey;" id="follow_button">
          Requested
        </button>
        
        `;
            } else {
              addFriendElem.setAttribute(
                "href",
                `../request/?requestedUserId=${contact_id}&requesterId=${id}`
              );
              addFriendElem.innerHTML += `
       
          <button id="follow_button">
          Add Friend
        </button>
        
        `;
            }
          })
          .catch((error) => {
            console.error(error);
          });
      }

      console.log(data);
    } else if (this.status > 400 || (this.status > 0 && this.status < 200)) {
      console.error("Request failed with status: " + this.status);
    }
  };

  request.send();
}
//---END OF CODE THAT I WROTE---

function checkIfRequestExist() {
  return new Promise((resolve, reject) => {
    var request = new XMLHttpRequest();
    var url = "/api/checkRequestRowExists/";

    url += `?requestedUserUsername=${encodeURIComponent(
      contact_username
    )}&requesterUsername=${encodeURIComponent(username)}`;

    request.open("GET", url, true);

    request.onreadystatechange = function () {
      if (this.readyState == 4 && this.status >= 200 && this.status < 400) {
        var data = JSON.parse(this.responseText);
        resolve(data.exists);
      } else if (this.status >= 400) {
        reject("Request failed with status: " + this.status);
      }
    };

    request.onerror = function () {
      reject("Network Error");
    };

    request.send();
  });
}

//---I WROTE THIS CODE---
// This function fetches and displays a list of all friends for the current user.
function allFriendsList() {
  // Makes an XMLHttpRequest to fetch a list of all friends.
  // Displays the list of friends on the webpage.
  var request = new XMLHttpRequest();

  request.onreadystatechange = function () {
    if (this.readyState == 4 && this.status >= 200 && this.status < 400) {
      console.log(this.status);
      var data = JSON.parse(this.responseText);

      data.forEach((elem) => {
        if (elem.current_user.user.username == username) {
          emptyFriendListDisplay.setAttribute("style", "display:none;");
          friendListContainerElem.innerHTML += `
          
          <li >
             <a href="../user_profile/${elem.following.user.username}">
              <img
                src=${
                  elem.following.profile_image
                    ? elem.following.profile_image
                    : "../../static/assets/blank-profile.jpeg"
                }
                alt=""
              />
              <p>${elem.following.name}</p>

              <a href="../chatRoom/${elem.following.user.username}"> 
              <button>Chat</button>
              <p id="chat_notification_${
                elem.following.id
              }" class="chat_notification_display"></p>
              </a>
              
              <a class="friendlist_delete" href="../follow/?following=${
                elem.following.user.username
              }&path=profile"> 
              <button style="background-color:lightcoral"><i style="color:black" class="fas fa-trash-alt"></i></button>
              </a>

              </a>

              </li>
             
                `;
          fetch(
            `/check_unread_message/?sender_username=${elem.following.user.username}`
          )
            .then((response) => response.json())
            .then((data) => {
              console.log(data);
              if (data.unread_count > 0) {
                chatNotifDisplay = document.querySelector(
                  `#chat_notification_${elem.following.id}`
                );
                chatNotifDisplay.textContent = data.unread_count;
                chatNotifDisplay.setAttribute(
                  "style",
                  "width:1.3vw;height:1.3vw"
                );
              }
            });
        }
      });

      console.log(data);
    } else if (this.status > 400 || (this.status > 0 && this.status < 200)) {
      console.error("Request failed with status: " + this.status);
    }
  };

  request.open("GET", "/api/friendList", true);

  request.send();
}
//---END OF CODE THAT I WROTE---

// This function fetches and displays a list of all friends for the current user.
function allRequestList() {
  // Makes an XMLHttpRequest to fetch a list of all friends.
  // Displays the list of friends on the webpage.
  var request = new XMLHttpRequest();

  request.onreadystatechange = function () {
    if (this.readyState == 4 && this.status >= 200 && this.status < 400) {
      console.log(this.status);
      var data = JSON.parse(this.responseText);
      if (data) {
        data.forEach((elem) => {
          if (elem.requested_user.user.username == username) {
            emptyRequestListDisplay.setAttribute("style", "display:none;");
            requestListContainerElem.innerHTML += `
            
            <li >
            <a href="../user_profile/${elem.requester.user.username}">
            <img
            src=${
              elem.requester.profile_image
                ? elem.requester.profile_image
                : "../../static/assets/blank-profile.jpeg"
            }
            alt=""
            />
            <p>${elem.requester.name}</p>
            <a href="../follow/?following=${
              elem.requester.user.username
            }"> <button style="background-color:green">Accept</button></a>
            <a href="../request/?requestedUserId=${
              elem.requested_user.id
            }&requesterId=${
              elem.requester.id
            }"> <button style="background-color:red">Reject</i></button></a>

              </a>

              </li>
              
              `;
          }
        });
      }

      console.log(data);
    } else if (this.status > 400 || (this.status > 0 && this.status < 200)) {
      console.error("Request failed with status: " + this.status);
    }
  };

  request.open("GET", "/api/requestList", true);

  request.send();
}

//---I WROTE THIS CODE---
// This function fetches and displays a list of gallery posts for the current user.
function galleryList() {
  // Makes an XMLHttpRequest to fetch a list of gallery posts.
  // Displays the gallery posts on the webpage.
  var request = new XMLHttpRequest();

  request.onreadystatechange = function () {
    if (this.readyState == 4 && this.status >= 200 && this.status < 400) {
      console.log(this.status);
      var data = JSON.parse(this.responseText);

      data.forEach((elem) => {
        let currentUser = contact_username ? contact_username : username;
        if (elem.appuser.user.username == currentUser) {
          if (document.querySelector("#no_post")) {
            document.querySelector("#no_post").remove();
          }
          // Convert elem.created_at to a JavaScript Date object
          const createdAtDate = new Date(elem.created_at);

          // Assuming 'createdAtDate' is your Date object
          const formattedDate = createdAtDate.toLocaleDateString("en-GB", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
          });
          
          postContainerElem.innerHTML += `
  <li>
    ${
      contact_id
        ? ""
        : `<a class="post_delete" href="../deletePost/${elem.id}" ><i class="fas fa-trash-alt"></i></a>`
    }
    
    ${
      elem.post_media
        ? /\.(mp4|webm|ogg)$/.test(elem.post_media)
          ? `<video controls><source src="${elem.post_media}" type="video/mp4"></video>`
          : `<img src="${elem.post_media}" alt="Post media" width="400" height="300" />`
        : `<img src="../../static/assets/annie-spratt-zA7I5BtFbvw-unsplash.jpeg" alt="Default image" width="400" height="300" />`
    }
    
    <div class="post_footer">
      <div class="likes_date">
        <p class="likes_container">
        <a id="like_${elem.id}" onclick="increment(${
            elem.id
          },true);" ><i class="fas fa-thumbs-up"></i></a> 
        <a id="unlike_${elem.id}" style="display:none" onclick="increment(${
            elem.id
          },false);" ><i style="color:red" class="fas fa-thumbs-up"></i></a> 
        <span id="likes_${elem.id}"> ${elem.likes}</span>
        </p>
        <p class="post_date">${formattedDate}</p>
      </div>
      <div class="desc">
        ${elem.description}
      </div>
    </div>
  </li>
`;
        }
      });

      console.log(data);
    } else if (this.status > 400 || (this.status > 0 && this.status < 200)) {
      console.error("Request failed with status: " + this.status);
    }
  };

  request.open("GET", "/api/galleryList", true);

  request.send();
}
//---END OF CODE THAT I WROTE---

//---I WROTE THIS CODE---
// This function increments the number of likes for a gallery post.
function increment(id, isLike) {
  // Increments the like count for a specific gallery post.
  // Sends a PUT request to update the like count on the server.
  let likes = parseInt(document.querySelector(`#likes_${id}`).textContent);
  if (isLike) {
    document.querySelector(`#like_${id}`).setAttribute("style", "display:none");
    document
      .querySelector(`#unlike_${id}`)
      .setAttribute("style", "display:inline");
    likes += 1;
  } else {
    document
      .querySelector(`#unlike_${id}`)
      .setAttribute("style", "display:none");
    document
      .querySelector(`#like_${id}`)
      .setAttribute("style", "display:inline");
    likes -= 1;
  }

  document.querySelector(`#likes_${id}`).textContent = likes;

  // Create a new XMLHttpRequest object
  var xhr = new XMLHttpRequest();

  // Define the HTTP method and the URL
  var method = "PUT"; // PUT request
  var url = `/api/updateLikes/${id}`; // Replace with your API endpoint and resource ID

  // Create the data to send (assuming it's a JSON payload)
  var data = JSON.stringify({
    likes: likes,
  });

  // Configure the request
  xhr.open(method, url, true); // true for asynchronous, false for synchronous

  // Set request headers (optional)
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.setRequestHeader("X-CSRFToken", csrftoken); // Set the CSRF token header

  // Set up a callback function to handle the response
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      // 4 means the request is complete
      if (xhr.status === 200) {
        // 200 means a successful response
        // Parse the response data (assuming it's JSON)
        var responseData = JSON.parse(xhr.responseText);
        console.log(responseData);
      } else {
        // Handle errors or other HTTP status codes
        console.error("Request failed with status: " + xhr.status);
      }
    }
  };

  // Send the request with the data
  xhr.send(data);

  // Note: Replace the URL with the actual endpoint and resource ID you want to update.
  // Also, adjust the data and response handling logic according to your specific use case.
}
//---END OF CODE THAT I WROTE---

//---I WROTE THIS CODE---
// This function fetches and displays the user's status on the webpage.
function getStatus() {
  // Makes an XMLHttpRequest to fetch the user's status.
  // Displays the user's status on the webpage.
  var request = new XMLHttpRequest();

  request.onreadystatechange = function () {
    if (this.readyState == 4 && this.status >= 200 && this.status < 400) {
      console.log(this.status);
      var data = JSON.parse(this.responseText);

      data.forEach((elem) => {
        let currentUser = contact_username ? contact_username : username;
        if (elem.appuser.user.username == currentUser) {
          // Convert elem.created_at to a JavaScript Date object
          const createdAtDate = new Date(elem.created_at);

          // Assuming 'createdAtDate' is your Date object
          const formattedDate = createdAtDate.toLocaleDateString("en-GB", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
          });
          if (elem.status == "" || elem.status == null) {
            statusElem.innerHTML = `
               <h2 id=no_status>No Status</h2>
             
             `;
          } else {
            statusElem.innerHTML = `
                <p id="status_text">${elem.status}</p>
                <p id="status_createdAt">Updated On: <span>${formattedDate}</span></p>
             
             `;
          }
        }
      });

      console.log(data);
    } else if (this.status > 400 || (this.status > 0 && this.status < 200)) {
      console.error("Request failed with status: " + this.status);
    }
  };

  request.open("GET", "/api/statusList", true);

  request.send();
}

//---END OF CODE THAT I WROTE---
