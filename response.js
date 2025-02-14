async function sendmessage() {
    let userText = document.getElementById("userInput").value;
    let responseBox = document.getElementById("response");

    if (userText.trim() === "") {
        responseBox.value = "It's okay, take your time. I'm here when you're ready.";
        return;
    }

    responseBox.value = "I'm listning....Let me gather my thoughts."; 
    // Placeholder while fetching

    try {
        let response = await fetch("http://localhost:8080/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ model: "mistral", prompt: userText })
        });

        let data = await response.json();
        responseBox.value = data.response || "I couldn't understand that. Can you please explain again?";
    } catch (error) {
        responseBox.value = "Error! couldn't connect to server";
    }
}
const defaultResponses = [
    "I'm here for you. Can you tell me more?",
    "That sounds tough. How does it make you feel?",
    "I hear you. What else is on your mind?",
    "Would you like to explore solutions together?"
];

function getResponse() {
    let userText = document.getElementById("userInput").value;
    let responseBox = document.getElementById("response");

    if (userText.trim() === "") {
        responseBox.value = "Please enter a message.";
        return;
    }

    let randomIndex = Math.floor(Math.random() * defaultResponses.length);
    responseBox.value = defaultResponses[randomIndex];
}

function clearText() {
    document.getElementById("userInput").value = "";  // Clear user input
    document.getElementById("response").value = "";   // Clear response
}
