/**
 * Created by aliHitawala on 11/1/16.
 */
function getFileName(elm) {
    console.log($(elm).val());
}
$(function () {
    $(':checkbox').checkboxpicker();
    $("a.my-tool-tip").tooltip();
 $('input[type="file"]').change(function () {
  if ($(this).val() != "") {
    var file = document.getElementById('id_docfile').files[0];
      console.log(file.name);
    if (file) {
        var fileSize = 0;
        if (file.size > 1024 * 1024)
            fileSize = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
        else
            fileSize = (Math.round(file.size * 100 / 1024) / 100).toString() + 'KB';

        document.getElementById('fileName').innerHTML = 'Name: ' + file.name;
        document.getElementById('fileSize').innerHTML = 'Size: ' + fileSize;
        document.getElementById('fileType').innerHTML = 'Type: ' + file.type;
    }
  }else{
     $('#label_upload').html("No file Choosen");
  }
 });
    $('#upload').submit(function(event){
    // Prevent multiple submits
    // TODO fix this to show progress bar on file upload
        console.log('submit function');
    if ($.data(this, 'submitted')) return false;
        console.log('ok here we are')
        // event.preventDefault();

        // var formData = new FormData($('#upload')[0]);
        // $.ajax({
        //     xhr : function() {
        //         var xhr = new window.XMLHttpRequest();
        //         console.log('inside ajax thingy')
        //
        //         xhr.upload.addEventListener('progress', function(e) {
        //
        //             if (e.lengthComputable) {
        //                 var percent = Math.round((e.loaded / e.total) * 100);
        //
        //                 $('#progressBar').attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%');
        //             }
        //
        //         });
        //
        //         return xhr;
        //     },
        //     type : 'POST',
        //     data : formData,
        //     processData : false,
        //     contentType : false,
        // });
        //
        // console.log('testing after here');
    // var freq = 10; // freqency of update in ms
    // var uuid = gen_uuid(); // id for this upload so we can fetch progress info.
    // var progress_url = 'admin/upload_progress/'; // ajax view serving progress info

    // Append X-Progress-ID uuid form action
    // this.action += (this.action.indexOf('?') == -1 ? '?' : '&') + 'X-Progress-ID=' + uuid;

    // var $progress = $('<div id="upload-progress" class="upload-progress"></div>').
    //    appendTo(document.body).append('<div class="progress-container"><span class="progress-info"></span><div class="progress-bar"></div></div>');

    // progress bar position
    // $progress.css({
    //    position: 'fixed',
    //    left: '50%', marginLeft: 0-($progress.width()/2), bottom: '20%'
    // }).show();

    // Update progress bar
    // function update_progress_info() {
    //     $progress.show();
    //     $.getJSON(progress_url, {'X-Progress-ID': uuid}, function(data, status){
    //         if (data) {
    //             var progress = parseInt(data.uploaded) / parseInt(data.length);
    //             var width = $progress.find('.progress-container').width()
    //             var progress_width = width * progress;
    //             console.log(progress_width);
    //             //$progress.find('.progress-bar').width(progress_width);
    //             //$progress.find('.progress-info').text('uploading ' + parseInt(progress*100) + '%');
    //         }
    //         window.setTimeout(update_progress_info, freq);
    //         });
    //     };
    //    window.setTimeout(update_progress_info, freq);

        $.data(this, 'submitted', true); // mark form as submitted.
    });
});
// function gen_uuid() {
//     var uuid = "";
//     for (var i=0; i < 32; i++) {
//         uuid += Math.floor(Math.random() * 16).toString(16);
//     }
//     return uuid
// }