const url_data = location.origin + examDataUrl
const url_submit = location.origin + examSubmit
const url_availableExams = location.origin + availableExams
var ajax_data
var time
var allow_correction = false
var user

let selectedAnswers = {}
let misconduct = false
let examstatus



var percentremain
var distance
var fixed
var timer

let warning=4
const innerWidth = window.innerWidth
const innerHeight = window.innerHeight





//to show instruction modal in new screen
$(window).on("load", function () {
	
	if(check_storage_for_data){
		alert("Continue from where you left off" )
		checkStorage()
	}else{
		//show instruction
		$('#ended').modal('show');
	}
	
});


function checkStorage() {
	ajax_data  = localStorage.getItem("questionData")
	selectedAnswers = localStorage.getItem("selectedAnswers")
	let meta_ = localStorage.getItem("meta_")
	
	if (meta_){
		ajax_data  = JSON.parse(localStorage.getItem("questionData"))
		selectedAnswers  = JSON.parse(localStorage.getItem("selectedAnswers"))
		
		let decrypted = decrypt(meta_,"28465").toString(CryptoJS.enc.Utf8);
		meta_ = JSON.parse(decrypted)

		
		examstatus = "active"
		percentremain = 0;
		time = meta_.time
		fixed = meta_.fixed
		user = meta_.user
		allow_correction = meta_.allow_correction
		warning = meta_.warning  + 1
		
		
		$("#warning").html(`
			<div class="alert alert-danger alert-dismissible">
				<button type="button" class="btn-close" data-bs-dismiss="alert"></button>
				<strong><i class="fas fa-exclamation-triangle"></i></strong> You were on your <strong>${warning > 1 ? warning : ""}${warning > 1 ? getOrdinal(warning) : "last"}</strong> warning. 
				<a href="#" onclick="activeExamInstruction()">Read instructions</a>
			</div> 
		`)
		

		
		displayExam(0)
		timer = setInterval(startTimer, 1000);
	
	}else{
		function closeWindow() {
			if (confirm("Previous session not found! Seek redress from the examiner.")) {
			  window.close();
			}
		}
		closeWindow()
	}
	
	// if (user != "") {
	//   alert("Welcome again " + user);
	// } else {
	//   user = prompt("Please enter your name:", "");
	//   if (user != "" && user != null) {
	// 	setCookie("username", user, 365);
	//   }
	// }
	
}
 function clearStorage(){
	localStorage.removeItem("questionData")
	localStorage.removeItem("selectedAnswers")
	localStorage.removeItem("meta_")
 }

function checkSizeofScreen(){
	//if (innerWidth != window.innerWidth |  window.innerHeight < innerHeight) {
	if (innerWidth != window.innerWidth) {
		warningFunc("You are not to resize this window, you have 10 secs to close any opened screen")
	}
	
}

//when exam is active instruction students will see
function activeExamInstruction() {
	
	$("#ended .modal-header button").removeClass("d-none")
	$("#ended .modal-footer button").addClass("d-none")
	$("#ended .warningCounterNotifier").text(`${warning > 1 ? warning : ""}${warning > 1 ? getOrdinal(warning) : "last"}`)
	$("#ended").modal("toggle")
}


//remove this because i'll remove correction
const endSession = () => {
	window.location = url_availableExams
}

const getData = () => {

	$("ended").modal("hide")
	$(".spinner-container").toggleClass("d-none")

	$.ajax({
		type: "GET",
		url: url_data,
		success: function (response) {
			user = response.user
			ajax_data = response.data;
			time = response.time;
			allow_correction = response.allow_correction
			examstatus = "active"


			
			JSON.stringify(ajax_data)
			localStorage.setItem("questionData", JSON.stringify(ajax_data))

			localStorage.setItem("selectedAnswers", JSON.stringify(selectedAnswers))

			percentremain = 0;
			distance = time * 1000;

			setTimeout(function () {
				$(".spinner-container").toggleClass("d-none")
				
				displayExam(0)
				fixed = new Date().getTime(); //gets the current time in milliseconds
				fixed += distance;
				timer = setInterval(startTimer, 1000);

				//encrypting to avoid manipulation
				encryptMeta_ = encrypt(JSON.stringify({"time":time, "fixed": fixed, "warning": warning, "allow_correction": allow_correction, "user": user}), "28465") //time included because of percent remain

				localStorage.setItem("meta_", encryptMeta_)
				//check that the student has not minimized screen before he starts exam
				checkSizeofScreen()
			}, 2000)



		},
		error: function (error) {
			alert("Something went wrong")
		}
	})
}


function startTimer() {

	if (distance<0){
		// for those that got there question from storage
		console.log($("#timer"))
		clearInterval(timer)
		no_AnsweredQuestions = Object.keys(selectedAnswers).length
		no_totalQuestion = Object.keys(ajax_data).length
		selectedAnswers["elapsedTime"] = time
		examstatus = "ended"
		submit()
		
	}

	//Test time in milliseconds
	distance = fixed - (new Date().getTime());
	percentremain = (distance * 100 / (time * 1000));
	// Time calculations for days, hours, minutes and seconds
	let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
	let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
	let seconds = Math.floor((distance % (1000 * 60)) / 1000);

	
	// if (seconds< 1 && minutes> 0)	{
	// 	seconds =59 //to prevent the seconds count down to zero
	// 	minutes = minutes - 1
	// }

	// If the count down is finished, write some text 
	if (hours == 0 && minutes == 0 && seconds < 1) {
		setTimeout(() => {
			clearInterval(timer)
			no_AnsweredQuestions = Object.keys(selectedAnswers).length
			no_totalQuestion = Object.keys(ajax_data).length
			selectedAnswers["elapsedTime"] = time
			examstatus = "ended"
			submit()

			// const myModalAlternative = new bootstrap.Modal('#myModal', {keyboard: false})
			// myModalAlternative.toggle()

			const myModal = document.querySelector('#myModal');
			const modal = bootstrap.Modal.getInstance(myModal);
			if (modal) {
				modal.toggle();
			}

			$('#ended').modal('show')

		}, 500)

	}
	// Display the result in the element with id="demo"
	if (distance>0){
		document.getElementById("timer").innerHTML =
		`<p  class="d-none d-md-block">Time remaining:</p>

		<div class="progress fs-4" style="height: 25px; border: 2px solid #d3d9df; background-color: white; border-radius: 20px">
			<div class="progress-bar progress-bar-animated progress-bar-striped py-2" id="bar" style="overflow: visible; width:${percentremain}%;">
				<span class="fw-bold" style="color: #bfbfbf">${hours > 0 ? hours + " : " : ""} ${minutes < 10 ? "0" + minutes : minutes} : ${seconds < 10 ? "0" + seconds : seconds}</span>
			</div>
		</div> `;
	}else{
		document.getElementById("timer").innerHTML = `<h3 class="text-center text-danger">Session ended</h3>`;
	}

	if (minutes < 1) {
		let ChangeColor = document.getElementById("bar")
		ChangeColor.classList.add("bg-danger")
	}

}


const getOptions = () => {
	document.getElementsByName("ans")
	let options = ""
	option_label = ["A", "B", "C", "D", "E"]
	for (let i = 0; i < Object.values(question_data)[0].length; i++) {
		let option = Object.values(question_data)[0][i]

		let selected = false
		if (selectedAnswers[`${Object.keys(question_data)[0]}`] == option) {
			selected = true
		}
		options += `
		<label>
			<input type="radio" name="ans" value="${option}" onclick="addAnswer()" ${selected ? `checked=true` : ""}/>
			<span>${option_label[i]}</span> 
			${option}
		</label>
		`
	}
	return options

}


const jumperBtns = (x) => {
	let jumper_div = $(x)
	btns = ""
	for (let i = 0; i < ajax_data.length; i++) {
		let answeredBtns = false
		let min = Object.keys(ajax_data[i])
		if (selectedAnswers[`${min[0]}`]) {
			answeredBtns = true
		}
		btns += `<div style="min-width: 40px; max-width: 40px; cursor: pointer;"class="col p-2 border text-center ${i == index ? `active` : ""} ${answeredBtns ? `answered` : ""} " onclick="displayExam(${i})" data-bs-dismiss="modal">${i + 1}</div>`
	}
	jumper_div.html(`${btns}`)
}

const SmalljumperBtns =() =>{
	const myModalAlternative = new bootstrap.Modal('#jumperbuttons', {backdrop: false})
	jumperBtns("#jumperbuttons .modal-body .row")
	myModalAlternative.show()
}

const addAnswer = () => {
	let currentOptions = document.getElementsByName("ans")
	currentOptions.forEach(currentOption => {
		if (currentOption.checked == true) {
			selectedAnswers[`${question}`] = currentOption.value
		}
	})
	localStorage.setItem("selectedAnswers", JSON.stringify(selectedAnswers))
}

const resetAnswer = () => {
	let currentOptions = document.getElementsByName("ans")
	currentOptions.forEach(currentOption => {
		if (currentOption.checked == true) {
			currentOption.checked = false
			delete (selectedAnswers[`${question}`])
		}
	})

}

let promptSubmit = () => {
	let modalBody = document.getElementById("modal-body")

	let message = ""
	no_AnsweredQuestions = Object.keys(selectedAnswers).length
	no_totalQuestion = Object.keys(ajax_data).length
	if (no_AnsweredQuestions < no_totalQuestion) {
		message += `<p>You have ${no_totalQuestion - no_AnsweredQuestions}  unanswered question</p>`
	}
	message += "Once you click the Yes button, this process cannot be reversed"
	modalBody.innerHTML = message
}


let submit = () => {
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
			clearStorage()
			examstatus = "ended"
			if (response) {
				no_of_correct_answer = response.no_of_correct_answer;
				score = response.score
				teacherRemark = response.pass
				$("#warning").html("")
				$(".jumperbtn").html("")
				$("#quiz-container").html("")

				$("#ended .modal-content").html(`
					<div class="modal-body text-center">
						<h2 id="modalMsg">Your session has been submitted</h2>
						<div id="modalemoji" class=text-success><i class="fas fa-check-circle fa-3x"></i></div>
					</div>
					<!-- Modal footer -->
					<div class="modal-footer" style="margin: 0 auto;">
						${allow_correction ? `<button type="button" class="btn btn-secondary" onclick="result()" data-bs-dismiss="modal" >See Result</button>` : `<button type="button" class="btn btn-secondary" onclick="window.close()" >End Session</button>`}
					</div>
				`)
				$('#ended').modal('show')
			}

		},
		error: function (error) {
			alert("Something went wrong")
		}

	});
}

//${allow_correction ? `<button type="button" class="btn btn-secondary" onclick="result()" data-bs-dismiss="modal" >See Result</button>`: `<button class="btn btn-primary mb-3 " onclick="window.close()">End Session</button>`}

const displayExam = (i) => {
	let questionContainer = document.getElementById("quiz-container")
	index = i
	if (ajax_data) {
		question_data = ajax_data[index] //an object for both question and answer
		question = Object.keys(question_data)[0] //an object question
		let options = getOptions() // an object of options array
		questionContainer.innerHTML = `
		<div class="" >
			<div class="d-flex justify-content-between">
				<p id="question" class="fw-bold" style="font-family: Georgia, 'Times New Roman', Times, serif;">Question ${i + 1} of ${ajax_data.length}</p>
				<a href="#" class="d-sm-block d-md-none" onclick="SmalljumperBtns()"><i class="fas fa-table"></i></a>
			</div>
			<hr>
			<span id="question" class="fw-bold text-justify fs-5" style="font-family: Georgia, 'Times New Roman', Times, serif;">${question}</span>
			
			<div class="mt-3" style="margin-bottom: 140px"> 
				${options}
			</div>
		</div>

		<div class="">
			<div class="d-flex justify-content-between flex-wrap fixed-bottom" id="all_btns" style="margin-bottom:30px"> 
				<div class="align-self-center mx-auto">
					<button type="reset" class="btn btn-dark px-4 py-2 fw-bold" onclick="resetAnswer()">Reset</button>
				</div>
				<div class="align-self-center mx-auto">
					<a href="#question" class="btn btn-primary px-4 py-2 fw-bold me-2" onclick="displayExam(${index - 1})" ${index < 1 ? "disabled" : ""}> <i class="fas fa-angle-double-left"></i> <span class="d-none d-md-inline-block">Previous</span></a> 
					<a href="#question" class="btn btn-primary px-4 py-2 fw-bold" onclick="displayExam(${index + 1})" ${index == ajax_data.length - 1 ? "disabled" : ""}>
					<span class="d-none d-md-inline-block">Next</span> <i class="fas fa-angle-double-right"></i></a> 
				</div>
				<div class="align-self-center mx-auto">
				<button ${index == ajax_data.length - 1 ? "" : "disabled"} type="button" class="btn btn-success px-4 py-2 fw-bold" data-bs-toggle="modal" data-bs-target="#myModal" onclick="promptSubmit()">Submit</button>
					
				</div>
				
			</div>
		</div>

	 
			


			`
		jumperBtns(".jumperbtn .row")
	} else {
		// console.log(window.location.host+"/student/available-exams")
		alert("No question")
	}
}



let submitHandler = () => {
	let elapsedTime = Math.ceil(time - (distance / 1000)) //no. of seconds used to answer the question
	selectedAnswers["elapsedTime"] = elapsedTime
	clearInterval(timer)
	document.getElementById("timer").innerHTML = `<h3 class="text-center">Exam ended</h3>`;
	document.getElementById("confirmSubmit").addEventListener("click",
		submit(),
		$('#myModal').modal('hide')
	)

}


document.forms[0].addEventListener("click", e => {
	e.preventDefault();
	submitHandler()
})


const result = () => {
	let elapsedTime = selectedAnswers.elapsedTime
	delete selectedAnswers.csrfmiddlewaretoken;
	delete selectedAnswers.elapsedTime
	// let nullCount = values.filter (value => value === null).length; 
	//document.getElementById("quiz-container").innerHTML =
	$("body").append(`
			<div class="col-10 mx-auto" style="border: 2px solid black">
			<div class="table-responsive mx-auto">
				<table class="table table-hover table-bordered caption-top">
					<caption><h1><span class="fw-bold text-decoration-underline">${user}</span> exam result:</h1></caption>
					<tbody>
						<tr>
							<th scope="row">Total number of answered Questions</th>
							<td class="text-center">${no_AnsweredQuestions} of ${no_totalQuestion} </td>
						</tr>
						<tr>
							<th scope="row">Total number of unanswered Questions</th>
							<td class="text-center">${no_totalQuestion - no_AnsweredQuestions} of ${no_totalQuestion}</td>
						</tr>

						<tr>
							<th scope="row">No of correct Answers</th>
							<td class="text-center"><sup class="fw-bold">${no_of_correct_answer}</sup>/<sub>${no_totalQuestion}</sub></td>
						</tr>
						<tr>
							<th scope="row">No of wrong answers</th>
							<td class="text-center"><sup class="fw-bold">${no_totalQuestion - no_of_correct_answer}</sup>/<sub>${no_totalQuestion}</sub></td>
						</tr>
						<tr>
							<th scope="row">Time spent </th>
							<td class="text-center">${elapsedTime < 60 ? Math.ceil(elapsedTime) + " sec(s)" : Math.ceil(elapsedTime / 60) + " min(s)"}</td>
						</tr>
						<tr>
							<th scope="row">Score</th>
							<td class="text-center"><b>${score}%</b></td>
						</tr>
						<tr>
							<th scope="row">Teacher's remark</th>
							<td class="text-center">${teacherRemark ? `<span class="text-success">Pass</span>` : `<span class="text-danger">Fail</span>`}</td>
						</tr>

					</tbody>
				</table>
			</div>
			<div class="text-center">
			
				<button class="btn btn-primary mb-3 " onclick="window.close()">End Session</button>
			</div>
		</div>
	`)
}

let correctionOption = () => {
	let options = ""
	for (let j = 0; j < Object.values(q_and_A)[0].length; j++) {
		let choice
		let choiceIcon
		if (Object.values(q_and_A)[0][j] == Object.values(q_and_A)[1]) {
			choice = "correct"
			if (Object.values(q_and_A)[0][j] == selectedAnswers[`${correctionQuestion}`]) {
				choiceIcon = `<i class="fas fa-check mt-1"></i>`
			} else {
				choiceIcon = ``
			}

		}
		if (Object.values(q_and_A)[0][j] != Object.values(q_and_A)[1] && selectedAnswers[`${correctionQuestion}`] == Object.values(q_and_A)[0][j]) {
			choice = "wrong"
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

let correction = () => {
	document.getElementById("quiz-container").innerHTML = ""
	let questionContainer = document.getElementById("quiz-container")
	document.getElementById("timer").innerHTML = `<button type="button" class="btn btn-secondary mt-2" data-bs-dismiss="modal" onclick="endSession()">End Session</button>`
	for (let corr_index = 0; corr_index < ajax_data.length; corr_index++) {
		q_and_A = ajax_data[corr_index]   // question and answer
		correctionQuestion = Object.keys(q_and_A)[0]
		questionContainer.innerHTML +=
			`
		<div class="col-12" >						
			<span class="fw-bold fs-4" style="font-family: Georgia, 'Times New Roman', Times, serif;">${corr_index + 1}. ${correctionQuestion}</span>
			<div class="mt-4"> 
			
				${correctionOption()}
			
			</div>
			<hr>
		</div>
	`

	}

}




function getOrdinal(n) {
	let ord = 'th';

	if (n % 10 == 1 && n % 100 != 11) {
		ord = 'st';
	}
	else if (n % 10 == 2 && n % 100 != 12) {
		ord = 'nd';
	}
	else if (n % 10 == 3 && n % 100 != 13) {
		ord = 'rd';
	}
	return ord;
}



let warningFunc = (warningMsg) => {
	beep()
		if (warning == 0) {
		no_AnsweredQuestions = Object.keys(selectedAnswers).length

		no_totalQuestion = Object.keys(ajax_data).length
		let elapsedTime = Math.ceil(time - (distance / 1000)) //no. of seconds used to answer the question
		selectedAnswers["elapsedTime"] = elapsedTime
		clearInterval(timer)
		document.getElementById("timer").innerHTML = `<h3 class="text-center text-danger">Exam Infringement</h3>`;
		misconduct = true //what will be sent to the database
		submit()

	}
	warning--  //for every infrigement decrease the warning
	$("#warning").html(`
	  	<div class="alert alert-danger alert-dismissible">
			<button type="button" class="btn-close" data-bs-dismiss="alert"></button>
			<strong><i class="fas fa-exclamation-triangle"></i></strong> This is the <strong>${warning > 1 ? warning : ""}${warning > 1 ? getOrdinal(warning) : "last"}</strong> warning. ${warningMsg} 
			<a href="#" onclick="activeExamInstruction(4)">Read instructions</a>
	 	</div> 
	`)


	let meta_ = localStorage.getItem("meta_")
	let decrypted = decrypt(meta_,"28465").toString(CryptoJS.enc.Utf8);
	meta_ = JSON.parse(decrypted)
	meta_.warning = warning
	encryptMeta_ = encrypt(JSON.stringify(meta_), "28465") //time included because of percent remain
	localStorage.setItem("meta_", encryptMeta_)
	
	
}




function keypressed(event) {
	let currentOptions = document.getElementsByName("ans")
	if (event.keyCode == 65) {
		currentOptions[0].checked = true
	}
	if (event.keyCode == 66) {
		currentOptions[1].checked = true
	}
	if (event.keyCode == 67) {
		currentOptions[2].checked = true
	}
	if (event.keyCode == 68) {
		currentOptions[3].checked = true
	}
	addAnswer()
	// if (event.keyCode==37 | event.keyCode==40){
	if (event.keyCode == 37) {
		if (index > 0) {
			index = index - 1
			displayExam(index)
		}
	}
	// if (event.keyCode==39 | event.keyCode==38){
	if (event.keyCode == 39) {
		if (index < ajax_data.length - 1) {
			index = index + 1
			displayExam(index)
		}
	}


}
document.addEventListener("visibilitychange", (event) => {
	if (document.visibilityState === "hidden") {
		if (examstatus == "active") {
			warningFunc("Continued session inactivity or attempts to leave this page will result in termination of your current session.")
			
		}

	}
});
document.addEventListener("keydown", (event) => {
	if (examstatus == "active") {
		keypressed(event)
	}
})



$(window).on("resize", function () {
	if (examstatus == "active") {
		// if (innerWidth != window.innerWidth | window.innerHeight < innerHeight) {
		if (innerWidth != window.innerWidth) {
			warningFunc("You are not to resize this window, you have 10 secs to close any opened screen")
			setTimeout(startCounter("You are not to resize this window, you have 30 secs to close any opened screen"),5000)
		}else{
			stopCounter()
			counter = 0
			$("#warning").html(`
			<div class="alert alert-danger alert-dismissible">
				<button type="button" class="btn-close" data-bs-dismiss="alert"></button>
				<strong><i class="fas fa-exclamation-triangle"></i></strong> This is the <strong>${warning > 1 ? warning : ""}${warning > 1 ? getOrdinal(warning) : "last"}</strong> warning. You are not to resize this window.
				<a href="#" onclick="activeExamInstruction(4)">Read instructions</a>
			</div> 
	`)
		}
	}

});


function encrypt(data, key){
	return CryptoJS.AES.encrypt(data, key);
  }
function decrypt(data, key){

	return CryptoJS.AES.decrypt(data, key);
}

function beep() {
    let snd = new Audio("data:audio/mpeg;base64,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");  
    snd.play();
}


let counter = 0;
let intervalId = null

// Function to start the counter
function startCounter(msg) {
	if (examstatus == "active"){
		intervalId = setInterval(() => {
			counter++;
			beep()
			$("#warning").html(`<div class="alert alert-danger alert-dismissible">
				<button type="button" class="btn-close" data-bs-dismiss="alert"></button>
				<strong><i class="fas fa-exclamation-triangle"></i></strong> This is the <strong>${warning > 1 ? warning : ""}${warning > 1 ? getOrdinal(warning) : "last"}</strong> warning. ${msg}: <span class="fw-bold">${counter}</span>
		 </div>
			`); // Display the count in the page title
		  }, 1000);
	}else{
		stopCounter()
	}
  }

  // Function to stop the counter
function stopCounter() {
	clearInterval(intervalId);
  }
