var username = JSON.parse(document.getElementById("username").textContent);
var id = JSON.parse(document.getElementById("id").textContent);
var contact_username = JSON.parse(document.getElementById("contact_username").textContent);
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
var friendFormElem = document.querySelector("#friend_form");
var friendListContainerElem=document.querySelector('#friend_list_container ul');
var link = document.querySelector("#friend_list_container a");
var chatButton = document.querySelector("#friend_list_container button");
var likesElem=document.querySelector("#likes");
var postDateElem = document.querySelector("#post_date");
var descriptionElem = document.querySelector("#desc");
var postContainerElem = document.querySelector("#post_container");
var statusTextElem=document.querySelector("#status_text");
var statusCreatedAtElem = document.querySelector("#status_createdAt span");
var statusElem = document.querySelector("#status");









//---I WROTE THIS CODE---
//Execute all functions 
getAllUsers();
allFriendsList();

if(contact_username){
checkIfFriend();
}
 galleryList()
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

  request.open("GET", "http://127.0.0.1:8080/api/users", true);

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
        emailElem.firstElementChild.textContent = elem.email;
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
             <a href="../user_home/${elem.user.username}">
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
  var url = "http://127.0.0.1:8080/api/checkRowExists/"; // Correct URL

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
        friendFormElem.innerHTML += `
        <button type="submit" id="follow_button">
          unFriend
        </button>
        
        `;
      } else {
        friendFormElem.innerHTML += `
        
        <button type="submit" id="follow_button">
          Friend
        </button>
        
        `;
      }

      console.log(data);
    } else if (this.status > 400 || (this.status > 0 && this.status < 200)) {
      console.error("Request failed with status: " + this.status);
    }
  };

  request.send();
}
//---END OF CODE THAT I WROTE---

//---I WROTE THIS CODE---
// This function fetches and displays a list of all friends for the current user.
function allFriendsList(){
  // Makes an XMLHttpRequest to fetch a list of all friends.
  // Displays the list of friends on the webpage.
  var request = new XMLHttpRequest();

  request.onreadystatechange = function () {
    if (this.readyState == 4 && this.status >= 200 && this.status < 400) {
      console.log(this.status);
      var data = JSON.parse(this.responseText);

      data.forEach((elem) => {
        if (elem.current_user.user.username == username) {
          friendListContainerElem.innerHTML += `
          
          <li >
             <a href="../user_home/${elem.following.user.username}">
              <img
                src=${
                  elem.following.profile_image
                    ? elem.following.profile_image
                    : "../../static/assets/blank-profile.jpeg"
                }
                alt=""
              />
              <p>${elem.following.name}</p>
              <a href="../chatRoom/${
                elem.following.user.username
              }"> <button>Chat</button></a>
              </a>

              </li>
             
                `;
        }
      });

      console.log(data);
    } else if (this.status > 400 || (this.status > 0 && this.status < 200)) {
      console.error("Request failed with status: " + this.status);
    }
  };

  request.open("GET", "http://127.0.0.1:8080/api/friendList", true);

  request.send();
}
//---END OF CODE THAT I WROTE---

//---I WROTE THIS CODE---
// This function fetches and displays a list of gallery posts for the current user.
function galleryList(){
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

          // Format the date as a string (e.g., "YYYY-MM-DD HH:MM:SS")
          const formattedDate = createdAtDate.toLocaleString();
          postContainerElem.innerHTML += `
          
          <li>
            ${
              contact_id
                ? ""
                : `<a id="post_delete" href="../deletePost/${elem.id}" ><i class="fas fa-trash-alt"></i></a>`
            }
          
           <img
                src=${
                  elem.post_image
                    ? elem.post_image
                    : "../../static/assets/annie-spratt-zA7I5BtFbvw-unsplash.jpeg"
                }
                alt=""
              />
            <div id="post_footer">
             <div id="likes_date">
              <p id="likes_container"><a onclick="increment(${
                elem.id
              });" ><i  class="fas fa-thumbs-up"> </i></a> <span id="likes_${
            elem.id
          }"> ${elem.likes}</span></p>
              <p id="post_date">${formattedDate}</p>
              
             </div>
             <div id="desc">
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

  request.open("GET", "http://127.0.0.1:8080/api/galleryList", true);

  request.send();
}
//---END OF CODE THAT I WROTE---

//---I WROTE THIS CODE---
// This function increments the number of likes for a gallery post.
function increment(id){
  // Increments the like count for a specific gallery post.
  // Sends a PUT request to update the like count on the server.
  let likes = parseInt(document.querySelector(`#likes_${id}`).textContent);
  likes += 1;

  document.querySelector(`#likes_${id}`).textContent = likes;

  // Create a new XMLHttpRequest object
  var xhr = new XMLHttpRequest();

  // Define the HTTP method and the URL
  var method = "PUT"; // PUT request
  var url = `http://127.0.0.1:8080/api/updateLikes/${id}`; // Replace with your API endpoint and resource ID

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
function getStatus(){
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

          // Format the date as a string (e.g., "YYYY-MM-DD HH:MM:SS")
          const formattedDate = createdAtDate.toLocaleString();
          if (elem.status == "" || elem.status == null) {
            statusElem.innerHTML = `
               <h2 id=no_status>No Status</h2>
             
             `;
          } else {
            statusElem.innerHTML = `
                <p id="status_text">${elem.status}</p>
                <p id="status_createdAt">Updated At: <span>${formattedDate}</span></p>
             
             `;
          }
        }
      });

      console.log(data);
    } else if (this.status > 400 || (this.status > 0 && this.status < 200)) {
      console.error("Request failed with status: " + this.status);
    }
  };

  request.open("GET", "http://127.0.0.1:8080/api/statusList", true);

  request.send();
}



//---END OF CODE THAT I WROTE---




