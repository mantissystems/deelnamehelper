$("#search-input").on("keyup", function () {
  var value = $(this).val();
  console.log("Value:", value);
  var data = searchTable(value, myArray);
  console.log(data);
  buildTable(data);
});

$.ajax({
  method: "GET",
  url: "http://127.0.0.1:8000/api/person/",
  success: function (response) {
    myArray = response;
    buildTable(myArray);
    console.log(myArray);
  },
});

function searchTable(value, data) {
  var filteredData = [];
  for (var i = 0; i < data.length; i++) {
    value = value.toLowerCase();
    var name = data[i].name.toLowerCase();
    var idee = data;
    console.log(value);
    if (name.includes(value || data[i].id === value)) {
      filteredData.push(data[i]);
    }
  }
  return filteredData;
}

function buildTable(data) {
  var table = document.getElementById("myTable");
  table.innerHTML = ``;
  let lengte = 5;
  for (var i = 0; i < lengte; i++) {
    var row = `<tr> 
  <td> ${data[i].id} </td> 
  <td> ${data[i].name} </td> 
  <td> <input type="checkbox" name="aanmelding" id="host{{ forloop.counter }}" value="${data[i].id}"> </td>
  </tr>`;
    table.innerHTML += row;
  }
}

function Check(value) {
  console.log("Value:", value);
  // var testid = $(this).val(testid)
  console.log("Value:", value.parentelement);
  document.getElementById("mantis").innerHTML = value.checked;
  console.log("Value:", value.checked);
}
