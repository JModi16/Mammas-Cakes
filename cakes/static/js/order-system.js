// SIMPLIFIED WORKING VERSION - No Complex Validation
console.log('Order System JavaScript Loading...');

class OrderSystem {
    constructor() {
        this.currentCake = null;
        this.init();
    }

    init() {
        this.attachEventListeners();
        this.setMinDates();
    }

    attachEventListeners() {
        // FIXED: Listen for correct class name
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('order-now-btn')) {  // ✅ Correct class name
                e.preventDefault();
                this.handleOrderClick(e.target);
            }
        });

        // Form submission
        const orderForm = document.getElementById('orderForm');
        if (orderForm) {
            orderForm.addEventListener('submit', (e) => this.handleOrderSubmission(e));
        }

        // Radio button changes
        document.addEventListener('change', (e) => {
            if (e.target.name === 'delivery_option') {
                this.toggleDeliveryOption();
            }
        });
    }

    setMinDates() {
        const today = new Date();
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        const minDate = tomorrow.toISOString().split('T')[0];

        const collectionDate = document.getElementById('collection-date');
        const deliveryDate = document.getElementById('delivery-date');
        
        if (collectionDate) collectionDate.min = minDate;
        if (deliveryDate) deliveryDate.min = minDate;
    }

    handleOrderClick(button) {
        console.log('Order button clicked!', button);
        
        // Check authentication
        if (window.isAuthenticated === "false") {
            const loginModal = new bootstrap.Modal(document.getElementById('loginRequiredModal'));
            loginModal.show();
            return;
        }

        // FIXED: Get cake data with correct attribute names
        this.currentCake = {
            id: button.dataset.id,      // ✅ Matches data-id
            name: button.dataset.name,  // ✅ Matches data-name  
            price: parseFloat(button.dataset.price) // ✅ Matches data-price
        };
        console.log('Current cake:', this.currentCake);

        // Check if modal exists
        const modal = document.getElementById('orderDetailsModal');
        if (!modal) {
            alert('Order form not found. Please refresh the page.');
            return;
        }

        // Pre-fill user data
        this.prefillUserData();

        // Update order summary
        this.updateOrderSummary();

        // Show modal
        const modalInstance = new bootstrap.Modal(modal);
        modalInstance.show();
    }

    prefillUserData() {
        if (window.userEmail) {
            const emailField = document.getElementById('customer-email');
            if (emailField) emailField.value = window.userEmail;
        }

        if (window.userName) {
            const nameField = document.getElementById('customer-name');
            if (nameField) nameField.value = window.userName;
        }
    }

    toggleDeliveryOption() {
        const deliveryRadio = document.getElementById('delivery');
        const collectionDetails = document.getElementById('collection-details');
        const deliveryDetails = document.getElementById('delivery-details');

        const isDelivery = deliveryRadio && deliveryRadio.checked;

        if (isDelivery) {
            if (collectionDetails) collectionDetails.style.display = 'none';
            if (deliveryDetails) deliveryDetails.style.display = 'block';
        } else {
            if (collectionDetails) collectionDetails.style.display = 'block';
            if (deliveryDetails) deliveryDetails.style.display = 'none';
        }

        this.updateOrderSummary();
    }

    updateOrderSummary() {
        if (!this.currentCake) return;

        const summaryItems = document.getElementById('order-summary-items');
        const subtotal = document.getElementById('order-subtotal');
        const total = document.getElementById('order-total');

        if (summaryItems) {
            summaryItems.innerHTML = `
                <div class="d-flex justify-content-between mb-2">
                    <span>${this.currentCake.name}</span>
                    <span>£${this.currentCake.price.toFixed(2)}</span>
                </div>
            `;
        }

        if (subtotal) subtotal.textContent = `£${this.currentCake.price.toFixed(2)}`;
        if (total) total.textContent = `£${this.currentCake.price.toFixed(2)}`;
    }

    handleOrderSubmission(e) {
        e.preventDefault();
        
        // Simple form data collection
        const formData = this.collectFormData();
        
        // Basic validation only
        if (!formData.customer_name || !formData.customer_email || !formData.customer_phone) {
            alert('Please fill in all required fields.');
            return;
        }

        if (!formData.delivery_option) {
            alert('Please select collection or delivery.');
            return;
        }

        // Submit the order
        this.submitOrder(formData);
    }

    collectFormData() {
        const getFieldValue = (id) => {
            const field = document.getElementById(id);
            return field ? field.value.trim() : '';
        };

        const getCheckedRadioValue = (name) => {
            const radio = document.querySelector(`input[name="${name}"]:checked`);
            return radio ? radio.value : '';
        };

        return {
            cake_id: this.currentCake ? this.currentCake.id : '',
            cake_name: this.currentCake ? this.currentCake.name : '',
            cake_price: this.currentCake ? this.currentCake.price : 0,
            customer_name: getFieldValue('customer-name'),
            customer_email: getFieldValue('customer-email'),
            customer_phone: getFieldValue('customer-phone'),
            delivery_option: getCheckedRadioValue('delivery_option'),
            collection_date: getFieldValue('collection-date'),
            collection_time: getFieldValue('collection-time'),
            delivery_address: getFieldValue('delivery-address'),
            delivery_city: getFieldValue('delivery-city'),
            delivery_postcode: getFieldValue('delivery-postcode'),
            delivery_date: getFieldValue('delivery-date'),
            delivery_time: getFieldValue('delivery-time'),
            special_instructions: getFieldValue('special-instructions')
        };
    }

    async submitOrder(formData) {
        try {
            const response = await fetch('/place-order/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.csrfToken
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok && result.success) {
                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('orderDetailsModal'));
                if (modal) modal.hide();

                // Show success message
                alert(`Order placed successfully! Order number: ${result.order_number}`);
                
            } else {
                alert('Failed to place order. Please try again.');
            }
        } catch (error) {
            console.error('Order submission error:', error);
            alert('Connection error. Please try again.');
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new OrderSystem();
});