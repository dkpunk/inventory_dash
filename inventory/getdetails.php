<?php

$ip=$_POST['ip'];
$output=shell_exec("sh Invent_collection.sh $ip");
echo "$output";
?>
