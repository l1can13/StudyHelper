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
                console.log(arr[i]);
            }
        }
    }
    return arr;
}

let hamburgerButton = document.querySelector('.spans');
let container = document.querySelector('.container');
let sideMenu = document.querySelector('.side_menu');
let showTeams = document.querySelector('.show_teams');
let manageBot = document.querySelector('.manage_bot');
let tableDiv = document.querySelector('.table_div');
let infoDiv = document.querySelector('.info_div');

let arrTeams = [], arrAllUser = [];
let helpArr = [["Название", "Продукт", "Администратор", "Ид"], ["Имя", "Группа", "Команда"]];

arrTeams = ajaxRequest("teams.php");
arrAllUser = ajaxRequest("all_users.php");
console.log(arrTeams);
console.log(arrTeams.length);
arrTeams.unshift(helpArr[0]);

console.log(arrTeams);
console.log(arrTeams[0]);
console.log(arrTeams[1]);
let table = createTable(arrTeams);
let temp = document.querySelector('.table');
temp.innerHTML = table;
tableDiv.appendChild(temp);

let trs = document.querySelectorAll('tr');

for (var i = 0; i < trs.length; ++i) {
    trs[i].addEventListener('click', function() {
        var input_name = this.getElementsByTagName("th")[0].innerHTML;
        var input_product = this.getElementsByTagName("th")[1].innerHTML;
        var input_admin = this.getElementsByTagName("th")[2].innerHTML;
        var url = 'team_list.html?'+ input_name + '&' + input_product + '&' + input_admin;
        window.location.href = url; 
    });
}

hamburgerButton.addEventListener('click', () => {
    hamburgerButton.classList.toggle('open');
    sideMenu.classList.toggle('show');
    showTeams.classList.toggle('show');
    manageBot.classList.toggle('show');
});

manageBot.addEventListener('click', () => {
    window.location.href = 'manage_bot.html';
});