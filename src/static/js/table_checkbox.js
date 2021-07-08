// var $  = require( 'jquery' );
// var dt = require( 'datatables.net' )();

$(document).ready(function() {
    $('#datatablesSimple').DataTable( {
        columnDefs: [ {
            orderable: false,
            className: 'select-checkbox',
            targets:   0
        } ],
        select: {
            style:    'os',
            selector: 'td:first-child'
        },
        order: [[ 1, 'asc' ]]
    } );
} );