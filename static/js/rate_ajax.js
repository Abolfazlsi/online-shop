function rating(slug) {
    let rate = document.getElementById("rating")
    let rate_count = document.getElementById("rating_count")

    $.get(`/product/rating/${slug}`).then(response => {
        if (response["response"] === "rating") {
            rate.className = "fa fa-star text text-warning"
            rate_count.innerText = Number(rate_count.innerText) + 1
        } else {
            rate.className = "fa fa-star text text-dark"
            rate_count.innerText = Number(rate_count.innerText) - 1

        }
    })
}
