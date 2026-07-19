fetch("http://127.0.0.1:8000/responses")

.then(response => response.json())

.then(data => {

    let table = document.getElementById("dataTable");

    data.forEach(item => {

        let row = table.insertRow();

        row.insertCell(0).innerHTML = item.id;
        row.insertCell(1).innerHTML = item.full_name;
        row.insertCell(2).innerHTML = item.mobile;
        row.insertCell(3).innerHTML = item.problem;
        row.insertCell(4).innerHTML = item.medical_history;
        row.insertCell(5).innerHTML = item.talent;
        row.insertCell(6).innerHTML = item.profession;
        row.insertCell(7).innerHTML = item.second_hand_product;

    });

});