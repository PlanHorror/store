// Init format all numbers
let numbers = document.querySelectorAll('.currency');
numbers.forEach(number => {
    number.textContent = formatNumber(parseInt(number.textContent));
});
// Init product total
let products = document.querySelectorAll('.product-card');
let total = 0;
let realTotal = 0;
products.forEach(product => {
    let price = parseInt(product.querySelector('.product-price').textContent);
    let quantity = parseInt(product.querySelector('input').value);
    let real_price = parseInt(product.querySelector('.product-real-price').textContent);
    let realProductTotal = real_price * quantity;
    total += price * quantity;
    realTotal += realProductTotal;
});
document.getElementById('total').textContent = formatNumber(total);
document.getElementById('real-total').textContent = formatNumber(realTotal);
function calculateTotal() {
    let total = 0;
    let realTotal = 0;
    let products = document.querySelectorAll('.product-card');
    products.forEach(product => {
        let price = parseInt(product.querySelector('.product-price').textContent);
        let quantity = parseInt(product.querySelector('input').value);
        total += price * quantity;
        realTotal += parseInt(product.querySelector('.product-real-price').textContent) * quantity;
    });
    document.getElementById('total').textContent = formatNumber(total);
    document.getElementById('real-total').textContent = formatNumber(realTotal);
}
function addQuantity(id) {
    let quantity = parseInt(document.getElementById(`quantity-${id}`).value);
    quantity += 1;
    document.getElementById(`quantity-${id}`).value = quantity;
    updateQuantity(id);
}
function subQuantity(id) {
    let quantity = parseInt(document.getElementById(`quantity-${id}`).value);
    if (quantity > 1) {
        quantity -= 1;
        document.getElementById(`quantity-${id}`).value = quantity;
        updateQuantity(id);
    }
}
function updateQuantity(id) {
    let quantity = parseInt(document.getElementById(`quantity-${id}`).value);
    if (quantity < 1) {
        quantity = 1;
        document.getElementById(`quantity-${id}`).value = quantity;
    } else if (quantity > 10) {
        quantity = 10;
        document.getElementById(`quantity-${id}`).value = quantity;
    }
    // if quantity is not number, set it to 1
    if (isNaN(quantity)) {
        quantity = 1;
        document.getElementById(`quantity-${id}`).value = quantity;
    }
    let real_price = parseInt(document.getElementById(`real-product-price-${id}`).textContent);
    let realProductTotal = real_price * quantity;
    document.getElementById(`product-price-total-${id}`).textContent = formatNumber(realProductTotal);
    calculateTotal();
}
function formatNumber(number) {
    console.log(number);
    console.log(number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + "đ");
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + "đ";
}