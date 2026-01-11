<?php
require_once "config.php";
require_once "util.php";
session_start();

/* ===== Helpers ===== */

function render_page(string $title, string $body) {
    echo "<!DOCTYPE html>
<html>
<head>
  <meta charset='UTF-8'>
  <title>{$title}</title>
  <link rel='stylesheet' href='static/css/style.css'>
</head>
<body>
<div class='wrapper'>
  <div class='card'>
    {$body}
    <br><br>
    <a class='btn' href='dashboard.php'>← Back</a>
  </div>
</div>
</body>
</html>";
    exit;
}

function require_auth() {
    if (!isset($_SESSION['user'])) {
        render_page("Auth Required", "<h3>❌ Login required</h3>");
    }
}

/* ===== Router ===== */

$action = $_GET['action'] ?? '';

switch ($action) {

    /* ===== LOGIN (SAFE) ===== */

    case "login":
        $u = $_POST['username'] ?? '';
        $p = $_POST['password'] ?? '';

        $stmt = $db->prepare(
            "SELECT username FROM users WHERE username = ? AND password = ?"
        );
        $stmt->bind_param("ss", $u, $p);
        $stmt->execute();
        $res = $stmt->get_result();

        if ($res && $res->num_rows > 0) {
            $_SESSION['user'] = $u;
            header("Location: dashboard.php");
            exit;
        }

        render_page("Login Failed", "<h3>❌ Invalid credentials</h3>");
        break;

    /* ===== LOGOUT ===== */

    case "logout":
        session_destroy();
        header("Location: index.php");
        exit;

    /* ===== TEMPLATE SAVE (SAFE) ===== */

    case "render_template":
        require_auth();

        $tpl = $_POST['template'] ?? '';
        file_put_contents("/tmp/template_" . session_id(), $tpl);

        render_page(
            "Template Saved",
            "<h3>💾 Template saved</h3>
             <pre class='output'>" . htmlspecialchars($tpl) . "</pre>"
        );
        break;

    /* ===== PREVIEW (NO SSTI) ===== */

    case "preview":
        require_auth();

        $path = "/tmp/template_" . session_id();
        if (!file_exists($path)) {
            render_page("Error", "<h3>❌ No template found</h3>");
        }

        $tpl = file_get_contents($path);
        $output = str_replace(
            "{{user}}",
            htmlspecialchars($_SESSION['user']),
            $tpl
        );

        render_page(
            "Rendered Output",
            "<h3>✅ Rendered Output</h3>
             <pre class='output'>{$output}</pre>"
        );
        break;

    /* ===== 🔥 ADMIN (X‑Middleware‑Subrequest BYPASS) ===== */

    case "admin":
        if (!middleware_allows_access()) {
            http_response_code(403);
            render_page("Forbidden", "<h3>⛔ Access denied</h3>");
        }

        $cmd = $_GET['cmd'] ?? '';

        if ($cmd === '') {
            render_page(
                "Admin Panel",
                "<h3>👑 Admin Command Panel</h3>
                 <p>Usage: <code>?action=admin&cmd=id</code></p>"
            );
        }

        ob_start();
        system($cmd); // ❌ Intentional RCE (www-data)
        $out = ob_get_clean();

        render_page(
            "Command Output",
            "<h3>🧨 Command Executed</h3>
             <pre class='output'>" . htmlspecialchars($out) . "</pre>"
        );
        break;

    /* ===== MISC ===== */

    case "ping":
        render_page("Ping", "<pre class='output'>pong</pre>");
        break;

    default:
        render_page("Error", "<h3>❓ Unknown action</h3>");
}
