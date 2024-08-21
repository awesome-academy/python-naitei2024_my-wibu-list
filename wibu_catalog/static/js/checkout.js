function showDetails(detailId) {
    // Hide all payment details
    document.querySelectorAll(".payment-details").forEach((detail) => {
        detail.style.display = "none";
    });

    // Show the selected payment details
    document.getElementById(detailId).style.display = "block";
}
