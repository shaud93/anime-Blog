var create_user_botton = document.getElementById("create_u")

function Go_Add_User()
{
    window.location.href = "/user/create"
}

create_user_botton.addEventListener("click", Go_Add_User)