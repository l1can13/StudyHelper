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

let tableDiv = document.querySelectorAll('.table_div');

let notInBotArr = ["Имя", "Группа"];
let helpArr = ["Имя", "Группа", "Команда", "Количество отчетов", "Количество оценок", "Необходимое количество оценок"];

let notInBot = ajaxRequest("../php/not_in_bot.php");
let arrFinalReport = ajaxRequest("../php/debtors.php");
notInBot.unshift(notInBotArr);
arrFinalReport.unshift(helpArr);

console.log(notInBot);

let table = createTable(notInBot);
let temp = document.querySelectorAll('.table');
temp[0].innerHTML = table;
tableDiv[0].appendChild(temp[0]);

table = createTable(arrFinalReport);
temp[1].innerHTML = table;
tableDiv[1].appendChild(temp[1]);