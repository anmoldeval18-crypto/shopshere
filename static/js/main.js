document.addEventListener("DOMContentLoaded", () => {
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach((alert) => {
        if (!alert.classList.contains("alert-danger")) {
            setTimeout(() => {
                const closeButton = alert.querySelector(".btn-close");
                if (closeButton) {
                    closeButton.click();
                }
            }, 3500);
        }
    });
});
