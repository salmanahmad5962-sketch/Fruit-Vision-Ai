export function showMessage(element, message, type = "info") {
  element.classList.remove("hidden", "info", "success", "error");
  element.classList.add(type);
  element.textContent = message;
}

export function hideMessage(element) {
  element.classList.add("hidden");
  element.classList.remove("info", "success", "error");
  element.textContent = "";
}

export function updateImagePreview(imageElement, dataUrl) {
  imageElement.src = dataUrl;
  imageElement.style.display = "block";
}

export function clearImagePreview(imageElement) {
  imageElement.src = "";
  imageElement.style.display = "none";
}

export function setClassifyButtonState(button, { disabled, loading }) {
  button.disabled = disabled;

  if (loading) {
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Classifying...';
    return;
  }

  button.innerHTML = 'Classify Fruit <i class="fas fa-arrow-right"></i>';
}

export function renderPredictionList(listElement, predictions) {
  listElement.innerHTML = "";

  predictions.forEach((prediction) => {
    const item = document.createElement("li");
    item.innerHTML = `
            <span>${prediction.name}</span>
            <span class="prediction-score">${prediction.confidence.toFixed(1)}%</span>
        `;

    listElement.appendChild(item);
  });
}

export function renderResult(result, elements) {
  elements.resultFruitName.textContent = result.fruitName;
  elements.resultFruitSubtitle.textContent = result.subtitle;

  elements.resultConfidenceFill.style.width = `${result.confidence.toFixed(1)}%`;
  elements.resultConfidenceText.textContent = `${result.confidence.toFixed(1)}% Confidence`;

  elements.resultImage.src = result.imageDataUrl;

  elements.calorieSearched.textContent = `${result.searchedCaloriesKcal} kcal`;
  elements.calorieProcessing.textContent = `${result.processingTimeMs}ms`;

  const classifiedLabel = result.classifiedAt
    ? `Classified at ${new Date(result.classifiedAt).toLocaleString()}`
    : "Classification complete";
  elements.resultMeta.textContent = classifiedLabel;

  renderPredictionList(elements.predictionList, result.predictions);
}
