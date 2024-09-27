document.addEventListener('DOMContentLoaded', function () {
    function generateGatePassId() {
        return Math.floor(Math.random() * 900000) + 100000;
    }

    function setCurrentDateTime(dateTimeField) {
        var currentDate = new Date();
        var year = currentDate.getFullYear();
        var month = ('0' + (currentDate.getMonth() + 1)).slice(-2);
        var day = ('0' + currentDate.getDate()).slice(-2);
        var hours = ('0' + currentDate.getHours()).slice(-2);
        var minutes = ('0' + currentDate.getMinutes()).slice(-2);
        var formattedDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
        dateTimeField.value = formattedDateTime;
    }

    var storedGatePassId = sessionStorage.getItem('gatePassId');
    if (!storedGatePassId) {
        var newGatePassId = "MAHE-" + generateGatePassId();
        sessionStorage.setItem('gatePassId', newGatePassId);
        storedGatePassId = newGatePassId;
    }

    document.getElementById('gatePassId').value = storedGatePassId;
    setCurrentDateTime(document.getElementById("dateTime"));

    function populateProductNames(category, productNameElement, productNameTextElement) {
        productNameElement.innerHTML = '<option value="">Select</option>';

        if (category in materials) {
            materials[category].forEach(item => {
                const option = document.createElement('option');
                option.value = item;
                option.textContent = item;
                productNameElement.appendChild(option);
            });

            productNameElement.style.display = 'block';
            productNameElement.required = true;
            productNameTextElement.style.display = 'none';
            productNameTextElement.required = false;
        } else {
            productNameElement.style.display = 'none';
            productNameElement.required = false;
            productNameTextElement.style.display = 'block';
            productNameTextElement.required = true;
        }
    }

    document.getElementById('sub_department').addEventListener('change', function () {
        populateProductNames(this.value, document.getElementById('product_name'), document.getElementById('productNameText'));
    });

    document.getElementById('product_name').addEventListener('change', function () {
        const otherProductName = document.getElementById('otherProductName');
        const otherProductNameInput = document.getElementById('otherProductNameInput');

        if (this.value === 'Other') {
            otherProductName.style.display = 'block';
            otherProductNameInput.required = true;
        } else {
            otherProductName.style.display = 'none';
            otherProductNameInput.required = false;
        }
    });

    document.getElementById('validateSerialsBtn').addEventListener('click', function () {
        const serialNumbers = document.getElementById('product_serial_nos').value.split(/[,\n]/).map(s => s.trim()).filter(s => s !== '');
        const quantity = parseInt(document.getElementById('product_quantity').value, 10);

        const serialsError = document.getElementById('serialsError');
        const serialsDuplicateError = document.getElementById('serialsDuplicateError');

        if (serialNumbers.length !== quantity) {
            serialsError.textContent = `Expected ${quantity} serial numbers, but found ${serialNumbers.length}.`;
            serialsError.style.display = 'block';
        } else {
            serialsError.style.display = 'none';
        }

        const uniqueSerials = new Set(serialNumbers);
        if (uniqueSerials.size !== serialNumbers.length) {
            serialsDuplicateError.textContent = 'Duplicate serial numbers found.';
            serialsDuplicateError.style.display = 'block';
        } else {
            serialsDuplicateError.style.display = 'none';
        }
    });

    document.getElementById('productImage').addEventListener('change', function () {
        const file = this.files[0];
        const reader = new FileReader();

        reader.onload = function (e) {
            const previewImage = document.getElementById('previewImage');
            const deleteImage = document.getElementById('deleteImage');

            previewImage.src = e.target.result;
            previewImage.style.display = 'block';
            deleteImage.style.display = 'inline';
        };

        reader.readAsDataURL(file);
    });

    document.getElementById('deleteImage').addEventListener('click', function () {
        document.getElementById('productImage').value = '';
        document.getElementById('previewImage').src = '#';
        document.getElementById('previewImage').style.display = 'none';
        this.style.display = 'none';
    });

    const expectedReturnDate = document.getElementById('expectedReturnDate');
    if (expectedReturnDate) {
        const currentDate = new Date();
        const nextWeek = new Date(currentDate.setDate(currentDate.getDate() + 7));
        expectedReturnDate.value = nextWeek.toISOString().slice(0, 10);

        expectedReturnDate.addEventListener('change', function () {
            const selectedDate = new Date(this.value);
            const today = new Date();

            if (selectedDate < today) {
                alert("Expected return date must be in the future.");
                this.value = nextWeek.toISOString().slice(0, 10);
            }
        });
    }
});

// Materials data for dropdown population
const materials = {
    'IT': ['All in one Desktop', 'Laptop', 'HDMI Cable', 'Polycom Studio',
        'Logitech Camera', 'Cisco IP Phone', 'Hard disk', 'Monitor', 'Keyboard/Mouse', 'Photo Copier',
        'Web Camera', 'Laptop Charger', 'LAN Cable', 'Printer', 'Printer Cartridge', 'Camera', 'Live Streaming Device',
        'Video Camera', 'Network Switch', 'Network Router', 'Headset', 'Cell Charger', 'Speakers', 'Tripod', 'Other'],
    'General Services': ['Electrical', 'Plumbing', 'HVAC/Mechanical', 'Carpentry', 'Civil', 'Fire & Safety', 'Medical', 'Other'],
    'HR': ['Employee Records', 'Forms', 'Documents', 'Other'],
    'Finance': ['Invoices', 'Receipts', 'Bills', 'Other'],
    'Marketing': ['Flyers', 'Brochures', 'Posters', 'Other']
};

