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

let hamburgerButton = document.querySelector('.spans');
let container = document.querySelector('.container');
let sideMenu = document.querySelector('.side_menu');
let showTeams = document.querySelector('.show_teams');
let showFinalReport = document.querySelector('.show_final_report');
let manageBot = document.querySelector('.manage_bot');
let manageDb = document.querySelector('.manage_db');
let excelBut = document.querySelector('.excel_button');
let tableDiv = document.querySelector('.table_div');
let infoDiv = document.querySelector('.info_div');

let arrFinalReport = [], arrIdAndRole = [];
let helpArr = ["Название команды", "Роль", "Имя", "Номер спринта", "Текст отчета"];

arrFinalReport = ajaxRequest("../php/sprints.php");
arrFinalReport.unshift(helpArr);

let table = createTable(arrFinalReport);
let temp = document.querySelector('.table');
temp.innerHTML = table;
tableDiv.appendChild(temp);

let trs = document.querySelectorAll('tr');

showTeams.addEventListener('click', () => {
    window.location.href = '../index/index.html';
});

manageBot.addEventListener('click', () => {
    window.location.href = '../manage_bot/manage_bot.html';
});