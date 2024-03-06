import { isLoggedIn } from "./utility.js";

const applyBtns=document.querySelectorAll(".apply-btn");

applyBtns.forEach((applyBtn)=>{
  applyBtn.addEventListener("click",async (evt)=>{
    evt.preventDefault();
    console.log("Button clicked");
    if (!(await isLoggedIn())) {
      console.log("event prevented");
      alert("Please login before apply");
      evt.preventDefault();
    } else{
      window.location.href = applyBtn.href;
    }
  });
});