const url = window.location.href
const quiz_box = document.getElementById("quiz-box")



$.ajax({
	type: "GET",  //the type of request we are making
	url: `${url}data`, //where to get question data
	success: function (response) { // if it gets the data run this block of code
		let data = response.data // the JSON file it would get from the above URL above
		data.forEach(element => { //loop through the data
			for (const [questions, answers] of Object.entries(element)) {
				quiz_box.innerHTML += `
                <hr>
                <div class="mb-2">
                
                    <b>${questions}</b>
                
                </div>

                `
				answers.forEach(answer => { //looop through the answer for each question
					quiz_box.innerHTML += `
                    <div>
                        <label for="${answer}"><input type="radio" name="${questions}" class="form-check-input ans" id="${answer}" value="${answer}"> ${answer}</label>
                    </div>
                `
				})

			}
		});
	},
	error: function (error) {  // if no data or an error occurs while making the get request output an error
		window.alert(error)
	}

})

const quizForm = document.getElementById("quiz-form") //get the form that would submit the quiz
const csrf = document.getElementsByName("csrfmiddlewaretoken") //get csrf token from the from the hidden input

//getElementsBy method always return a collect of elements while getElementby returns just an element

const sendData = () => {
	const elements = [...document.getElementsByClassName("ans")] // get all the input field with class "ans"
	const data = {} // create an empty object
	data["csrfmiddlewaretoken"] = csrf[0].value  // add the csrf token to the data object
	elements.forEach(el => { 
		if (el.checked) {   //foreach of the element, if the element has been answered, append the element to the data object with it's answer
			data[el.name] = el.value
		} else {  // else if its not checked
			if (!data[el.name]) { // check if el.name exists in the data object if 'it does not', create it and
				data[el.name] = null // save it as a null
			}
		}
	})

	$.ajax({
		type: "POST", // make a post request to the url: student/session/4/save
		url: `${url}save`,
		data: data, // the data object from above
		success: function (response) {  // if the post request was sucessful a jsonresponse was created in the view as as this JsonResponse({"pass": True, "score": score_, "result":results})
			const results = response.result // from the response, get result attribute
			quizForm.classList.add("d-none") // clear the form element for correction

			results.forEach(res => { // for each of the result
				const resDiv = document.createElement("div") // create a div element
				for (const [question, resp] of Object.entries(res)) {
					resDiv.innerHTML += `${question}<br><hr>`
					const cls = ["container", "p-3", "text-light", "h3"]
					resDiv.classList.add(...cls)

					if (resp == "not answered") {
						resDiv.innerHTML += "-not answered"
						resDiv.classList.add("bg-danger")
					}
					else {
						const answer = resp["answered"]
						const correct = resp["correct_answer"]

						if (answer == correct) {
							resDiv.classList.add("bg-success")
							resDiv.innerHTML += `answered: ${answer}`
						} else {
							resDiv.classList.add("bg-danger")
							resDiv.innerHTML += `   |correct answer: ${correct}`
							resDiv.innerHTML += `   |answered: ${answer}`
						}

					}
					
				}
				document.getElementById("head").innerHTML = "Corrections"
				const quiz_box = document.getElementById("jaden")
				quiz_box.appendChild(resDiv)
				// console.log(resDiv)
			})
		},
		error: function (error) {
			console.error(error)
		}

	})
}

quizForm.addEventListener("submit", e => {
	e.preventDefault() //prevent the submit button from behaving as it would

	sendData() // call the send button that would send the your request to python

})


