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
        console.log(data);
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
let teamName = document.querySelector('.team_name');
let productName = document.querySelector('.product_name');
let admin = document.querySelector('.admin');
let tableDiv = document.querySelector('.table_div');
let id = document.querySelector('.id');

let arrTeams = [], arrAllUser = [], arrOneTeamUsers = [], usernameAndId = [];
let helpArr = [["Название", "Продукт", "Администратор", "Ид"], ["Ид пользователя", "Имя", "Группа", "Роль"]];

var textt = decodeURIComponent(location.search.substring(1)).split('&');
teamName.textContent = textt[0];
productName.textContent = textt[1];
admin.textContent = textt[2];
id.textContent = textt[3];

arrTeams = ajaxRequest("teams.php");
arrOneTeamUsers = ajaxRequest("one_team_users.php?team=" + textt[3]);
arrTeams.unshift(helpArr[0]);
arrOneTeamUsers.unshift(helpArr[1]);

let table = createTable(arrOneTeamUsers);
let temp = document.querySelector('.table');
temp.innerHTML = table;
tableDiv.appendChild(temp)

let trs = document.querySelectorAll('tr');

for (var i = 0; i < trs.length; ++i) {
    trs[i].style.cursor = 'pointer';
    trs[i].addEventListener('click', function() {
        var input_id = this.getElementsByTagName("th")[0].innerHTML;
        var input_name = this.getElementsByTagName("th")[1].innerHTML;
        var input_group = this.getElementsByTagName("th")[2].innerHTML;
        var input_role = this.getElementsByTagName("th")[3].innerHTML;
        var url = 'person_list.html?'+ input_name  + '&' + input_id + '&' + input_group + '&' + textt[0] + '&' + input_role;
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

showTeams.addEventListener('click', () => {
    window.location.href = 'index.html';
});

showFinalReport.addEventListener('click', () => {
    window.location.href = 'final_report.html';
});

manageBot.addEventListener('click', () => {
    window.location.href = 'manage_bot.html';
});