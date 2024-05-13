function addToWishlist(movieId) {
    fetch('/add_to_wishlist/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({'movieId': movieId})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Update the UI based on response
    });
}
