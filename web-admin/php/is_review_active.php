<?php header('Access-Control-Allow-Origin: *');

$connection = ssh2_connect('studhelper.online', 22);
ssh2_auth_password($connection, 'root', '4E%$@7-#?$|@');

$stream = ssh2_exec($connection, 'sudo systemctl status tgbot_review');
stream_set_blocking($stream, true);
$output = stream_get_contents($stream);

echo strrpos($output, "Active: active");