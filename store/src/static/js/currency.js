    // Take currency elements
    const currencyElements = document.querySelectorAll('.currency');
    currencyElements.forEach(element => {
        element.textContent = new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(element.textContent);
    });