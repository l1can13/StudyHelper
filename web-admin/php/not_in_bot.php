<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

$par1_ip = "studhelper.online";
$par2_name = "studhelper";
$par3_p = "admin123";
$par4_db = "studhelper_dev";

$mysqli = new mysqli($par1_ip, $par2_name, $par3_p, $par4_db);
mysqli_set_charset($mysqli,'utf8');

$sql = "SELECT
  au.name AS 'Имя',
  au.group_num AS 'Группа'
FROM all_users au
LEFT JOIN users u ON au.name = u.name AND au.group_num = u.group_num
WHERE u.user_id IS NULL;
";

$result = $mysqli->query($sql);

while ($row = $result->fetch_assoc()) {
    $array[] = $row;
}

echo json_encode($array);

?>