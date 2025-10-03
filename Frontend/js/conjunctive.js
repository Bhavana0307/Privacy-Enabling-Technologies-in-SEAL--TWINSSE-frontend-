function generateRandomID(length = 12) {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let id = "";
  for (let i = 0; i < length; i++) {
    id += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return id;
}

function search() {
  const input = document.getElementById("queryInput").value.trim().toLowerCase();
  const resultDiv = document.getElementById("results");
  resultDiv.innerHTML = "";

  const data = JSON.parse(localStorage.getItem("sse_setup_data") || "{}");

  if (!data || Object.keys(data).length === 0) {
    resultDiv.innerHTML = "<p>❌ Please upload the setup file first.</p>";
    return;
  }

  const keywords = input.split(/\s+/);
  const resultSet = keywords.reduce((acc, keyword) => {
    const files = data[keyword] || [];
    if (acc === null) return new Set(files);
    return new Set([...acc].filter(x => files.includes(x)));
  }, null);

  if (!resultSet || resultSet.size === 0) {
    resultDiv.innerHTML = "<p>No matching files found.</p>";
    return;
  }

  resultDiv.innerHTML = "<h3>Matching Results (Simulated):</h3>";
  resultSet.forEach(() => {
    const fakeID = generateRandomID();
    const link = document.createElement("a");
    link.href = "files/dummy_result.txt"; // Replace with backend path later
    link.textContent = `📄 File ID: ${fakeID}`;
    link.download = "result.txt";
    link.className = "download-link";
    resultDiv.appendChild(link);
    resultDiv.appendChild(document.createElement("br"));
  });
}
