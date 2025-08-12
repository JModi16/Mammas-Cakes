class ShoppingCart {
    constructor() {
        // Only initialize if user is authenticated
        if (!isAuthenticated) {
            console.log('User not authenticated - cart disabled');
            return;
        }
        
        this.items = JSON.parse(localStorage.getItem('cart')) || [];
        this.deliveryFee = 3.99;
        this.updateCartDisplay();
        this.bindEvents();
    }

    // Check authentication before any cart operation
    requireAuth() {
        if (!isAuthenticated) {
            const loginModal = new bootstrap.Modal(document.getElementById('loginRequiredModal'));
            loginModal.show();
            return false;
        }
        return true;
    }

    // Add item to cart (requires authentication)
    addItem(id, name, price, image) {
        if (!this.requireAuth()) return;
        
        const existingItem = this.items.find(item => item.id === id);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            this.items.push({
                id: id,
                name: name,
                price: parseFloat(price),
                image: image,
                quantity: 1
            });
        }
        
        this.saveCart();
        this.updateCartDisplay();
        this.showCartNotification(`${name} added to cart!`);
    }

    // Enhanced checkout with Django backend
    async checkout() {
        if (!this.requireAuth()) return;
        
        if (this.items.length === 0) {
            alert('Your cart is empty!');
            return;
        }
        
        this.showCheckoutModal();
    }

    // Process order through Django backend
    async processOrder() {
        const isDelivery = document.getElementById('delivery-option')?.checked;
        const subtotal = this.getTotal();
        const total = isDelivery ? subtotal + this.deliveryFee : subtotal;
        
        // Collect all form data
        const orderData = {
            customer: {
                name: document.getElementById('customer-name').value,
                email: document.getElementById('customer-email').value,
                phone: document.getElementById('customer-phone').value
            },
            orderType: isDelivery ? 'delivery' : 'collection',
            specialInstructions: document.getElementById('special-instructions').value,
            items: this.items,
            subtotal: subtotal,
            deliveryFee: isDelivery ? this.deliveryFee : 0,
            total: total
        };
        
        if (isDelivery) {
            orderData.delivery = {
                address: document.getElementById('delivery-address').value,
                city: document.getElementById('delivery-city').value,
                postcode: document.getElementById('delivery-postcode').value,
                date: document.getElementById('delivery-date').value,
                time: document.getElementById('delivery-time').value || 'Any time'
            };
        } else {
            orderData.collection = {
                date: document.getElementById('collection-date').value,
                time: document.getElementById('collection-time').value,
                location: "Mamma's Cakes Bakery, 123 Baker Street, London, W1U 6TU"
            };
        }
        
        // Send order to Django backend
        try {
            const response = await fetch('/process-order/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(orderData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Show success message with real order number
                this.showOrderConfirmation({
                    ...orderData,
                    orderNumber: result.order_number
                });
                
                // Clear cart
                this.clearCart();
                
                // Close modals
                const checkoutModal = bootstrap.Modal.getInstance(document.getElementById('checkoutModal'));
                const cartModal = bootstrap.Modal.getInstance(document.getElementById('cartModal'));
                
                if (checkoutModal) checkoutModal.hide();
                if (cartModal) cartModal.hide();
                
            } else {
                alert('Failed to process order: ' + (result.error || 'Unknown error'));
            }
            
        } catch (error) {
            console.error('Order processing error:', error);
            alert('Failed to process order. Please try again.');
        }
    }

    // Show order confirmation with real order number
    showOrderConfirmation(orderData) {
        let locationInfo = '';
        if (orderData.orderType === 'delivery') {
            locationInfo = `Delivery to: ${orderData.delivery.address}, ${orderData.delivery.city}<br>
                          Delivery Date: ${orderData.delivery.date}`;
        } else {
            locationInfo = `Collection from: Mamma's Cakes Bakery<br>
                          Collection Date: ${orderData.collection.date} at ${orderData.collection.time}`;
        }
        
        const confirmationHtml = `
            <div class="alert alert-success alert-dismissible fade show position-fixed" 
                 style="top: 100px; right: 20px; z-index: 9999; min-width: 400px;">
                <h6><i class="fas fa-check-circle"></i> Order Confirmed!</h6>
                <strong>Order #${orderData.orderNumber}</strong><br>
                Customer: ${orderData.customer.name}<br>
                ${locationInfo}<br>
                Total: £${orderData.total.toFixed(2)}<br>
                <small class="text-muted">📧 Confirmation email sent to ${orderData.customer.email}</small>
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', confirmationHtml);
        
        // Auto remove after 10 seconds
        setTimeout(() => {
            const alert = document.querySelector('.alert-success');
            if (alert) alert.remove();
        }, 10000);
    }

    // Enhanced checkout modal display
    showCheckoutModal() {
        // Update checkout items display
        const checkoutItems = document.getElementById('checkout-items');
        const checkoutSubtotal = document.getElementById('checkout-subtotal');
        const checkoutTotal = document.getElementById('checkout-total');
        
        if (checkoutItems) {
            checkoutItems.innerHTML = this.items.map(item => `
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span>${item.name} x ${item.quantity}</span>
                    <span>£${(item.price * item.quantity).toFixed(2)}</span>
                </div>
            `).join('');
        }
        
        const subtotal = this.getTotal();
        if (checkoutSubtotal) {
            checkoutSubtotal.textContent = `£${subtotal.toFixed(2)}`;
        }
        
        // Set minimum collection/delivery date (tomorrow)
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        const collectionDateInput = document.getElementById('collection-date');
        const deliveryDateInput = document.getElementById('delivery-date');
        
        if (collectionDateInput) {
            collectionDateInput.min = tomorrow.toISOString().split('T')[0];
        }
        if (deliveryDateInput) {
            deliveryDateInput.min = tomorrow.toISOString().split('T')[0];
        }
        
        // Update total based on selected option
        this.updateOrderTotal();
        
        // Show checkout modal
        const checkoutModal = new bootstrap.Modal(document.getElementById('checkoutModal'));
        checkoutModal.show();
    }

    // Update order total based on collection/delivery choice
    updateOrderTotal() {
        const isDelivery = document.getElementById('delivery-option')?.checked;
        const deliveryFeeElement = document.getElementById('delivery-fee');
        const deliveryFeeLabel = document.getElementById('delivery-fee-label');
        const checkoutTotal = document.getElementById('checkout-total');
        
        const subtotal = this.getTotal();
        let total = subtotal;
        
        if (isDelivery) {
            total += this.deliveryFee;
            if (deliveryFeeElement) deliveryFeeElement.textContent = `£${this.deliveryFee.toFixed(2)}`;
            if (deliveryFeeLabel) deliveryFeeLabel.textContent = 'Delivery Fee:';
        } else {
            if (deliveryFeeElement) deliveryFeeElement.textContent = '£0.00';
            if (deliveryFeeLabel) deliveryFeeLabel.textContent = 'Collection (Free):';
        }
        
        if (checkoutTotal) {
            checkoutTotal.textContent = `£${total.toFixed(2)}`;
        }
    }

    // Toggle between collection and delivery details
    toggleOrderType() {
        const isDelivery = document.getElementById('delivery-option')?.checked;
        const collectionDetails = document.getElementById('collection-details');
        const deliveryDetails = document.getElementById('delivery-details');
        const deliveryFields = ['delivery-address', 'delivery-city', 'delivery-postcode', 'delivery-date'];
        
        if (isDelivery) {
            if (collectionDetails) collectionDetails.style.display = 'none';
            if (deliveryDetails) deliveryDetails.style.display = 'block';
            
            // Make delivery fields required
            deliveryFields.forEach(fieldId => {
                const field = document.getElementById(fieldId);
                if (field) field.required = true;
            });
            
            // Remove required from collection fields
            const collectionDate = document.getElementById('collection-date');
            const collectionTime = document.getElementById('collection-time');
            if (collectionDate) collectionDate.required = false;
            if (collectionTime) collectionTime.required = false;
            
        } else {
            if (collectionDetails) collectionDetails.style.display = 'block';
            if (deliveryDetails) deliveryDetails.style.display = 'none';
            
            // Remove required from delivery fields
            deliveryFields.forEach(fieldId => {
                const field = document.getElementById(fieldId);
                if (field) field.required = false;
            });
            
            // Make collection fields required
            const collectionDate = document.getElementById('collection-date');
            const collectionTime = document.getElementById('collection-time');
            if (collectionDate) collectionDate.required = true;
            if (collectionTime) collectionTime.required = true;
        }
        
        this.updateOrderTotal();
    }

    // Enhanced event binding
    bindEvents() {
        // Add to cart buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('add-to-cart')) {
                e.preventDefault();
                
                if (!this.requireAuth()) return;
                
                const button = e.target;
                const id = button.dataset.id;
                const name = button.dataset.name;
                const price = button.dataset.price;
                const image = button.dataset.image;
                
                this.addItem(id, name, price, image);
            }
        });
        
        // Checkout form submission
        document.addEventListener('submit', (e) => {
            if (e.target.id === 'checkout-form') {
                e.preventDefault();
                this.processOrder();
            }
        });
        
        // Order type radio buttons
        document.addEventListener('change', (e) => {
            if (e.target.name === 'order-type') {
                this.toggleOrderType();
            }
        });
    }

    // All existing methods (removeItem, updateQuantity, etc.) remain the same...
    removeItem(id) {
        this.items = this.items.filter(item => item.id !== id);
        this.saveCart();
        this.updateCartDisplay();
    }

    updateQuantity(id, quantity) {
        const item = this.items.find(item => item.id === id);
        if (item) {
            item.quantity = parseInt(quantity);
            if (item.quantity <= 0) {
                this.removeItem(id);
            } else {
                this.saveCart();
                this.updateCartDisplay();
            }
        }
    }

    getTotal() {
        return this.items.reduce((total, item) => total + (item.price * item.quantity), 0);
    }

    getItemCount() {
        return this.items.reduce((total, item) => total + item.quantity, 0);
    }

    saveCart() {
        localStorage.setItem('cart', JSON.stringify(this.items));
    }

    updateCartDisplay() {
        const cartBadge = document.getElementById('cart-badge');
        const cartCount = document.getElementById('cart-count');
        const itemCount = this.getItemCount();
        
        if (cartBadge) {
            cartBadge.textContent = itemCount;
            cartBadge.style.display = itemCount > 0 ? 'inline' : 'none';
        }
        
        if (cartCount) {
            cartCount.textContent = itemCount;
        }
        
        this.updateCartModal();
    }

    updateCartModal() {
        const cartItems = document.getElementById('cart-items');
        const cartTotal = document.getElementById('cart-total');
        
        if (!cartItems) return;
        
        if (this.items.length === 0) {
            cartItems.innerHTML = '<p class="text-center">Your cart is empty</p>';
            if (cartTotal) cartTotal.textContent = '£0.00';
            return;
        }
        
        cartItems.innerHTML = this.items.map(item => `
            <div class="cart-item border-bottom pb-3 mb-3">
                <div class="row align-items-center">
                    <div class="col-3">
                        <img src="${item.image}" alt="${item.name}" class="img-fluid rounded" style="height: 60px; object-fit: cover;">
                    </div>
                    <div class="col-6">
                        <h6 class="mb-1">${item.name}</h6>
                        <small class="text-muted">£${item.price.toFixed(2)} each</small>
                    </div>
                    <div class="col-3">
                        <div class="input-group input-group-sm">
                            <button class="btn btn-outline-secondary" type="button" onclick="cart.updateQuantity('${item.id}', ${item.quantity - 1})">-</button>
                            <input type="text" class="form-control text-center" value="${item.quantity}" readonly>
                            <button class="btn btn-outline-secondary" type="button" onclick="cart.updateQuantity('${item.id}', ${item.quantity + 1})">+</button>
                        </div>
                        <div class="text-center mt-1">
                            <small>£${(item.price * item.quantity).toFixed(2)}</small>
                            <button class="btn btn-sm btn-link text-danger p-0 ms-2" onclick="cart.removeItem('${item.id}')">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
        
        if (cartTotal) {
            cartTotal.textContent = `£${this.getTotal().toFixed(2)}`;
        }
    }

    showCartNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'alert alert-success alert-dismissible fade show position-fixed';
        notification.style.cssText = 'top: 100px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 3000);
    }

    clearCart() {
        this.items = [];
        this.saveCart();
        this.updateCartDisplay();
    }
}

// Initialize cart when page loads (only if authenticated)
let cart;
document.addEventListener('DOMContentLoaded', function() {
    if (isAuthenticated) {
        cart = new ShoppingCart();
    }
});