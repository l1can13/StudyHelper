function getBotStatusText() {
    let result;
    $.ajax({
        url: '../php/get_bot_status.php',
        method: 'GET',
        async: false,
    }).done(function (data, textStatus, jqXHR) {
        result = jqXHR.responseText;
    });

    return result;
}

function getBotStatus() {
    let result;
    $.ajax({
        url: '../php/is_bot_active.php',
        method: 'GET',
        async: false,
    }).done(function (data, textStatus, jqXHR) {
        result = jqXHR.responseText;
    });

    return result;
}

function getReviewStatus() {
    let result;
    $.ajax({
        url: '../php/is_review_active.php',
        method: 'GET',
        async: false,
    }).done(function (data, textStatus, jqXHR) {
        result = jqXHR.responseText;
    });

    return result;
}

function changeBotStatus(status) {
    $.ajax({
        url: (status === 'off') ? '../php/turn_off_bot.php' : '../php/turn_on_bot.php',
        method: 'POST',
        async: false,
    });
}

function changeReviewVisibility(review) {
    $.ajax({
        url: review ? '../php/turn_on_review.php' : '../php/turn_off_review.php',
        method: 'POST',
        async: false,
    });
}

let hamburgerButton = document.querySelector('.spans');
let sideMenu = document.querySelector('.side_menu');
let showTeams = document.querySelector('.show_teams');
let showFinalReport = document.querySelector('.show_final_report');
let manageBot = document.querySelector('.manage_bot');
let manageDb = document.querySelector('.manage_db');
let getBotStatusButton = document.querySelector('.get_bot_status');
let statusText = document.querySelector('.status_text');
let checkboxBot = document.querySelector('#checkbox_bot');
let checkboxReview = document.querySelector('#checkbox_review');

switch (getBotStatus()) {
    case '1':
        checkboxBot.checked = true;
        break;
    case '':
        checkboxBot.checked = false;
        break;
}

switch (getReviewStatus()) {
    case '':
        checkboxReview.checked = false;
        break;
    default:
        checkboxReview.checked = true;
        break;
}


hamburgerButton.addEventListener('click', () => {
    hamburgerButton.classList.toggle('open');
    sideMenu.classList.toggle('show');
    showTeams.classList.toggle('show');
    showFinalReport.classList.toggle('show');
    manageBot.classList.toggle('show');
    manageDb.classList.toggle('show');
});

getBotStatusButton.addEventListener('click', () => {
    statusText.textContent = getBotStatusText();
});

checkboxBot.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
        changeBotStatus('on');
    } else {
        changeBotStatus('off');
        checkboxReview.checked = false;
    }
});

checkboxReview.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
        changeReviewVisibility(true);
    } else {
        changeReviewVisibility(false);
    }
});

showTeams.addEventListener('click', () => {
    window.location.href = '../index/index.html';
});

showFinalReport.addEventListener('click', () => {
    window.location.href = '../final_report/final_report.html';
});