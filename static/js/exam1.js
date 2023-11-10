
const url_data = location.origin+examDataUrl
const url_submit = location.origin+examSubmit
let ajax_data	//questions gotten from ajax call --> [ {…}, {…}, {…}, {…} ]
let time
let selectedAnswers = {}

//Get the data
$.ajax({
	type: "GET",
	url: url_data,
	async: false,  //to make sure i can save the variable ajax_data
	success: function (response) {
		ajax_data = response.data
		time = response.time
	},
	error: function (error){
		console.log(error)
	}
})


    //code for timer

    // Update the count down every 1 second
let percentremain=0;
let distance = time * 1000;
let fixed=new Date().getTime(); //gets the current time in milliseconds
fixed +=distance;

let timer = setInterval(function() {

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
			submit();
			alert("Your session has ended")
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
	
}, 1000);

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
		if (selectedAnswers[`${Object.keys(question_data)}`] == option){
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
	$.ajax({
		method: "POST",
		url: url_submit,
		data: selectedAnswers,
		success: function (success) {
			console.log(success)
		},
		else: function(error){
			alert("Something went wrong")
		}

	})
	result()
}


const addAnswer = ()=>{
    let currentOptions = document.getElementsByName("ans")
    currentOptions.forEach(currentOption =>{
        if (currentOption.checked == true){
			
            selectedAnswers[`${question}`] = currentOption.value
        }
    })
	
}

let questionContainer = document.getElementById("quiz-container")
const displayExam = (i)=>{
	index = i
	if (ajax_data[index]){
		question_data = ajax_data[index] //an object for both question and answer
		question = Object.keys(question_data)[0] //an object question
		let options = getOptions() // an object of options array
		let btns =jumperBtns()
		questionContainer.innerHTML = `
		<div class="col-12" >
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
					<button type="reset" class="btn btn-dark px-4 py-2 fw-bold">Reset</button>
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
		alert("No question")
	}
	
}

displayExam(0)
document.forms[0].addEventListener("click", e =>{
	e.preventDefault();
	
	let elapsedTime = Math.ceil(time - (distance/1000)) //no. of seconds used to answer the question
	selectedAnswers["elapsedTime"] = elapsedTime
	clearInterval(timer)
	document.getElementById("timer").innerHTML = `<h3 class="text-center">Exam ended</h3>`;
	alert("Your session has ended")
	submit();

})

let result = ()=>{
	let elapsedTime = selectedAnswers.elapsedTime
	delete selectedAnswers.csrfmiddlewaretoken;
	delete selectedAnswers.elapsedTime
	console.log(elapsedTime)
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
							<td class="text-center">${elapsedTime < 60 ? elapsedTime + " sec(s)" : (elapsedTime / 60) + " min(s)"}</td>
						</tr>
						<tr>
							<th scope="row">Donuts</th>
							<td class="text-center">3,000</td>
						</tr>
						<tr>
							<th scope="row">Donuts</th>
							<td class="text-center">3,000</td>
						</tr>
						<tr>
							<th scope="row">Donuts</th>
							<td class="text-center">3,000</td>
						</tr>
						<tr>
							<th scope="row">Donuts</th>
							<td class="text-center">3,000</td>
						</tr>

					</tbody>
				</table>
			</div>
			<div class="text-center"><button class="btn btn-primary mb-3 ">See Correction</button></div>
		</div>
	`
}

// $.ajax({
//     type: "GET", 
//     url : url_data,
// 	async: false, //i did this so that i would be able to save the data gotten from the api into mydata variable above
//     success: function (response) {
//         let data = response.data

//         data.forEach(element => { //loop through the data
// 			for (const [questions, answers] of Object.entries(element)) {
// 				quiz_box.innerHTML += `
//                 <hr>
//                 <div class="mb-2">
                
//                     <b>${questions}</b>
                
//                 </div>

//                 `
// 				answers.forEach(answer => { //looop through the answer for each question
// 					quiz_box.innerHTML += `
//                     <div>
//                         <label for="${answer}"><input type="radio" name="${questions}" class="form-check-input ans" id="${answer}" value="${answer}"> ${answer}</label>
//                     </div>
//                 `
// 				})

// 			}
// 		});
// 		mydata = response.data
// 		console.log(`Inside console.log ${mydata}`)
//     },
//     error: function(error){
//         console.log(error)
//     }
// })

// const quizForm = document.getElementById("quiz-form") //get the form that would submit the quiz
// const csrf = document.getElementsByName("csrfmiddlewaretoken") //get csrf token from the from the hidden input

// //getElementsBy method always return a collect of elements while getElementby returns just an element

// const sendData = () => {
// 	const elements = [...document.getElementsByClassName("ans")] // get all the input field with class "ans"
// 	const data = {} // create an empty object
// 	data["csrfmiddlewaretoken"] = csrf[0].value  // add the csrf token to the data object
// 	elements.forEach(el => { 
// 		if (el.checked) {   //foreach of the element, if the element has been answered, append the element to the data object with it's answer
// 			data[el.name] = el.value
// 		} else {  // else if its not checked
// 			if (!data[el.name]) { // check if el.name exists in the data object if 'it does not', create it and
// 				data[el.name] = null // save it as a null
// 			}
// 		}
// 	})

// 	$.ajax({
// 		type: "POST", // make a post request to the url: student/session/4/save
// 		url: usrl_submit, // A string containing the URL to which the request is sent.
// 		data: data, // the data object from above to be sent to the server
// 		success: function (response) {  // if the post request was sucessful a jsonresponse was created in the view as as this JsonResponse({"pass": True, "score": score_, "result":results})
// 			const results = response.result // from the response, get result attribute
// 			quizForm.classList.add("d-none") // clear the form element for correction

// 			results.forEach(res => { // for each of the result
// 				const resDiv = document.createElement("div") // create a div element
// 				for (const [question, resp] of Object.entries(res)) {
// 					resDiv.innerHTML += `${question}<br><hr>`
// 					const cls = ["container", "p-3", "text-light", "h3"]
// 					resDiv.classList.add(...cls)

// 					if (resp == "not answered") {
// 						resDiv.innerHTML += "-not answered"
// 						resDiv.classList.add("bg-danger")
// 					}
// 					else {
// 						const answer = resp["answered"]
// 						const correct = resp["correct_answer"]

// 						if (answer == correct) {
// 							resDiv.classList.add("bg-success")
// 							resDiv.innerHTML += `answered: ${answer}`
// 						} else {
// 							resDiv.classList.add("bg-danger")
// 							resDiv.innerHTML += `   |correct answer: ${correct}`
// 							resDiv.innerHTML += `   |answered: ${answer}`
// 						}

// 					}
					
// 				}
// 				document.getElementById("head").innerHTML = "Corrections"
// 				const quiz_box = document.getElementById("jaden")
// 				quiz_box.appendChild(resDiv)
// 				// console.log(resDiv)
// 			})
// 		},
// 		error: function (error) {
// 			console.error(error)
// 		}

// 	})
// }

// quizForm.addEventListener("submit", e => {
// 	e.preventDefault() //prevent the submit button from behaving as it would

// 	sendData() // call the send button that would send the your request to python

// })

// console.log(`Outside console.log ${mydata}`)



