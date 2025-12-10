<?php
$host = getenv("MYSQL_HOST") ?: "127.0.0.1";
$user = getenv("MYSQL_USER") ?: "root";
$pass = getenv("MYSQL_PASSWORD") ?: "";
$dbn  = getenv("MYSQL_DATABASE") ?: "app";

$db = new mysqli($host, $user, $pass, $dbn);
if ($db->connect_error) {
    die("DB error");
}
