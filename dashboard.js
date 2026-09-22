/* ==========================================
   TRANSITFLOW INTELLIGENCE
========================================== */


/* ==========================================
   RIDERSHIP LINE CHART
========================================== */

const ridershipCanvas =
    document.getElementById(
        "ridershipChart"
    );


const ridershipChart =
    new Chart(
        ridershipCanvas,
        {

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

                        label:
                            "Passenger journeys",

                        data: [

                            154,
                            168,
                            162,
                            181,
                            193,
                            139,
                            126

                        ],

                        borderWidth: 2,

                        tension: 0.35,

                        fill: false

                    }

                ]

            },


            options: {

                responsive: true,

                maintainAspectRatio: true,


                plugins: {

                    legend: {

                        labels: {

                            color:
                                "#a7afc0"

                        }

                    }

                },


                scales: {

                    x: {

                        ticks: {

                            color:
                                "#737c91"

                        },


                        grid: {

                            color:
                                "rgba(255,255,255,.04)"

                        }

                    },


                    y: {

                        ticks: {

                            color:
                                "#737c91"

                        },


                        grid: {

                            color:
                                "rgba(255,255,255,.04)"

                        }

                    }

                }

            }

        }
    );



/* ==========================================
   PEAK HOURS BAR CHART
========================================== */

const peakCanvas =
    document.getElementById(
        "peakChart"
    );


const peakChart =
    new Chart(
        peakCanvas,
        {

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

                        label:
                            "Demand",

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

                        borderWidth: 0

                    }

                ]

            },


            options: {

                responsive: true,


                plugins: {

                    legend: {

                        display: false

                    }

                },


                scales: {

                    x: {

                        ticks: {

                            color:
                                "#737c91"

                        },

                        grid: {

                            display: false

                        }

                    },


                    y: {

                        ticks: {

                            color:
                                "#737c91"

                        },

                        grid: {

                            color:
                                "rgba(255,255,255,.04)"

                        }

                    }

                }

            }

        }
    );



/* ==========================================
   ASK TRANSITFLOW
========================================== */

function askFlow() {


    const input =
        document.getElementById(
            "question"
        );


    const answer =
        document.getElementById(
            "answer"
        );


    const question =
        input.value
            .toLowerCase()
            .trim();



    if (!question) {

        answer.innerHTML = `

            <span>
                ✦
            </span>

            <div>
                Ask me something about
                the transit network.
            </div>

        `;

        return;
    }



    let response = `

        TransitFlow found that
        Route 204 currently records
        the highest passenger volume
        in the demo dataset.

        Demand is concentrated around
        the morning and evening commute
        windows.

    `;



    /* ==========================
       REVENUE QUESTION
    ========================== */

    if (
        question.includes("revenue") ||
        question.includes("money") ||
        question.includes("income")
    ) {

        response = `

            The current demo network
            estimates ₹8.6M in revenue
            for the selected period.

            The production version can
            calculate this directly from
            the connected transit dataset.

        `;

    }



    /* ==========================
       PEAK QUESTION
    ========================== */

    else if (

        question.includes("peak") ||
        question.includes("time") ||
        question.includes("busy")

    ) {

        response = `

            The strongest demand window
            in the current demo data is
            08:00–10:00.

            A second high-demand period
            appears around 18:00.

        `;

    }



    /* ==========================
       ROUTE QUESTION
    ========================== */

    else if (

        question.includes("route") ||
        question.includes("bus")

    ) {

        response = `

            Route 204 currently leads the
            demo network with approximately
            18,421 passenger journeys.

            Route 116 follows with around
            16,205 journeys.

        `;

    }



    /* ==========================
       PASSENGER QUESTION
    ========================== */

    else if (

        question.includes("passenger") ||
        question.includes("ridership")

    ) {

        response = `

            The network currently contains
            approximately 1.24M passenger
            journeys in the displayed
            demonstration period.

        `;

    }



    answer.innerHTML = `

        <span>
            ✦
        </span>

        <div>
            ${response}
        </div>

    `;

}
