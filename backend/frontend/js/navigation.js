function loadNavigation() {

    const role = localStorage.getItem("role");

    const navigation = document.getElementById("navigation");

    if (!navigation) {
        return;
    }

    let menu = `
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container-fluid">

                <a class="navbar-brand" href="/products-page">
                    Warehouse System
                </a>

                <div class="navbar-nav">

                    <a class="nav-link" href="/dashboard-page">
                        Dashboard
                    </a>

                    <a class="nav-link" href="/products-page">
                        Products
                    </a>

                    <a class="nav-link" href="/categories-page">
                        Categories
                    </a>

                    <a class="nav-link" href="/orders-page">
                        Orders
                    </a>

                    <a class="nav-link" href="/stock-movements-page">
                        Stock Movements
                    </a>
                    
                    <a class="nav-link" href="/reports-page">
                        Reports
                    </a>
    `;

    if (role === "admin") {
        menu += `
                    <a class="nav-link" href="/users-page">
                        Users
                    </a>
        `;
    }

    menu += `
                </div>

                <div class="d-flex">
                    <button
                        class="btn btn-outline-light btn-sm"
                        onclick="logout()">
                        Logout
                    </button>
                </div>

            </div>
        </nav>
    `;

    navigation.innerHTML = menu;
}


function logout() {

    localStorage.removeItem("token");
    localStorage.removeItem("role");

    window.location.href = "/login";
}