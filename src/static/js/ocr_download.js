//let csrftoken = '{{ csrf_token }}'
$('#ocr_download').click(function(){
    $.ajax({
        //headers:{'X-CSRFToken':csrftoken},
      url: '',
      method: 'POST',
      headers: { "X-CSRFToken": getCookie("csrftoken") }, //funktioniert
      data: {
        request_name: 'download_ocr',
        //csrfmiddlewaretoken: '{{ csrf_token }}',
      },
      
      
      success: function (data) {        
          var element = document.createElement('a');
          element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(data));
          //element.setAttribute('href', "Content-Type: application/x-www-form-urlencoded", encodeURIComponent(data));
          //element.setAttribute('href')
          element.setAttribute('download', 'foo.txt');

          element.style.display = 'none';
          document.body.appendChild(element);

          element.click();

          document.body.removeChild(element);
      },
      error: function (err) {
        console.log('Error downloading file');
      }
    });
});

// function download(filename, text) {
              
//     //creating an invisible element
//     var element = document.createElement('a');
//     element.setAttribute('href', 
//     'data:text/plain;charset=utf-8, '
//     + encodeURIComponent(text));
//     element.setAttribute('download', filename);
  
//     // Above code is equivalent to
//     // <a href="path of file" download="file name">
  
//     document.body.appendChild(element);
  
//     //onClick property
//     element.click();
  
//     document.body.removeChild(element);
// }
  
// // Start file download.
// document.getElementById("ocr_download").addEventListener("click", function() {
//     // Generate download of hello.txt 
//     // file with some content
//     var text = document.getElementById("my_textarea").value;
//     var filename = "GFG.txt";
  
//     download(filename, text);
// }, false);
function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }