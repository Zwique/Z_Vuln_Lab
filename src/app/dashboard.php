<?php
session_start();
if (!isset($_SESSION['user'])) {
    header("Location: index.php");
    exit;
}
?>

<!DOCTYPE html>
<html>
<head>
  <title>Dashboard</title>
  <link rel="stylesheet" href="static/css/style.css">
</head>
<body>

<div class="header">
  <div>Middleware Vulnerability Lab</div>
  <div>
    Hello <strong><?= htmlspecialchars($_SESSION['user']) ?></strong> ·
    <a href="api.php?action=logout">Logout</a>
  </div>
</div>

<div class="wrapper">

  <div class="card">
    <h3>Save Template <span class="danger">UNSAFE</span></h3>
    <p class="subtext">
      This template is rendered server‑side without sanitization.
    </p>

    <form method="POST" action="api.php?action=render_template">
      <textarea
        name="template"
        rows="6"
        placeholder="Hello {{whoami}}"
      ></textarea>

      <br><br>
      <button>Save Template</button>
    </form>
  </div>

  <div class="card">
    <h3>Preview</h3>
    <p class="subtext">
      Execute the template using the server template engine.
    </p>

    <a class="btn" href="api.php?action=preview">Render Template</a>
  </div>

</div>

</body>
</html>
