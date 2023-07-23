function createTable(arr) {
    var thead = `<thead>${arr[0].map(i => `<th>${i}</th>`).join("")}</thead>`;
    var tbody = `<tbody>${arr.slice(1).map(i => `<tr>${i.map(i => `<th>${i}</th>`).join("")}</tr>`).join("")}</tbody>`;
    var table = `<table>${thead}${tbody}</table>`;
    return table;
}

function ajaxRequest(phpName) {
    let arr = [];
    let result;

    $.ajax({
        url: phpName,
        method: 'GET',
        async: false,
    }).done(function (data, textStatus, jqXHR) {
        result = JSON.parse(data);
    });

    for (let i = 0; i < result.length; ++i) {
        arr.push(Object.values(result[i]));
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
let tableDiv = document.querySelector('.table_div');
let infoDiv = document.querySelector('.info_div');

let arrTeams = [], ids = [];
let helpArr = [["Команда", "Продукт", "Администратор"], ["Имя", "Группа", "Команда"]];

arrTeams = ajaxRequest("../php/teams.php");
namesByIds = ajaxRequest("../php/name_by_id.php");

for (var i = 0; i < arrTeams.length; ++i) {
    ids.push(arrTeams[i][2]);
    for (var j = 0; j < namesByIds.length; ++j) {
        if (namesByIds[j][0] == arrTeams[i][2]) {
            arrTeams[i][2] = namesByIds[j][1];
        }
    }
}
arrTeams.unshift(helpArr[0]);

let table = createTable(arrTeams);
let temp = document.querySelector('.table');
temp.innerHTML = table;
tableDiv.appendChild(temp);

let trs = document.querySelectorAll('tr');

for (var i = 0; i < trs.length; ++i) {
    trs[i].style.cursor = 'pointer';
    trs[i].addEventListener('click', function() {
        var input_name = this.getElementsByTagName("th")[0].innerHTML;
        var input_product = this.getElementsByTagName("th")[1].innerHTML;
        var input_admin = this.getElementsByTagName("th")[2].innerHTML;
        var input_id = ids[this.rowIndex - 1];
        var url = '../team_list/team_list.html?'+ input_name + '&' + input_product + '&' + input_admin + '&' + input_id;
        window.location.href = url; 
    });
}

hamburgerButton.addEventListener('click', () => {
    hamburgerButton.classList.toggle('open');
    sideMenu.classList.toggle('show');
    showTeams.classList.toggle('show');
    showFinalReport.classList.toggle('show');
    manageBot.classList.toggle('show');
    manageDb.classList.toggle('show');
});

manageBot.addEventListener('click', () => {
    window.location.href = '../manage_bot/manage_bot.html';
});

showFinalReport.addEventListener('click', () => {
    window.location.href = '../final_report/final_report.html';
});