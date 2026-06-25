const fileInput = document.getElementById("fileInput");
const preview = document.getElementById("preview");

fileInput.addEventListener("change", () => {

    const file = fileInput.files[0];

    if (file) {

        const reader = new FileReader();

        reader.onload = function (e) {

            preview.src = e.target.result;
            preview.style.display = "block";

        };

        reader.readAsDataURL(file);

    }

});