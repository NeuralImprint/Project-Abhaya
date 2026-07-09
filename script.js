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


function generateReport(){



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

        alert("Please enter your age");

        return;

    }







    let score = 100;





    if(cycle==="irregular"){

        score -= 20;

    }


    if(acne){

        score -= 8;

    }


    if(hair){

        score -= 8;

    }


    if(pain){

        score -= 15;

    }


    if(weight){

        score -= 10;

    }





    if(score < 35){

        score = 35;

    }







    let risk;



    if(score >= 80){

        risk="Low";

    }

    else if(score >= 55){

        risk="Moderate";

    }

    else{

        risk="High";

    }









    document.querySelector(".assessment-card").innerHTML = `


    <h2>
    🌸 Abhaya AI Report
    </h2>



    <div class="health-score">

    ${score}%

    </div>



    <h3 style="text-align:center">

    Wellness Score

    </h3>



    <br>



    <p>
    🧬 PCOS Risk:
    <b>${risk}</b>
    </p>



    <p>
    🩸 Cycle Health:
    <b>
    ${
        cycle==="regular"
        ?
        "Healthy"
        :
        "Needs Monitoring"
    }
    </b>
    </p>




    <br>


    <h3>

    Personalized Advice

    </h3>



    <p>
    🥗 Maintain hormone-friendly nutrition
    </p>


    <p>
    💧 Stay hydrated
    </p>


    <p>
    🏃 Exercise regularly
    </p>


    <p>
    🧘 Practice stress management
    </p>



    <button onclick="closeAssessment()">

    View Dashboard

    </button>




    <button 
    onclick="resetAssessment()"
    style="
    background:#f1e7ff;
    color:#5b3c70;
    margin-top:10px;
    ">

    🔄 Retake Analysis

    </button>



    `;





    updateDashboardScore(score);



}









// ===============================
// RESET ASSESSMENT
// ===============================


function resetAssessment(){



document.querySelector(".assessment-card").innerHTML = `


<h2>
🌸 Health Assessment
</h2>



<label>
Age
</label>


<input 
id="age"
type="number"
placeholder="Enter your age">





<label>
Cycle Pattern
</label>



<select id="cycle">


<option value="regular">

Regular

</option>


<option value="irregular">

Irregular

</option>


</select>





<label>
Symptoms
</label>




<div class="symptom">

<input id="acne" type="checkbox">

Acne

</div>



<div class="symptom">

<input id="hair" type="checkbox">

Hair Loss

</div>




<div class="symptom">

<input id="pain" type="checkbox">

Severe Pain

</div>




<div class="symptom">

<input id="weight" type="checkbox">

Weight Changes

</div>




<button onclick="generateReport()">

Generate AI Report

</button>


`;



}









// ===============================
// DASHBOARD SCORE ANIMATION
// ===============================



function updateDashboardScore(finalScore){



let scoreElement =
document.getElementById("score");



let current=0;



let animation =
setInterval(()=>{


current++;


scoreElement.innerHTML =
current+"%";



if(current>=finalScore){

clearInterval(animation);

}



},15);



}









// ===============================
// AI CHATBOT
// ===============================



function chat(){



let input =
document.getElementById("question");



let question =
input.value.toLowerCase();



let reply =
document.getElementById("reply");




if(question===""){

return;

}




reply.innerHTML =
"🌸 Abhaya AI is thinking...";





setTimeout(()=>{



let answer;



if(question.includes("pcos")){


answer =
"PCOS is a hormonal condition. Common signs include irregular periods, acne, weight changes and hair loss. Early detection helps manage health better.";

}



else if(question.includes("period")){


answer =
"Tracking your cycle helps understand patterns, predict periods and identify unusual changes.";

}



else if(question.includes("diet")){


answer =
"A balanced diet with proteins, iron-rich foods, vegetables and hydration supports hormonal wellness.";

}



else if(question.includes("pain")){


answer =
"Severe menstrual pain should not be ignored. Consider consulting a healthcare professional.";

}



else{


answer =
"I can help you with menstrual health, PCOS awareness, wellness, nutrition and lifestyle guidance 🌸";

}





reply.innerHTML=answer;



},1000);




input.value="";



}









// ===============================
// INITIAL SCORE ANIMATION
// ===============================


window.onload=function(){



let scoreElement =
document.getElementById("score");



if(scoreElement){



let value=0;



let animation =
setInterval(()=>{


value++;


scoreElement.innerHTML =
value+"%";



if(value>=92){


clearInterval(animation);


}



},20);



}



}