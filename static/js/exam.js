const url_data = examDataUrl
const url_submit = examSubmit
let ajax_data
let see_score
let elapsedTime

let warning =3
let misconduct = false

let time
let fixed
let timer
let distance


let index
let allow_correction = false
let user
let selectedAnswers = {}
let question
let examstatus

let resultData

let isModalOpen = false;


let countdown;
let timeLeft
let blurredFrame = false
let screenWidth = window.outerWidth
let screenheight = window.outerHeight

//get exam data by making a promise
async function getData() {
	$(".spinner-container").toggleClass("d-none")
    try {
        let response = await fetch(url_data);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        let data = await response.json();
        return data;
    } catch (error) {
		$(".spinner-container").toggleClass("d-none")
        throw new Error(`Network error: ${error.message}`);
    }
}

showExamInstructions()
//handle promise

const fetchAndInitializeExam = () => {
	if (check_storage_for_data){
		getStoredData()
	}else{
		getData().then((data)=>{
			$(".spinner-container").toggleClass("d-none")
				ajax_data = data.data;
				time= data.time
				see_score = data.see_score
				fixed = new Date().getTime() + time*1000;
				
				examstatus = "active"
				// Set the interval to call startTimer every second
				timer = setInterval(startTimer, 1000);
				displayExam(0)
				storeFixedData()
				
		}).catch((error) => {
			connectivityErrorDisplay({"content":error}); // Handle any errors
		});
	}
}


function storeFixedData(){
	localStorage.setItem("questions", JSON.stringify(ajax_data))
	localStorage.setItem("selectedAnswers", JSON.stringify({}))
	localStorage.setItem("meta", JSON.stringify({"fixed": fixed, "time":time, "see_score": see_score, "screenWidth": screenWidth, "screenheight":screenheight}))

}
function clearStoredData(){
	localStorage.removeItem("questions")
	localStorage.removeItem("selectedAnswers")
	localStorage.removeItem("meta")
	localStorage.removeItem("index")
}

function getStoredData(){
	let stored_ajax_data  = localStorage.getItem("questions")
	let stored_selectedAnswers = localStorage.getItem("selectedAnswers")
	let stored_meta = localStorage.getItem("meta")
	index = Number(localStorage.getItem("index"))
	
	if (stored_ajax_data != null & stored_selectedAnswers!= null & stored_meta!= null){
		ajax_data = JSON.parse(stored_ajax_data);
		stored_meta = JSON.parse(stored_meta)
		time= stored_meta.time
		fixed = stored_meta.fixed
		see_score = stored_meta.see_score
		screenWidth = stored_meta.screenWidth
		screenheight =  stored_meta.screenheight
		selectedAnswers = JSON.parse(stored_selectedAnswers)
		

		examstatus = "active"
		// Set the interval to call startTimer every second
		timer = setInterval(startTimer, 1000);
		displayExam(index)
	}else{
		alert("Couldn't get exam it")
	}
}

function createModal({title="",content="",show_header=true, show_footer=false, icon=null}){
	// Create modal structure
	let modalHTML =  `<div class="modal fade" id="alertModal" ${show_header?"":`data-bs-backdrop="static" data-bs-keyboard="false"`} tabindex="-1" aria-labelledby="alertModalLabel" aria-hidden="true">
	<div class="modal-dialog modal-dialog-centered">
	  <div class="modal-content">
		${show_header?
			`<div class="modal-header">
				<h4 class="modal-title text-center fw-bold">${title}</h4>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
			</div>`:
			""}
		<div class="modal-body text-center">
			${icon? icon: ``}
		  	<p>${content}</p>
		</div>

		${show_footer? 
			`<div class="modal-footer d-flex justify-content-between">
				
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
					<button type="submit" class="btn btn-success" id="confirmSubmit">Yes</button>
				
			</div>`: 
			""
		}
	  </div>
	</div>
  </div>`
  
  // Append modal to body
  document.body.insertAdjacentHTML('beforeend', modalHTML);

  // Initialize modal
  const modalElement = document.getElementById('alertModal');
  const modal = new bootstrap.Modal(modalElement);

  // Show the modal
  modal.show();
  isModalOpen = true;  // Set to true when the modal is shown

  // Event listener to remove the modal from the DOM after it's closed
  modalElement.addEventListener('hidden.bs.modal', () => {
	  modalElement.remove();
	  isModalOpen = false;  // Set to false when the modal is hidden
  });

  
}



function rules(){
	return `
		<div class="d-flex align-items-start">
			<p class="fw-bold w-50 text-start">Assessment name</p>
			<div class="ms-2 ">
				<p class="text-start">${examDetails.examName}</p>
			</div>
		</div>
		<div class="d-flex align-items-start">
			<p class="fw-bold w-50 text-start">No of questions</p>
			<div class="ms-2">
				<p class="text-start">${examDetails.countQuestion}</p>
			</div>
		</div>
		<div class="d-flex align-items-start">
			<p class="fw-bold w-50 text-start">Test duration</p>
			<div class="ms-2">
				<p class="text-start">${examDetails.duration}</p>
			</div>
		</div>
		<div class="d-flex align-items-start">
			<p class="fw-bold w-50 text-start">Monitored</p>
			<div class="ms-2">
				<p class="text-start text-danger fw-bold">True</p>
			</div>
		</div>
		<div class="d-flex align-items-start">
			<p class="fw-bold w-50 text-start">Infringement</p>
			<div class="ms-2">
				<p class="text-start text-danger fw-bold">-</p>
			</div>
		</div>
		${check_storage_for_data ?

			`<ol class="text-start">
				<li>Read all questions carefully and keep track of time using the on-screen timer.</li>
				<li>Answer all questions before the time elapses; the system will auto-submit your session when time runs out.</li>
				<li>Maintain academic integrity; cheating is strictly prohibited.</li>
				<li>Do not leave or resize the browser window once the exam starts. Violations may lead to session termination.</li>
				<li>If interrupted, return to the same browser window to resume the exam. Contact support if issues persist.</li>
				<li>If terminated for malpractice, you will not be allowed a retake, if retakes are supported.</li>
			</ol>`:""

		}
		
			<div class="d-grid">
				<button class="btn btn-outline-success" type="button" data-bs-dismiss="modal" id="startBtn">Start</button>
			</div>
	`

}

function showExamInstructions(){
	let msg
	if (check_storage_for_data){
		msg = `<p class="text-muted text-start fw-bolder">Please read the following instructions before you commence</p>
				<div id="instructionBody">
					<p>You have have an unfinished session. Click the button below to continue</p>
					<div class="d-grid gap-2">
						<button class="btn btn-outline-success" type="button" id="next">Continue session</button>
					</div>
				</div>`
	}else{	
		msg = `
				<p class="text-muted text-start fw-bolder">Please read the following instructions before you commence</p>
				<div id="instructionBody">
					<div class="d-flex align-items-start">
						<i class="bi-lightbulb" style="font-size: 2rem; color: cornflowerblue;"></i>
						<div class="ms-2 text-start">
							<h3 class="fw-bold mb-0 fs-5 text-body-emphasis">Before You Begin</h3>
							<ul>
								<li>Ensure a strong and stable internet connection.</li>
								<li>Use a compatible device (laptop/desktop/Android) with an updated browser.</li>
								<li>Have permitted materials ready.</li>
							</ul>
						</div>
					</div>
					<div class="d-flex align-items-start">
						<i class="bi-alarm" style="font-size: 2rem; color: cornflowerblue;"></i>
						<div class="ms-2 text-start">
							<h3 class="fw-bold mb-0 fs-5 text-body-emphasis">During the Exam</h3>
							<ul>
								<li>Read all questions carefully and keep track of time using the on-screen timer.</li>
								<li>Answer all questions before the time elapses; the system will auto-submit your session when time runs out.</li>
								<li>Maintain academic integrity; cheating is strictly prohibited.</li>
								<li>Do not leave or resize the browser window once the exam starts. Violations may lead to session termination.</li>
								<li>If interrupted, return to the same browser window to resume the exam. Contact support if issues persist.</li>
								<li>If terminated for malpractice, you will not be allowed a retake, if retakes are supported.</li>
							</ul>
						</div>
					</div>
					<div class="form-check mb-2">
						<input class="form-check-input" type="checkbox" value="" id="agreeCheck">
						<label class="form-check-label text-start p-0 " for="agreeCheck">
							I have read and agree to the instructions.
						</label>
					</div>
					<div class="d-grid gap-2">
						<button class="btn btn-outline-success" type="button" id="next" disabled>Next</button>
					</div>
				</div>	
				
		`
	}
	createModal({
		content: msg, 
		show_header: false, 
		icon: ""
	});

	let next = $("#next")
	$("#agreeCheck").on("change", function(){
		next.prop("disabled", !this.checked)
	})

	next.on("click", function(){
		msg = rules()
		$("#instructionBody").html(msg)
	})

	$("#instructionBody").on("click", "#startBtn", function(){
		// Set the interval to call startTimer every second
		fetchAndInitializeExam()
	})

	
}



// Function to close the modal if it's open
function closeModalAndCreateNew({content= content, closeBtn= false, icon=`<i class="text-success fas fa-check-circle fa-3x"></i>`, resize=false}) {
    let msg ;
    if (closeBtn){
		icon = `<i class="text-warning fas fa-exclamation-triangle fa-3x"></i>`
		msg = `<p id="modalMsg">${content}</p>`;
		msg += `<p>You have <strong>${warning}</strong> warnings left.</p><div class="d-grid mt-2 gap-2 col-6 mx-auto">
				${!resize? `<button class="btn btn-danger" id="closeCountdown" type="button" data-bs-dismiss="modal" onclick="clearNavIntervalViolation()">Close</button>` : `<button class="btn btn-danger" id="resizeBrowser" type="button" data-bs-dismiss="modal" onclick="resizewindow()">Resize</button>`}
			</div>`;
	}else{
		msg = `<p id="modalMsg">${content}</p>`;
		msg += `<div class="d-grid mt-2 gap-2 col-6 mx-auto">
				${see_score ? `<button class="btn btn-success" id="seeScore" type="button" data-bs-dismiss="modal" disabled>Processing <i class="fas fa-spinner fa-spin"></i></button>` 
				: `<button class="btn btn-success" type="button" onclick="window.close()">End Session</button>`}
			</div>`;
	}

    const handleModalHidden = (modalElement) => {
        const modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) {
            modal.dispose(); // Dispose of the modal instance
        }
        modalElement.remove(); // Remove the modal's HTML from the DOM
        isModalOpen = false; // Update the state variable

        // Ensure new modal is created after the current one is fully hidden
        createModal({
            content: msg, 
            show_header: false, 
            icon: icon
        });

		
    };

    if (isModalOpen) {
        const modalElement = document.getElementById('alertModal');
        if (modalElement) {
            const modal = bootstrap.Modal.getInstance(modalElement);
            if (modal) {
                modalElement.addEventListener('hidden.bs.modal', () => handleModalHidden(modalElement), { once: true });
                modal.hide(); // Hide the modal
            } else {
                handleModalHidden(modalElement);
            }
        } else {
            // If modalElement is null, just create a new modal
            createModal({
                content: msg, 
                show_header: false, 
                icon: icon
            });
			
        }
    } else {
        createModal({
            content: msg, 
            show_header: false, 
            icon: icon
        });
		
    }

	document.addEventListener('ajaxSuccess', function(event) {
		//this event contains details of the exam
		$("#seeScore").text("See score")
		seeScoreBtn(event.detail)
		$("#seeScore").prop("disabled", false)

		// Dispatch the custom event to signal that the process is complete
        document.dispatchEvent(new CustomEvent('closeModalAndCreateNewComplete'));
	});

}

//check if score button is clicked?
function seeScoreBtn(metrics){
	// Add event listener for the custom event
    document.addEventListener('closeModalAndCreateNewComplete', function() {
        // Add event listener for the seeScore button
        const seeScoreButton = document.getElementById('seeScore');
        if (seeScoreButton) {
            seeScoreButton.addEventListener('click', () => {
                result(metrics);
				
            });
        }
    }, { once: true });
}

//display getData error if any
function connectivityErrorDisplay(content){
	createModal({title:"", content:content})
}


//display exam
const displayExam = (i) => {
	index = i < ajax_data.length ? i : ajax_data.length
	let questionContainer = $("#quiz-container")
	question_data = ajax_data[index]
	question = Object.keys(question_data)[0] //an object question
	let options = getOptions() // an object of options array
	questionContainer.html(`
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
				<a href="#question" class="btn btn-primary px-4 py-2 fw-bold me-2" onclick="displayExam(${index > 0 ? index -1 : 0})" > <i class="fas fa-angle-double-left"></i> <span class="d-none d-md-inline-block">Previous</span></a> 

				<a href="#question" class="btn btn-primary px-4 py-2 fw-bold" onclick="displayExam(${index < ajax_data.length-1 ? index +1 : index})">
					<span class="d-none d-md-inline-block">Next</span> <i class="fas fa-angle-double-right"></i></a> 
			</div>
			<div class="align-self-center mx-auto">
			<button ${index == ajax_data.length - 1 ? "" : "disabled"} type="button"  id="submitBtn" class="btn btn-success px-4 py-2 fw-bold">Submit</button>
				
			</div>   
			
		</div>
	</div>


	
	`)
	// jumperBtns(".jumperbtn .row")
	$(".jumperbtn .md-screen").html(createJumperBtns())
	localStorage.setItem("index", index)
	
}

//get and structure
const getOptions = () => {
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

function startTimer() {
	const now = new Date().getTime();
    distance = fixed - now;
	percentremain = (distance * 100 / (time * 1000));
	
	
	// Calculate time components
	let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
	let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
	let seconds = Math.floor((distance % (1000 * 60)) / 1000);


	// Display the result in the element with id="demo"
	if (distance>0){
		document.getElementById("timer").innerHTML =
		`<p  class="d-none d-md-block">Time remaining:</p>

		<div class="progress fs-4" style="height: 25px; border: 2px solid #d3d9df; background-color: white; border-radius: 20px">
			<div class="progress-bar progress-bar-animated progress-bar-striped" id="bar" style="overflow: visible; width:${percentremain}%;">
				<span class="fw-bold" style="color: #bfbfbf">${hours > 0 ? hours + " : " : ""} ${minutes < 10 ? "0" + minutes : minutes} : ${seconds < 10 ? "0" + seconds : seconds}</span>
			</div>
		</div> `;
		//if less than a minute
		if (minutes < 1) {
			let ChangeColor = document.getElementById("bar")
			ChangeColor.classList.add("bg-danger")
		}
	}else{
		$("#timer").html(`<h3 class="text-center text-danger">Session ended</h3>`);
		clearInterval(countdown);
		clearInterval(timer)
		closeModalAndCreateNew({content:"Time's up! Your responses have been auto-submitted."})
		submit()
	}

	

}

//get jumper buttons for large screens

const SmalljumperBtns =() =>{
	let btns = createJumperBtns()
	let btnStructure = `<div class="container jumperbtn ">
					<div class="row">
						${btns}
					</div>
					
				</div>`
	
	createModal({title:"", content:btnStructure})

	$(".jumper-button").on("click", function(){
		$("#alertModal").modal("hide")
	})
	
}
function createJumperBtns(){
	const totalButtons = ajax_data.length;
	let btns = ""
	for (let i = 0; i < totalButtons; i++) {
		let answeredBtns = false
		let min = Object.keys(ajax_data[i])
		if (selectedAnswers[`${min[0]}`]) {
			answeredBtns = true
		}
		const btn = `<div class="col-auto p-0"><button class='btn btn-outline-secondary jumper-button text-center ${i == index ? "active" : ""} ${answeredBtns ? `answered` : ""}' onclick="displayExam(${i})">${i + 1}</button></div>`
		btns += btn
	}
	return btns
	
}

//add answers when an option is clicked
const addAnswer = () => {
	let currentOptions = document.getElementsByName("ans")
	currentOptions.forEach(currentOption => {
		if (currentOption.checked == true) {
			selectedAnswers[`${question}`] = currentOption.value
		}
	})
	localStorage.setItem("selectedAnswers", JSON.stringify(selectedAnswers)) //important
}

const resetAnswer = () => {
	let currentOptions = document.getElementsByName("ans")
	currentOptions.forEach(currentOption => {
		if (currentOption.checked == true) {
			currentOption.checked = false
			delete (selectedAnswers[`${question}`])
		}
	})
	localStorage.setItem("selectedAnswers", JSON.stringify(selectedAnswers))

}



//function to detect clicked button
function keypressed(event) {
	let currentOptions = document.getElementsByName("ans")
	if (event.keyCode == 65) {
		currentOptions[0].checked = true
		addAnswer()
	}
	if (event.keyCode == 66) {
		currentOptions[1].checked = true
		addAnswer()
	}
	if (event.keyCode == 67) {
		currentOptions[2].checked = true
		addAnswer()
	}
	if (event.keyCode == 68) {
		currentOptions[3].checked = true
		addAnswer()
	}

	//prevent resize of window
	if (event.keyCode == 123){ //f12
		//event.preventDefault()
	}
	if (event.ctrlKey && event.shiftKey && event.key === 'I'){ //ctrl +shft+1
		//event.preventDefault()
	}
	
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


let promptSubmit = () => {
	let message = ""
	no_AnsweredQuestions = Object.keys(selectedAnswers).length
	let no_totalQuestion = Object.keys(ajax_data).length
	if (no_AnsweredQuestions < no_totalQuestion) {
		message += `<p class="fw-bold">You have ${no_totalQuestion - no_AnsweredQuestions}  unanswered question</p>`
	}
	message += "Once you click the Yes button, this process cannot be reversed.<br><br>Do you want to continue?"
	return message
}


//when ever submit button is clicked
$(document).on("click",  "#submitBtn", function(event){

	createModal({title :"Are you sure you want to Submit?",content :promptSubmit(), show_footer:true})

	$(document).on("click","#confirmSubmit", function(){
		
		if (timer){
			$("#timer").html(`<h3 class="text-center text-danger">Session ended</h3>`);
			clearInterval(timer)
			closeModalAndCreateNew({content:"Exam submited successfully"})
			submit()
			
		}
	})	
})



//listen for clicked buttons
document.addEventListener("keydown", (event) => {
	if (examstatus == "active") {
		keypressed(event)
	}
})
document.addEventListener("contextmenu", function(event){
	if (examstatus == "active") {
		event.preventDefault()
	}
})

//handle everything submit
let submit = () => {
	$("#majorContainer").html("")
	elapsedTime = Math.ceil(time - (distance / 1000)) >= time ? time : Math.ceil(time - (distance / 1000))
	
	selectedAnswers["elapsedTime"] = elapsedTime
	selectedAnswers["csrfmiddlewaretoken"] = csrftoken
	selectedAnswers["misconduct"] = misconduct
	
	let questions = ajax_data.map(x => Object.keys(x)[0]) //get just the questions
	questions.forEach(question =>{
		if (selectedAnswers[question]==undefined){
			selectedAnswers[question] = null
		}
	})
	if (countdown){
		clearInterval(countdown);
	}
	examstatus="ended"
	$.ajax({
		type: "POST",
		url: url_submit,
		data: selectedAnswers,
		success: function(success){
			clearStoredData()
			setTimeout(()=>{
				resultData = success
				let event = new CustomEvent('ajaxSuccess', { detail: success });
            document.dispatchEvent(event);
			}, 2000)
			
		},
		error: function(error){
			console.log(error)
		}
	})
}

function formatTime(seconds) {
    let minutes = Math.floor(seconds / 60);
    let remainingSeconds = seconds % 60;

    if (minutes > 0) {
        return `${minutes} minute${minutes > 1 ? 's' : ''} ${remainingSeconds} second${remainingSeconds !== 1 ? 's' : ''}`;
    } else {
        return `${remainingSeconds} second${remainingSeconds !== 1 ? 's' : ''}`;
    }
}

const result = (metrics) =>{
	// const {pass, score, no_of_correct_answer, correctAnswers} = data
	$("#majorContainer").addClass("reportContainer")
	let newDiv = document.createElement("div"); 
	
	let resultHtml = `
	<div class="report-card p-4">
		<div class="report-card-header mb-4">
			<h1>Student Report Card</h1>
			<p><strong>Exam Name</strong> ${examDetails.examName}</p>
			<p><strong>Subject:</strong> ${examDetails.subject}</p>
			
		</div>
		
		<div class="student-info ">
			<div class="row">
				<div class="text-start">
					<p><strong>Student Name:</strong> ${examDetails.studentName}</p>
				</div>
				<div class="text-end">
					<p><strong>Grade:</strong> ${examDetails.grade}</p>
				</div>
			</div>
		</div>

		<table class="table table-bordered mx-auto text-start">
			<thead>
				<tr>
					<th scope="col" colspan=2>Metric</th>
					
				</tr>
			</thead>
			<tbody>
				<tr>
					<td>Total number of answered questions</td>
					<td>${metrics.no_of_correct_answer + metrics.no_of_wrong_answers}</td>
				</tr>
				<tr>
					<td>Number of <span class="text-success fw-bold">correct</span>  answers</td>
					<td>${metrics.no_of_correct_answer}</td>
				</tr>
				<tr>
					<td>Number of <span class="text-danger fw-bold">wrong</span> questions</td>
					<td>${metrics.no_of_wrong_answers}</td>
				</tr>
				<tr>
					<td>Total number of <span class="fw-bold">unanswered</span>  questions</td>
					<td>${metrics.no_of_unanswered}</td>
				</tr>
				<tr>
					<td>Time spent</td>
					<td>${formatTime(elapsedTime)}</td>
				</tr>
				<tr>
					<td>Score</td>
					<td><div class="frac">
								<span>${metrics.no_of_correct_answer}</span>
								<span class="symbol">/</span>
								<span class="bottom">${metrics.total_questions}</span>
							</div>
					</td>
				</tr>
				<tr>
					<td>Percentage Score</td>
					<td>${metrics.score}%</td>
				</tr>
			</tbody>
		</table>

		<div class="report-card-footer mt-4">
			<p><strong>Teacher's Remark:</strong> <span class="text-decoration-underline ${metrics.pass? 'text-success' :'text-danger'}">${metrics.pass?"Pass":"Fail"}</span></p>
			<p class="text-muted">Corrections to this exam will be made available after the exam period ends as scheduled by the teacher.</p>
		</div>

		<div class="text-center mt-4">
			<button class="btn btn-success" type="button" onclick="window.close()">End Session</button>
		</div>
	</div>
	
	`    
	
	newDiv.innerHTML = resultHtml
	$("#majorContainer").html(newDiv)

	if (metrics.pass){
		makeConfetti()
	}
}



// Function to get the CSRF token from a cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Get the CSRF token
const csrftoken = getCookie('csrftoken');




// document.addEventListener("visibilitychange", (event) => {
// 	if (document.visibilityState === "hidden") {
// 		// track minimized the browser
// 		if (examstatus == "active") {
// 			alert("Opened new tab")
			
// 		}

// 	}
// });




 // Sound for the alarm
// const alarmSound = new Audio('alarm.mp3'); // Replace with the actual path to your sound file

window.addEventListener("blur", (event) =>{
	if (examstatus == "active") {
		
		// Play alarm sound
        // alarmSound.play();
		if (countdown){
			clearInterval(countdown);
		}else{
			timeLeft = 30;
		}
		
		closeModalAndCreateNew({content:`You have navigated away from the exam window. Please return within <span id='countdown' class='fw-bold'>${countdown? timeLeft : 30}</span> seconds to avoid penalties. Else you session will be terminated.<br> <span class="text-muted fw-bold">Click the button below to:</span>`, closeBtn:true})
		

		countdown = setInterval(function() {
			//start countdown until all
			timeLeft--;
			blurredFrame = true
			try {
				document.getElementById('countdown').textContent = timeLeft;
			} catch (error) {
				
			}

			let closeCountdown = $("#closeCountdown")
			if (closeCountdown) {
				closeCountdown.on("click", function () {
					clearInterval(countdown);
					
				})
			}

			if (timeLeft <= 0) {
				misconduct = true
				clearInterval(countdown);
				clearInterval(timer)
				submit()
				closeModalAndCreateNew({content:`Exam submitted because of <span class="text-danger">Violation(s)</span>.You have been penalized for leaving the exam window even after warning. If exam supports retake, you will not be eligible. Contact support`})
			}
			
		}, 1000);
	}
})



let resizeTimeout= false;
window.addEventListener('resize', () => {
    
	if (examstatus == "active") {
		if(window.outerWidth != screenWidth){
			if (resizeTimeout !== false){
				clearTimeout(resizeTimeout);
				blurredFrame = false
			}
			
			resizeTimeout = setTimeout(() => {
				if (blurredFrame == false){
					closeModalAndCreateNew({content:`Please do not resize your browser during the exam.<br> <span class="text-muted fw-bold">Click the button below to:</span>`, closeBtn:true, resize:true})
				}
			}, 2000); // Adjust the timeout duration as needed
		
			
		}
		
	}	
});

function resizewindow(){
	window.resizeTo(screenWidth, screenheight)
	window.moveTo(0, 0);
	warningFunc()
}

function clearNavIntervalViolation(){
	$("#closeCountdown").on("click", function () {
		clearInterval(countdown);
			
	})
	warningFunc()
}

const warningFunc = ()=>{
	warning--

	if (warning <0){
		misconduct = true
		clearInterval(countdown);
		clearInterval(timer)
		submit()
		closeModalAndCreateNew({content:`You have been penalized for <span class="text-danger">Violation(s)</span> after multiple warnings. As a result, your exam has been terminated and submitted. If the exam supports retakes, you will not be eligible. Please contact support for further assistance.`})
	}
	
}


function makeConfetti(){
	const majorContainer = document.getElementById("majorContainer")

	// Retrieves the position and size of the button to calculate where the confetti should appear.
	const rect = majorContainer.getBoundingClientRect();
	// Calculates the horizontal (x) center of the button.
	const x = (rect.left + rect.right) / 2;
            
	// Calculates the vertical (y) center of the button.
	const y = (rect.top + rect.bottom) / 2;

	// Configures the settings for the confetti effect.
	const confettiSettings = {
	  particleCount: 100, // Defines the number of confetti particles.
	  spread: 70,         // Sets the spread angle of the confetti.
	  // Specifies the origin point for the confetti effect based on the button's location.
	  origin: { x: x / window.innerWidth, y: y / window.innerHeight }
	};

	// Triggers the confetti effect with the defined settings when the button is clicked.
	confetti(confettiSettings);
}

window.onunload = function() {
	if (window.opener && !window.opener.closed) {
		window.opener.location.reload();
	}
};