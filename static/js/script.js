import {isLoggedIn} from "./utility.js";

const loginBtn= document.querySelector("#login");
const logoutBtn= document.querySelector("#logout");


async function changeVisibility(){
  if (await isLoggedIn()){
    loginBtn.style.display= "none";
    logoutBtn.style.display= "inline-block"
  } else {
    loginBtn.style.display= "inline-block";
    logoutBtn.style.display= "none"
  }
}

window.addEventListener("load",()=>{
  changeVisibility();
});