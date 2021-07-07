const uploadForm = document.getElementById('upload-form');
const pdfInput = document.getElementById('id-pdf');
const progressbar = document.getElementById('progessbar-upload');
const cancelBtn = document.getElementById('cancel-btn');
const cancelBox = document.getElementById('cancel-box');
const submitBtn = document.getElementById('submit-btn');

const csrf = document.getElementById('csrfmiddlewaretoken');

// when pressing Submit Button, a progressbar and Cancel Button will appear by removing own css class .not-visible
uploadForm.addEventListener('change', ()=>{
    progressbar.classList.remove('not-visible');
    cancelBox.classList.remove('not-visible');

    const data = submitBtn.files[0]
    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('data', data)

    // $.ajax({
    //     data: fd,
    //     beforeSend: function(){

    //     },
    //     xhr: function(){
    //         const xhr = new window.XMLHttpRequest();
    //         xhr.upload.addEventListener('progress', e=>{
    //             if(e.lengthComputable) {
    //                 const percent = e.loaded / e.total * 100
    //                 // console.log(percent)
    //                 progressbar.innerHTML = `<div class="progress"><div class="progress-bar" role="progressbar" style="width: ${percent}%" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100"></div></div>
    //                                         <p>${percent.toFixed(1)}</p>`

    //             }
    //         })
    //         return xhr
    //     },
    //     success: function(response){
    //         console.log("YES-----------------------")
    //     },
    //     error: function(error){

    //     },
    //     cache: false,
    //     contentType: false,
    //     processData: false,
    //     // url: {% url 'upload' %}
    // })


});

