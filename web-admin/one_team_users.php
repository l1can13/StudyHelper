<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

$par1_ip = "server241.hosting.reg.ru";
$par2_name = "u1841284";
$par3_p = "gcb6Z3o89KTLkg1I";
$par4_db = "u1841284_studhelper";

$mysqli = new mysqli($par1_ip, $par2_name, $par3_p, $par4_db);
mysqli_set_charset($mysqli,'utf8');

$param = $_GET['team'];
$result = $mysqli->query("SELECT `Имя`, `Группа`, `User_name`, `Роль` FROM `Пользователи` WHERE `Команда` = '$param'");

while ($row = $result->fetch_assoc()) {
    $array[] = $row;
}

echo json_encode($array);

?>