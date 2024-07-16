<?php
// Path to the JSON file
$dataFile = 'data/users.json';

// Get the input data
$username = $_POST['username'];
$password = $_POST['password'];

// Check if all fields are filled
if (empty($username) || empty($password)) {
    die("Please fill all fields.");
}

// Read the existing data
$data = file_get_contents($dataFile);
$users = json_decode($data, true);

// Verify the user credentials
foreach ($users as $user) {
    if ($user['username'] === $username) {
        if (password_verify($password, $user['password_hash'])) {
            echo "Login successful!";
            exit;
        } else {
            die("Incorrect password.");
        }
    }
}

// User not found
die("Username not found.");
?>