<?php header('Access-Control-Allow-Origin: *');

$connection = ssh2_connect('studhelper.online', 22);
ssh2_auth_password($connection, 'root', '9hfeygRJw~-$');

ssh2_exec($connection, 'sudo systemctl stop tgbot_review');
ssh2_exec($connection, 'sudo systemctl start tgbot');