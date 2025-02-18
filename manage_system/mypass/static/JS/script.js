// Form initialization and event handlers
document.addEventListener('DOMContentLoaded', () => {
    initializeFormData();
    setupEventListeners();
    setupInitialProductEntry();
});

// Initialize form data
const initializeFormData = () => {
    // Generate and set gate pass ID
    const gatePassId = sessionStorage.getItem('gatePassId') || 
                      `MAHE-${(Math.floor(Math.random() * 900000) + 100000)}`;
    sessionStorage.setItem('gatePassId', gatePassId);
    document.getElementById('gatePassId').value = gatePassId;

    // Set current date/time
    const now = new Date();
    document.getElementById('dateTime').value = now.toISOString().slice(0, 16);

    // Set default return date (7 days from now)
    const nextWeek = new Date(now.setDate(now.getDate() + 7));
    document.getElementById('expectedReturnDate').value = nextWeek.toISOString().slice(0, 10);
};

// Setup all event listeners
const setupEventListeners = () => {
    // Add product button
    document.getElementById('addProductBtn').addEventListener('click', handleAddProduct);

    // Form type change
    document.getElementById('formType').addEventListener('change', handleFormTypeChange);

    // Form submission
    document.getElementById('gatePassForm').addEventListener('submit', handleFormSubmit);

    // Image preview
    setupImagePreview();
};

// Product entry handlers
const handleAddProduct = () => {
    const container = document.getElementById('product_entries');
    const template = container.querySelector('.product-entry').cloneNode(true);
    
    // Reset values
    template.querySelectorAll('input, select, textarea').forEach(el => el.value = '');
    
    // Add delete button
    const deleteButton = createDeleteButton();
    template.querySelector('.card-body').appendChild(deleteButton);
    
    // Update indices
    updateProductIndices(template, container.children.length);
    
    container.appendChild(template);
};

const createDeleteButton = () => {
    const btn = document.createElement('button');
    btn.className = 'btn btn-danger btn-sm position-absolute';
    btn.style.cssText = 'right: 10px; top: 10px;';
    btn.innerHTML = '×';
    btn.onclick = (e) => e.target.closest('.product-entry').remove();
    return btn;
};

const updateProductIndices = (template, index) => {
    template.querySelectorAll('[name]').forEach(el => {
        const name = el.getAttribute('name');
        if (name && name.includes('[]')) {
            el.setAttribute('name', name.replace('[]', `[${index}]`));
        }
    });
};

// Form type change handler
const handleFormTypeChange = () => {
    const formType = document.getElementById('formType').value;
    const returnDateGroup = document.getElementById('expectedReturnDate').closest('.form-group');
    const returnDateInput = document.getElementById('expectedReturnDate');

    returnDateGroup.style.display = formType === 'returnable' ? 'block' : 'none';
    returnDateInput.disabled = formType !== 'returnable';
};

// Image preview handling
const setupImagePreview = () => {
    const imageInput = document.getElementById('productImage');
    const preview = document.getElementById('previewImage');
    const deleteBtn = document.getElementById('deleteImage');
    const container = document.getElementById('previewImageContainer');

    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                preview.src = e.target.result;
                preview.style.display = 'block';
                container.classList.add('image-preview-wrapper');
                deleteBtn.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });

    deleteBtn.addEventListener('click', () => {
        imageInput.value = '';
        preview.src = '#';
        preview.style.display = 'none';
        container.classList.remove('image-preview-wrapper');
        deleteBtn.style.display = 'none';
    });
};

// Form validation
const validateForm = () => {
    let isValid = true;
    const errors = [];

    // Required fields validation
    document.querySelectorAll('[required]').forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('is-invalid');
            errors.push(`${field.getAttribute('name')} is required`);
        } else {
            field.classList.remove('is-invalid');
        }
    });

    // Product entries validation
    document.querySelectorAll('.product-entry').forEach((entry, index) => {
        const quantity = entry.querySelector('.product-quantity').value;
        const name = entry.querySelector('.material-name').value;

        if (!quantity || !name) {
            isValid = false;
            errors.push(`Product ${index + 1} is incomplete`);
        }
    });

    // Pattern validation
    const patterns = {
        'employee_name': /^[a-zA-Z\s]+$/,
        'employee_id': /^[0-9a-zA-Z]+$/,
        'designation': /^[a-zA-Z\s]+$/,
        'contact_info': /^\d{10}$/
    };

    Object.entries(patterns).forEach(([fieldName, pattern]) => {
        const field = document.querySelector(`[name="${fieldName}"]`);
        if (field && !pattern.test(field.value)) {
            isValid = false;
            field.classList.add('is-invalid');
            errors.push(`Invalid ${fieldName.replace('_', ' ')}`);
        }
    });


    // Display errors if any
    if (!isValid) {
        showErrors(errors);
    }

    return isValid;
};

// Error display
const showErrors = (errors) => {
    const errorContainer = document.createElement('div');
    errorContainer.className = 'alert alert-danger mt-3';
    errorContainer.innerHTML = `
        <h5>Please correct the following errors:</h5>
        <ul>
            ${errors.map(error => `<li>${error}</li>`).join('')}
        </ul>
    `;

    const form = document.getElementById('gatePassForm');
    const existingError = form.querySelector('.alert-danger');
    if (existingError) {
        existingError.remove();
    }
    form.insertBefore(errorContainer, form.firstChild);
};

// Form submission handler
const handleFormSubmit = (event) => {
    event.preventDefault();
    
    if (validateForm()) {
        const submitBtn = document.querySelector('[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Submitting...';
        
        // Submit the form
        event.target.submit();
    }
};
