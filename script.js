// ==========================================
// 1. ORIGINAL CORE INTERACTION FUNCTIONS
// ==========================================

function openAssessment() {
    const popup = document.getElementById("popup");
    if (popup) popup.style.display = "flex";
}

// Close popup if user clicks outside the card
window.onclick = function(event) {
    const popup = document.getElementById("popup");
    if (event.target === popup) {
        popup.style.display = "none";
    }
}

async function generateReport() {
    const age = document.getElementById("age").value;
    const cycle = document.getElementById("cycle").value;
    const hasAcne = document.getElementById("acne").checked;
    const hasHairLoss = document.getElementById("hair").checked;
    const hasDarkSkin = document.getElementById("weight").checked; // mapping weight changes/skin parameters 
    
    if (!age) {
        alert("Please enter your age first.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/api/predict/pcos-risk", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                age: parseInt(age),
                cycle_length_days: cycle === "irregular" ? 35 : 28,
                weight_gain_sudden: hasDarkSkin,
                hair_growth_excessive: hasHairLoss,
                skin_darkening: hasDarkSkin,
                mood_swings_severity: 3
            })
        });
        const data = await response.json();
        alert(`AI Analysis Report:\nRisk Classification: ${data.risk_classification}\nProbability: ${(data.pcos_risk_probability * 100).toFixed(0)}%\n\n${data.message}`);
        document.getElementById("popup").style.display = "none";
    } catch (error) {
        alert("Could not connect to the healthcare engine.");
    }
}

async function chat() {
    const questionInput = document.getElementById("question");
    const replyDiv = document.getElementById("reply");
    if (!questionInput || !replyDiv) return;

    const query = questionInput.value.trim();
    if (!query) return;

    replyDiv.innerText = "Abhaya AI is thinking... 🌸";
    questionInput.value = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/api/chat/abhaya-bot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: query })
        });
        const data = await response.json();
        replyDiv.innerText = data.response;
    } catch (error) {
        replyDiv.innerText = "Error: Could not reach Abhaya AI core engine system.";
    }
}

// ==========================================
// 2. RE-INTEGRATED COMMUNITY SECTION FUNCTION
// ==========================================
async function openCommunitySection(category) {
    const container = document.getElementById("community-content-display");
    if (!container) return;
    
    // Clear other dynamic sections to avoid overlay clutter
    clearOtherSections("community");
    container.innerHTML = "<p>Loading live community discussions...</p>";

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/community/${category}`);
        const data = await response.json();
        
        let html = `<div style="background: #fff5f7; padding: 20px; border-radius: 20px; text-align: left; margin-bottom: 20px;">`;
        html += `<h3 style="color: #d53f8c; margin-bottom: 15px;">💬 ${category.toUpperCase()} Shared Spaces</h3>`;
        
        // Inline submission field for community posts
        html += `
        <div style="background: white; padding: 15px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.02);">
            <input id="new-post-title" type="text" placeholder="Post Topic Title..." style="width:100%; padding:8px; margin-bottom:8px; border-radius:6px; border:1px solid #ddd;">
            <textarea id="new-post-content" placeholder="Share your experience securely..." rows="2" style="width:100%; padding:8px; margin-bottom:8px; border-radius:6px; border:1px solid #ddd; resize:none;"></textarea>
            <button onclick="submitCommunityPost('${category}')" style="background:#d53f8c; color:white; border:none; padding:6px 16px; border-radius:15px; cursor:pointer;">Post Anonymously</button>
        </div>`;

        if (!data.feed || data.feed.length === 0) {
            html += "<p style='color: #718096;'>Be the first to share your journey here!</p>";
        } else {
            data.feed.forEach(post => {
                html += `
                <div style="background: white; padding: 12px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #d53f8c;">
                    <h4 style="margin:0 0 5px 0; color:#4a5568;">${post.title}</h4>
                    <p style="margin:0; font-size:14px; color:#4a5568;">${post.content}</p>
                    <small style="color:#a0aec0; display:block; margin-top:5px;">Posted by: ${post.author}</small>
                </div>`;
            });
        }
        html += `</div>`;
        container.innerHTML = html;
    } catch (e) {
        container.innerHTML = "<p style='color:red;'>Failed to load community streams.</p>";
    }
}

async function submitCommunityPost(category) {
    const title = document.getElementById("new-post-title").value.trim();
    const content = document.getElementById("new-post-content").value.trim();
    if (!title || !content) return alert("Fields cannot be blank.");

    try {
        await fetch(`http://127.0.0.1:8000/api/community/${category}/post`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, content })
        });
        openCommunitySection(category);
    } catch (e) {
        alert("Post delivery failed.");
    }
}


// ==========================================
// 3. PERIOD AWARENESS DISPLAY WITH SWITCHER
// ==========================================
async function loadPeriodAwareness(category) {
    const container = document.getElementById("awareness-content-display");
    if(!container) return;
    
    clearOtherSections("awareness");
    container.innerHTML = "<p style='padding: 10px;'>🔄 Accessing scientific health tracks...</p>";

    let navigationTabs = `
    <div style="display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap;">
        <button onclick="loadPeriodAwareness('hygiene')" style="background: ${category === 'hygiene' ? '#ff5c9a' : '#fff0f5'}; color: ${category === 'hygiene' ? 'white' : '#5b3c70'}; border: 1px solid #ff5c9a; padding: 8px 16px; border-radius: 20px; font-weight: 600; cursor: pointer;">🧼 Hygiene Management</button>
        <button onclick="loadPeriodAwareness('cramps')" style="background: ${category === 'cramps' ? '#ff5c9a' : '#fff0f5'}; color: ${category === 'cramps' ? 'white' : '#5b3c70'}; border: 1px solid #ff5c9a; padding: 8px 16px; border-radius: 20px; font-weight: 600; cursor: pointer;">🔥 Cramps & Pain Relief</button>
        <button onclick="loadPeriodAwareness('nutrition')" style="background: ${category === 'nutrition' ? '#ff5c9a' : '#fff0f5'}; color: ${category === 'nutrition' ? 'white' : '#5b3c70'}; border: 1px solid #ff5c9a; padding: 8px 16px; border-radius: 20px; font-weight: 600; cursor: pointer;">🥦 Nutrition & Cycle Care</button>
    </div>`;

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/awareness/${category}`);
        const articles = await response.json();
        
        let articlesHTML = navigationTabs + `<div style="display: flex; flex-direction: column; gap: 15px; text-align: left; background: #fff0f5; padding: 25px; border-radius: 25px;">`;
        articlesHTML += `<h3 style="color: #c93b77; margin-bottom: 15px; text-transform: capitalize;">🌸 Scientific Insights: ${category}</h3>`;
        
        if (!articles || articles.length === 0) {
            articlesHTML += `<p style="color: #a08da3;">No resource guidelines loaded for this category yet.</p>`;
        } else {
            articles.forEach(art => {
                articlesHTML += `
                    <div style="background: white; padding: 20px; border-radius: 15px; border-left: 5px solid #ff5c9a; box-shadow: 0 4px 15px rgba(0,0,0,0.01);">
                        <h4 style="color: #5b3c70; margin-bottom: 8px; font-size: 16px;">${art.title}</h4>
                        <p style="font-size: 14px; color: #555; line-height: 1.6;">${art.content}</p>
                        <small style="color: #a08da3; display: block; margin-top: 10px; font-style: italic;">Resource Track: ${art.last_updated || 'Verified Care'}</small>
                    </div>`;
            });
        }
        articlesHTML += `</div>`;
        container.innerHTML = articlesHTML;
    } catch (error) {
        container.innerHTML = navigationTabs + `<p style="color: #ef4444; padding: 20px;">⚠️ Problem establishing pipeline connection with backend.</p>`;
    }
}


// ==========================================
// 4. INTERACTIVE WELLNESS STORIES (SUBMISSION & FEED)
// ==========================================
async function loadWellnessStories() {
    const container = document.getElementById("stories-content-display");
    if(!container) return;
    
    clearOtherSections("stories");
    container.innerHTML = "<p style='padding: 10px;'>📖 Synchronizing shared journey timelines...</p>";

    try {
        const response = await fetch("http://127.0.0.1:8000/api/stories");
        const stories = await response.json();
        
        let storiesHTML = `<div style="display: flex; flex-direction: column; gap: 20px; text-align: left; background: #eef7ff; padding: 25px; border-radius: 25px;">`;
        
        storiesHTML += `
        <div style="background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); padding: 20px; border-radius: 20px; border: 2px dashed #bcdcff; margin-bottom: 10px;">
            <h4 style="color: #2b6cb0; margin-bottom: 12px; font-size: 16px;">✨ Share Your Personal Wellness or Recovery Story</h4>
            <div style="display: flex; gap: 10px; margin-bottom: 10px; flex-wrap: wrap;">
                <input id="story-author" type="text" placeholder="Your Name (Leave blank for Anonymous)" style="flex: 1; min-width: 200px; padding: 10px 15px; border-radius: 10px; border: 1px solid #cbd5e0; font-family: inherit; font-size: 14px;">
                <input id="story-title" type="text" placeholder="Journey Title (e.g., My PCOS Victory)" style="flex: 2; min-width: 250px; padding: 10px 15px; border-radius: 10px; border: 1px solid #cbd5e0; font-family: inherit; font-size: 14px;">
            </div>
            <textarea id="story-body" placeholder="Write details about your wellness path..." rows="3" style="width: 100%; padding: 12px; border-radius: 10px; border: 1px solid #cbd5e0; margin-bottom: 12px; font-family: inherit; font-size: 14px; resize: vertical;"></textarea>
            <button onclick="submitUserStory()" style="background: #4dadff; color: white; border: none; padding: 10px 24px; border-radius: 20px; font-weight: 600; cursor: pointer;">Publish My Journey 🚀</button>
        </div>
        
        <h3 style="color: #2b6cb0; margin-bottom: 5px;">✨ Inspiring Global Health Timelines</h3>`;
        
        if (!stories || stories.length === 0) {
            storiesHTML += `<p style="color: #666;">No dynamic wellness testimonies compiled yet.</p>`;
        } else {
            stories.forEach(story => {
                storiesHTML += `
                    <div style="background: white; padding: 20px; border-radius: 15px; border-left: 5px solid #4dadff; box-shadow: 0 4px 15px rgba(0,0,0,0.01);">
                        <h4 style="color: #2b6cb0; margin-bottom: 6px; font-size: 16px;">${story.title}</h4>
                        <p style="font-size: 14px; color: #4a5568; line-height: 1.6;">${story.story_body}</p>
                        <small style="color: #718096; display: block; margin-top: 10px; font-weight: 500;">Journey by: <b>${story.author}</b> • 👍 ${story.likes || 0} Likes</small>
                    </div>`;
            });
        }
        storiesHTML += `</div>`;
        container.innerHTML = storiesHTML;
    } catch (error) {
        container.innerHTML = `<p style="color: #ef4444; padding: 20px;">⚠️ Unable to sync the global wellness feed layout.</p>`;
    }
}

async function submitUserStory() {
    const authorInput = document.getElementById("story-author");
    const titleInput = document.getElementById("story-title");
    const bodyInput = document.getElementById("story-body");

    const author = authorInput.value.trim() || "Anonymous User";
    const title = titleInput.value.trim();
    const story_body = bodyInput.value.trim();

    if (!title || !story_body) {
        alert("Please include a title and your journey's description before publishing.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/api/stories/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, author, story_body })
        });

        if (response.ok) {
            titleInput.value = "";
            bodyInput.value = "";
            authorInput.value = "";
            loadWellnessStories();
        } else {
            alert("Server rejected the submission.");
        }
    } catch (error) {
        alert("Network routing error. Unable to save your entry.");
    }
}

// ==========================================
// 5. HELPER CLEANUP UTILITY
// ==========================================
function clearOtherSections(activeSection) {
    if (activeSection !== "community") document.getElementById("community-content-display").innerHTML = "";
    if (activeSection !== "awareness") document.getElementById("awareness-content-display").innerHTML = "";
    if (activeSection !== "stories") document.getElementById("stories-content-display").innerHTML = "";
}