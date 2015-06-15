<?php
$send_email= new class_email_sender($name,$from,$to,$message);
$send_email->send_email();
?>
