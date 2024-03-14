
const bodyElem=document.querySelector("body");
const themeButtonList=document.querySelectorAll(".theme-btn");
const textSizeElem=document.querySelector("#text-size");
const resetButton=document.querySelector("#reset-btn");
const slideUp=document.querySelector("#slideUp");
const slideDown = document.querySelector("#slideDown");
const contentContainer=document.querySelector("#accessibility-content-container");


let storedThemeData=sessionStorage.getItem("theme");
let storedTextColorData = sessionStorage.getItem("textColor");
let storedTextSize = sessionStorage.getItem("textSize");

let readAloudEnabled = false;



if(storedThemeData && storedTextColorData){
  bodyElem.setAttribute("style",`background-color:${storedThemeData};color:${storedTextColorData}`);
  themeButtonList.forEach((button) => {
    if (button.getAttribute("data-theme") === storedThemeData) {
      button.classList.add("active");
    } else {
      button.classList.remove("active");
    }
  });
}

if(storedTextSize){
  bodyElem.style.fontSize = storedTextSize;
  textSizeElem.value = storedTextSize; 
}

function changeTheme(theme,textColor){
 
  themeButtonList.forEach(elem=>{
  if(elem.getAttribute("data-theme")==theme){
    elem.classList.add("active");
    //bodyElem.setAttribute("style",`background-color:${theme};color:${textColor}`);
   
    bodyElem.style.backgroundColor = theme;
    bodyElem.style.color = textColor;

    sessionStorage.setItem("theme",theme);
    sessionStorage.setItem("textColor", textColor);


  }
  else{
    if(elem.classList.contains("active")){
       elem.classList.remove("active");
    }
    }


  });

 
}


textSizeElem.addEventListener("change",(e)=>{
 bodyElem.style.fontSize = e.target.value;
 sessionStorage.setItem("textSize", e.target.value);
})



const toggleReadAloud = () => {
  readAloudEnabled = !readAloudEnabled;
  if (readAloudEnabled) {
    document.getElementById("readAloudToggle").textContent =
      "Disable Read Aloud";
  } else {
    document.getElementById("readAloudToggle").textContent =
      "Enable Read Aloud";
    window.speechSynthesis.cancel(); // Stop any ongoing speech
  }
};

document
  .getElementById("readAloudToggle")
  .addEventListener("click", toggleReadAloud);

document.addEventListener("click", function (event) {
  
  if (readAloudEnabled && event.target.textContent) {
    const speech = new SpeechSynthesisUtterance(event.target.textContent);
    window.speechSynthesis.speak(speech);
  }
});


resetButton.addEventListener("click",(e)=>{
  bodyElem.removeAttribute("style");
  sessionStorage.removeItem("theme");
  sessionStorage.removeItem("textSize");
  sessionStorage.removeItem("textColor");

  themeButtonList.forEach((button) => {
    button.classList.remove("active");
  });


 textSizeElem.value = "100%"; 
 
    
      readAloudEnabled =false;
      document.getElementById("readAloudToggle").textContent =
        "Enable Read Aloud";
      window.speechSynthesis.cancel(); // Stop any ongoing speech
   
});


slideUp.addEventListener("click",(e)=>{
  contentContainer.setAttribute("style","display:block");
  
  slideDown.setAttribute("style","display:block")
  slideUp.setAttribute("style", "display:none");
})

slideDown.addEventListener("click", (e) => {
  contentContainer.setAttribute("style", "display:none");
  
  slideDown.setAttribute("style", "display:none");
  slideUp.setAttribute("style", "display:block");
});