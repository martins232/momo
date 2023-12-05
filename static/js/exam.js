const url_data = location.origin+examDataUrl
const url_submit = location.origin+examSubmit
const url_availableExams = location.origin+availableExams
var ajax_data
var time
var allow_correction = false
var user

let selectedAnswers = {}
let misconduct = false
let examstatus 
let warning



var percentremain
var distance
var fixed
var timer



const getData = () => $.ajax({
	type: "GET",
	url: url_data,
	success: function (response) {
		user = response.user
		ajax_data = response.data;
		time = response.time;
		allow_correction = response.allow_correction

		examstatus = "active"

		// allow_retake = response.allow_retake
		
		

		
		
		
		percentremain=0;
		distance = time * 1000;
		fixed=new Date().getTime(); //gets the current time in milliseconds
		fixed +=distance;

		//timer
		timer = setInterval(startTimer, 1000);
		displayExam(0)
	}
})
getData()


function startTimer() {

	//Test time in milliseconds
	distance=fixed-(new Date().getTime());
	percentremain=(distance * 100/(time * 1000));
	// Time calculations for days, hours, minutes and seconds
	let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
	let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
	let seconds = Math.floor((distance % (1000 * 60)) / 1000);
	

	
	if (seconds< 1 && minutes> 0)	{
		seconds =59 //to prevent the seconds count down to zero
		minutes = minutes - 1
	}
	
	// If the count down is finished, write some text 
	if (hours == 0 && minutes ==0 && seconds < 1) {
		setTimeout(()=>{
			document.getElementById("timer").innerHTML = `<h3 class="text-center">Time up</h3>`;
			clearInterval(timer)
			no_AnsweredQuestions = Object.keys(selectedAnswers).length
			no_totalQuestion = Object.keys(ajax_data).length
			selectedAnswers["elapsedTime"] = time
			examstatus = "ended"
			submit()
			$('#ended').modal('show')
			
		}, 500)
	
	}
	// Display the result in the element with id="demo"
	document.getElementById("timer").innerHTML = 
	`<h3 class="text-center">Time remaining:</h3>

		<div class="progress mt-2 fs-4" style="height: 30px; border: 2px solid #d3d9df; background-color: white;">
			<div class="progress-bar progress-bar-animated progress-bar-striped py-2" id="bar" style="overflow: visible; width:${percentremain}%;">
				<span class="fw-bold" style="color: #bfbfbf">${hours>0 ? hours + " : ": ""} ${minutes<10 ? "0"+minutes: minutes} : ${seconds<10 ? "0"+seconds : seconds}</span>
			</div>
		</div> `;

	if (minutes<1){
		let ChangeColor = document.getElementById("bar")
		ChangeColor.classList.add("bg-danger")
	}
	
}


const getOptions = () =>{
	document.getElementsByName("ans")
	let options = ""
	for (let i= 0; i < Object.values(question_data)[0].length; i++){
		let option = Object.values(question_data)[0][i]
		let selected = false
		if (selectedAnswers[`${Object.keys(question_data)[0]}`] == option){
			selected = true
		}
		options += `
		<div class="form-check">
			<input type="radio" class="form-check-input" name="ans" id="${option}" value="${option}" onclick="addAnswer()" ${selected ? `checked=true` : ""}>
			<label class="form-check-label" for="${option}">${option}</label>
	  	</div>
		`
	}
	return options

}

const jumperBtns = () =>{
	btns = ""
	for (let i = 0; i < ajax_data.length; i++) {
		let answeredBtns = false
		let min = Object.keys(ajax_data[i])
		if (selectedAnswers[`${min[0]}`]) {
			answeredBtns = true
		}
		btns += `<li class="page-item"><button class="page-link ${answeredBtns ? `answered`:""}  ${i==index ? `active`:""}"  onclick="displayExam(${i})">${i + 1}</button></li>`
	}
	return btns
}

const addAnswer = ()=>{
    let currentOptions = document.getElementsByName("ans")
    currentOptions.forEach(currentOption =>{
        if (currentOption.checked == true){
            selectedAnswers[`${question}`] = currentOption.value
        }
    })
	
}

const resetAnswer = ()=>{
    let currentOptions = document.getElementsByName("ans")
    currentOptions.forEach(currentOption =>{
        if (currentOption.checked == true){
			currentOption.checked = false
            delete(selectedAnswers[`${question}`] )
        }
    })
	
}

let promptSubmit = () => {
	let modalBody = document.getElementById("modal-body")
	
	let message = ""
	no_AnsweredQuestions = Object.keys(selectedAnswers).length
	no_totalQuestion = Object.keys(ajax_data).length
	if (no_AnsweredQuestions < no_totalQuestion){
		message += `<p>You have ${no_totalQuestion - no_AnsweredQuestions}  unanswered question</p>`
	}
	message += "Once you click the Yes button, this process cannot be reversed"
	modalBody.innerHTML = message
}


let submit = ()=>{
	let csrf = document.getElementsByName("csrfmiddlewaretoken")
	for (let i = 0; i < ajax_data.length; i++) {
		let allQuestions = ajax_data[i]
		if (selectedAnswers[`${Object.keys(allQuestions)[0]}`] == undefined) {
			selectedAnswers[`${Object.keys(allQuestions)[0]}`] = null
		}
	}

	selectedAnswers["csrfmiddlewaretoken"] = csrf[0].value 
	selectedAnswers["misconduct"] = misconduct
	// selectedAnswers["attempts"] = attempts
	$.ajax({
		method: "POST",
		url: url_submit,
		data: selectedAnswers,
		success: function (response) {
			examstatus = "ended"
			if (response){
				no_of_correct_answer = response.no_of_correct_answer;
				score = response.score
				teacherRemark = response.pass
				document.getElementById("quiz-container").innerHTML=""
				$('#ended').modal('show')
				document.getElementById("modalMsg").innerHTML="Your session has been submitted"
				document.getElementById("modalemoji").innerHTML=`<i class="fas fa-check-circle fa-3x"></i>`
			}
			
		},
		error: function(error){
			console.log("Something went wrong")
		}
		
	});
}


const displayExam = (i)=>{
	let questionContainer = document.getElementById("quiz-container")
	index = i
	if (ajax_data){
		question_data = ajax_data[index] //an object for both question and answer
		question = Object.keys(question_data)[0] //an object question
		let options = getOptions() // an object of options array
		let btns =jumperBtns()
		questionContainer.innerHTML = `
		<div class="col-12" >
			<div id ="warning"></div>
			<p class="fw-bold" style="font-family: Georgia, 'Times New Roman', Times, serif;">Question ${i +1} of ${ajax_data.length}</p>
			<hr>
			<span class="fw-bold fs-4" style="font-family: Georgia, 'Times New Roman', Times, serif;">${question}</span>
			
			<div class="mt-4"> 
				${options}
			</div>
		</div>

		<div class="col-12 mb-2">
			<div class="d-flex justify-content-between flex-wrap" id="all_btns"> 
				<div class="align-self-center mx-auto">
					<button type="reset" class="btn btn-dark px-4 py-2 fw-bold" onclick="resetAnswer()">Reset</button>
				</div>
				<div class="align-self-center mx-auto">
					<button class="btn btn-primary px-4 py-2 fw-bold me-2" onclick="displayExam(${index - 1})" ${index < 1 ? "disabled" : ""}> Previous</button> 
					<button class="btn btn-primary px-4 py-2 fw-bold" onclick="displayExam(${index + 1})" ${index == ajax_data.length -1 ? "disabled" : ""}> Next</button> 
				</div>
				<div class="align-self-center mx-auto">
				<button type="button" class="btn btn-success px-4 py-2 fw-bold" data-bs-toggle="modal" data-bs-target="#myModal" onclick="promptSubmit()">Submit</button>
					
				</div>
				
			</div>
		</div>

		<div class="col-12" >
			<nav aria-label="Page navigation example" >
				<ul class="pagination justify-content-center flex-wrap">
					${btns}
				</ul>
			</nav>
		</div>
			


			`
	}else{
		// console.log(window.location.host+"/student/available-exams")
		alert("No question")
	}
}



let submitHandler = ()=> {
	let elapsedTime = Math.ceil(time - (distance/1000)) //no. of seconds used to answer the question
	selectedAnswers["elapsedTime"] = elapsedTime
	clearInterval(timer)
	document.getElementById("timer").innerHTML = `<h3 class="text-center">Exam ended</h3>`;
	document.getElementById("confirmSubmit").addEventListener("click",
	submit(),
	$('#myModal').modal('hide')
	)
	
}


document.forms[0].addEventListener("click", e =>{
	e.preventDefault();
	submitHandler()
})


const result = ()=>{
	let elapsedTime = selectedAnswers.elapsedTime
	delete selectedAnswers.csrfmiddlewaretoken;
	delete selectedAnswers.elapsedTime
	// let nullCount = values.filter (value => value === null).length; 
	document.getElementById("quiz-container").innerHTML = `
			<div class="col-10 mx-auto" style="border: 2px solid black">
			<div class="table-responsive mx-auto">
				<table class="table table-hover table-bordered caption-top">
					<caption><h1><span class="fw-bold text-decoration-underline">${user}</span> exam result:</h1></caption>
					<tbody>
						<tr>
							<th scope="row">Total number of answered Questions</th>
							<td class="text-center">${no_AnsweredQuestions} / ${no_totalQuestion}</td>
						</tr>
						<tr>
							<th scope="row">Total number of unanswered Questions</th>
							<td class="text-center">${no_totalQuestion - no_AnsweredQuestions} / ${no_totalQuestion}</td>
						</tr>
						<tr>
							<th scope="row">Time spent </th>
							<td class="text-center">${elapsedTime < 60 ? Math.ceil(elapsedTime) + " sec(s)" : Math.ceil(elapsedTime / 60) + " min(s)"}</td>
						</tr>
						<tr>
							<th scope="row">No of correct Answers</th>
							<td class="text-center">${no_of_correct_answer}</td>
						</tr>
						<tr>
							<th scope="row">No of wrong answers</th>
							<td class="text-center">${no_totalQuestion - no_of_correct_answer}</td>
						</tr>
						<tr>
							<th scope="row">Score</th>
							<td class="text-center"><b>${score}</b></td>
						</tr>
						<tr>
							<th scope="row">Teacher's remark</th>
							<td class="text-center">${teacherRemark ? `<span class="text-success">Pass</span>` : `<span class="text-danger">Fail</span>`}</td>
						</tr>

					</tbody>
				</table>
			</div>
			<div class="text-center">
				${allow_correction ? `<button class="btn btn-primary mb-3 " onclick="correction()">See Correction</button>`: ""}
			</div>
		</div>
	`
}

let correctionOption = () => {
	let options = ""				
	for (let j=0; j < Object.values(q_and_A)[0].length; j++){
		let choice																		
		let choiceIcon 
		if (Object.values(q_and_A)[0][j] == Object.values(q_and_A)[1]){
			choice= "correct"
			if (Object.values(q_and_A)[0][j] == selectedAnswers[`${correctionQuestion}`]){
				choiceIcon = `<i class="fas fa-check mt-1"></i>`
			}else{
				choiceIcon = ``
			}

		}
		if (Object.values(q_and_A)[0][j] != Object.values(q_and_A)[1] && selectedAnswers[`${correctionQuestion}`] == Object.values(q_and_A)[0][j]){
			choice="wrong"
			choiceIcon = `<i class="fas fa-xmark mt-1"></i>`
		}
		options += `
					<div class="d-flex ${choice ? choice : "no_choice"} justify-content-between">
					<span> ${Object.values(q_and_A)[0][j]} </span> ${choiceIcon ? choiceIcon : ""}
					</div>				
				`
	}
	return options
}

let correction = () =>{
	document.getElementById("quiz-container").innerHTML =""
	let questionContainer = document.getElementById("quiz-container")
	document.getElementById("timer").innerHTML = "<h2>Correction</h2>"
	for (let corr_index = 0; corr_index < ajax_data.length; corr_index++) {
		q_and_A = ajax_data[corr_index]   // question and answer
		correctionQuestion = Object.keys(q_and_A)[0]
		questionContainer.innerHTML += 
		`
		<div class="col-12" >						
			<span class="fw-bold fs-4" style="font-family: Georgia, 'Times New Roman', Times, serif;">${corr_index +1}. ${correctionQuestion}</span>
			<div class="mt-4"> 
			
				${correctionOption()}
			
			</div>
			<hr>
		</div>
	`
		
	}
	
}



warning = 3
let warningFunc = () =>{
	try {
		document.getElementById("warning").innerHTML = `
	  <div class="alert alert-danger">
	  <strong>Warning</strong> You are not to leave this site, while in session. <br> You are on your ${warning} warning. The final warning shall 
	  result in an abrupt termination of this session.
	</div> 
	  `
	} catch (error) {
		
	}
	  if (warning==0){
		  	no_AnsweredQuestions = Object.keys(selectedAnswers).length
		  	
		  	no_totalQuestion = Object.keys(ajax_data).length
			  let elapsedTime = Math.ceil(time - (distance/1000)) //no. of seconds used to answer the question
			  selectedAnswers["elapsedTime"] = elapsedTime
			  clearInterval(timer)
			  document.getElementById("timer").innerHTML = `<h3 class="text-center text-danger">Exam Infringement</h3>`;
			misconduct = true //what will be sent to the database
			submit()
			
	  }
	  warning--  //for every infrigement decrease the warning
}

document.addEventListener("visibilitychange", (event) => {
	if (document.visibilityState === "hidden") {
		if (examstatus == "active"){
			warningFunc()  //only call this function when exam is active
		}
	  
	}
  });

//   $(window).resize(function() {
// 	// console.log("Please don't resize you browser")
// 	console.log("The height of your screen: " + screen.height);
// 	console.log("The width of your screen: " + screen.width);
// 	console.log("Your available screen width: " + screen.availWidth);
// 	console.log("Your available screen height: " + screen.availHeight);
// 	console.log("Available resized width: " + window.innerWidth);
// 	console.log("Available resized height: " + window.innerHeight);
// 	console.log("-----------------------------------------------------------")
//   });