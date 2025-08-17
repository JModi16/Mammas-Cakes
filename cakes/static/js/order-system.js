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
        this.addRealTimeValidation(); // Add this line
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
        
        console.log('=== ORDER SUBMISSION STARTED ===');

        // Collect form data
        const formData = this.collectFormData();
        console.log('Collected form data:', formData);
        
        // Check if we have cake data
        if (!this.currentCake) {
            alert('Error: No cake selected. Please try again.');
            return;
        }
        
        // Validate form
        console.log('Starting validation...');
        if (!this.validateFormData(formData)) {
            console.log('❌ Validation failed');
            return;
        }
        
        console.log('✅ Validation passed, submitting order...');
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
        console.log('Validating form data:', formData);

        // Basic validation - always required
        if (!formData.customer_name) {
            alert('Please enter your full name.');
            document.getElementById('customer-name')?.focus();
            return false;
        }

        if (!formData.customer_email) {
            alert('Please enter your email address.');
            document.getElementById('customer-email')?.focus();
            return false;
        }

        if (!formData.customer_phone) {
            alert('Please enter your phone number.');
            document.getElementById('customer-phone')?.focus();
            return false;
        }

        if (!formData.delivery_option) {
            alert('Please select collection or delivery option.');
            return false;
        }

        // Collection validation
        if (formData.delivery_option === 'collection') {
            console.log('Validating collection fields...');
            console.log('Collection date:', formData.collection_date);
            console.log('Collection time:', formData.collection_time);
            
            if (!formData.collection_date || formData.collection_date === '') {
                alert('Please select a collection date.');
                document.getElementById('collection-date')?.focus();
                return false;
            }
            
            if (!formData.collection_time || formData.collection_time === '') {
                alert('Please select a collection time slot.');
                document.getElementById('collection-time')?.focus();
                return false;
            }
        }

        // Delivery validation  
        if (formData.delivery_option === 'delivery') {
            console.log('Validating delivery fields...');
            console.log('Delivery address:', formData.delivery_address);
            console.log('Delivery date:', formData.delivery_date);
            console.log('Delivery time:', formData.delivery_time);
            
            if (!formData.delivery_address || formData.delivery_address === '') {
                alert('Please enter your delivery address.');
                document.getElementById('delivery-address')?.focus();
                return false;
            }
            
            if (!formData.delivery_city || formData.delivery_city === '') {
                alert('Please enter your delivery city.');
                document.getElementById('delivery-city')?.focus();
                return false;
            }
            
            if (!formData.delivery_postcode || formData.delivery_postcode === '') {
                alert('Please enter your delivery postcode.');
                document.getElementById('delivery-postcode')?.focus();
                return false;
            }
            
            if (!formData.delivery_date || formData.delivery_date === '') {
                alert('Please select a delivery date.');
                document.getElementById('delivery-date')?.focus();
                return false;
            }
            
            if (!formData.delivery_time || formData.delivery_time === '') {
                alert('Please select a delivery time slot.');
                document.getElementById('delivery-time')?.focus();
                return false;
            }
        }

        console.log('✅ All validation passed');
        return true;
    }

    async submitOrder(formData) {
        try {
            console.log('Submitting order with data:', formData);
            
            const response = await fetch('/place-order/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.csrfToken
                },
                body: JSON.stringify(formData)
            });

            console.log('Response status:', response.status);
            
            const result = await response.json();
            console.log('Response data:', result);

            if (response.ok && result.success) {
                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('orderDetailsModal'));
                if (modal) modal.hide();

                // Show success message
                alert('Order placed successfully! You will receive a confirmation email shortly.');
                
            } else {
                // Show detailed error message
                const errorMsg = result.error || 'Unknown error occurred';
                console.error('Order submission failed:', errorMsg);
                alert(`Failed to place order: ${errorMsg}\n\nPlease check all required fields are filled correctly.`);
            }
        } catch (error) {
            console.error('Order submission error:', error);
            alert('Connection error. Please check your internet connection and try again.');
        }
    }

    addRealTimeValidation() {
        // Add event listeners for real-time validation
        const requiredFields = [
            'customer-name', 'customer-email', 'customer-phone',
            'collection-date', 'collection-time',
            'delivery-address', 'delivery-city', 'delivery-postcode', 
            'delivery-date', 'delivery-time'
        ];

        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('blur', () => {
                    this.validateField(fieldId);
                });
            }
        });
    }

    validateField(fieldId) {
        const field = document.getElementById(fieldId);
        if (!field) return;

        const isRequired = field.hasAttribute('required');
        const isEmpty = !field.value.trim();

        if (isRequired && isEmpty) {
            field.classList.add('is-invalid');
            field.classList.remove('is-valid');
        } else if (!isEmpty) {
            field.classList.add('is-valid');
            field.classList.remove('is-invalid');
        } else {
            field.classList.remove('is-invalid', 'is-valid');
        }
    }

    debugFormState() {
        const formData = this.collectFormData();
        console.log('=== FORM STATE DEBUG ===');
        console.log('Current cake:', this.currentCake);
        console.log('Form data:', formData);
        
        // Check which option is selected
        const collectionRadio = document.getElementById('collection');
        const deliveryRadio = document.getElementById('delivery');
        
        console.log('Collection radio checked:', collectionRadio?.checked);
        console.log('Delivery radio checked:', deliveryRadio?.checked);
        
        // Check field visibility
        const collectionDetails = document.getElementById('collection-details');
        const deliveryDetails = document.getElementById('delivery-details');
        
        console.log('Collection details visible:', collectionDetails?.style.display !== 'none');
        console.log('Delivery details visible:', deliveryDetails?.style.display !== 'none');
        
        console.log('========================');
    }
}

// Initialize the order system when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new OrderSystem();
});