var proj_id = $('#project_id').html();
var workflow_id = $('#wf_id').html();
var ds_name = $('#ds_name').html();

window.onload = function () {
    createTable(tuple_pairs, table_a_attributes, table_b_attributes, selectedColumns);
};

function createTable(tuplePairs, tableA, tableB, selectedColumns){
    var div = document.getElementById('divTable');

    table_object = document.getElementById("attribute-table");
    if(table_object)
        table_object.remove();

    var table = document.createElement('table');
    table.id = "attribute-table";
    table.setAttribute('class', 'table table-striped table-bordered table-hover');
    if(tableDisplayModeHorizontal) {
        for (var i = 0; i < ids.length; i++) {
            var row = table.insertRow();
            for (var selectedColumn in selectedColumns) {
                var attribute_cell = row.insertCell();
                attribute_cell.setAttribute('style', 'text-align: center; background-color: #eea43c;');
                attribute_cell.innerHTML = selectedColumns[selectedColumn];
            }

            var rowA = table.insertRow();
            for (var selectedColumn in selectedColumns) {
                sIndex = attributes.indexOf(selectedColumns[selectedColumn]);
                var attribute_cell = rowA.insertCell();
                attribute_cell.innerHTML = tableA[i][sIndex];
            }

            var rowB = table.insertRow();
            for (var selectedColumn in selectedColumns) {
                sIndex = attributes.indexOf(selectedColumns[selectedColumn]);
                var attribute_cell = rowB.insertCell();
                attribute_cell.innerHTML = tableB[i][sIndex];
            }

            var tuple_pair = ids[i];
            var custom_id = "custom$"+ tuple_pair[0]+ "$" + tuple_pair[1];

            var row1 = table.insertRow();
            setupLabelRow(row1, tableA[i], tableB[i], custom_id);

        }
    } else {
        for (var i=0; i< tuplePairs.length;i++) {
            for(var selectedColumn in selectedColumns) {
                sIndex = attributes.indexOf(selectedColumns[selectedColumn]);

                var row = table.insertRow();
                var attribute_cell = row.insertCell(0);
                attribute_cell.setAttribute('style','text-align: center; background-color: #eea43c;');
                attribute_cell.innerHTML = attributes[sIndex];

                var tableA_cell = row.insertCell(1);
                tableA_cell.innerHTML = tableA[i][sIndex];

                var tableB_cell = row.insertCell(2);
                tableB_cell.innerHTML = tableB[i][sIndex];
            }

            var tuple_pair = ids[i];
            var custom_id = "custom$"+ tuple_pair[0]+ "$" + tuple_pair[1];

            var row1 = table.insertRow();
            setupLabelRow(row1, tableA[i], tableB[i], custom_id);
        }

    }
    div.appendChild(table);

}

function createCommentTable(tableA, tableB){
    var div = document.getElementById('divCommentTable');

    table_object = document.getElementById("comment-table");
    if(table_object)
        table_object.remove();

    var table = document.createElement('table');
    table.id = "comment-table";
    //table-bordered
    table.setAttribute('class', 'table table-striped table-hover');

    var row = table.insertRow();
    for (var attribute in attributes) {
        var attribute_cell = row.insertCell();
        attribute_cell.setAttribute('style', 'text-align: center; background-color: #eea43c;');
        attribute_cell.innerHTML = attributes[attribute];
    }
    var rowA = table.insertRow();
    for (var index in tableA) {
        var attribute_cell = rowA.insertCell();
        attribute_cell.innerHTML = tableA[index];
    }
    var rowB = table.insertRow();
    for (var index in tableB) {
        var attribute_cell = rowB.insertCell();
        attribute_cell.innerHTML = tableB[index];
    }

    div.appendChild(table);

}

function onTuplePairLabelled(tableA, tableB, label_type){
    if(label_type === 't' || label_type === 'f' || label_type === 'u' ){
        save_label(label_type);
        return;
    }

    var modal = document.getElementById('myModal');
    modal.style.display = "block";

    var comment_div = document.getElementById("comment_div");
    comment_div.style.visibility = "hidden";

    if(label_type === "c"){
        comment_div.style.visibility = "visible";
    }

    createCommentTable(tableA, tableB);
}

function onCheckBoxChecked() {
    var checkboxes = document.getElementsByName("checkbox");
    var checkboxesChecked = [];

    for (var i=0; i<checkboxes.length; i++) {

        if (checkboxes[i].checked) {
            checkboxesChecked.push(checkboxes[i].value);
        }
    }
    createTable(tuple_pairs, table_a_attributes, table_b_attributes, checkboxesChecked);
    selectedColumns = checkboxesChecked;
}

function onDisplayModeChanged(value) {
    tableDisplayModeHorizontal = ("horizontal" === value);
    createTable(tuple_pairs, table_a_attributes, table_b_attributes, selectedColumns);
}


function onModalCancelClicked() {
    var modal = document.getElementById('myModal');
    modal.style.display = "none";
}

function save_label(save_label) {
    var assignment_id = $('#assignment_id').html();
    var pair_id = $('#pair_id').html();
    var service_url = '/labeling_service/' + assignment_id + '/';
    var notice_url = '/completion_notice/' + assignment_id + '/';

    var el = document.getElementsByName("csrfmiddlewaretoken");
    csrf_value = el[0].getAttribute("value");

    $.ajax({
        type: 'POST',
        url: service_url,
        dataType: 'json',
        data: {csrfmiddlewaretoken: csrf_value, save_flag: true,
            assignment_id: assignment_id, pair_id: pair_id, label: save_label},
        success: function (e, textStatus) {
            console.log("in save_label, POST to " + service_url + " successful: " + textStatus)
            console.log(e['label_complete']);
            var label_complete = e['label_complete'];
            if (label_complete === true) {
                // debugger;
                window.location = notice_url;

            } else {
                refresh_tuplepair(service_url);
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log('failure of POST to ' + service_url);
            console.log(textStatus);
            console.log(errorThrown);
            var error = "<div class='alert alert-danger'><p>We encountered an error while processing: <br /><strong>" + errorThrown + "</strong></p>";
            error += "<p>Please contact us if this error persists.</p>";
            error += "</div>";
            $('#upload_message').html(error);
            $('.progress').fadeOut();
        }
    });
}

function setupLabelRow(row_object, pairA, pairB, custom_id) {
    var label_div = document.createElement('div');
    label_div.setAttribute('style', "position:relative; margin:0;");
    label_div.setAttribute('class', "btn-group");
    label_div.setAttribute('data-toggle', "buttons");
    label_div.setAttribute('width',  '100%');
    for(var idx in labels){
        var name = labels[idx]['name'];
        var val = labels[idx]['value'];
        label = document.createElement('label');

        label.custom_id = custom_id;
        label.tableA = pairA;
        label.tableB = pairB;
        label.label_type = val;
        label.setAttribute("value", val);
        label.setAttribute("name", custom_id);

        label.onclick = function(){
            this.radio_button.checked = true;
            onTuplePairLabelled(this.tableA, this.tableB, this.label_type);
            this.radio_button.checked = false;
            this.classList.remove("active");
        };

        label.setAttribute('style',"margin-left:10px;");
        if(val === "t"){
            label.setAttribute('class', "train-success btn btn-default custom-label-btn");
            var span1 = document.createElement('span');
            span1.setAttribute('class', "glyphicon glyphicon-ok");
            label.appendChild(span1);

        } else if (val === "f"){
            label.setAttribute('class', "train-danger btn btn-default custom-label-btn");
            var span = document.createElement('span');
            span.setAttribute('class', "glyphicon glyphicon-remove");
            span.setAttribute('aria-hidden', "true");
            label.appendChild(span);
        } else {
            label.setAttribute('class', "btn btn-default custom-label-btn");
        }
        var radio = document.createElement('input');
        radio.setAttribute("type", "radio");
        radio.setAttribute("value", val);
        radio.setAttribute("name", custom_id);
        radio.setAttribute("class", "hide");
        label.radio_button = radio;
        label.innerText = name;
        label.appendChild(radio);
        label_div.appendChild(label);
    }

    var attribute_cell = row_object.insertCell();
    attribute_cell.setAttribute('colspan', selectedColumns.length);
    // attribute_cell.setAttribute('width',  '100%');
    attribute_cell.setAttribute('text-align',  'center');
    attribute_cell.appendChild(label_div);

}

function refresh_tuplepair(url){
    $('#divTable').empty();
    url = url + "?reload=false";
    console.log("Going to execute get against " + url);

    $.ajax({
        type: 'GET',
        url: url,
        success: function (data, textStatus) {
            table_a_attributes = data['rows'][0];
            table_b_attributes = data['rows'][1];
            labels = data['labels'];
            ids = data['ids'];
            attributes = data['headers'][0];
            updateUI(data);
            createTable(tuple_pairs, table_a_attributes, table_b_attributes, selectedColumns);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log('failure in refresh_tuple get');
            console.log(textStatus);
            console.log(errorThrown);
            var message  = textStatus + ": " + errorThrown;
            var error = "<div class='alert alert-danger'><p>We encountered an error while processing: <br /><strong>" + message + "</strong></p>";
            error += "<p>Please <a href='mailto:uwcloudmatcher@gmail.com'>contact us</a> if this error persists.</p>";
            error += "</div>";
            $('#upload_message').html(error);
            $('.progress').fadeOut();
        },
        complete: function(jqxhr, textStatus) {
           console.log("refresh_tuple ajax complete with status " + textStatus);
        }
    });
}

function updateUI(data){
    document.getElementById('true_label_count').innerHTML = data['true_label_count'];
    document.getElementById('false_label_count').innerHTML = data['false_label_count'];
    document.getElementById('unsure_label_count').innerHTML = data['unsure_label_count'];
    document.getElementById('done_count').innerHTML = data['done_count'] + 1;
    document.getElementById('total_count').innerHTML = data['total_count'];
    document.getElementById('pair_id').innerHTML = data['ids'][0];
}
