function orderView(show) {
    // tabs
    var tabs = document.querySelectorAll('.tab-button')

    // orders
    var current, past
    current = document.querySelector('#current')
    past = document.querySelector('#past')

    // displaying and hiding contents as needed
    if(show == 'past') {
        // swapping from current to past and vice versa
        past.setAttribute('style', 'display: block;')
        current.setAttribute('style', 'display: none;')
    } else {
        // swapping from past to current
        past.setAttribute('style', 'display: none;')
        current.setAttribute('style', 'display: block;')
    }

    for(let tab of tabs) {
        if (tab == event.target) {
            tab.classList.add('active')
        } else {
            tab.classList.remove('active')
        }
    }
}

function updateCost() {
    var cost = document.querySelector('#cost')
    cost.textContent = (event.target.value * 50).toLocaleString()
}

function search() {
    var input, query, rows;
    input = document.querySelector('#searchBtn')

    // search query
    query = input.value.toLowerCase().trim()
    
    // NodeList of staff rows from table body
    rows = (document.querySelectorAll('.order'))

    for(let row of rows) {
        // staff name from class name
        let name = row.className.toLowerCase()
        if(name.includes(query)) {
            row.removeAttribute('style')
        } else {
            row.setAttribute('style', 'display: none;')
        }
    }
}

// close flash message
function dismissFlash() {
    var flash = document.getElementsByClassName('pop-flash')[0]
    console.log(flash);
    flash.style.opacity = 0 // start fading out
    setTimeout(function(){
        flash.style.display = 'none'
    }, 600) // duration in milliseconds of fade out
}

setTimeout(dismissFlash, 5000)