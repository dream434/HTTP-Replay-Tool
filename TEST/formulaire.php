<?php

$user_stocke = "admin";
$pass_stocke = "123456";

// Variables
$message = "";

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $user = $_POST["user"] ?? "";
    $pass = $_POST["pass"] ?? "";

    if ($user === $user_stocke && $pass === $pass_stocke) {
        $message = "<p style='color:green;'><strong>Bravo ! Connexion réussie</strong></p>";
    } else {
        $message = "<p style='color:red;'><strong>Identifiants invalides</strong></p>";
    }
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Connexion simple PHP</title>
</head>
<body>
  <h1>Connexion</h1>

  <?= $message ?>

  <form method="post">
    <label>Nom d'utilisateur : 
      <input type="text" name="user" required>
    </label><br><br>
    <label>Mot de passe : 
      <input type="password" name="pass" required>
    </label><br><br>
    <button type="submit">Se connecter</button>
  </form>
</body>
</html>
