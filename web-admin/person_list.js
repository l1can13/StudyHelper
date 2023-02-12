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
let personName = document.querySelector('.name');
let groupName = document.querySelector('.groupname');
let userId = document.querySelector('.id');
let teamName = document.querySelector('.teamname');
let roleName = document.querySelector('.rolename');
let totalMark = document.querySelector('.itog_number');
let reportsText = document.querySelector('.reports_text');
let marksDiv = document.querySelector('.marks');
let getReports = document.querySelector('.get_reports');

let arrOneTeamUsers = [], arrOnePerson = [], arrReports = [], nameAndId = [];
let helpArr = [["Название", "Продукт", "Администратор", "Ид"], ["Имя", "Группа", "Username", "Роль"], ["Ид автора оценки", "Автор оценки", "Общая оценка", "Положительные моменты", "Отрицательные моменты", "Дата"]];
let clicked = false;

var textt = decodeURIComponent(location.search.substring(1)).split('&');
personName.textContent = textt[0];
userId.textContent = textt[1];
groupName.textContent = textt[2];
teamName.textContent = textt[3];
roleName.textContent = textt[4];

nameAndId = ajaxRequest("name_by_id.php");
console.log(nameAndId);
arrUserInfo = ajaxRequest("one_person_info.php?username=" + textt[1]);
arrUserInfo.unshift(helpArr[2]);

for (var i = 1; i < arrUserInfo.length; ++i) {
    for (var j = 0; j < nameAndId.length; ++j){
        if (nameAndId[j][0] == arrUserInfo[i][0]) {
            arrUserInfo[i][1] = nameAndId[j][1];
        }
    }
}

let table = createTable(arrUserInfo);
let temp = document.querySelector('.table');
temp.innerHTML = table;
marksDiv.appendChild(temp);

let reports = "";
arrReports = ajaxRequest("user_reports.php?userid=" + textt[1]);
for (var i = 0; i < arrReports.length; ++i) {
    reports += 'Спринт № ' + arrReports[i][0]+ ' , дата отчёта: ' + arrReports[i][1] + ' , текст отчёта: ' + arrReports[i][2] + '\n';
}

getReports.addEventListener('click', () => {
    if (getReports.innerHTML === 'Показать отчеты пользователя') {
        reportsText.textContent = reports;
        getReports.innerHTML = 'Скрыть отчеты пользователя'
        getReports.style.background = '#28293D';
        getReports.style.color = '#FEFFFF';
    }
    else {
        reportsText.textContent = '';
        getReports.innerHTML = 'Показать отчеты пользователя';
        getReports.style.background = '#D9D9D9';
        getReports.style.color = '#28293D';
    }
});

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