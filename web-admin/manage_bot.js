async function getSSHCommandResult(phpName) {
    await $.ajax({
        url: 'ssh_connect.php',
        method: 'GET',
    }).done(function (data, textStatus, jqXHR) {
        console.log(jqXHR.responseText);
    });
}

let info = getSSHCommandResult();
let hamburgerButton = document.querySelector('.spans');
let sideMenu = document.querySelector('.side_menu');
let showTeams = document.querySelector('.show_teams')
let showAllUser = document.querySelector('.show_all_users')
let manageBot = document.querySelector('.manage_bot');
let statistics = document.querySelector('.statistics');

hamburgerButton.addEventListener('click', () => {
    hamburgerButton.classList.toggle('open');
    sideMenu.classList.toggle('show');
    showTeams.classList.toggle('show');
    showAllUser.classList.toggle('show');
    manageBot.classList.toggle('show');
    statistics.classList.toggle('show');
});