<!DOCTYPE html>
<html>
<head>
  <title>SSTI Vuln Lab</title>
  <link rel="stylesheet" href="static/css/style.css">
</head>
<body>

<div class="wrapper">
  <div class="card">
    <h1>🧪 SSTI Vuln Lab</h1>
    <p class="subtext">Intentionally vulnerable login portal</p>

    <form method="POST" action="api.php?action=login">
      <input name="username" placeholder="username">
      <br><br>
      <input type="password" name="password" placeholder="password">
      <br><br>
      <button>Login</button>
    </form>

    <div class="subtext" style="margin-top:1rem">
      ⚠️ Do not deploy on the internet
    </div>
  </div>

  <div class="footer">
    Beginner‑friendly exploitation lab
  </div>
</div>

</body>
</html>
