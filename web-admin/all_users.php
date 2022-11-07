<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

$par1_ip = "server136.hosting.reg.ru";
$par2_name = "u1789997";
$par3_p = "v9VFX935Zqj8x05Hp";
$par4_db = "u1789997_studhelper";

$mysqli = new mysqli($par1_ip, $par2_name, $par3_p, $par4_db);
mysqli_set_charset($mysqli,'utf8');

$result = $mysqli->query("SELECT `Имя`, `Группа`, `Команда` FROM `Пользователи`");

$array = [];

while ($row = $result->fetch_assoc()) {
    $array[] = $row;
}

echo json_encode($array);

?>