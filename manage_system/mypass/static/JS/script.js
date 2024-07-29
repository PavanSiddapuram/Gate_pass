function validateForm() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    if (username === "MAHE" && password === "123") {
        window.location.href = "dashboard.html"; // Redirect to the dashboard page
        return false; // Prevent form submission
    } else {
        alert("Invalid username or password.");
        return false; // Prevent form submission
    }
}

function showDashboard(username) {
    history.pushState({ page: "dashboard" }, "Dashboard", "#dashboard");
    sessionStorage.setItem("page", "dashboard");
    document.getElementById("login-container").style.display = "none";
    document.getElementById("dashboard-container").style.display = "block";
}

function goBack() {
    history.pushState({ page: "login" }, "Login", "#login");
    sessionStorage.setItem("page", "login");
    document.getElementById("dashboard-container").style.display = "none";
    document.getElementById("login-container").style.display = "block";
    document.getElementById("loginForm").reset(); // Clear the login form
}

window.onpopstate = function(event) {
    if (event.state) {
        if (event.state.page === "dashboard") {
            document.getElementById("login-container").style.display = "none";
            document.getElementById("dashboard-container").style.display = "block";
        } else if (event.state.page === "login") {
            document.getElementById("dashboard-container").style.display = "none";
            document.getElementById("login-container").style.display = "block";
        }
    }
};

// Handle page reload or direct access
window.onload = function() {
    var page = sessionStorage.getItem("page");
    if (page === "dashboard") {
        document.getElementById("login-container").style.display = "none";
        document.getElementById("dashboard-container").style.display = "block";
    } else {
        document.getElementById("dashboard-container").style.display = "none";
        document.getElementById("login-container").style.display = "block";
    }
};



//// script for Entry form ////
//// validation

document.addEventListener('DOMContentLoaded', function () {
    const entranceForm = document.getElementById('entranceForm');
    
    entranceForm.addEventListener('submit', function (e) {
        const visitorName = document.getElementById('visitorName').value;
        const visitorplace = document.getElementById('visitorplace').value;
        const Department = document.getElementById('Department').value;
        const moblienumber = document.getElementById('moblienumber').value;
        const DateTime = document.getElementById('DateTime').value;

        // Simple validation check
        if (!visitorName || !visitorplace || !Department || !moblienumber || !DateTime) {
            alert('Please fill in all required fields.');
            e.preventDefault(); // Prevent form submission
        }
    });
});


