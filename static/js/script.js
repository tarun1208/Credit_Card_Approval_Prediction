/* =====================================================
        CREDIT CARD APPROVAL PREDICTION
        JavaScript
===================================================== */

document.addEventListener("DOMContentLoaded", function () {

    console.log("Application Loaded Successfully");

    initializeCounters();

    initializeProgressBars();

    initializeCards();

    initializeNavbar();

});

/* =====================================================
        NUMBER COUNTER
===================================================== */

function initializeCounters() {

    const counters = document.querySelectorAll(".stat-card h2");

    counters.forEach(counter => {

        const text = counter.innerText;

        const number = parseFloat(text.replace(/[^\d.]/g, ""));

        if (isNaN(number)) return;

        const suffix = text.replace(/[\d.]/g, "");

        let current = 0;

        const increment = number / 80;

        function updateCounter() {

            current += increment;

            if (current >= number) {

                counter.innerText = number + suffix;

            }

            else {

                counter.innerText = Math.floor(current) + suffix;

                requestAnimationFrame(updateCounter);

            }

        }

        updateCounter();

    });

}

/* =====================================================
        PROGRESS BAR
===================================================== */

function initializeProgressBars() {

    const bars = document.querySelectorAll(".progress-bar");

    bars.forEach(bar => {

        const width = bar.style.width;

        bar.style.width = "0%";

        setTimeout(() => {

            bar.style.transition = "2s";

            bar.style.width = width;

        }, 500);

    });

}

/* =====================================================
        CARD HOVER
===================================================== */

function initializeCards() {

    const cards = document.querySelectorAll(

        ".feature-box,.prediction-card,.result-card,.summary-card,.customer-profile"

    );

    cards.forEach(card => {

        card.addEventListener("mouseenter", function () {

            this.style.transform = "translateY(-10px)";

        });

        card.addEventListener("mouseleave", function () {

            this.style.transform = "translateY(0px)";

        });

    });

}

/* =====================================================
        NAVBAR
===================================================== */

function initializeNavbar() {

    const navbar = document.querySelector(".custom-navbar");

    if (!navbar) return;

    window.addEventListener("scroll", function () {

        if (window.scrollY > 40) {

            navbar.style.boxShadow =

                "0 15px 40px rgba(0,0,0,.20)";

        }

        else {

            navbar.style.boxShadow =

                "0 10px 25px rgba(0,0,0,.15)";

        }

    });

}

/* =====================================================
        SCROLL ANIMATION
===================================================== */

const observer = new IntersectionObserver(

    entries => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("show");

            }

        });

    },

    {

        threshold: 0.15

    }

);

document.querySelectorAll(

    ".feature-box,.stat-card,.prediction-card,.result-card"

).forEach(el => {

    el.classList.add("hidden");

    observer.observe(el);

});

/* =====================================================
            AI LOADING SCREEN
===================================================== */

/* =====================================================
        PREMIUM AI LOADING ANIMATION
===================================================== */

document.addEventListener("DOMContentLoaded", function () {

    const loadingScreen = document.getElementById("loading-screen");
    const loaderBar = document.getElementById("loader-bar");
    const loaderPercent = document.getElementById("loader-percent");
    const loadingMessage = document.getElementById("loading-message");
    const predictForm = document.getElementById("prediction-form");

    // Hide loader after page loads
    if (loadingScreen) {
        loadingScreen.classList.remove("active");
    }

    if (predictForm) {

        predictForm.addEventListener("submit", function () {

            loadingScreen.classList.add("active");
            loaderBar.style.width = "0%";
            loaderPercent.innerHTML = "0%";
            loadingMessage.innerHTML = "Initializing AI Engine...";

            let progress = 0;

            const messages = [

                "Initializing AI Engine...",

                "Validating Customer Details...",

                "Encoding Categorical Features...",

                "Scaling Numerical Features...",

                "Running Random Forest Model...",

                "Calculating Approval Probability...",

                "Assessing Credit Risk...",

                "Generating Final Decision..."

            ];

            let index = 0;

            loadingMessage.innerHTML = messages[0];

            const progressInterval = setInterval(function () {

                if (progress < 95) {

                    progress++;

                    loaderBar.style.width = progress + "%";

                    loaderPercent.innerHTML = progress + "%";

                }

            }, 40);

            const messageInterval = setInterval(function () {

                index++;

                if (index < messages.length) {

                    loadingMessage.style.opacity = 0;

                    setTimeout(function () {

                        loadingMessage.innerHTML = messages[index];

                        loadingMessage.style.opacity = 1;

                    }, 200);

                }

                else {

                    clearInterval(messageInterval);

                }

            }, 700);

        });

    }

});