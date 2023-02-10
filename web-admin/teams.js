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
let manageBot = document.querySelector('.manage_bot');
let manageDb = document.querySelector('.manage_db');
let tableDiv = document.querySelector('.table_div');
let infoDiv = document.querySelector('.info_div');

let arrTeams = [];
let helpArr = [["Ид команды", "Команда", "Продукт", "Имя администратора", "Ид администратора"], ["Имя", "Группа", "Команда"]];

arrTeams = ajaxRequest("teams.php");
namesByIds = ajaxRequest("name_by_id.php");

for (var i = 0; i < arrTeams.length; ++i) {
    arrTeams[i].push("");
    arrTeams[i][4] = arrTeams[i][3];
    for (var j = 0; j < namesByIds.length; ++j) {
        if (namesByIds[j][0] == arrTeams[i][4]) {
            arrTeams[i][3] = namesByIds[j][1];
        }
    }
}
console.log(arrTeams);
arrTeams.unshift(helpArr[0]);

let table = createTable(arrTeams);
let temp = document.querySelector('.table');
temp.innerHTML = table;
tableDiv.appendChild(temp);

let trs = document.querySelectorAll('tr');

for (var i = 0; i < trs.length; ++i) {
    trs[i].style.cursor = 'pointer';
    trs[i].addEventListener('click', function() {
        var input_team_id = this.getElementsByTagName("th")[0].innerHTML;
        var input_name = this.getElementsByTagName("th")[1].innerHTML;
        var input_product = this.getElementsByTagName("th")[2].innerHTML;
        var input_admin = this.getElementsByTagName("th")[3].innerHTML;
        var url = 'team_list.html?'+ input_name + '&' + input_product + '&' + input_admin + '&' + input_team_id;
        window.location.href = url; 
    });
}

hamburgerButton.addEventListener('click', () => {
    hamburgerButton.classList.toggle('open');
    sideMenu.classList.toggle('show');
    showTeams.classList.toggle('show');
    manageBot.classList.toggle('show');
    manageDb.classList.toggle('show');
});

manageBot.addEventListener('click', () => {
    window.location.href = 'manage_bot.html';
});