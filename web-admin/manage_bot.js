function getBotStatus() {
    let result;
    $.ajax({
        url: 'get_bot_status.php',
        method: 'GET',
        async: false,
    }).done(function (data, textStatus, jqXHR) {
       result = jqXHR.responseText;
    });

    return result;
}

function changeBotStatus(status) {
    $.ajax({
        url: (status === 'off') ? 'turn_off_bot.php' : 'turn_on_bot.php',
        method: 'GET',
        async: false,
    }).done(function (data, textStatus, jqXHR) {
       result = jqXHR.responseText;
    });
}

let hamburgerButton = document.querySelector('.spans');
let sideMenu = document.querySelector('.side_menu');
let showTeams = document.querySelector('.show_teams')
let showAllUser = document.querySelector('.show_all_users')
let manageBot = document.querySelector('.manage_bot');
let statistics = document.querySelector('.statistics');
let getBotStatusButton = document.querySelector('.get_bot_status');
let statusText = document.querySelector('.status_text');
let checkboxBot = document.querySelector('#checkbox_bot');

getBotStatus().includes('Active: active') ? checkboxBot.checked = true : checkboxBot.checked = false;


hamburgerButton.addEventListener('click', () => {
    hamburgerButton.classList.toggle('open');
    sideMenu.classList.toggle('show');
    showTeams.classList.toggle('show');
    showAllUser.classList.toggle('show');
    manageBot.classList.toggle('show');
    statistics.classList.toggle('show');
});

getBotStatusButton.addEventListener('click', () => {
    statusText.textContent = getBotStatus();
});

checkboxBot.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
        changeBotStatus('on');
      } else {
        changeBotStatus('off');
      }
});