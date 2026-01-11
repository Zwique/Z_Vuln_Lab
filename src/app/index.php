<!DOCTYPE html>
<html>
<head>
  <title>SSTI Vuln Lab Version 2.0</title>
  <link rel="stylesheet" href="static/css/style.css">
</head>
<body>

<div class="wrapper">
  <div class="card">
    <h1>🧪 SSTI Vuln Lab</h1>
    <p class="subtext">Intentionally vulnerable PHP lab</p>

    <form method="POST" action="api.php?action=login">
      <input name="username" placeholder="username">
      <br><br>
      <input type="password" name="password" placeholder="password">
      <br><br>
      <button>Login</button>
    </form>

    <p class="subtext">⚠️ Never deploy on the internet</p>
  </div>
</div>

</body>
</html>
