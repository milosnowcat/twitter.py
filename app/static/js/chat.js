let chat = document.getElementById("chat");
chat.scrollTop = chat.scrollHeight - chat.clientHeight;

function previewFile() {
  let popup = document.getElementById("preview_img");
  popup.classList.add("active-modal");

  let preview = popup.querySelector("img");
  let file = document.querySelector("input[type=file]").files[0];
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
