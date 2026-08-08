import { HISTORY_LIMIT, HISTORY_STORAGE_KEY } from "./constants.js";

function safeParse(jsonValue) {
  try {
    const parsed = JSON.parse(jsonValue);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

export function getClassificationHistory() {
  const raw = localStorage.getItem(HISTORY_STORAGE_KEY);
  if (!raw) {
    return [];
  }

  return safeParse(raw);
}

export function saveClassificationRecord(record) {
  const history = getClassificationHistory();

  const sanitized = {
    fileName: record.fileName,
    fileSize: record.fileSize,
    fruitName: record.fruitName,
    confidence: Number(record.confidence.toFixed(1)),
    searchedCaloriesKcal: record.searchedCaloriesKcal,
    classifiedAt: record.classifiedAt,
    modelVersion: record.modelVersion,
  };

  const updated = [sanitized, ...history].slice(0, HISTORY_LIMIT);
  localStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(updated));

  return updated;
}
