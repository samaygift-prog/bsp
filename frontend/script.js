function saveData() {

    let data = {
        full_name: document.getElementById("name").value,
        mobile: document.getElementById("mobile").value,
        problem: document.getElementById("problem").value,
        medical_history: document.getElementById("medical").value,
        talent: document.getElementById("talent").value,
        profession: document.getElementById("profession").value,
        second_hand_product: document.getElementById("second_hand_product").value
    };

    fetch("http://127.0.0.1:8000/responses", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)

    })

    .then(response => response.json())

    .then(result => {

        alert(result.message);

        // Clear form after successful submit
        document.getElementById("name").value = "";
        document.getElementById("mobile").value = "";
        document.getElementById("problem").value = "";
        document.getElementById("medical").value = "";
        document.getElementById("talent").value = "";
        document.getElementById("profession").value = "";
        document.getElementById("second_hand_product").value = "";

    })

    .catch(error => {

        alert("Error: " + error);

    });

}