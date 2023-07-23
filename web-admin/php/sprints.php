<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

$par1_ip = "studhelper.online";
$par2_name = "studhelper";
$par3_p = "admin123";
$par4_db = "studhelper";

$mysqli = new mysqli($par1_ip, $par2_name, $par3_p, $par4_db);
mysqli_set_charset($mysqli,'utf8');

//$sql = "SELECT a.name, a.group_num, c.team_name, ROUND(AVG(d.overall_rating), 2), COUNT(d.assessored_user_id) FROM users a, team_members b, teams c, team_members_ratings d WHERE a.user_id = b.user_id AND b.team_id = c.team_id AND a.user_id = d.assessored_user_id GROUP BY a.user_id ORDER BY a.group_num, a.name";
$sql = "SELECT t.team_name, tm.role, u.name, sr.sprint_num, sr.report_text FROM teams t JOIN team_members tm ON t.team_id = tm.team_id JOIN users u ON u.user_id = tm.user_id LEFT JOIN sprint_reports sr ON sr.user_id = u.user_id ORDER BY t.team_id, t.team_name, tm.role, u.name, sr.sprint_num";

$result = $mysqli->query($sql);

while ($row = $result->fetch_assoc()) {
    $array[] = $row;
}

echo json_encode($array);

?>