async function parseJson(response) {
  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("application/json")) {
    return {};
  }

  try {
    return await response.json();
  } catch {
    return {};
  }
}

async function throwIfNotOk(response) {
  if (response.ok) {
    return;
  }

  const payload = await parseJson(response);
  const message =
    payload.error || `Request failed with status ${response.status}.`;
  throw new Error(message);
}

export async function classifyImageViaApi(file) {
  const formData = new FormData();
  formData.append("image", file, file.name);

  const response = await fetch("/api/classify", {
    method: "POST",
    body: formData,
  });

  await throwIfNotOk(response);
  return parseJson(response);
}

export async function submitContactMessage({ name, email, message }) {
  const response = await fetch("/api/contact", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name, email, message }),
  });

  await throwIfNotOk(response);
  return parseJson(response);
}

export async function fetchAdminSummary(adminKey) {
  const response = await fetch("/api/admin/summary", {
    method: "GET",
    headers: {
      "X-Admin-Key": adminKey,
    },
  });

  await throwIfNotOk(response);
  return parseJson(response);
}

export async function saveFruitFromAdmin(adminKey, fruitPayload) {
  const response = await fetch("/api/admin/fruits", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Admin-Key": adminKey,
    },
    body: JSON.stringify(fruitPayload),
  });

  await throwIfNotOk(response);
  return parseJson(response);
}

export async function activateModelFromAdmin(adminKey, modelPayload) {
  const response = await fetch("/api/admin/model/activate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Admin-Key": adminKey,
    },
    body: JSON.stringify(modelPayload),
  });

  await throwIfNotOk(response);
  return parseJson(response);
}
