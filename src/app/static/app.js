let checkbox = {
  // apply
  m: document.querySelector("#m"),
  raider: document.querySelector("#raider"),

  cloth: document.querySelector("#cloth"),
  plate: document.querySelector("#plate"),
  leather: document.querySelector("#leather"),
  mail: document.querySelector("#mail"),
};

let alertMessage = document.querySelectorAll(".alert");
let form = document.querySelector("form");

let category;

let horde = document.querySelector("#horde");
let aliance = document.querySelector("#alliance");

let realm = document.querySelector("#realm");

horde.addEventListener("click", function (e) {
  e.preventDefault();
  category = "horder";

  horde.classList.add("active");
  aliance.classList.remove("active");
});

aliance.addEventListener("click", function (e) {
  e.preventDefault();
  category = "aliance";

  aliance.classList.add("active");
  horde.classList.remove("active");
});

form.onsubmit = function (form_data) {
  if (!checkbox.m.checked && !checkbox.raider.checked) {
    alert("please specify what you are applying for.");
    return false;
  }

  if (category == undefined) {
    alert("please specify you category");
    return false;
  }

  if (
    !checkbox.cloth.checked &&
    !checkbox.plate.checked &&
    !checkbox.leather.checked &&
    !checkbox.mail.checked
  ) {
    alert("please specify what armor classes you can boost with.");
    return false;
  }

  if (!realm.value.includes("-")) {
    alert("please follow examples to fill real and character");
    return false;
  }

  let cat = document.createElement("input");
  cat.type = "hidden";
  cat.name = "category";
  cat.value = category;

  form.appendChild(cat);

  return true;
};
