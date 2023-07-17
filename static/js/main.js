// ▼ カレンダー ▼ //
const today = new Date();
// 月末だとずれる可能性があるため、1日固定で取得
var showDate = new Date(today.getFullYear(), today.getMonth(), 1);
// 初期表示
window.onload = function () {
  showProcess(today);
};
// 前の月表示
function prev(){
  showDate.setMonth(showDate.getMonth() - 1);
  showProcess(showDate);
}
// 次の月表示
function next(){
  showDate.setMonth(showDate.getMonth() + 1);
  showProcess(showDate);
}
// カレンダー表示
function showProcess(date) {
  var year = date.getFullYear();
  var month = date.getMonth();
  document.querySelector('#month').innerHTML = year + "年" + (month + 1) + "月";
}
// ▲ カレンダー ▲ //

// ▼ 入力ページ ▼ //

// フォーム追加 //
// function addForm() {
//   var i = 1 ;
//   var input_category = document.createElement('input');
//   var input_item = document.createElement('input');
//   var input_price = document.createElement('input');
//   input_category.type = 'text';
//   input_category.className = 'input_category';
//   input_category.name = 'category_' + i;
//   input_item.type = 'text';
//   input_item.className = 'input_item';
//   input_item.name = 'item_' + i;
//   input_price.type = 'text';
//   input_price.className = 'input_price';
//   input_price.name = 'price_' + i;
//   var parent = document.getElementById('form_area');
//   parent.appendChild(input_category);
//   parent.appendChild(input_item);
//   parent.appendChild(input_price);
//   i++ ;
//}
// ▲ 入力ページ ▲ //