
const url_data = location.origin+examDataUrl
const url_submit = location.origin+examSubmit
let ajax_data	//questions gotten from ajax call --> [ {…}, {…}, {…}, {…} ]
let time
let selectedAnswers = {}
let no_of_correct_answer //provided from post data
let no_AnsweredQuestions;
let attempts = 0
let examstatus
let warning
let misconduct = false


//Get the data
const  getData = () =>{ 
	$.ajax({
		type: "GET",
		url: url_data,
		async: false,  //to make sure i can save the variable ajax_data
		success: function (response) {
			ajax_data = response.data
			if (ajax_data){
				time = response.time
				allow_retake = response.retake
				window.review = response.review
				examstatus = "active"
				warning = 2
				attempts = response.attempts
				if (!allow_retake || review ){ //if don't allow retake or review after exam
					attempts = 2	
				}
				console.log(response.review)
			}else{
				alert("No exam at the moment")
				window.location.href = "http://127.0.0.1:8000/student/available-exams"
			}
		},
		error: function (error){
			console.log(error)
		}
	})
	
}

// -----------------------
getData()
// -----------------------


// const restart = () =>{
// 	getData()
	
// 	selectedAnswers ={}
// 	displayExam(0)
// 	percentremain=0;
// 	distance = time * 1000;
// 	fixed=new Date().getTime(); //gets the current time in milliseconds
// 	fixed +=distance;
// 	timer = setInterval(startTimer, 1000);
	
// }






//     Update the count down every 1 second
let percentremain=0;
let distance = time * 1000;
let fixed=new Date().getTime(); //gets the current time in milliseconds
fixed +=distance;

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
	if (hours == 0 && minutes ==0 && seconds <1) {
		setTimeout(()=>{
			document.getElementById("timer").innerHTML = ``;
			clearInterval(timer)
			no_AnsweredQuestions = Object.keys(selectedAnswers).length
			no_totalQuestion = Object.keys(ajax_data).length
			selectedAnswers["elapsedTime"] = time
			$('#timeUp').modal('show')
			
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

let timer = setInterval(startTimer, 1000);

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

// let questionContainer = document.getElementById("quiz-container")
// const displayExam = (i)=>{
// 	index = i
// 	if (ajax_data[index]){
// 		question_data = ajax_data[index] //an object for both question and answer
// 		question = Object.keys(question_data)[0] //an object question
// 		let options = getOptions() // an object of options array
// 		let btns =jumperBtns()
// 		questionContainer.innerHTML = `
// 		<div class="col-12" >
// 			<div id ="warning"></div>
// 			<p class="fw-bold" style="font-family: Georgia, 'Times New Roman', Times, serif;">Question ${i +1} of ${ajax_data.length}</p>
// 			<hr>
// 			<span class="fw-bold fs-4" style="font-family: Georgia, 'Times New Roman', Times, serif;">${question}</span>
			
// 			<div class="mt-4"> 
// 				${options}
// 			</div>
// 		</div>

// 		<div class="col-12 mb-2">
// 			<div class="d-flex justify-content-between flex-wrap" id="all_btns"> 
// 				<div class="align-self-center mx-auto">
// 					<button type="reset" class="btn btn-dark px-4 py-2 fw-bold" onclick="resetAnswer()">Reset</button>
// 				</div>
// 				<div class="align-self-center mx-auto">
// 					<button class="btn btn-primary px-4 py-2 fw-bold me-2" onclick="displayExam(${index - 1})" ${index < 1 ? "disabled" : ""}> Previous</button> 
// 					<button class="btn btn-primary px-4 py-2 fw-bold" onclick="displayExam(${index + 1})" ${index == ajax_data.length -1 ? "disabled" : ""}> Next</button> 
// 				</div>
// 				<div class="align-self-center mx-auto">
// 				<button type="button" class="btn btn-success px-4 py-2 fw-bold" data-bs-toggle="modal" data-bs-target="#myModal" onclick="promptSubmit()">Submit</button>
					
// 				</div>
				
// 			</div>
// 		</div>

// 		<div class="col-12" >
// 			<nav aria-label="Page navigation example" >
// 				<ul class="pagination justify-content-center flex-wrap">
// 					${btns}
// 				</ul>
// 			</nav>
// 		</div>
			


// 			`
// 	}else{
// 		// console.log(window.location.host+"/student/available-exams")
// 		alert("No question")
// 	}
	
// }
// // -----------------------------------------------------------------------------------------
// displayExam(0)

// // -----------------------------------------------------------------------------------------
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
let csrf = document.getElementsByName("csrfmiddlewaretoken")
let submit = ()=>{
	
	for (let i = 0; i < ajax_data.length; i++) {
		let allQuestions = ajax_data[i]
		if (selectedAnswers[`${Object.keys(allQuestions)[0]}`] == undefined) {
			selectedAnswers[`${Object.keys(allQuestions)[0]}`] = null
		}
	}

	selectedAnswers["csrfmiddlewaretoken"] = csrf[0].value 
	selectedAnswers["misconduct"] = misconduct
	selectedAnswers["attempts"] = attempts
	$.ajax({
		method: "POST",
		url: url_submit,
		data: selectedAnswers,
		async: false,
		success: function (response) {
			no_of_correct_answer = response.no_of_correct_answer;
			score = response.score
			teacherRemark = response.pass
			// console.log(response)
			examstatus = "ended"
			
		},
		else: function(error){
			alert("Something went wrong")
		}
	});
	
	result()
}


// If the student finishes before time this is the function that handles the submition 
let submitHandler = ()=> {
	let elapsedTime = Math.ceil(time - (distance/1000)) //no. of seconds used to answer the question
	selectedAnswers["elapsedTime"] = elapsedTime
	clearInterval(timer)
	document.getElementById("timer").innerHTML = `<h3 class="text-center">Exam ended</h3>`;
	document.getElementById("confirmSubmit").addEventListener("click",
	submit()
	)
	$('#myModal').modal('hide')
}

document.forms[0].addEventListener("click", e =>{
	e.preventDefault();
	
	submitHandler()
})



let result = ()=>{
	let elapsedTime = selectedAnswers.elapsedTime
	delete selectedAnswers.csrfmiddlewaretoken;
	delete selectedAnswers.elapsedTime
	// let nullCount = values.filter (value => value === null).length; 
	questionContainer.innerHTML = `
			<div class="col-10 mx-auto" style="border: 2px solid black">
			<div class="table-responsive mx-auto">
				<table class="table table-hover table-bordered caption-top">
					<caption><h1>Exam result</h1></caption>
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
							<td class="text-center">${teacherRemark ? "Pass" : "Fail"}</td>
						</tr>

					</tbody>
				</table>
			</div>
			<div class="text-center">
				
				${attempts<2 ? '<button class="btn btn-primary mb-3 " onclick="restart()">Restart</button>' : ""}
				${attempts==2 ? '<button class="btn btn-primary mb-3 " onclick="correction()">See Correction</button>' : ""}
			</div>
		</div>
	`
}

let correction = () =>{
	let quizContainer = document.getElementById("quiz-container")
	document.getElementById("timer").innerHTML = "<h2>Correction</h2>"
	questionContainer.innerHTML = ""
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
	attempts = 2
	
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
				choiceIcon = `<i class="fas fa-exclamation-circle mt-1"></i>`
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


// // correction()
// // $.ajax({
// //     type: "GET", 
// //     url : url_data,
// // 	async: false, //i did this so that i would be able to save the data gotten from the api into mydata variable above
// //     success: function (response) {
// //         let data = response.data

// //         data.forEach(element => { //loop through the data
// // 			for (const [questions, answers] of Object.entries(element)) {
// // 				quiz_box.innerHTML += `
// //                 <hr>
// //                 <div class="mb-2">
                
// //                     <b>${questions}</b>
                
// //                 </div>

// //                 `
// // 				answers.forEach(answer => { //looop through the answer for each question
// // 					quiz_box.innerHTML += `
// //                     <div>
// //                         <label for="${answer}"><input type="radio" name="${questions}" class="form-check-input ans" id="${answer}" value="${answer}"> ${answer}</label>
// //                     </div>
// //                 `
// // 				})

// // 			}
// // 		});
// // 		mydata = response.data
// // 		console.log(`Inside console.log ${mydata}`)
// //     },
// //     error: function(error){
// //         console.log(error)
// //     }
// // })

// // const quizForm = document.getElementById("quiz-form") //get the form that would submit the quiz
// // const csrf = document.getElementsByName("csrfmiddlewaretoken") //get csrf token from the from the hidden input

// // //getElementsBy method always return a collect of elements while getElementby returns just an element

// // const sendData = () => {
// // 	const elements = [...document.getElementsByClassName("ans")] // get all the input field with class "ans"
// // 	const data = {} // create an empty object
// // 	data["csrfmiddlewaretoken"] = csrf[0].value  // add the csrf token to the data object
// // 	elements.forEach(el => { 
// // 		if (el.checked) {   //foreach of the element, if the element has been answered, append the element to the data object with it's answer
// // 			data[el.name] = el.value
// // 		} else {  // else if its not checked
// // 			if (!data[el.name]) { // check if el.name exists in the data object if 'it does not', create it and
// // 				data[el.name] = null // save it as a null
// // 			}
// // 		}
// // 	})

// // 	$.ajax({
// // 		type: "POST", // make a post request to the url: student/session/4/save
// // 		url: usrl_submit, // A string containing the URL to which the request is sent.
// // 		data: data, // the data object from above to be sent to the server
// // 		success: function (response) {  // if the post request was sucessful a jsonresponse was created in the view as as this JsonResponse({"pass": True, "score": score_, "result":results})
// // 			const results = response.result // from the response, get result attribute
// // 			quizForm.classList.add("d-none") // clear the form element for correction

// // 			results.forEach(res => { // for each of the result
// // 				const resDiv = document.createElement("div") // create a div element
// // 				for (const [question, resp] of Object.entries(res)) {
// // 					resDiv.innerHTML += `${question}<br><hr>`
// // 					const cls = ["container", "p-3", "text-light", "h3"]
// // 					resDiv.classList.add(...cls)

// // 					if (resp == "not answered") {
// // 						resDiv.innerHTML += "-not answered"
// // 						resDiv.classList.add("bg-danger")
// // 					}
// // 					else {
// // 						const answer = resp["answered"]
// // 						const correct = resp["correct_answer"]

// // 						if (answer == correct) {
// // 							resDiv.classList.add("bg-success")
// // 							resDiv.innerHTML += `answered: ${answer}`
// // 						} else {
// // 							resDiv.classList.add("bg-danger")
// // 							resDiv.innerHTML += `   |correct answer: ${correct}`
// // 							resDiv.innerHTML += `   |answered: ${answer}`
// // 						}

// // 					}
					
// // 				}
// // 				document.getElementById("head").innerHTML = "Corrections"
// // 				const quiz_box = document.getElementById("jaden")
// // 				quiz_box.appendChild(resDiv)
// // 				// console.log(resDiv)
// // 			})
// // 		},
// // 		error: function (error) {
// // 			console.error(error)
// // 		}

// // 	})
// // }

// // quizForm.addEventListener("submit", e => {
// // 	e.preventDefault() //prevent the submit button from behaving as it would

// // 	sendData() // call the send button that would send the your request to python

// // })

// // console.log(`Outside console.log ${mydata}`)


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
			attempts = 2 //make exam not restartable
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



// //   <div class="card text-white bg-primary mb-3" style="max-width: 18rem;">
// // 		<div class="card-header">Class Stats</div>
// // 		<div class="card-body">
// // 		  <div class="d-flex align-items-center">
// // 			<i class="fas fa-graduation-cap fa-3x me-3"></i>
// // 			<div class="text-end">
// // 			  <h5 class="card-title">Total Students</h5>
// // 			  <p class="card-text display-4">25</p>
// // 			</div>
// // 		  </div>
// // 		</div>
// // 	  </div>


// /* <div  class="bg-image hover-overlay ripple shadow-1-strong rounded" data-mdb-ripple-color="light">
//   <img src="https://mdbcdn.b-cdn.net/img/new/fluid/city/113.webp" class="w-100 h-25" alt="Louvre" />
//   <a href="#!">
//     <div class="mask" style="background-color: hsla(0, 0%, 98%, 0.2)"></div>
//   </a>
// </div> */