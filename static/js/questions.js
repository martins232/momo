let $table = $('#table')
let $remove = $('#remove')
let selections 
const formDataObj = {};
let nos 


function ajaxRequest(params) {
  let url = 'question-data'
  $.get(url+ '?' + $.param(params.data)).then(function (res) {
    nos = res.offset
    
    params.success(res)
    selections = []
    $remove.prop("disabled", true)
    
  })
}

//edit formatter
function operateFormatter(value, row, index) {
  return `<button type="button" class="btn btn-light js-edit-question" data-id="${row.id}"><i class="fas fa-pencil"></i></i></button>`
}

//edtiting a question view
window.operateEvents = {
  'click .js-edit-question': function (e, value, row, index) {
    let btn = $(e.currentTarget)
    $("#addQuestion .modal-content").html("");
    $.ajax({
        url: `edit-myquestion/${btn.attr('data-id')}`,
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#addQuestion").modal("show");
        },
        success: function (data) {

            $("#addQuestion .modal-content").html(data.html_form);
        },
        error: function(error){
            
        }
      });
  }}


//create a new question view
$(function () {
  $("#addQuestion .modal-content").html("");
    $(".js-create-question").click(function () {
        $.ajax({
            url: 'create-myquestion',
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
              $("#addQuestion").modal("show");
            },
            success: function (data) {
                $("#addQuestion .modal-content").html(data.html_form);
            },
            error: function(error){
                
            }
          });
    });
  
});


  //submiting a new question
  $("#addQuestion").on("submit", ".js-question-create-form",function  () {
    let form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
            notify("success", "Question created succesfully");  // <-- This is just a placeholder for now for testing
            $("#addQuestion").modal("hide");
            $table.bootstrapTable("refresh")
            const autoCloseElements = [...$(".auto-close")]
            setTimeout(function () {
                autoCloseElements.forEach(el => fadeAndSlide(el));
            }, 5000); 
        }
        else {
          $("#addQuestion .modal-content").html(data.html_form);
          $("#addQuestion").modal("show");

        }
      }
    });
    return false;
  }
  );


//submitting an edited question
$("#addQuestion").on("submit", ".js-question-edit-form", function  () {
  let form = $(this);
  $.ajax({
    url: form.attr("action"),
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        notify("success", "Question saved succesfully");  // <-- This is just a placeholder for now for testing
        $("#addQuestion").modal("hide");
        $table.bootstrapTable("refresh")
        const autoCloseElements = [...$(".auto-close")]
        setTimeout(function () {
            autoCloseElements.forEach(el => fadeAndSlide(el));
        }, 5000);
      }
      else {
        $("#addQuestion .modal-content").html(data.html_form);
        $("#addQuestion").modal("show");

      }
    }
  });
  return false;
}
 
  
);

//control disabled delete button
$table.on('check.bs.table uncheck.bs.table ' + 'check-all.bs.table uncheck-all.bs.table', function () {
  $remove.prop('disabled', !$table.bootstrapTable('getSelections').length)

  // save your data, here just save the current page
  selections = getIdSelections()
  // push or splice the selections if you want to save all data selections
})

function getIdSelections() {
  return $.map($table.bootstrapTable('getSelections'), function (row) {
    return row.id
  })
}


//delete button view  
$($remove.click(function () {
  $("#addQuestion .modal-content").html("");
  $.ajax({
    url: `delete-myquestion?id=${selections}`,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
      $("#addQuestion").modal("show");
    },
    success: function (data) {
        $("#addQuestion .modal-content").html(data.html_form);
    },
    error: function(error){
        
    }
  });


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
  const csrftoken = getCookie('csrftoken');

  //delete question
  $("#addQuestion").on("submit" , ".js-question-delete-form", function(event){
      event.preventDefault()
      $.ajax({
        type: "POST",
        url: "delete-myquestion/",
        data:{"csrfmiddlewaretoken": csrftoken , id:JSON.stringify(selections)},
        success: function(data){
            if (data.deleted){
              notify("success", "Question(s) deleted")
              const autoCloseElements = [...$(".auto-close")]
              setTimeout(function () {
                  autoCloseElements.forEach(el => fadeAndSlide(el));
              }, 5000);
              $table.bootstrapTable("refresh")
            }
            $("#addQuestion").modal("hide");
        },
        error: function(error){
          console.log(error)
        }
      })
      


  })
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
)

//numbering formatter
function numberingFormatter(){
  nos = nos + 1
  return nos
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
         </div>`
 }

 //alerts *****************************************************************************************************************

function notify(color, msg){
  $("#alert").html(`
      <div class="auto-close alert alert-${color} alert-dismissible fade show py-1" role="alert" >
          ${msg}
      </div>
  `)
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
