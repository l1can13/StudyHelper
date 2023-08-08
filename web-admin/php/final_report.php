<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

$par1_ip = "studhelper.online";
$par2_name = "studhelper";
$par3_p = "admin123";
$par4_db = "studhelper";

$mysqli = new mysqli($par1_ip, $par2_name, $par3_p, $par4_db);
mysqli_set_charset($mysqli,'utf8');

//$sql = "SELECT a.name, a.group_num, c.team_name, ROUND(AVG(d.overall_rating), 2), COUNT(d.assessored_user_id) FROM users a, team_members b, teams c, team_members_ratings d WHERE a.user_id = b.user_id AND b.team_id = c.team_id AND a.user_id = d.assessored_user_id GROUP BY a.user_id ORDER BY a.group_num, a.name";
$sql = "SELECT u.name, u.group_num, ( SELECT t.team_name FROM teams AS t WHERE t.team_id IN ( SELECT tm.team_id FROM team_members AS tm WHERE tm.user_id = u.user_id ) LIMIT 1 ) AS team_name, ( SELECT COALESCE(AVG(tmr.overall_rating), '-') FROM team_members_ratings AS tmr WHERE tmr.assessored_user_id = u.user_id ) AS avg_mark, ( SELECT COUNT(tmr.assessor_user_id) FROM team_members_ratings AS tmr WHERE tmr.assessor_user_id = u.user_id ) AS count_marks, ( SELECT COUNT(sr.user_id) FROM sprint_reports AS sr WHERE sr.user_id = u.user_id ) AS count_sprint_reports FROM users AS u ORDER BY u.group_num";
$result = $mysqli->query($sql);

while ($row = $result->fetch_assoc()) {
    $array[] = $row;
}

echo json_encode($array);

?>