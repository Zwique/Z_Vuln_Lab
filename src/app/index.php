<!DOCTYPE html>
<html>
<head>
  <title>Middleware Vulnerability Lab</title>
  <link rel="stylesheet" href="static/css/style.css">
</head>
<body>

<div class="wrapper">
  <div class="card">
    <h1>Middleware Vulnerability Lab</h1>
    <p class="subtext">Intentionally vulnerable PHP lab</p>

    <form method="POST" action="api.php?action=login">
      <input name="username" placeholder="username">
      <br><br>
      <input type="password" name="password" placeholder="password">
      <br><br>
      <button>Login</button>
    </form>

    <p class="subtext">Do not deploy this lab on the internet.</p>
  </div>
</div>

</body>
</html>
