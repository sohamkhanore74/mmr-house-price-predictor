document.getElementById("predict-form").addEventListener("submit", async function (e) {
  e.preventDefault();
  const form = e.target;
  const data = Object.fromEntries(new FormData(form).entries());

  const resultBox = document.getElementById("result");
  const errorBox = document.getElementById("error");
  resultBox.classList.add("hidden");
  errorBox.classList.add("hidden");

  try {
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const out = await res.json();

    if (!res.ok) {
      errorBox.textContent = out.error || "Something went wrong.";
      errorBox.classList.remove("hidden");
      return;
    }

    document.getElementById("price-value").textContent = out.price;
    document.getElementById("range-value").textContent = "Likely range: " + out.low + " to " + out.high;
    resultBox.classList.remove("hidden");
  } catch (err) {
    errorBox.textContent = "Could not reach the server.";
    errorBox.classList.remove("hidden");
  }
});
