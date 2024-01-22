document.getElementById('registerForm').addEventListener('submit', function (event) {
    var birthDateInput = document.querySelector('input[type="date"]');
    var birthDate = new Date(birthDateInput.value);
    var today = new Date();

    var age = today.getFullYear() - birthDate.getFullYear();
    var m = today.getMonth() - birthDate.getMonth();

    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }

    if (age < 13) {
        alert('You must be at least 13 years old to register.');
        event.preventDefault();
    }
});
