/* =========================================
   PROJECT ABHAYA
   FINAL SCRIPT.JS
========================================= */



// ===============================
// OPEN HEALTH ASSESSMENT
// ===============================


function openAssessment(){

    document.getElementById("popup").style.display="flex";

    document.body.style.overflow="hidden";

}






// ===============================
// CLOSE POPUP
// ===============================


function closeAssessment(){

    document.getElementById("popup").style.display="none";

    document.body.style.overflow="auto";

}








// ===============================
// GENERATE AI HEALTH REPORT
// ===============================


async function generateReport(){



    let age =
    document.getElementById("age").value;



    let cycle =
    document.getElementById("cycle").value;



    let acne =
    document.getElementById("acne").checked;



    let hair =
    document.getElementById("hair").checked;



    let pain =
    document.getElementById("pain").checked;



    let weight =
    document.getElementById("weight").checked;





    if(age===""){

        alert("Please enter age");

        return;

    }



    let card =
    document.querySelector(".assessment-card");


    card.innerHTML=`
    <div style="text-align:center; padding:40px 0;">
       <h3>🌸 Abhaya AI Analysis...</h3>
    </div>
    `;

    try {
        const response = await fetch("http://127.0.0.1:8000/api/predict/pcos-risk", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                age: parseInt(age),
                cycle_length_days: cycle === "regular" ? 28 : 35,
                weight_gain_sudden: weight,
                hair_growth_excessive: hair,
                skin_darkening: acne,
                mood_swings_severity: pain ? 4 : 2
            })
        });

        const result = await response.json();
        const score = Math.round((1 - result.pcos_risk_probability) * 100);

        card.innerHTML=`
        <h2>🌸 Abhaya AI Insights</h2>
        <div class="health-score">${score}%</div>
        <h3 style="text-align:center">Overall Wellness Score</h3>
        <br>
        <p>🧬 Classification: <b>${result.risk_classification}</b></p>
        <br>
        <p>🩺 ${result.message}</p>
        <button onclick="closeAssessment()">View Dashboard</button>
        `;

        document.getElementById("score").innerHTML = `${score}%`;
        const fillDegrees = Math.round(result.pcos_risk_probability * 360);
        let activeColor = "#22c55e";
        if (result.risk_classification === "Moderate") activeColor = "#f59e0b";
        if (result.risk_classification === "High") activeColor = "#ef4444";
        
        const meter = document.querySelector(".risk-meter");
        const label = document.querySelector(".low-risk");
        if(meter) meter.style.background = `conic-gradient(${activeColor} 0deg, ${activeColor} ${fillDegrees}deg, #eee ${fillDegrees}deg)`;
        if(label) {
            label.innerHTML = `${result.risk_classification} Risk`;
            label.style.color = activeColor;
        }
    } catch (error) {
        alert("Failed to connect to backend service.");
    }
}








// ===============================
// LIVE AI CHATBOT 
// ===============================


async function chat(){



    let input =
    document.getElementById("question");


    let reply =
    document.getElementById("reply");



    let question =
    input.value.trim();




    if(question===""){

        return;

    }




    reply.innerHTML =
    "🌸 Abhaya AI is thinking...";





    try {
        const response = await fetch("http://127.0.0.1:8000/api/chat/abhaya-bot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: question })
        });
        const data = await response.json();
        reply.innerHTML = data.response;
    } catch (error) {
        reply.innerHTML = " Connection error with server.";
    }




    input.value="";



}