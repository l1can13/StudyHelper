<?php header('Access-Control-Allow-Origin: *');

$connection = ssh2_connect('studhelper.online', 22);
ssh2_auth_password($connection, 'root', '4E%$@7-#?$|@');

ssh2_exec($connection, 'sudo systemctl start tgbot');