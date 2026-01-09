<?php
require_once "config.php";
require_once "util.php";
session_start();

/* ===== Helpers (STYLE ONLY) ===== */
 
function render_page($title, $body) {
    echo <<<HTML
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{$title}</title>
  <link rel="stylesheet" href="static/css/style.css">
</head>
<body>

<div class="wrapper">
  <div class="card">
    {$body}
    <br>
    <a class="btn" href="dashboard.php">← Back</a>
  </div>
</div>

</body>
</html>
HTML;
    exit;
}

function require_auth() {
    if (!isset($_SESSION['user'])) {
        render_page("Auth required", "<h3>Authentication required</h3>");
    }
}
 
/* ===== Router ===== */

$action = $_GET['action'] ?? '';

switch ($action) {

    /* ================= LOGIN (SQLi) ================= */

    case "login":
        $u = $_POST['username'] ?? '';
        $p = $_POST['password'] ?? '';

        // ❌ INTENTIONAL SQL INJECTION
        $sql = "SELECT username FROM users WHERE username='$u' AND password='$p'";
        $res = $db->query($sql);

        if ($res && $res->num_rows > 0) {
            $row = $res->fetch_assoc();
            $_SESSION['user'] = $row['username'];
            header("Location: dashboard.php");
            exit;
        }

        render_page(
            "Login Failed",
            "<h3>❌ Invalid credentials</h3>"
        );

    /* ================= LOGOUT ================= */

    case "logout":
        session_destroy();
        header("Location: index.php");
        exit;

    /* ================= SQLi → FILE WRITE ================= */

    case "load_note_to_template":
        require_auth();

        $title = $_GET['title'] ?? '';

        // ❌ INTENTIONAL SQL INJECTION
        $sql = "SELECT content FROM notes WHERE title = '$title'";
        $res = $db->query($sql);

        if ($res && $row = $res->fetch_assoc()) {
            file_put_contents(
                "/tmp/template_" . session_id(),
                $row['content']
            );

            render_page(
                "Template Loaded",
                "<h3>✅ Template loaded from database</h3>
                 <pre class='output'>" . htmlspecialchars($row['content']) . "</pre>"
            );
        }

        render_page(
            "No Note",
            "<h3>⚠️ No note found</h3>"
        );

    /* ================= MANUAL TEMPLATE SAVE ================= */

    case "render_template":
        require_auth();

        $tpl = $_POST['template'] ?? '';

        file_put_contents(
            "/tmp/template_" . session_id(),
            $tpl
        );

        render_page(
            "Template Saved",
            "<h3>💾 Template saved</h3>
             <pre class='output'>" . htmlspecialchars($tpl) . "</pre>"
        );

    /* ================= SSTI → RCE ================= */

    case "preview":
        require_auth();

        $path = "/tmp/template_" . session_id();
        if (!file_exists($path)) {
            render_page("Error", "<h3>❌ No template found</h3>");
        }

        $output = dangerous_template_render(
            file_get_contents($path)
        );

        render_page(
            "Template Output",
            "<h3>🧨 Rendered Output</h3>
             <pre class='output'>{$output}</pre>"
        );

    /* ================= MISC ================= */

    case "ping":
        render_page("Ping", "<pre class='output'>pong</pre>");

    default:
        render_page(
            "Unknown Action",
            "<h3>❓ Unknown action</h3>"
        );
}
