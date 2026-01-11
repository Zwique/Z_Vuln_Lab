console.log("Loaded frontend");

// Example vulnerable client-side endpoint caller
async function ping() {
    let r = await fetch("/api.php?action=ping");
    console.log(await r.text());
}
