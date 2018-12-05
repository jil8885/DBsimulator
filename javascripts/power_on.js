function render() {
    let yesButton = document.getElementById("yes");
    yesButton.style.fontWeight = "bold";
}

function change_selection(code, choice) {
    let yesButton = document.getElementById("yes");
    let noButton = document.getElementById("no");
    if(code === 39 && choice === 1){
        choice = 2;
        yesButton.style.fontWeight="normal";
        noButton.style.fontWeight="bold";
    } else if (code === 37 && choice === 2){
        choice = 1;
        yesButton.style.fontWeight="bold";
        noButton.style.fontWeight="normal";
    } else if (code === 13){
        if (choice === 1){
            location.href = "boot_with_reset.html";
        } else if (choice === 2){
            location.href = "boot_without_reset.html";
        }
    }
    return choice;
}