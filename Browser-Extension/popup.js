document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.sync.get(["provider", "token"], (data) => {
    if (data.provider) document.getElementById("provider").value = data.provider;
    if (data.token) document.getElementById("token").value = data.token;
  });

  document.getElementById("generate").addEventListener("click", () => {
    const provider = document.getElementById("provider").value;
    const token = document.getElementById("token").value;
    const post_url = document.getElementById("post_url").value;

    chrome.storage.sync.set({ provider, token });

    fetch("http://localhost:8000/linkedin-comment", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ post_url, provider, token })
    })
    .then(response => response.json())
    .then(data => {
      const comment = data.suggested_comment || "No comment generated.";
      document.getElementById("output").value = comment;
      navigator.clipboard.writeText(comment);
    })
    .catch(err => {
      console.error(err);
      document.getElementById("output").value = "Error generating comment.";
    });
  });
});