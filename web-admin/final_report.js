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
let excelBut = document.querySelector('.excel_button');
let tableDiv = document.querySelector('.table_div');
let infoDiv = document.querySelector('.info_div');

let arrFinalReport = [], arrIdAndRole = [];
let helpArr = [["Имя", "Группа", "Команда", "СО", "КО", "Количество отчетов"], ["Имя", "Группа", "Команда"]];

arrFinalReport = ajaxRequest("final_report.php");
console.log(arrFinalReport);
arrFinalReport.unshift(helpArr[0]);

let table = createTable(arrFinalReport);
let temp = document.querySelector('.table');
temp.innerHTML = table;
tableDiv.appendChild(temp);

let trs = document.querySelectorAll('tr');

for (var i = 0; i < trs.length; ++i) {
    trs[i].style.cursor = 'pointer';
    trs[i].addEventListener('click', function() {
        var input_name = this.getElementsByTagName("th")[0].innerHTML;
        var input_group = this.getElementsByTagName("th")[1].innerHTML;
        var input_team = this.getElementsByTagName("th")[2].innerHTML;
        arrIdAndRole = ajaxRequest("find_id_and_role.php?name=" + input_name + '&group=' + input_group +'&team=' + input_team);
        var input_role = arrIdAndRole[0][1];
        var input_id = arrIdAndRole[0][0];
        var url = 'person_list.html?'+ input_name  + '&' + input_id + '&' + input_group + '&' + input_team + '&' + input_role;
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

excelBut.addEventListener('click', () => {
    var excelFile = XLSX.utils.table_to_book(tableDiv, {sheet: "sheet1"});
    XLSX.write(excelFile, { bookType: 'xlsx', bookSST: true, type: 'base64' });
    XLSX.writeFile(excelFile, 'ExportedFile:HTMLTableToExcel' + '.xlsx');
})

showTeams.addEventListener('click', () => {
    window.location.href = 'index.html';
});

manageBot.addEventListener('click', () => {
    window.location.href = 'manage_bot.html';
});