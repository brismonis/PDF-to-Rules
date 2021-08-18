function spin_nlp() {
    const spin_btn2 = document.getElementById('spin_nlp')
    spin_btn2.onclick = function() {
        spin_btn2.innerHTML = `Processing NLP ... <div class="spinner-border text-light" role="status"><span class="sr-only"></span></div>`;
    }
}