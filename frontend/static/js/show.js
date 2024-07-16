document.getElementById('head').addEventListener('click', async function(event) {
    const url = `/api/show/head`;

    const response = await fetch(url, {
        method: 'GET'
    });

    const resultDiv = document.getElementById('result');

    if (response.ok) {
        const data = await response.json();
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = formatTable(data);
    } else {
        const errorData = await response.json();
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `<p>${errorData.error}</p>`;
    }
});
//tail script:
document.getElementById('tail').addEventListener('click', async function(event) {
    const url = `/api/show/tail`;

    const response = await fetch(url, {
        method: 'GET'
    });

    const resultDiv = document.getElementById('result');

    if (response.ok) {
        const data = await response.json();
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = formatTable(data);
    } else {
        const errorData = await response.json();
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `<p>${errorData.error}</p>`;
    }
});
function formatTable(data) {
    let formattedTable = '<table><thead><tr>';
    // Create table headers
    for (const key in data[0]) {
        formattedTable += `<th>${key}</th>`;
    }
    formattedTable += '</tr></thead><tbody>';

    // Create table rows
    data.forEach(item => {
        formattedTable += '<tr>';
        for (const key in item) {
            formattedTable += `<td>${item[key]}</td>`;
        }
        formattedTable += '</tr>';
    });

    formattedTable += '</tbody></table>';
    return formattedTable;
}