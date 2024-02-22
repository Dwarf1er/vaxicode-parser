function urlSafeBase64Decode(base64UrlSafeString) {
    const base64String = base64UrlSafeString.replace(/-/g, '+').replace(/_/g, '/');

    const binaryString = atob(base64String);

    const length = binaryString.length;
    const bytes = new Uint8Array(length);
    for (let i = 0; i < length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }

    return bytes;
}

function shcToJwt(shcString) {
    shcString = shcString.split("/")[1];
    
    const pairs = [];
    for (let i = 0; i < shcString.length; i += 2) {
        pairs.push(shcString.slice(i, i + 2));
    }

    const asciiChars = [];
    for (const pair of pairs) {
        const asciiChar = parseInt(pair, 10);
        asciiChars.push(String.fromCharCode(asciiChar + 45));
    }

    const jwt = asciiChars.join("");

    return jwt;
}

function decodeJwt(jwt) {
    const [header, payload, signature] = jwt.split(".");

    const base64UrlSafePayload = urlSafeBase64Decode(payload);
    const inflatedPayload = pako.inflateRaw(base64UrlSafePayload);
    const decodedPayload = new TextDecoder().decode(inflatedPayload);

    return decodedPayload;
}

function decodeShc() {
    const shcString = document.getElementById("shcInput").value;
    const jwt = shcToJwt(shcString);
    const decodedData = decodeJwt(jwt);
    const decodedOutput = JSON.stringify(JSON.parse(decodedData), null, 4);
    document.getElementById("decodedOutput").value = decodedOutput;
}
