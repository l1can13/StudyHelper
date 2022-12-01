function createTable(arr) {
    var thead = `<thead>${arr[0].map(i => `<th>${i}</th>`).join("")}</thead>`;
    var tbody = `<tbody>${arr.slice(1).map(i => `<tr>${i.map(i => `<th>${i}</th>`).join("")}</tr>`).join("")}</tbody>`;
    var table = `<table>${thead}${tbody}</table>`;
    return table;
}

function ajaxRequest(phpName) {
    let arr = [];
    let ajax = new XMLHttpRequest();
    let dbData;
    ajax.open("GET", phpName, true);
    ajax.send();
    ajax.onreadystatechange = function () {
        if (ajax.readyState == 4 && ajax.status == 200) {
            let data = ajax.responseText;
            dbData = JSON.parse(data);

            for (let i = 0; i < dbData.length; ++i) {
                arr.push(Object.values(dbData[i]));
            }
        }
    }
    return arr;
}

let hamburgerButton = document.querySelector('.spans');
let container = document.querySelector('.container');
let sideMenu = document.querySelector('.side_menu');
let showTeams = document.querySelector('.show_teams')
let manageBot = document.querySelector('.manage_bot');
let teamName = document.querySelector('.team_name');
let productName = document.querySelector('.product_name');
let admin = document.querySelector('.admin');
let tableDiv = document.querySelector('.table_div');

let arrTeams = [], arrAllUser = [];
let helpArr = [["Название", "Администратор", "Продукт", "Ид"], ["Имя", "Фамилия", "Группа", "Username", "Роль"]];

arrTeams = ajaxRequest("teams.php");
arrAllUser = ajaxRequest("all_users.php");
arrTeams.unshift(helpArr[0]);

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