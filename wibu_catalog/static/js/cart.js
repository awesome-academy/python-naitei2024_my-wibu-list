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
        var product_id = $(this).data("product-id");
        var subtotal = $(this).data("subtotal");
        var checked = $(this).is(":checked");
        var quantity = $(this).data("quantity");
        console.log("Value of checked: ", quantity);

        $.ajax({
            url: '/update-cart-item/',  // Update this to the correct URL
            type: 'POST',
            data: {
                'product_id': product_id,
                'quantity': quantity,
                'subtotal': subtotal,
                'checked': checked,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response){
                // Update the cart total
                updateCartTotal();
            },
            error: function(response){
                console.log("Error: ", response);
            }
        });
    });
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
$(".quantity-input").each(function () {
    $(this).change(function () {
        var quantity = parseInt($(this).val());
        var inventory = parseInt($(this).data("inventory"));

        if (quantity > inventory) {
            alert(
                "The quantity you want to order is greater than the inventory"
            );
            $(this).val(inventory); // Set the input value to the maximum inventory
        } else if (quantity <= 0) {
            alert("The quantity must be greater than 0");
            $(this).val(1); // Set the input value to the minimum valid quantity
        } else {
            // Update the quantity in the cart
            var productId = $(this).data("product-id");
            var newQuantity = $(this).val();

            $.ajax({
                type: "POST",
                url: "/update_cart/", // Update this to the URL of your update cart endpoint
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
                },
            });
        }
    });
});

$(".quantity-input").change(function () {
    var newQuantity = $(this).val();
    var productId = $(this).data("product-id");
    updateQuantity(productId, newQuantity);
});
