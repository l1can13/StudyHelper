<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

$par1_ip = "server241.hosting.reg.ru";
$par2_name = "u1841284";
$par3_p = "gcb6Z3o89KTLkg1I";
$par4_db = "u1841284_studhelper";

$mysqli = new mysqli($par1_ip, $par2_name, $par3_p, $par4_db);
mysqli_set_charset($mysqli,'utf8');

$result = $mysqli->query("SELECT `Дата отправки`, `Текст отчета` FROM `Отчеты` WHERE `Автор отчета` LIKE '$_GET[username]'");

while ($row = $result->fetch_assoc()) {
    $array[] = $row;
}

echo json_encode($array);

?>