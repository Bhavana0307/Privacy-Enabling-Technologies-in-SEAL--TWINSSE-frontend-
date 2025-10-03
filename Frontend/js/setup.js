document.getElementById("setupBtn").addEventListener("click", () => {
  document.getElementById("uploadInput").click();
});

document.getElementById("uploadInput").addEventListener("change", (event) => {
  const file = event.target.files[0];
  if (file && file.name.endsWith(".txt")) {
    const reader = new FileReader();
    reader.onload = function (e) {
      try {
        const textContent = e.target.result;

        // Simulated encrypted keyword index
        const fakeIndex = {
          demo: ["file1.txt", "file2.txt"],
          privacy: ["file2.txt"],
          tech: ["file3.txt"]
        };

        localStorage.setItem("sse_setup_data", JSON.stringify(fakeIndex));
        document.getElementById("setupStatus").innerText = `✅ Setup complete with: ${file.name}`;
      } catch (err) {
        alert("❌ Error parsing the file.");
      }
    };
    reader.readAsText(file);
  } else {
    alert("❌ Please upload a .txt file only for setup.");
  }
});
