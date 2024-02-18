function previewImg() {
  let preview = document.getElementById("preview_img");
  let file = document.querySelector("input[name=image]").files[0];
  let reader = new FileReader();

  reader.onloadend = function () {
    preview.src = reader.result;
  };

  if (file) {
    reader.readAsDataURL(file);
  } else {
    preview.src = "";
  }
}

function previewPdf() {
  let preview = document.getElementById("preview_pdf");
  let file = document.querySelector("input[name=cv]").files[0];
  if (file) {
    preview.alt = "You have uploaded a pdf file";
  }
}
