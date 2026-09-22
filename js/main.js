/* ==========================================
   TRANSITFLOW MAIN JAVASCRIPT
========================================== */


/* ==========================================
   ANIMATED STATISTICS
========================================== */

const countElements =
    document.querySelectorAll("[data-count]");


countElements.forEach(element => {

    const target =
        Number(element.dataset.count);

    let current = 0;

    const step =
        Math.max(
            1,
            Math.ceil(target / 60)
        );


    const timer =
        setInterval(() => {

            current += step;


            if (current >= target) {

                current = target;

                clearInterval(timer);
            }


            if (target >= 1000000) {

                element.textContent =
                    (current / 1000000)
                    .toFixed(2) + "M";

            }

            else if (target >= 1000) {

                element.textContent =
                    Math.round(current / 1000) + "K";

            }

            else {

                element.textContent =
                    current.toLocaleString();
            }

        }, 18);

});


/* ==========================================
   JOURNEY PLANNER
========================================== */

function planJourney() {

    const from =
        document.getElementById("from").value ||
        "Origin";


    const to =
        document.getElementById("to").value ||
        "Destination";


    const results =
        document.getElementById("routeResults");


    results.classList.remove("hidden");


    results.innerHTML = `

        <div class="result-head">

            <b>${from}</b>

            <span>→</span>

            <b>${to}</b>

        </div>


        <div class="journey">

            <div>

                <strong>
                    🚌 Route 204
                </strong>

                <span>
                    Fastest · 4 stops · Moderate
                </span>

            </div>

            <b>
                32 min
            </b>

            <button class="secondary">
                View route
            </button>

        </div>


        <div class="journey">

            <div>

                <strong>
                    🚌 Route 116
                </strong>

                <span>
                    Cheapest · 6 stops · Low
                </span>

            </div>

            <b>
                41 min
            </b>

            <button class="secondary">
                View route
            </button>

        </div>

    `;
}
