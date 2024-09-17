document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.quantity-btn').forEach(button => {
      button.addEventListener('click', function() {
          const action = this.getAttribute('data-action');
          const itemId = this.getAttribute('data-item-id');
          const input = this.parentElement.querySelector('input');
          const itemPrice = parseFloat(this.parentElement.parentElement.querySelector('.item-price').innerText.replace('₹', ''));
          let quantity = parseInt(input.value, 10);

          if (action === 'increase') {
              quantity += 1;
          } else if (action === 'decrease' && quantity > 1) {
              quantity -= 1;
          }

          // Update quantity in the input field
          input.value = quantity;

          // Calculate the new subtotal
          const subtotal = quantity * itemPrice;
          this.parentElement.parentElement.querySelector('.item-subtotal').innerText = `₹${subtotal.toFixed(2)}`;

          // Update the cart on the server
          fetch(`/cart/update/${itemId}/`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCookie('csrftoken') // Ensure you have CSRF token handling
              },
              body: JSON.stringify({ quantity: quantity })
          })
          .then(response => response.json())
          .then(data => {
              if (data.status === 'success') {
                  // Update cart summary
                  document.querySelector('.cart-summary .summary-details p span.subtotal').innerText = `₹${data.total_price.toFixed(2)}`;
                  document.querySelector('.cart-summary .summary-details p span.total').innerText = `₹${data.total_price.toFixed(2)}`;
              } else {
                  console.error('Error:', data.message);
              }
          })
          .catch(error => console.error('Error:', error));
      });
  });
});

// Utility function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; cookies.length > i; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}