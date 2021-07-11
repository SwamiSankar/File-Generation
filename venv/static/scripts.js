$(document).ready(function() {

   //We use this AJAX call to get the list of files from the server and populate it in drop-down 
   $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:5000/getFiles',
        success: function(data) { 
            //Iterating through the list of files and dynamically appending them  
            $.each(data, function (i, fileName) {
                $('#file-select').append($('<option>', {
                    value: fileName,
                    text : fileName
                }));
            });
        },
        error: function(error) {
            console.log("error", error);
        },
    });
   
    //We use this AJAX call to get the list of columns from a particular file  
    $.ajax({
        type:'GET',
        url: 'http://127.0.0.1:5000/getColumns',
        success: function(data) {
            //Iterating through column names and creating checkbox dynamically
            $.each(data, function (i, columnName) {
                let container = $('#check-box-contents');
                let inputs = container.find('input');
                let id = inputs.length + 1;
                $('<input />', { type: 'checkbox', id: 'cb'+id, value: columnName }).appendTo(container);
                $('<label />', { 'for': 'cb'+id, text: columnName }).appendTo(container);
            });
        },
        error: function(error) {
            console.log("error", error);
        }
    })
});

//This method sends the filename and list of columns to our API and fetches back the necessary data
const getData = () => {

    //We are getting the selected filename from the drop down 
    let selectedFile = $('#file-select').find(":selected").text();
    let columns = [];
    //We are storing the list of selected columns in an array
    $('#check-box-contents input:checked').each(function() {
        columns.push($(this).attr('value'));
    });

    //Preparing Request Data
    let request = {
        "filename" : selectedFile,
        "columns": columns
    }

    //Making the POST API call to fetch the data
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:5000/getData',
        data: JSON.stringify(request),
        success: function(data) {
            //Clearing the table entries
            $('#result-table tr').remove();
            //Showing the results to the user
            $('.results-container').show();
            buildTable(data)
        },
        error: function(error) {
            //Clearing the table entries
            $('#result-table tr').remove();
            //Hiding the results
            $('.results-container').hide();
            console.log("error", error);
        },
        contentType: "application/json",
        dataType: 'json'
    });

    //Renders the table contents dynamically 
    const buildTable = (data) => {
        $.each(data , function (index, item) {
            $.each(item, function (i, k) {
                createTableRows(i, k, index);
            });
        });
    }

    //Sets the table Column headers dynamically
    const createTableHeaders = (headColumns) => {
        let tableHeadElementRows = $('#result-table thead');
        //If table heading row is already present, append table head column 
        if ($('#result-table thead tr').length) {
            
            $('#result-table thead tr').append(
                $('<th>').text(headColumns),
            );
        }
        //If there is no table heading row present , create a new row and append the columns
        else {
            let $tr = $(`<tr>`).append(
                $('<th>').text(headColumns),
            ).appendTo(tableHeadElementRows);
         }
    }

    //Populates the table content
    const createTableRows = (rowIndex, rows, index) => {
        
        //If this is the first element of the column, create heading
        if (rowIndex == 0) {
            createTableHeaders(index)
        }

        let tableElementRows = $('#result-table tbody');

        //If table row is already present, append column data 
        if($('.tr-' + rowIndex).length) {
            let tableElementRowData = $('.tr-' + rowIndex);
            $(tableElementRowData).append(
                $('<td>').text(rows),
            );
        } 
        //If there is no table row present , create a new row and append the column data
        else {
            let $tr = $(`<tr class=tr-${rowIndex}>`).append(
                $('<td>').text(rows),
            ).appendTo(tableElementRows);
        }
    }
}
