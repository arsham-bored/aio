let checkbox = {

    // apply
    m: document.querySelector("#m"),
    raider : document.querySelector("#raider"),

    cloth: document.querySelector("#cloth"),
    plate: document.querySelector("#plate"),
    leather: document.querySelector("#leather"),
    mail: document.querySelector("#mail"),
}

let alertMessage = document.querySelectorAll(".alert")
let form = document.querySelector("form")

form.onsubmit = function(form) {
    if (!checkbox.m.checked && !checkbox.raider.checked) {
        alertMessage[0].classList.remove("hidden")
        return false
    }

    if (
        !checkbox.cloth.checked &&
        !checkbox.plate.checked &&
        !checkbox.leather.checked &&
        !checkbox.mail.checked
    ) {
        alertMessage[1].classList.remove("hidden")
        return false
    }

    return true
}