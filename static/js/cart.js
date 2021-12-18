var updateButtons = document.getElementsByClassName('update-cart')

//Loop for all the add buttons
for (var i = 0; i < updateButtons.length; i++) {
    updateButtons[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)
        
        updateUserOrder(productId, action)
    })
}

function updateUserOrder(productId, action) {
    console.log('sending data...')

    var url = '/update_item/'
    //post request
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })

        //promise, turn the data to json value
        .then((response) => {
            return response.json()
        })

        .then((data) => {
            console.log('data:', data) //jsonresponse from views.py
            location.reload()
        })
}