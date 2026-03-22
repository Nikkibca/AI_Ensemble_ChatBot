// function addMessage(text, sender, provider = "") {
//   const chatBox = document.getElementById("chat-box");

//   if (sender === "user") {
//     chatBox.innerHTML += `
//       <div class="user-msg">${text}</div>
//     `;
//   } else {
//     chatBox.innerHTML += `
//       <div class="bot-msg">
//         <pre>${text}</pre>
//         <div class="provider">Provider: ${provider}</div>
//       </div>
//     `;
//   }

//   chatBox.scrollTop = chatBox.scrollHeight;
// }

// async function sendMessage() {
//   const promptInput = document.getElementById("prompt");
//   const prefer = document.getElementById("prefer").value;
//   const prompt = promptInput.value.trim();

//   if (!prompt) return;

//   addMessage(prompt, "user");
//   promptInput.value = "";

//   const res = await fetch("/chat", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ prompt, prefer }),
//   });

//   const data = await res.json();

//   // addMessage(data.chosen_answer, "bot", data.chosen_provider);

//   addMessage(data.chosen_answer, "bot");
// }

function addMessage(text, sender) {
  const chatBox = document.getElementById("chat-box");

  const msg = document.createElement("div");
  msg.className = "message";

  if (sender === "user") {
    msg.innerHTML = `<div class="user">${text}</div>`;
  } else {
    msg.innerHTML = `<div class="bot">${text}</div>`;
  }

  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const promptInput = document.getElementById("prompt");
  const prefer = document.getElementById("prefer").value;
  const prompt = promptInput.value.trim();

  if (!prompt) return;

  addMessage(prompt, "user");
  promptInput.value = "";

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt, prefer }),
  });

  const data = await res.json();

  addMessage(data.chosen_answer, "bot");
}
