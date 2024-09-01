<?php 

$servername = "sql7.freesqldatabase.com";
$database = "sql7728907";
$username = "sql7728907";
$password = "7lyDm7mLFT";

// Create connection

$conn = mysqli_connect($servername, $username, $password, $database);

// Check connection

if (!$conn) {

    die("Connection failed: " . 
mysqli_connect_error());

}
echo "Connected successfully";
mysqli_close($conn);


?>

