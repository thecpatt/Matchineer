document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript loaded!"); // Debugging check

    function enforceCheckboxLimit(questionName, maxSelection = 3) {
        const checkboxes = document.querySelectorAll(`input[name="${questionName}"]`);

        function updateCheckboxState() {
            let checkedBoxes = document.querySelectorAll(`input[name="${questionName}"]:checked`);

            checkboxes.forEach(cb => {
                if (checkedBoxes.length >= maxSelection && !cb.checked) {
                    cb.disabled = true;  // Disable unchecked checkboxes when max is reached
                } else {
                    cb.disabled = false; // Re-enable when below max
                }
            });
        }

        checkboxes.forEach(checkbox => {
            checkbox.addEventListener("change", updateCheckboxState);
        });
    }

    // Automatically apply to all checkbox groups
    document.querySelectorAll("input[type='checkbox']").forEach(checkbox => {
        let questionName = checkbox.name;
        enforceCheckboxLimit(questionName, 3);
    });
});
