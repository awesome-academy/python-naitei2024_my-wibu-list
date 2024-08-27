function removeItem(itemId) {
    // Create a new FormData object
    var formData = new FormData();
    formData.append("item_id", itemId);

    // Send a POST request to the server
    fetch("/remove-from-cart/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCookie("csrftoken"), // Assuming you have a function to get the CSRF token
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                // Update the cart total on the page
                document.getElementById("cart-total").textContent =
                    data.cart_total;
                document.getElementById("item-" + itemId).remove();
            } else {
                // Handle the error
                console.error(data.error);
            }
        })
        .catch((error) => {
            // Handle the error
            console.error(error);
        });
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

function updateCartTotal() {
    var cartItems = document.getElementsByClassName("cart-item");
    var newTotal = 0;

    // Loop through all cart items
    for (var i = 0; i < cartItems.length; i++) {
        // Get the checkbox and subtotal for this item
        var checkbox = cartItems[i].getElementsByClassName("select-input")[0];
        var subtotal = parseFloat(
            cartItems[i]
                .getElementsByClassName("product-subtotal")[0]
                .innerText.replace("₫", "")
        );

        // If the checkbox is checked, add the subtotal to the total
        if (checkbox.checked) {
            newTotal += subtotal;
        }
    }

    // Update the total
    $("#cart-total").text(`₫${newTotal.toFixed(2)}`);

    // Show the empty cart message if the total is 0
    if (newTotal === 0) {
        $("#empty-cart").show();
    } else {
        $("#empty-cart").hide();
    }
}

// Add a change event listener to each checkbox
$(document).ready(function () {
    $(".select-input").change(function () {
        updateCartTotal();
    });

    // Call updateCartTotal to initialize the total
    updateCartTotal();
});
function updateQuantity(productId, newQuantity) {
    // Send an AJAX request to the server
    $.ajax({
        url: "/update-quantity/", // Update this to the URL of your view
        type: "POST",
        data: {
            product_id: productId,
            quantity: newQuantity,
            csrfmiddlewaretoken: "{{ csrf_token }}",
        },
        success: function (response) {
            // Update the subtotal
            $("#item-" + productId + " .product-subtotal").text(
                "₫" + response.new_subtotal.toFixed(2)
            );

            // Update the quantity in the session
            sessionStorage.setItem("product-" + productId, newQuantity);

            // Check if the item is checked
            var isChecked = $("#item-" + productId + " .select-input").prop(
                "checked"
            );
            if (isChecked) {
                // Update the total
                updateCartTotal();
            }
        },
    });
}

// Add event listeners to quantity inputs
$(".quantity-input").change(function () {
    var newQuantity = $(this).val();
    var productId = $(this).data("product-id");
    updateQuantity(productId, newQuantity);
});
