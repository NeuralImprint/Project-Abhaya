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
// ===============================
// COMMUNITY PILLARS DATA FETCHER
// ===============================

async function openCommunitySection(category) {
    let grid = document.querySelector(".community-grid");
    if (!grid) return;

    // Save the original layout structure so we can restore it later
    if (!window.originalCommunityHTML) {
        window.originalCommunityHTML = grid.innerHTML;
    }

    grid.innerHTML = `
    <div style="grid-column: 1 / -1; text-align: center; padding: 40px 0;">
        <h3>🌸 Loading Abhaya Community Feed...</h3>
    </div>`;

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/community/${category}`);
        const data = await response.json();
        
        let feedHTML = `
        <div style="grid-column: 1 / -1; width: 100%;">
            <button onclick="document.querySelector('.community-grid').innerHTML = window.originalCommunityHTML" style="margin-bottom: 20px; background: #f1e7ff; color: #5b3c70; padding: 8px 16px; border: none; border-radius: 20px; cursor: pointer; font-weight: 500;">🔙 Back to Categories</button>
            <div style="display: flex; flex-direction: column; gap: 15px;">
        `;

        data.feed.forEach(post => {
            feedHTML += `
                <div style="background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.02); border: 1px solid #fcf0f7;">
                    <h4 style="color: #5b3c70; margin-bottom: 8px;">${post.title}</h4>
                    <p style="font-size: 14px; color: #555; line-height: 1.6;">${post.content}</p>
                    <small style="color: #a08da3; display: block; margin-top: 10px; font-style: italic;">By: ${post.author}</small>
                </div>
            `;
        });

        feedHTML += `</div></div>`;
        grid.innerHTML = feedHTML;

    } catch (error) {
        grid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 20px; color: #ef4444;">
            ⚠️ Unable to load feed. Ensure your FastAPI application server is running.
            <br><br>
            <button onclick="document.querySelector('.community-grid').innerHTML = window.originalCommunityHTML" style="background: #eee; padding: 5px 15px; border: none; border-radius: 5px; cursor: pointer;">Close</button>
        </div>`;
    }
}
// ===============================
// DYNAMIC MONGODB COMMUNITY REGISTRY
// ===============================

async function openCommunitySection(category) {
    let grid = document.querySelector(".community-grid");
    if (!grid) return;

    if (!window.originalCommunityHTML) {
        window.originalCommunityHTML = grid.innerHTML;
    }

    grid.innerHTML = `
    <div style="grid-column: 1 / -1; text-align: center; padding: 40px 0;">
        <h3>🌸 Fetching Community Insights from MongoDB...</h3>
    </div>`;

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/community/${category}`);
        const data = await response.json();
        
        let feedHTML = `
        <div style="grid-column: 1 / -1; width: 100%; text-align: left;">
            <button onclick="document.querySelector('.community-grid').innerHTML = window.originalCommunityHTML" style="margin-bottom: 25px; background: #f1e7ff; color: #5b3c70; padding: 10px 20px; border: none; border-radius: 20px; cursor: pointer; font-weight: 600;">🔙 Back to Categories</button>
            
            <div style="background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); padding: 25px; border-radius: 25px; margin-bottom: 30px; border: 2px dashed #ffd7ea;">
                <h4 style="color: #5b3c70; margin-bottom: 15px;">🌸 Share Your Experience Anonymously</h4>
                <input id="post-title" type="text" placeholder="Topic Title (e.g., My Lifestyle Routine)" style="width: 100%; padding: 12px; border-radius: 12px; border: 1px solid #ddd; margin-bottom: 12px; font-family: inherit;">
                <textarea id="post-content" placeholder="Type your experience here... Your contribution will be safely shared across the network." rows="3" style="width: 100%; padding: 12px; border-radius: 12px; border: 1px solid #ddd; margin-bottom: 15px; font-family: inherit; resize: vertical;"></textarea>
                <button onclick="submitCommunityPost('${category}')" style="background: #ff5c9a; color: white; border: none; padding: 10px 24px; border-radius: 20px; font-weight: 600; cursor: pointer;">Post to Portal 🚀</button>
            </div>

            <div id="live-posts-container" style="display: flex; flex-direction: column; gap: 20px;">
        `;

        if (data.feed.length === 0) {
            feedHTML += `
                <div style="text-align: center; color: #a08da3; padding: 20px;">
                    🌱 No experiences shared yet. Be the first to start the conversation!
                </div>`;
        } else {
            data.feed.forEach(post => {
                feedHTML += `
                    <div style="background: white; padding: 25px; border-radius: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.02); border: 1px solid #fff0f7;">
                        <h4 style="color: #ff5c9a; font-size: 17px; margin-bottom: 8px;">${post.title}</h4>
                        <p style="font-size: 14px; color: #5b4963; line-height: 1.6;">${post.content}</p>
                        <small style="color: #a08da3; display: block; margin-top: 12px; font-style: italic;">Shared by: ${post.author}</small>
                    </div>`;
            });
        }

        feedHTML += `</div></div>`;
        grid.innerHTML = feedHTML;

    } catch (error) {
        grid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 30px; color: #ef4444;">
            ⚠️ Problem establishing database handshake. Ensure your Uvicorn server is up.
            <br><br>
            <button onclick="document.querySelector('.community-grid').innerHTML = window.originalCommunityHTML" style="background: #eee; padding: 6px 18px; border: none; border-radius: 8px; cursor: pointer;">Close</button>
        </div>`;
    }
}

async function submitCommunityPost(category) {
    const titleInput = document.getElementById("post-title");
    const contentInput = document.getElementById("post-content");

    const title = titleInput.value.trim();
    const content = contentInput.value.trim();

    if (!title || !content) {
        alert("Please provide both a title and details of your experience.");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/community/${category}/post`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title: title, content: content })
        });

        if (response.ok) {
            // Clean out text inputs and instantly refresh view to show the new MongoDB entry
            titleInput.value = "";
            contentInput.value = "";
            openCommunitySection(category);
        } else {
            alert("The server encountered an error processing your document collection post.");
        }
    } catch (error) {
        alert("Network routing error. Unable to write object entry to remote MongoDB storage.");
    }
}