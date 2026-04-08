const terminal = document.getElementById("terminal");
const inputBox = document.getElementById("userInput");
const SESSION_ID = "default"; // 可改成动态生成

function printLine(text) {
    const line = document.createElement("div");
    line.textContent = text;
    terminal.appendChild(line);
    terminal.scrollTop = terminal.scrollHeight;
}

async function sendMessage(message) {
    printLine("> " + message);

    try {
        const resp = await fetch("/api/message", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: SESSION_ID, user_input: message })
        });

        if (!resp.ok) {
            printLine(`[错误] ${resp.status} ${resp.statusText}`);
            return;
        }

        const data = await resp.json();
        console.log("后端返回:", data); // 调试
        printLine(data.response || "[空响应]");
    } catch (err) {
        printLine(`[异常] ${err}`);
    }
}

inputBox.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        const msg = inputBox.value.trim();
        if (msg) {
            sendMessage(msg);
            inputBox.value = "";
            inputBox.focus();
        }
    }
});