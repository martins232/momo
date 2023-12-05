let modalBtns = [...document.getElementsByClassName("delete")]
const modalBody = document.getElementById("modal-body-confirm")
const modalDelete = document.getElementById("confirmDelete")

modalBtns.forEach(modalBtn => modalBtn.addEventListener("click", ()=>{
    const pk  = modalBtn.getAttribute("data-id")
    const obj = modalBtn.getAttribute("data-name")
    const url = modalBtn.getAttribute("data-url")
     
    modalBody.innerHTML = `<h5">You want to delete the following <ul><li><span class="text-danger">'${obj}'</span></li></ul> </h5>`
    
    modalDelete.addEventListener("click", ()=>{
        window.location.href = "http://" + window.location.host + url
        console.log(url)
    })

})
)