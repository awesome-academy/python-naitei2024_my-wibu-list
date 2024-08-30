function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
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

const csrftoken = getCookie("csrftoken");

document
    .getElementById("add-to-cart-btn")
    .addEventListener("click", function () {
        var url = this.getAttribute("data-url");
        var product_id = this.getAttribute("data-product-id");
        var quantity = parseInt(
            document.getElementById("quantity-input").value
        );
        var inventory = this.getAttribute("data-inventory");
        var sl_in_cart = parseInt(
            document.getElementById("quantity-input").getAttribute("sl-in-cart")
        );

        if (quantity + sl_in_cart > inventory) {
            alert("Số lượng sản phẩm trong giỏ hàng vượt quá số lượng tồn kho");
            document.getElementById("error-modal").style.display = "block";
        } else if (quantity <= 0) {
            document.getElementById("error-modal").style.display = "block";
        } else {
            fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify({
                    product_id: product_id,
                    quantity: quantity,
                }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        // Show a notification and open the modal
                        document.getElementById(
                            "notification-modal"
                        ).style.display = "block";
                    } else {
                        console.error(data.error);
                        document.getElementById("error-modal").style.display =
                            "block";
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                    document.getElementById("error-modal").style.display =
                        "block";
                });
        }
    });

function closeModal() {
    document.getElementById("notification-modal").style.display = "none";
    document.getElementById("error-modal").style.display = "none";
}
