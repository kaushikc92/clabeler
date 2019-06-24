$("#close-step[type='button']").click(function () {
  window.close()
});

$("#download-step[type='button']").click(function (e) {
  e.preventDefault();
  var ds_loc = $('#ds_loc').html();
  window.open('/download_file/?ds_loc=' + ds_loc);
});
