<?php

function middleware_allows_access(): bool {
    $hdr = $_SERVER['HTTP_X_MIDDLEWARE_SUBREQUEST'] ?? '';

    // ❌ VULNERABLE: trust client-supplied internal header
    if (strpos($hdr, 'middleware') !== false) {
        return true;
    }

    return isset($_SESSION['user']);
}
