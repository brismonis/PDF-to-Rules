const spin_btn = document.getElementById('spin')
spin_btn.onclick = function() {
    spin_btn.innerHTML = `Processing OCR ... <div class="spinner-border text-light" role="status"><span class="sr-only"></span></div>`;
}