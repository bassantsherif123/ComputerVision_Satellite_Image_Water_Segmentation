const model = document.getElementById("predictionModel");

function openModel() {
  model.style.display = "flex";
}

function closeModel() {
  model.style.display = "none";
}

window.onclick = function(event) {
  if (event.target === model) {
    model.style.display = "none";
  }
};

const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");

uploadArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  uploadArea.classList.add("dragover");
});

uploadArea.addEventListener("dragleave", () => {
  uploadArea.classList.remove("dragover");
});

uploadArea.addEventListener("drop", (e) => {
  e.preventDefault();
  uploadArea.classList.remove("dragover");
  const file = e.dataTransfer.files[0];
  fileInput.files = e.dataTransfer.files;
  handleFileUpload(file);
});

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (file) {
    handleFileUpload(file);
  }
});

function handleFileUpload(file) {
  const formData = new FormData();
  formData.append("file", file);

  uploadArea.innerHTML = `<p>📤 Uploading "${file.name}"...</p>`;

  fetch("/predict", {
    method: "POST",
    body: formData,
  })
    .then(async (response) => {
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || "Prediction failed");
      }
      return response.json();
    })
    .then((data) => {
      // Inject results with close button
      uploadArea.innerHTML = `
        <div style="position: relative; top=30px;">
          <button id="closeResultBtn" class="close-btn">×</button>
          <p>✅ File "${file.name}" uploaded successfully!</p>

          <div style="margin-top: 1em;">
            <h3>Bands Visualization</h3>
            <img src="${data.bands}" style="max-width: 100%;" />

            <h3 style="margin-top: 1em;">Predicted Mask</h3>
            <img src="${data.mask}" style="max-width: 100%;" />
          </div>

          <div style="margin-top: 1em;">
            <a href="${data.mask}" download="predicted_mask.png" class="download-btn"> Download Mask</a>
            <a href="${data.bands}" download="bands_visualization.png" class="download-btn"> Download Bands</a>
          </div>
        </div>
      `;

      // Handle close/reset button
      document.getElementById("closeResultBtn").addEventListener("click", resetUploadArea);
    })
    .catch((err) => {
      console.error("Prediction error:", err);
      uploadArea.innerHTML = `<p style="color:red;">❌ Error: ${err.message}</p>`;
    });
}

function resetUploadArea() {
  uploadArea.innerHTML = `
    <p>🛰️ Please Upload a Satellite Image here</p>
    <p class="upload-info"> <em> .tif, .tiff only </em> </p>
    <label class="upload-btn">
      Browse files
      <input type="file" id="fileInput" accept=".tif,.tiff">
    </label>
  `;

  // Reattach listener to new input
  const newFileInput = uploadArea.querySelector("input[type='file']");
  newFileInput.addEventListener("change", () => {
    const file = newFileInput.files[0];
    if (file) {
      handleFileUpload(file);
    }
  });
}