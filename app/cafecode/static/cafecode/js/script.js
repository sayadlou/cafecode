//ghasem
// Scroll Page for Menu Items:
var dotItems = $("#rightMenu .dots").length;
console.log("Circled Menu Items = " + dotItems + "x");
for (i = 0; i < dotItems; i++) {
    document.querySelectorAll("#rightMenu .dots")[i].text = "";
};

// Change Menu Style on Scroll
window.onscroll = function() {scrollFunction()};
function scrollFunction() {
  // if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
  //   document.getElementById("navbar").classList.add("nav-fix");
  // } else {
  //   document.getElementById("navbar").classList.remove("nav-fix");
  // }
}

// check and uncheck Items:
var items = document.querySelectorAll(".list-group .form-control").length;
for (i = 0; i < items; i++) {
    document.querySelectorAll(".list-group .form-control")[i].classList.add("item-uncheck");
    document.querySelectorAll(".list-group .form-control")[i].onclick = function () {
        this.classList.toggle("item-check");
    };
}

// Price Calculator
let startPrice = 2500;
let totalPrice = startPrice;

$(document).ready(function() {
    $('.item-uncheck').click(function() {
        var itemPrice = $(this).attr('value');
        totalPrice += itemPrice*1;
        console.log("Start Price: " + startPrice + " / Item Price: " + itemPrice + " / Total Price: " + totalPrice);
    });
});

document.getElementById("price").innerHTML = "<h4>Preis: " + totalPrice + " €</h4>";

// email
var email = document.getElementById("id_email");

if ($('#alart-body').children().length === 0) {
    $("#alert-div").addClass("d-none");
} else {
    $("#alert-div").removeClass("d-none");
}

$('#stage1').click(evt => {
        if (email.validity.valid) {
            var accountType = $('#id_account_type').val();
            setTimeout(function () {
                if (accountType === 'Personal') {
                    $('#intro-sign').carousel(2);
                } else if (accountType === 'Company') {
                    $('#intro-sign').carousel(1);
                }
            }, 200);
        } else {
            alert("enter a valid Email")
        }
    }
)
