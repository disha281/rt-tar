async function sendMessage() {
  const input = document.getElementById("userInput");
  const chatBox = document.getElementById("chatBox");
  const message = input.value.trim();
  if (!message) return;

  // Add user bubble
  chatBox.innerHTML += `
        <div class="flex justify-end">
          <div class="max-w-xs bg-pinkdeep text-white px-4 py-2 rounded-2xl rounded-br-none shadow-md animate-fadeIn">
            ${message}
          </div>
        </div>`;
  input.value = "";
  chatBox.scrollTop = chatBox.scrollHeight;

  // Send to backend
  const res = await fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  const data = await res.json();

  // Add bot bubble
  chatBox.innerHTML += `
        <div class="flex justify-start">
          <div class="max-w-xs bg-white border border-pinkmain/40 text-gray-700 px-4 py-2 rounded-2xl rounded-bl-none shadow-md animate-fadeIn">
            ${data.reply || "⚠️ Server error, try again."}
          </div>
        </div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Small fade-in animation
const style = document.createElement("style");
style.textContent = `
      @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
      }
      .animate-fadeIn { animation: fadeIn 0.4s ease; }
    `;
document.head.appendChild(style);
