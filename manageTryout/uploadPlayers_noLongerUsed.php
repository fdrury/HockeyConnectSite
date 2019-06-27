<?php
echo("test");
echo('<br>');
echo('<br>');
//POST csv file to REST service

echo readfile($_FILES["csvfileplayers"]["name"]);
echo('<br>');
echo basename($_FILES["csvfileplayers"]["name"]);
echo('<br>');
echo realpath($_FILES["csvfileplayers"]["name"]);
echo('<br>');
echo('<br>');

echo readfile($_FILES["csvfilecriteria"]["name"]);
echo('<br>');
echo basename($_FILES["csvfilecriteria"]["name"]);
echo('<br>');
echo realpath($_FILES["csvfilecriteria"]["name"]);
echo('<br>');
echo('<br>');

$fileplayers = $_FILES["csvfileplayers"]["name"];
$filecriteria = $_FILES["csvfilecriteria"]["name"];

/*
if (file_exists($file)) {
    echo("downloading");
    header('Content-Description: File Transfer');
    header('Content-Type: application/octet-stream');
    header('Content-Disposition: attachment; filename="'.basename($file).'"');
    header('Expires: 0');
    header('Cache-Control: must-revalidate');
    header('Pragma: public');
    header('Content-Length: ' . filesize($file));
    readfile($file);
    exit;
}
*/


$request = curl_init('localhost:5000/uploadPlayers');
curl_setopt($request, CURLOPT_POST, true);
curl_setopt($request, CURLOPT_POSTFIELDS, array('file' => '@' . $_FILES["csvfileplayers"]["name"]));
curl_setopt($request, CURLOPT_POSTFIELDS, array('file' => '@' . $_FILES["csvfilecriteria"]["name"]));
curl_setopt($request, CURLOPT_RETURNTRANSFER, true);
echo curl_exec($request);

curl_close($request);


?>