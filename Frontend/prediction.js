// ✅ prediction.js – uses backend /video stream instead of direct webcam

const startBtn = document.getElementById("startPrediction");
const result = document.getElementById("predictionResult");

let isPredicting = false;

// 🧠 When user clicks Start Prediction
startBtn.addEventListener("click", () => {
  if (isPredicting) {
    isPredicting = false;
    startBtn.innerText = "Start Prediction";
    result.innerText = "";
  } else {
    isPredicting = true;
    startBtn.innerText = "Stop Prediction";
    updatePrediction();
  }
});

// 🔁 Fetch prediction from backend every 1 sec
async function updatePrediction() {
  if (!isPredicting) return;

  try {
    const response = await fetch("http://127.0.0.1:5000/prediction");
    const data = await response.json();

    if (data.label) {
      result.innerText = `Prediction: ${data.label} (${data.confidence}%)`;
    } else {
      result.innerText = "No hand detected...";
    }
  } catch (error) {
    console.error("Error fetching prediction:", error);
    result.innerText = "Error connecting to backend!";
  }

  // repeat every second
  setTimeout(updatePrediction, 1000);
}
