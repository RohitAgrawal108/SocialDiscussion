$(function() { 
  $('#sidebarCollapse').on('click', function() {
    $('#sidebar, #content').toggleClass('active');
  });
});
function AddUser() {
  const val = document.getElementById('addusername').value;
  console.log(val);
  location.href = `http://127.0.0.1:8000/chat/${val}/`;
}
// row_list = document.getElementsByClassName("allign_side")
// row_list[0].inn