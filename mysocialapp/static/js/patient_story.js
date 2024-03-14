const searchInput = document.getElementById("disease_overview_search_input");
const searchList = document.getElementById("disease_overview_search_list");
const searchButton = document.getElementById("content_search");

let debounceTimer;

searchInput.addEventListener("input", function (e) {
  clearTimeout(debounceTimer); // Clear the previous timer
  const query = e.target.value;

  // Set a new timer
  debounceTimer = setTimeout(() => {
    if (query.length >= 0) {
      // Check if the query length is at least 2
      fetch(`/api/search_patient_story/?q=${query}`)
        .then((response) => response.json())
        .then((data) => {
          if (data != null && data != " ") {
            const searchListUl = searchList.querySelector("ul");
            searchList.style.display = "block";
            searchListUl.innerHTML = ""; // Clear previous results

            data.forEach((item) => {
              searchListUl.innerHTML += `
              <li class="list_title">
             <a style="text-decoration: none; color:black" href="../patient_story/?contentId=${item.id}#information_content_container">
              
              ${item.title}
              </a>

              </li>
              `;
            });
          }
        })
        .catch((error) => console.error("Error fetching data:", error));
    }
  }, 1000); // Wait for 1 second (1000 milliseconds) before executing the fetch
});

document.addEventListener("click", function (event) {
  const isClickInsideInput = searchInput.contains(event.target);
  const isClickInsideList = searchList.contains(event.target);

  if (!isClickInsideInput && !isClickInsideList) {
    // Hide the search list
    searchList.style.display = "none";
    // Clear the input field
    searchInput.value = "";
  }
});

searchButton.addEventListener("click", function () {
  let query = searchInput.value.trim();
  query = " " + query + " ";
  // Redirect to the URL handled by your Django view, including the query parameter
  if (query != "") {
    window.location.href = `/patient_story_list/?q=${encodeURIComponent(
      query
    )}#information_content_container`;
  }
});
