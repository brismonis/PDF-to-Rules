const table_delete = document.getElementById("table_delete")
const table_download = document.getElementById("table_download")
const table_selectAll = document.getElementById("table_selectAll")

$(document).ready(function() {
    //var table = $('#datatablesSimple').DataTable();
    table = $('#datatablesSimple').DataTable( {
        // columnDefs: [ {
        //     orderable: false,
        //     className: 'select-checkbox',
        //     targets:   0
        // } ],
        dom:"B<'row'<'col-lg-10 col-md-10 col-xs-12'f><'col-lg-2 col-md-2 col-xs-12'l>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",

        
        select: {
            style: 'multi'
        },
        // select: {
        //     style:    'os',
        //     selector: 'td:first-child'
        // },
        // order: [[ 1, 'asc' ]]
        // buttons: [{
        //     text: 'Select All',
        //     attr: {
        //       id: 'table_selectAll'
        //     },
        //     action: function selectAll() {
        //         table.rows({
        //          page: 'current'
        //             }).select();
        //         }
        // }]
        buttons: [
            {
            text: 'Select all on Page',
            action: function selectAll () {
            table.rows({
                page: 'current'
              }).select();}
            },
            {
            text: 'Select none',
            action: function () {
            table.rows().deselect();
            }
            },
            

            ]
        
        
    } );
    // $('#datatablesSimple > .dt-buttons').appendTo("body");

} );

// $(document).ready(function() {
//     var table = $('#datatablesSimple').DataTable( {
//         dom: 'frtipB',
//         lengthChange: false,
//         buttons: [ 'copy', 'pdf', 'colvis' ],
//         select: { style: 'multi'},
//     } );
 
//     table.buttons().container()
//         .appendTo( '#body .col-md-6:eq(0)' );
// } );