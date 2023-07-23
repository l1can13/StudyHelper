<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

$par1_ip = "studhelper.online";
$par2_name = "studhelper";
$par3_p = "admin123";
$par4_db = "studhelper_dev";

$mysqli = new mysqli($par1_ip, $par2_name, $par3_p, $par4_db);
mysqli_set_charset($mysqli,'utf8');

$sql = "SELECT au.name as Имя, IF(u.user_id IS NULL, 'ОТСУТСТВУЕТ В БОТЕ', t.team_name) AS Команда, IF(u.user_id IS NULL, 'ОТСУТСТВУЕТ В БОТЕ', IFNULL(COUNT(sr.report_text), 0)) AS `Количество отчётов`, IF(u.user_id IS NULL, 'ОТСТУСТВУЕТ В БОТЕ', IFNULL(COUNT(tmr.assessor_user_id), 0) + IFNULL(COUNT(tmr.assessored_user_id), 0)) AS `Количество оценок`, IF(u.user_id IS NULL, 'ОТСУТСТВУЕТ В БОТЕ', IFNULL((SELECT COUNT(*) FROM team_members tm WHERE tm.team_id = t.team_id) - 1, 0)) AS `Необходимое количество отзывов` FROM all_users au LEFT JOIN users u ON au.name = u.name AND au.group_num = u.group_num LEFT JOIN sprint_reports sr ON u.user_id = sr.user_id LEFT JOIN team_members tm ON u.user_id = tm.user_id LEFT JOIN teams t ON tm.team_id = t.team_id LEFT JOIN team_members_ratings tmr ON u.user_id = tmr.assessor_user_id OR u.user_id = tmr.assessored_user_id GROUP BY au.name, au.group_num";

$result = $mysqli->query($sql);

while ($row = $result->fetch_assoc()) {
    $array[] = $row;
}

echo json_encode($array);

?>