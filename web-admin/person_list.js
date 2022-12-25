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
        console.log(data);
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
let showTeams = document.querySelector('.show_teams')
let manageBot = document.querySelector('.manage_bot');
let personName = document.querySelector('.name');
let groupName = document.querySelector('.groupname');
let userName = document.querySelector('.username');
let teamName = document.querySelector('.teamname');
let roleName = document.querySelector('.rolename');
let totalMark = document.querySelector('.itog_number');
let reportsText = document.querySelector('.reports_text');
let marksDiv = document.querySelector('.marks');
let getReports = document.querySelector('.get_reports');

let arrOneTeamUsers = [], arrOnePerson = [], arrReports = [];
let helpArr = [["Название", "Продукт", "Администратор", "Ид"], ["Имя", "Группа", "Username", "Роль"], ["Общая оценка", "Решение задач", "Командная работа", "Ответственность", "Помощь членам команды", "Автор оценки", "Дата"]];

var textt = decodeURIComponent(location.search.substring(1)).split('&');
personName.textContent = textt[0];
groupName.textContent = textt[1];
userName.textContent = textt[2];
teamName.textContent = textt[3];
roleName.textContent = textt[4];

arrUserInfo = ajaxRequest("one_person_info.php?username=" + textt[2]);
arrUserInfo.unshift(helpArr[2]);

let total_mark = 0;
for (var i = 1; i < arrUserInfo.length; ++i) {
    total_mark += Number(arrUserInfo[i][0]);
    total_mark += Number(arrUserInfo[i][1]);
    total_mark += Number(arrUserInfo[i][2]);

    var elem = arrUserInfo[i][6].split('.');
    arrUserInfo[i][6] = elem[0];
}
total_mark /= ((arrUserInfo.length - 1) * 3);
totalMark.textContent = total_mark.toFixed(2).toString();

let table = createTable(arrUserInfo);
let temp = document.querySelector('.table');
temp.innerHTML = table;
marksDiv.appendChild(temp);


let reports = "";
arrReports = ajaxRequest("user_reports.php?username=" + textt[2]);
for (var i = 0; i < arrReports.length; ++i) {
    reports += arrReports[i];
    reports += '\n';
}

getReports.addEventListener('click', () => {
    reportsText.textContent = reports;
});

hamburgerButton.addEventListener('click', () => {
    hamburgerButton.classList.toggle('open');
    sideMenu.classList.toggle('show');
    showTeams.classList.toggle('show');
    manageBot.classList.toggle('show');
});

showTeams.addEventListener('click', () => {
    window.location.href = 'index.html';
});

manageBot.addEventListener('click', () => {
    window.location.href = 'manage_bot.html';
});