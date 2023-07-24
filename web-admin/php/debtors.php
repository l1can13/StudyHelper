<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

$par1_ip = "studhelper.online";
$par2_name = "studhelper";
$par3_p = "admin123";
$par4_db = "studhelper_dev";

$mysqli = new mysqli($par1_ip, $par2_name, $par3_p, $par4_db);
mysqli_set_charset($mysqli,'utf8');

$sql = "SELECT
  u.name AS 'Имя',
  u.group_num AS 'Группа',
  COALESCE(t.team_name, 'Отсутствует в боте') AS 'Команда',
  COALESCE(reports_count, 0) AS 'Количество отчетов',
  COALESCE(ratings_count, 0) AS 'Количество оценок',
  (COALESCE((SELECT COUNT(*) FROM team_members tm WHERE t.team_id = tm.team_id AND u.user_id != tm.user_id), 0)) AS 'Необходимое количество оценок'
FROM users u
LEFT JOIN team_members tm ON u.user_id = tm.user_id
LEFT JOIN teams t ON tm.team_id = t.team_id
LEFT JOIN (
  SELECT user_id, COUNT(*) AS reports_count
  FROM sprint_reports
  GROUP BY user_id
) sr ON u.user_id = sr.user_id
LEFT JOIN (
  SELECT assessor_user_id, COUNT(*) AS ratings_count
  FROM team_members_ratings
  GROUP BY assessor_user_id
) tr ON u.user_id = tr.assessor_user_id
WHERE COALESCE(reports_count, 0) < 6
OR COALESCE(ratings_count, 0) < COALESCE((SELECT COUNT(*) FROM team_members tm WHERE t.team_id = tm.team_id AND u.user_id != tm.user_id), 0);
";

$result = $mysqli->query($sql);

while ($row = $result->fetch_assoc()) {
    $array[] = $row;
}

echo json_encode($array);

?>