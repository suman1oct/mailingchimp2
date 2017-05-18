var vBtn = '';

$(".select-temp").click(function() {
    vBtn = $(this).data('templateId');
    localStorage.setItem("templateId", vBtn);
});

if(localStorage.hasOwnProperty('templateId')) {
    var temVal = localStorage.getItem("templateId", vBtn);
    $("#id_template").val(temVal);
}
