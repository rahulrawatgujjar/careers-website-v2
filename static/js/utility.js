// user login or not
export async function isLoggedIn(){
  try{
    let response= await fetch("/check_login");
    if (!response.ok){
      throw new Error("Network response was not ok");
    }
    let data=await response.json();
    return data.logged_in;
  } catch(error){
    console.log(error);
  }
}