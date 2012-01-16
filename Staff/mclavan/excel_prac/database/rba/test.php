<?php
include 'Loginfo.php';
$sql = "SELECT * FROM Student_info";
$result = mysql_query($sql,$link) or die("Unable to select: ".mysql_error());
print "<table>\n";
while($row = mysql_fetch_row($result)) {
    print "<tr>\n";
    foreach($row as $field) {
        print "<td>$field</td>\n";
    }
    print "</tr>\n";
}
print "</table>\n";
mysql_close($link);

?>
