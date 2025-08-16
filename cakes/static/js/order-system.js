// Order System JavaScript - FIXED VERSION
// Handles single cake orders (not cart-based)

class OrderSystem {
    constructor() {
        this.currentCakeData = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupDeliveryToggle();
    }

    bindEvents() {
        // Order Now button clicks
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('order-now-btn')) {
                this.handleOrderNowClick(e.target);
            }
        });

        // Form submission
        const orderForm = document.getElementById('orderForm');
        if (orderForm) {
            orderForm.addEventListener('submit', (e) => {
                this.handleOrderSubmission(e);
            });
        }
    }

    handleOrderNowClick(button) {
        const cakeData = {
            id: button.dataset.id,
            name: button.dataset.name,
            price: button.dataset.price,
            image: button.dataset.image
        };

        this.currentCakeData = cakeData;
        this.populateOrderModal(cakeData);
        this.showOrderModal();
    }

    populateOrderModal(cakeData) {
        // Pre-fill user information if available
        if (window.isAuthenticated === 'true') {
            const nameField = document.getElementById('customer-name');
            const emailField = document.getElementById('customer-email');
            
            if (nameField && window.userName) {
                nameField.value = window.userName;
            }
            if (emailField && window.userEmail) {
                emailField.value = window.userEmail;
            }
        }

        // Update order summary
        const summaryItems = document.getElementById('order-summary-items');
        if (summaryItems) {
            summaryItems.innerHTML = `
                <div class="d-flex justify-content-between">
                    <span>${cakeData.name}</span>
                    <span>£${cakeData.price}</span>
                </div>
            `;
        }

        const subtotalElement = document.getElementById('order-subtotal');
        if (subtotalElement) {
            subtotalElement.textContent = '£' + cakeData.price;
        }

        // Set minimum date to tomorrow
        this.setMinimumDates();

        // Store cake data for form submission
        const orderForm = document.getElementById('orderForm');
        if (orderForm) {
            orderForm.setAttribute('data-cake-id', cakeData.id);
            orderForm.setAttribute('data-cake-name', cakeData.name);
            orderForm.setAttribute('data-cake-price', cakeData.price);
        }

        // Update total
        this.updateOrderTotal();
    }

    setMinimumDates() {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        const minDate = tomorrow.toISOString().split('T')[0];

        const collectionDate = document.getElementById('collection-date');
        const deliveryDate = document.getElementById('delivery-date');

        if (collectionDate) collectionDate.setAttribute('min', minDate);
        if (deliveryDate) deliveryDate.setAttribute('min', minDate);
    }

    showOrderModal() {
        const modal = document.getElementById('orderDetailsModal');
        if (modal && typeof bootstrap !== 'undefined') {
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
        }
    }

    setupDeliveryToggle() {
        // FIXED: Use correct radio button names from your base.html
        const collectionRadio = document.getElementById('collection');
        const deliveryRadio = document.getElementById('delivery');

        if (collectionRadio) {
            collectionRadio.addEventListener('change', () => this.toggleDeliveryOption());
        }
        if (deliveryRadio) {
            deliveryRadio.addEventListener('change', () => this.toggleDeliveryOption());
        }
    }

    toggleDeliveryOption() {
        const deliveryRadio = document.getElementById('delivery');
        const collectionDetails = document.getElementById('collection-details');
        const deliveryDetails = document.getElementById('delivery-details');
        const deliveryFee = document.getElementById('delivery-fee');
        const deliveryFeeLabel = document.getElementById('delivery-fee-label');

        if (deliveryRadio && deliveryRadio.checked) {
            if (collectionDetails) collectionDetails.style.display = 'none';
            if (deliveryDetails) deliveryDetails.style.display = 'block';
            if (deliveryFee) deliveryFee.textContent = '£5.00';
            if (deliveryFeeLabel) deliveryFeeLabel.textContent = 'Delivery Fee:';
        } else {
            if (collectionDetails) collectionDetails.style.display = 'block';
            if (deliveryDetails) deliveryDetails.style.display = 'none';
            if (deliveryFee) deliveryFee.textContent = '£0.00';
            if (deliveryFeeLabel) deliveryFeeLabel.textContent = 'Collection Fee:';
        }
        
        // ADD this line:
        this.updateRequiredFields();
        this.updateOrderTotal();
    }

    updateRequiredFields() {
        const deliveryRadio = document.getElementById('delivery');
        const isDelivery = deliveryRadio && deliveryRadio.checked;
        
        // Collection fields
        const collectionDate = document.getElementById('collection-date');
        const collectionTime = document.getElementById('collection-time');
        
        // Delivery fields
        const deliveryAddress = document.getElementById('delivery-address');
        const deliveryCity = document.getElementById('delivery-city');
        const deliveryPostcode = document.getElementById('delivery-postcode');
        const deliveryDate = document.getElementById('delivery-date');
        const deliveryTime = document.getElementById('delivery-time');
        
        if (isDelivery) {
            // Remove required from collection fields
            if (collectionDate) collectionDate.removeAttribute('required');
            if (collectionTime) collectionTime.removeAttribute('required');
            
            // Add required to delivery fields
            if (deliveryAddress) deliveryAddress.setAttribute('required', 'required');
            if (deliveryCity) deliveryCity.setAttribute('required', 'required');
            if (deliveryPostcode) deliveryPostcode.setAttribute('required', 'required');
            if (deliveryDate) deliveryDate.setAttribute('required', 'required');
            if (deliveryTime) deliveryTime.setAttribute('required', 'required');
        } else {
            // Add required to collection fields
            if (collectionDate) collectionDate.setAttribute('required', 'required');
            if (collectionTime) collectionTime.setAttribute('required', 'required');
            
            // Remove required from delivery fields
            if (deliveryAddress) deliveryAddress.removeAttribute('required');
            if (deliveryCity) deliveryCity.removeAttribute('required');
            if (deliveryPostcode) deliveryPostcode.removeAttribute('required');
            if (deliveryDate) deliveryDate.removeAttribute('required');
            if (deliveryTime) deliveryTime.removeAttribute('required');
        }
    }

    updateOrderTotal() {
        const subtotalElement = document.getElementById('order-subtotal');
        const deliveryFeeElement = document.getElementById('delivery-fee');
        const totalElement = document.getElementById('order-total');

        if (subtotalElement && deliveryFeeElement && totalElement) {
            const subtotal = parseFloat(subtotalElement.textContent.replace('£', '')) || 0;
            const deliveryFee = parseFloat(deliveryFeeElement.textContent.replace('£', '')) || 0;
            const total = subtotal + deliveryFee;
            totalElement.textContent = '£' + total.toFixed(2);
        }
    }

    handleOrderSubmission(e) {
        e.preventDefault();

        const formData = this.collectFormData();
        
        if (!this.validateFormData(formData)) {
            return;
        }

        this.submitOrder(formData);
    }

    collectFormData() {
        const orderForm = document.getElementById('orderForm');
        
        return {
            cake_id: orderForm.getAttribute('data-cake-id'),
            cake_name: orderForm.getAttribute('data-cake-name'),
            cake_price: orderForm.getAttribute('data-cake-price'),
            customer_name: this.getFieldValue('customer-name'),
            customer_email: this.getFieldValue('customer-email'),
            customer_phone: this.getFieldValue('customer-phone'),
            delivery_option: this.getCheckedRadioValue('deliveryOption'),
            collection_date: this.getFieldValue('collection-date'),
            collection_time: this.getFieldValue('collection-time'),
            delivery_address: this.getFieldValue('delivery-address'),
            delivery_city: this.getFieldValue('delivery-city'),
            delivery_postcode: this.getFieldValue('delivery-postcode'),
            delivery_date: this.getFieldValue('delivery-date'),
            delivery_time: this.getFieldValue('delivery-time'),
            special_instructions: this.getFieldValue('special-instructions')
        };
    }

    getFieldValue(fieldId) {
        const field = document.getElementById(fieldId);
        return field ? field.value : '';
    }

    getCheckedRadioValue(name) {
        const radio = document.querySelector(`input[name="${name}"]:checked`);
        return radio ? radio.value : '';
    }

    validateFormData(formData) {
        // Basic validation
        if (!formData.customer_name || !formData.customer_email || !formData.customer_phone) {
            alert('Please fill in all required customer information.');
            return false;
        }

        if (formData.delivery_option === 'collection' && (!formData.collection_date || !formData.collection_time)) {
            alert('Please select collection date and time.');
            return false;
        }

        if (formData.delivery_option === 'delivery' && (!formData.delivery_address || !formData.delivery_city || !formData.delivery_postcode)) {
            alert('Please fill in all delivery address fields.');
            return false;
        }

        return true;
    }

    submitOrder(formData) {
        // Show loading state
        const submitButton = document.querySelector('#orderForm button[type="submit"]');
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        submitButton.disabled = true;

        // FIXED: Use correct endpoint that matches your Django URLs
        fetch('/order/place/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.csrfToken
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Order placed successfully! Order number: ' + data.order_number);
                this.closeOrderModal();
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                }
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to place order. Please check your connection and try again.');
        })
        .finally(() => {
            // Restore button state
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        });
    }

    closeOrderModal() {
        const modal = document.getElementById('orderDetailsModal');
        if (modal && typeof bootstrap !== 'undefined') {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        }
    }
}

// Initialize the order system when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new OrderSystem();
});