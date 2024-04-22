let $table = $("#table");
let $remove = $("#remove");
let selections;
const formDataObj = {};
let nos;

let quest_id
let sub_url

function ajaxRequest(params) {
	let url = "question-data";
	$.get(url + "?" + $.param(params.data)).then(function (res) {
		nos = res.offset;

		params.success(res);
		selections = [];
		$remove.prop("disabled", true);
	});
}

//edit formatter
function operateFormatter(value, row, index) {
	
	return `<button ${row.exam != null ? "disabled" : "" } type="button" class="btn btn-light js-edit-question" data-id="${row.id}"><i class="fas fa-pencil"></i></i></button>`;
}

function clearForm(){
	// $("#question-data").get(0).reset()
	$("#question-data select[name=subject]").val()
	$("#question-data textarea[name=option_A]").val()
	$("#question-data textarea[name=option_B]").val()
	$("#question-data textarea[name=option_C]").val()
	$("#question-data textarea[name=option_D]").val()
	$("#question-data input[name=answer]").prop( "checked", false )
	
	$("#question-data .invalid-feedback").remove();
	$("#question-data .is-invalid").removeClass("is-invalid");
	
	
	
	

}

//edtiting a question view
window.operateEvents = {
	"click .js-edit-question": function (e, value, row, index) {
		let btn = $(e.currentTarget);

		$("#addQuestion .modal-title").text("Edit Question")


		// hiding save and add another button
		if (!$(".modal-footer :button:nth-child(2)").hasClass( "d-none" )){
			$(".modal-footer :button:nth-child(2)").addClass( "d-none" )
		}
		
		quest_id = row.id
		sub_url = `/teacher/edit-myquestion/${quest_id}/`
		$("#question-data select[name=subject]").val(row.subject)
		$("#question-data textarea[name=option_A]").val(row.option_A)
		$("#question-data textarea[name=option_B]").val(row.option_B)
		$("#question-data textarea[name=option_C]").val(row.option_C)
		$("#question-data textarea[name=option_D]").val(row.option_D)
		$(`#question-data input[value=${row.answer}]`).prop( "checked", true )
		// $("#question-data textarea[name=question]").val(row.question)
		tinymce.activeEditor.setContent(row.question)
		$("#addQuestion").modal("show");
		
		
	},
};

//create a new question view
$(function () {
	$(".js-create-question").click(function () {
		sub_url = "/teacher/create-myquestion"
		if ($(".modal-footer :button:nth-child(2)").hasClass( "d-none" )){
			$(".modal-footer :button:nth-child(2)").removeClass( "d-none" )
		}
		$("#addQuestion .modal-title").text("Add Question")
		$("#addQuestion").modal("show");
		
		
		// $.ajax({
		//     url: 'create-myquestion',
		//     type: 'get',
		//     dataType: 'json',
		//     beforeSend: function () {
		//       $("#addQuestion").modal("show");
		//     },
		//     success: function (data) {
		//         $("#addQuestion .modal-content").html(data.html_form);
		//     },
		//     error: function(error){

		//     }
		//   });
	});
});



$("#question-data").on("submit", function (event) {
	$(".spinner").toggleClass("d-none")
	event.preventDefault();
	let subBtn  = event.originalEvent.submitter.value
	var form = $(this);
	tinymce.triggerSave();
	let data = form.serialize();
	$.ajax({
		type:"POST", 
		url: sub_url,
		data: data, 
		success: function (data) {
			$(".spinner").toggleClass("d-none")
			if (data.form_is_valid) {
				notify("success", "Question created succesfully");  // <-- This is just a placeholder for now for testing
				$("#question-data").get(0).reset()
				if (subBtn =="false"){
					$("#addQuestion").modal("hide");
				}else{
					$('#addQuestion').animate({ scrollTop: $('#addQuestion').scrollTop(0) }, 500);
				}
				$table.bootstrapTable("refresh")
				const autoCloseElements = [...$(".auto-close")]
				setTimeout(function () {
					autoCloseElements.forEach(el => fadeAndSlide(el));
				}, 5000);
			}else{
				notify("danger", "Question not created");  // <-- This is just a placeholder for now for testing
				$("#addQuestion   .modal-body").html(data.html_form)
				
				
				
				const autoCloseElements = [...$(".auto-close")]
				setTimeout(function () {
					autoCloseElements.forEach(el => fadeAndSlide(el));
					}, 5000);
			}
		}, 
		error: function(error){
			alert("Couldn't fetch data")
		}
	})
});


// //submiting a new question
// $("#addQuestion").on("submit", ".js-question-create-form",function  () {
//   let form = $(this);
//   $.ajax({
//     url: form.attr("action"),
//     data: form.serialize(),
//     type: form.attr("method"),
//     dataType: 'json',
//     success: function (data) {
//       if (data.form_is_valid) {
//           notify("success", "Question created succesfully");  // <-- This is just a placeholder for now for testing
//           $("#addQuestion").modal("hide");
//           $table.bootstrapTable("refresh")
//           const autoCloseElements = [...$(".auto-close")]
//           setTimeout(function () {
//               autoCloseElements.forEach(el => fadeAndSlide(el));
//           }, 5000);
//       }
//       else {
//         $("#addQuestion .modal-content").html(data.html_form);
//         $("#addQuestion").modal("show");

//       }
//     }
//   });
//   return false;
// }
// );

//submitting an edited question
$("#addQuestion").on("submit", ".js-question-edit-form", function () {
	let form = $(this);
	$.ajax({
		url: form.attr("action"),
		data: form.serialize(),
		type: form.attr("method"),
		dataType: "json",
		success: function (data) {
			if (data.form_is_valid) {
				notify("success", "Question saved succesfully"); // <-- This is just a placeholder for now for testing
				$("#addQuestion").modal("hide");
				$table.bootstrapTable("refresh");
				const autoCloseElements = [...$(".auto-close")];
				setTimeout(function () {
					autoCloseElements.forEach((el) => fadeAndSlide(el));
				}, 5000);
			} else {
				$("#addQuestion .modal-content").html(data.html_form);
				$("#addQuestion").modal("show");
			}
		},
	});
	return false;
});

//control disabled delete button
$table.on(
	"check.bs.table uncheck.bs.table " +
	"check-all.bs.table uncheck-all.bs.table",
	function () {
		$remove.prop("disabled", !$table.bootstrapTable("getSelections").length);

		// save your data, here just save the current page
		selections = getIdSelections();
		// push or splice the selections if you want to save all data selections
	}
);

function getIdSelections() {
	return $.map($table.bootstrapTable("getSelections"), function (row) {
		return row.id;
	});
}

//delete button view
$(
	$remove.click(function () {
		$("#addQuestion .modal-content").html("");
		$.ajax({
			url: `delete-myquestion?id=${selections}`,
			type: "get",
			dataType: "json",
			beforeSend: function () {
				$("#addQuestion").modal("show");
			},
			success: function (data) {
				$("#addQuestion .modal-content").html(data.html_form);
			},
			error: function (error) { },
		});

		function getCookie(name) {
			let cookieValue = null;
			if (document.cookie && document.cookie !== "") {
				const cookies = document.cookie.split(";");
				for (let i = 0; i < cookies.length; i++) {
					const cookie = cookies[i].trim();
					// Does this cookie string begin with the name we want?
					if (cookie.substring(0, name.length + 1) === name + "=") {
						cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
						break;
					}
				}
			}
			return cookieValue;
		}
		const csrftoken = getCookie("csrftoken");

		//delete question
		$("#addQuestion").on(
			"submit",
			".js-question-delete-form",
			function (event) {
				event.preventDefault();
				$.ajax({
					type: "POST",
					url: "delete-myquestion/",
					data: {
						csrfmiddlewaretoken: csrftoken,
						id: JSON.stringify(selections),
					},
					success: function (data) {
						if (data.deleted) {
							notify("success", "Question(s) deleted");
							const autoCloseElements = [...$(".auto-close")];
							setTimeout(function () {
								autoCloseElements.forEach((el) => fadeAndSlide(el));
							}, 5000);
							$table.bootstrapTable("refresh");
						}
						$("#addQuestion").modal("hide");
					},
					error: function (error) {
						alert("Couldn't fetch data");
					},
				});
			}
		);
		// $.ajax({
		//     type: "POST",
		//     url: "delete-question",
		//     data: {
		//         id: JSON.stringify(selections),
		//         "csrfmiddlewaretoken": csrftoken
		//                   //or
		//         //"csrfmiddlewaretoken": "{{csrf_token}}"
		//     },
		//     success: function (success){
		//         notify("success", "Question(s) deleted")
		//         //$table.bootstrapTable('remove', {field: 'id',values: getIdSelections()})
		//           $table.bootstrapTable("refresh")
		//           $remove.prop('disabled', true)
		//           //$table.bootstrapTable('refresh')
		//           const autoCloseElements = [...$(".auto-close")]
		//           setTimeout(function () {
		//               autoCloseElements.forEach(el => fadeAndSlide(el));
		//           }, 5000);
		//     },
		//     error: function (error){
		//       notify("danger", "Something went wrong")
		//     }
		// })
	})
);

//numbering formatter
function numberingFormatter() {
	nos = nos + 1;
	return nos;
}

//detail formatter
function detailFormatter(index, row) {
	return `<div class="mx-auto border border-2 p-2">
           
           <p class="fw-bold fs-5" style=" margin-right: 50px;">Q: ${row.question}</p>
           <p class="ms-5"><span class="me-2 fw-bold">[A]</span> ${row.option_A} </p>
           <p class="ms-5"><span class="me-2 fw-bold">[B]</span> ${row.option_B} </p>
           <p class="ms-5"><span class="me-2 fw-bold">[C]</span> ${row.option_C} </p>
           <p class="ms-5"><span class="me-2 fw-bold">[D]</span> ${row.option_D} </p>

           <p class="ms-5"><span class="me-2 fst-italic text-decoration-underline">Answer</span> <span class="fw-bold">${row.answer} </span> </p>
         </div>`;
}

//alerts *****************************************************************************************************************

function notify(color, msg) {
	$("#alert").html(`
      <div class="auto-close alert alert-${color} alert-dismissible fade show py-1" role="alert" >
          ${msg}
      </div>
  `);
}

function fadeAndSlide(element) {
	const fadeDuration = 500;
	const slideDuration = 100;

	// Step 1: Fade out the element
	let opacity = 1;
	const fadeInterval = setInterval(function () {
		if (opacity > 0) {
			opacity -= 0.1;
			element.style.opacity = opacity;
		} else {
			clearInterval(fadeInterval);
			// Step 2: Slide up the element
			let height = element.offsetHeight;
			const slideInterval = setInterval(function () {
				if (height > 0) {
					height -= 10;
					element.style.height = height + "px";
				} else {
					clearInterval(slideInterval);
					// Step 3: Remove the element from the DOM
					element.parentNode.removeChild(element);
				}
			}, slideDuration / 10);
		}
	}, fadeDuration / 10);
}
// *****************************************************************************************************************

function examCellStyle(value, row, index) {
	return {
		css: {
			"min-width": "150px",
		},
		// classes: "text-center"
	};
}
function questionCellStyle(value, row, index) {
	return {
		css: {
			"min-width": "300px",
		},
	};
}





