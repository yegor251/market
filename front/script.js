let token = '';
let user = {};
let bonusInterval;

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    const result = await response.json();
    console.log(result)
    if (result.status) {
        token = result.access_token;
        user = result.user;
        document.getElementById("response").innerText = "Login successful!";
        switchToMain();
        renderUserInfo();
        renderItems();
        startBonusTimer();
    } else {
        document.getElementById("response").innerText = result.error_type;
    }
}

async function register() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    const result = await response.json();
    if (result.status) {
        token = result.access_token;
        user = result.user;
        document.getElementById("response").innerText = "Register successful!";
        switchToMain();
        renderUserInfo();
        renderItems();
        startBonusTimer();
    } else {
        document.getElementById("response").innerText = result.error_type;
    }
}

function switchToMain() {
    document.getElementById("auth-container").classList.add("hidden");
    document.getElementById("main-container").classList.remove("hidden");
}

function renderUserInfo() {
    document.getElementById("money-display").innerText = `💰 Money: $${user.money}`;
}

function renderItems() {
    const itemsGrid = document.getElementById("items-grid");
    itemsGrid.innerHTML = '';

    for (const [id, item] of Object.entries(user.items)) {
        const itemCard = document.createElement("div");
        itemCard.className = `item-card ${item.status ? 'purchased' : ''}`;
        itemCard.innerHTML = `
            <h3>${item.name}</h3>
            <p>Price: $${item.price}</p>
            ${item.status
                ? '<p>Purchased</p>'
                : `<button onclick="buyItem('${id}')">Buy</button>`}
        `;
        itemsGrid.appendChild(itemCard);
    }
}

async function getDailyBonus() {
    if (!token) {
        alert("Please login first!");
        return;
    }

    const now = Math.floor(Date.now() / 1000);
    if (user.bonus_timestamp + 60 <= now) {
        const response = await fetch("http://127.0.0.1:8000/dailybonus", {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` },
        });

        const result = await response.json();
        console.log(result)

        user.money = result.user.money;
        user.bonus_timestamp = result.user.bonus_timestamp;
        renderUserInfo();
        startBonusTimer();
        document.getElementById("bonus-timer").innerText = `🎁 Bonus available in: 60s`;
    }
}

async function buyItem(itemId) {
    const response = await fetch("http://127.0.0.1:8000/buy_item", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token, item_id: itemId }),
    });

    const result = await response.json();
    if (result.status) {
        user.money -= user.items[itemId].price;
        user.items[itemId].status = 1;
        renderUserInfo();
        renderItems();
    } else {
        alert("Purchase failed!");
    }
}

function startBonusTimer() {
    if (bonusInterval) clearInterval(bonusInterval);

    bonusInterval = setInterval(() => {
        const now = Math.floor(Date.now() / 1000);

        if (user.bonus_timestamp + 60 <= now) {
            document.getElementById("bonus-timer").innerText = "🎁 Bonus available now!";
        } else {
            const seconds = 60 - now + user.bonus_timestamp
            document.getElementById("bonus-timer").innerText = `🎁 Bonus available in: ${seconds}s`;
        }
    }, 1000);
}

window.addEventListener('beforeunload', function () {
    if (token) {
        fetch('http://127.0.0.1:8000/log-close', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token }),
        });
    }
});
