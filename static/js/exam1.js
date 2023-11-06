
const url_data = location.origin+examDataUrl
const usrl_submit = location.origin+examSubmit
let ajax_data	//questions gotten from ajax call
let selectedAnswers = {}

//Get the data
$.ajax({
	type: "GET",
	url: url_data,
	async: false,
	success: function (response) {
		ajax_data = response.data
	},
	error: function (error){
		console.log(error)
	}
})

var counter;
    //code for timer

    // Update the count down every 1 second
    var percentremain=0;
    var distance = 3600000;
    var fixed=new Date().getTime();
    fixed+=distance;
    var x = setInterval(function() {

    //Test time in milliseconds
    distance=fixed-(new Date().getTime());
    percentremain=(distance/36000.0);
    // Time calculations for days, hours, minutes and seconds
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Display the result in the element with id="demo"
    document.getElementById("timer").innerHTML = `<h3 class="text-center">Time remaining:</h3>

            <div class="progress mt-2 fs-4" style="height: 30px; border:2px solid black" >
                <div class="progress-bar progress-bar-striped py-2" id="bar" style="width:${percentremain}%;">
                    <span id="timer">${hours} : ${minutes} : ${seconds}</span>
                </div>
            </div> `;

    // If the count down is finished, write some text 
    if (distance < 0) {
    clearInterval(x);
    document.getElementById("timer").innerHTML = "EXPIRED";
    counter=61;
    submitgreen();
    }
    }, 1000);

const jumperBtns = () =>{
	btns = ""
	let answeredQuestion = false
	
	currentOptions =document.getElementsByName("ans")
	for (let i = 0; i < ajax_data.length; i++) {
		btns += `<li class="page-item"><button class="page-link  ${i==index ? `active`:""}"  onclick="displayExam(${i})">${i + 1}</button></li>`
	}
	currentOptions.forEach(currentOption =>{
		if (currentOption.checked == true){
			answeredQuestion = true
		}
	})
	console.log(answeredQuestion)
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
				<div>
					<button class="btn btn-dark px-4 py-2 fw-bold">Bookmark</button>
				</div>
				<div>
					<button class="btn btn-primary px-4 py-2 fw-bold me-2" onclick="displayExam(${index - 1})" ${index < 1 ? "disabled" : ""}> Previous</button> 
					<button class="btn btn-primary px-4 py-2 fw-bold" onclick="displayExam(${index + 1})" ${index == ajax_data.length -1 ? "disabled" : ""}> Next</button> 
				</div>
				<div>
					<button type="submit" class="btn btn-success px-4 py-2 fw-bold">Submit</button>
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



