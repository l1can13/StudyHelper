<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

$par1_ip = "studhelper.online";
$par2_name = "studhelper";
$par3_p = "admin123";
$par4_db = "studhelper";

$mysqli = new mysqli($par1_ip, $par2_name, $par3_p, $par4_db);
mysqli_set_charset($mysqli,'utf8');

$sql = "SELECT a.user_id FROM users a, team_members b WHERE a.user_id = b.user_id AND a.name LIKE '$_GET[name]' AND a.group_num LIKE '$_GET[group]' AND b.role LIKE '$_GET[role]' AND b.team_id LIKE '$_GET[team]'";
$result = $mysqli->query($sql);

while ($row = $result->fetch_assoc()) {
    $array[] = $row;
}

echo json_encode($array);

?>