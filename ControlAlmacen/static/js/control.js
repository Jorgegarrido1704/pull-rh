function cambios() {
    var invoiceNum = document.getElementById('impo').value;

    if (invoiceNum) {
        // Send AJAX request to Django view
        fetch('/cambios/?impo=' + invoiceNum)
            .then(response => response.json())
            .then(data => {
                // If data is returned successfully
                if (data.status === 'ok') {
                    var tableBody = document.getElementById('table-body');
                    tableBody.innerHTML = '';  // Clear existing rows

                    // Loop through the returned data and create new rows
                    data.datosImpo.forEach(item => {
                        var row = document.createElement('tr');
                        
                        var itemCell = document.createElement('td');
                        itemCell.textContent = item.mfcInterno;  // 'mfcInterno' is the item value
                        
                        var qtyCell = document.createElement('td');
                        qtyCell.textContent = item.qty;  // 'qty' is the quantity value
                        
                        var invoiceCell = document.createElement('td');
                        invoiceCell.textContent = item.invoiceNum;  // 'invoiceNum' is the invoice number

                        row.appendChild(itemCell);
                        row.appendChild(qtyCell);
                        row.appendChild(invoiceCell);

                        tableBody.appendChild(row);
                    });
                } else {
                    // Handle error response
                    console.error('No records found or error occurred');
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }
}