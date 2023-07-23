function createTable(arr) {
    var thead = `<thead>${arr[0].map(i => `<th>${i}</th>`).join("")}</thead>`;
    var tbody = `<tbody>${arr.slice(1).map(i => `<tr>${i.map(i => `<th>${i}</th>`).join("")}</tr>`).join("")}</tbody>`;
    var table = `<table>${thead}${tbody}</table>`;
    return table;
}

function ajaxRequest(phpName) {
    let arr = [];
    let result = [];

    $.ajax({
        url: phpName,
        method: 'GET',
        async: false,
    }).done(function (data, textStatus, jqXHR) {
        result = JSON.parse(data);
    });
    if (result) {
        for (let i = 0; i < result.length; ++i) {
            arr.push(Object.values(result[i]));
        }
    }

    return arr;
}

let container = document.querySelector('.container');
let tableDiv = document.querySelector('.table_div');

let helpArr = ["Имя", "Команда", "Количество отчетов", "Количество отзывов", "Необходимое количество отзывов"];

arrFinalReport = ajaxRequest("../php/debtors.php");
arrFinalReport.unshift(helpArr);

let table = createTable(arrFinalReport);
let temp = document.querySelector('.table');
temp.innerHTML = table;
tableDiv.appendChild(temp);