// Order System JavaScript - COMPLETELY FIXED VERSION
class OrderSystem {
    constructor() {
        this.currentCake = null;
        this.deliveryFee = 0;
        this.init();
    }

    init() {
        this.attachEventListeners();
        this.setMinDates();
    }

    attachEventListeners() {
        // Order buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('order-btn')) {
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
        // Check if user is authenticated
        if (window.isAuthenticated === "false") {
            const loginModal = new bootstrap.Modal(document.getElementById('loginRequiredModal'));
            loginModal.show();
            return;
        }

        // Get cake data
        this.currentCake = {
            id: button.dataset.cakeId,
            name: button.dataset.cakeName,
            price: parseFloat(button.dataset.cakePrice)
        };

        // Set form attributes
        const orderForm = document.getElementById('orderForm');
        if (orderForm) {
            orderForm.setAttribute('data-cake-id', this.currentCake.id);
            orderForm.setAttribute('data-cake-name', this.currentCake.name);
            orderForm.setAttribute('data-cake-price', this.currentCake.price);
        }

        // Pre-fill user data if available
        this.prefillUserData();

        // Update order summary
        this.updateOrderSummary();

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('orderDetailsModal'));
        modal.show();
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
        const deliveryFee = document.getElementById('delivery-fee');
        const deliveryFeeLabel = document.getElementById('delivery-fee-label');

        const isDelivery = deliveryRadio && deliveryRadio.checked;

        if (isDelivery) {
            if (collectionDetails) collectionDetails.style.display = 'none';
            if (deliveryDetails) deliveryDetails.style.display = 'block';
            if (deliveryFeeLabel) deliveryFeeLabel.textContent = 'Delivery Fee:';
            if (deliveryFee) deliveryFee.textContent = '£0.00';
            this.deliveryFee = 0;
        } else {
            if (collectionDetails) collectionDetails.style.display = 'block';
            if (deliveryDetails) deliveryDetails.style.display = 'none';
            if (deliveryFeeLabel) deliveryFeeLabel.textContent = 'Collection Fee:';
            if (deliveryFee) deliveryFee.textContent = '£0.00';
            this.deliveryFee = 0;
        }

        this.updateRequiredFields();
        this.updateOrderSummary();
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
        
        const totalAmount = this.currentCake.price + this.deliveryFee;
        if (total) total.textContent = `£${totalAmount.toFixed(2)}`;
    }

    handleOrderSubmission(e) {
        e.preventDefault();

        // Collect form data
        const formData = this.collectFormData();
        
        // Validate form
        if (!this.validateFormData(formData)) {
            return;
        }

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

    validateFormData(formData) {
        // Basic validation
        if (!formData.customer_name) {
            alert('Please enter your full name.');
            return false;
        }

        if (!formData.customer_email) {
            alert('Please enter your email address.');
            return false;
        }

        if (!formData.customer_phone) {
            alert('Please enter your phone number.');
            return false;
        }

        if (!formData.delivery_option) {
            alert('Please select collection or delivery option.');
            return false;
        }

        if (formData.delivery_option === 'collection') {
            if (!formData.collection_date) {
                alert('Please select a collection date.');
                return false;
            }
            if (!formData.collection_time) {
                alert('Please select a collection time.');
                return false;
            }
        }

        if (formData.delivery_option === 'delivery') {
            if (!formData.delivery_address) {
                alert('Please enter delivery address.');
                return false;
            }
            if (!formData.delivery_city) {
                alert('Please enter delivery city.');
                return false;
            }
            if (!formData.delivery_postcode) {
                alert('Please enter delivery postcode.');
                return false;
            }
            if (!formData.delivery_date) {
                alert('Please select delivery date.');
                return false;
            }
            if (!formData.delivery_time) {
                alert('Please select delivery time.');
                return false;
            }
        }

        return true;
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
                alert('Order placed successfully! You will receive a confirmation email shortly.');
                
                // Optionally redirect to order confirmation page
                if (result.redirect_url) {
                    window.location.href = result.redirect_url;
                }
            } else {
                alert('Error placing order: ' + (result.error || 'Please try again.'));
            }
        } catch (error) {
            console.error('Order submission error:', error);
            alert('Error placing order. Please try again.');
        }
    }
}

// Initialize the order system when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new OrderSystem();
});