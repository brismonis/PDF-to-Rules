function deleteRow(index) {
    document.getElementById("nlp-table").deleteRow(index);
    
}

function addRow() {
    
    
    var tbodyRef = document.getElementById('nlp-table').getElementsByTagName('tbody')[0];
    var rowindex = tbodyRef.rows.length
    //document.getElementById("nlp-table").addRow()
    var newRow = tbodyRef.insertRow(-1);
    var myHtmlContent = `<tr><td style="width: 40px;"><button onclick="deleteRow(parentNode.parentNode.rowIndex)" type="button" class="btn btn-outline-danger btn-sm py-0 style="font-size: 0.8em;"><i class="fas fa-trash-alt"></i></button></td>
    <td style="width: 30px;">` + rowindex + `</td>
    <td><span><textarea name="value" id="value" style="font-family: Arial;font-size: 12pt; width: 100%; border: none; height: 30px; text-align: left; background: none;"></textarea> </span></td>
    
    </tr>`
    newRow.innerHTML = myHtmlContent;
}