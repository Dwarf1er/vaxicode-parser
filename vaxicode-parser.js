function urlSafeBase64Decode(base64UrlSafeString) {
    const base64String = base64UrlSafeString.replace(/-/g, "+").replace(/_/g, "/");

    const binaryString = atob(base64String);

    const length = binaryString.length;
    const bytes = new Uint8Array(length);
    for (let i = 0; i < length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }

    return bytes;
}

function readQRCode(imageInput, callback) {
    const reader = new FileReader();
    reader.readAsDataURL(imageInput);

    reader.onload = function(event) {
        const image = new Image();
        image.onload = function() {
            const canvas = document.createElement("canvas");
            const ctx = canvas.getContext("2d");
            canvas.width = image.width;
            canvas.height = image.height;
            ctx.drawImage(image, 0, 0);
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const code = jsQR(imageData.data, imageData.width, imageData.height);
            if (code) {
                callback(code.data);
            } else {
                document.getElementById("decodedOutput").style.color = "red";
                document.getElementById("decodedOutput").value = "No QR code was found in this image, or reading information from canvas is disabled in your browser";
            }
        };
        image.src = event.target.result;
    };
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
    const imageInput = document.getElementById("imageInput").files[0];
    const pdfInput = document.getElementById("pdfInput").files[0];

    let decodedOutputTextArea = document.getElementById("decodedOutput");

    if (pdfInput) {
        // PDF LOGIC
        console.log("PDF INPUT");
    } else if (imageInput) {
        readQRCode(imageInput, function(shcString) {
            const jwt = shcToJwt(shcString);
            const decodedData = decodeJwt(jwt);
            const decodedOutput = JSON.stringify(JSON.parse(decodedData), null, 4);
            decodedOutputTextArea.value = decodedOutput;
            document.getElementById("imageInput").value = null; 
        });
    } else if (shcString.trim() !== "") {
        const jwt = shcToJwt(shcString);
        const decodedData = decodeJwt(jwt);
        const decodedOutput = JSON.stringify(JSON.parse(decodedData), null, 4);
        decodedOutputTextArea.value = decodedOutput;
        document.getElementById("shcInput").value = null;
    } else {
        decodedOutput.style.color = "red";
        decodedOutput.value = "Please provide either a SHC string, QR code image, or PDF!";
    }
}
