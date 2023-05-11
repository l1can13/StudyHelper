<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

$par1_ip = "studhelper.online";
$par2_name = "studhelper";
$par3_p = "admin123";
$par4_db = "studhelper";

$mysqli = new mysqli($par1_ip, $par2_name, $par3_p, $par4_db);
mysqli_set_charset($mysqli,'utf8');

//$sql = "SELECT a.name, a.group_num, c.team_name, ROUND(AVG(d.overall_rating), 2), COUNT(d.assessored_user_id) FROM users a, team_members b, teams c, team_members_ratings d WHERE a.user_id = b.user_id AND b.team_id = c.team_id AND a.user_id = d.assessored_user_id GROUP BY a.user_id ORDER BY a.group_num, a.name";
$sql = "SELECT users.name, users.group_num, (SELECT teams.team_name FROM teams WHERE teams.team_id = (SELECT team_members.team_id FROM team_members WHERE team_members.user_id = users.user_id)) AS team_name, (SELECT COALESCE(AVG(team_members_ratings.overall_rating), '-') FROM team_members_ratings WHERE team_members_ratings.assessored_user_id = users.user_id) AS avg_mark, (SELECT COUNT(team_members_ratings.assessor_user_id) FROM team_members_ratings WHERE team_members_ratings.assessor_user_id = users.user_id) AS count_marks, (SELECT COUNT(sprint_reports.user_id) FROM sprint_reports WHERE sprint_reports.user_id = users.user_id) AS count_sprint_reports FROM users ORDER BY users.group_num";
$result = $mysqli->query($sql);

while ($row = $result->fetch_assoc()) {
    $array[] = $row;
}

echo json_encode($array);

?>