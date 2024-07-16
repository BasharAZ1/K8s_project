document.getElementById('userForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const userId = document.getElementById('user_id').value;
    const url = `/api/${userId}`;

    const response = await fetch(url, {
        method: 'GET'
    });

    const resultDiv = document.getElementById('result');

    if (response.ok) {
        const data = await response.json();
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = formatUserData(data);
    } else {
        const errorData = await response.json();
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `<p>${errorData.error}</p>`;
    }
});

document.getElementById('chargeForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const monthlyCharges = document.getElementById('monthly_charges').value;
    const url = `/api/charges/${monthlyCharges}`;

    const response = await fetch(url, {
        method: 'GET'
    });

    const resultDiv = document.getElementById('highChargesResult');

    if (response.ok) {
        const data = await response.json();
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = formatChargeData(data);
    } else {
        const errorData = await response.json();
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `<p>${errorData.error}</p>`;
    }
});

function formatUserData(data) {
    let formattedData = '<h2>User Data</h2>';
    for (const key in data) {
        formattedData += `<p><span>${key}:</span> ${data[key]}</p>`;
    }
    return formattedData;
}

function formatChargeData(data) {
    let formattedData = '<h2>Customer IDs with High Monthly Charges</h2>';
    data.forEach(customerID => {
    formattedData += `<p><span>Customer ID:</span> ${customerID}</p>`;
    });
    return formattedData;
}