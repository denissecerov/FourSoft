<?php
// Path to the JSON file
$dataFile = 'data/users.json';

// Get the input data
$username = $_POST['username'];
$email = $_POST['email'];
$password = $_POST['password'];

// Check if all fields are filled
if (empty($username) || empty($email) || empty($password)) {
    die("Please fill all fields.");
}

// Hash the password
$passwordHash = password_hash($password, PASSWORD_DEFAULT);

// Read the existing data
$data = file_get_contents($dataFile);
$users = json_decode($data, true);

// Check if the username or email already exists
foreach ($users as $user) {
    if ($user['username'] === $username) {
        die("Username already taken.");
    }
    if ($user['email'] === $email) {
        die("Email already registered.");
    }
}

// Add the new user to the array
$users[] = [
    'username' => $username,
    'email' => $email,
    'password_hash' => $passwordHash,
    'created_at' => date('Y-m-d H:i:s')
];

// Save the updated array back to the JSON file
file_put_contents($dataFile, json_encode($users));

// Registration successful
echo "Registration successful!";
?>