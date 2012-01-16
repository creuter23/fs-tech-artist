<?php

$hostname = "rba.thekotsch-war.com"; 
$username = "web_userck";   
$password = "Hr5kPNf7";   
$database = "rba_class";   

$link = mysql_connect($hostname,$username,$password);
mysql_select_db($database) or die("Unable to select database");

?>
