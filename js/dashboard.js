// ==========================================
// TRANSITFLOW DASHBOARD
// ==========================================


// RIDERSHIP CHART
const ridershipCanvas =
    document.getElementById("ridershipChart");

if (ridershipCanvas) {

    new Chart(ridershipCanvas, {

        type: "line",

        data: {

            labels: [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun"
            ],

            datasets: [

                {
                    label: "Passenger journeys",

                    data: [
                        154,
                        168,
                        162,
                        181,
                        193,
                        139,
                        126
                    ],

                    borderWidth: 3,

                    tension: 0.4,

                    fill: true,

                    pointRadius: 4,

                    pointHoverRadius: 7
                }

            ]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {
                    display: false
                }
            },

            scales: {

                y: {

                    beginAtZero: false,

                    grid: {
                        color: "rgba(255,255,255,0.06)"
                    },

                    ticks: {
                        color: "#87958e"
                    }
                },

                x: {

                    grid: {
                        display: false
                    },

                    ticks: {
                        color: "#87958e"
                    }
                }
            }
        }
    });
}


// ==========================================
// PEAK HOURS CHART
// ==========================================

const peakCanvas =
    document.getElementById("peakChart");

if (peakCanvas) {

    new Chart(peakCanvas, {

        type: "bar",

        data: {

            labels: [
                "6 AM",
                "8 AM",
                "10 AM",
                "12 PM",
                "2 PM",
                "4 PM",
                "6 PM",
                "8 PM"
            ],

            datasets: [

                {
                    label: "Demand",

                    data: [
                        42,
                        91,
                        73,
                        58,
                        52,
                        67,
                        88,
                        49
                    ],

                    borderRadius: 6,

                    borderWidth: 0
                }

            ]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {
                    display: false
                }
            },

            scales: {

                y: {

                    beginAtZero: true,

                    grid: {
                        color: "rgba(255,255,255,0.06)"
                    },

                    ticks: {
                        color: "#87958e"
                    }
                },

                x: {

                    grid: {
                        display: false
                    },

                    ticks: {
                        color: "#87958e"
                    }
                }
            }
        }
    });
}


// ==========================================
// ASK TRANSITFLOW
// ==========================================

function askTransitFlow() {

    const input =
        document.getElementById("aiQuestion");

    const answer =
        document.getElementById("aiAnswer");

    const question =
        input.value.toLowerCase().trim();


    if (!question) {

        answer.innerHTML = `
            <span>AI</span>
            <p>
                Please enter a question first.
            </p>
        `;

        return;
    }


    let response = "";


    if (
        question.includes("revenue") ||
        question.includes("earning") ||
        question.includes("money")
    ) {

        response =
            "Estimated network revenue for the current demonstration period is ₹8.6M.";

    }

    else if (
        question.includes("peak") ||
        question.includes("busy") ||
        question.includes("highest") ||
        question.includes("demand")
    ) {

        response =
            "Demand is strongest around 08:00–10:00, with another significant peak around 18:00.";

    }

    else if (
        question.includes("route") ||
        question.includes("bus")
    ) {

        response =
            "Route 204 currently records the highest demonstration ridership at 18,421 passenger journeys, followed by Route 116 at 16,205.";

    }

    else if (
        question.includes("passenger") ||
        question.includes("ridership")
    ) {

        response =
            "The demonstration network contains approximately 1.24M passenger journeys for the displayed period.";

    }

    else {

        response =
            "Based on the displayed demonstration data, Route 204 has the highest ridership and morning demand is strongest between 08:00 and 10:00.";

    }


    answer.innerHTML = `
        <span>AI</span>

        <p>
            ${response}
        </p>
    `;
}
