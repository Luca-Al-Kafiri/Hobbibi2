document.addEventListener("DOMContentLoaded", function(){
    let form = document.querySelector("#form");
    form.onsubmit = function(event){
        event.preventDefault();
        let hobbi = document.querySelector("#hobby").value;
        fetch('/add', {
            method: "POST", 
            body: JSON.stringify({
                hobbi: hobbi,
            })
        })
        .then(response => response.json())
        .then(result => {
            if (result.status == 201){

        let l = document.createElement('li');
        l.innerHTML = `${result.hobbi} <a href=""><img id="icon" src="/static/hobbibi/icon-delete-16.png" alt=""></a>`;
        let a = l.children[0];
        a.className = `hobbi${result.id}`;
        a.setAttribute("id", "h")
        a.dataset.hobbi = `${result.id}`;
        document.querySelector('#hobbies').appendChild(l);
        a.addEventListener("click", delete_hobbi());
        }
        })
    }

    document.querySelectorAll('a').forEach((a) => {
    a.addEventListener("click", delete_hobbi());
})

function delete_hobbi(){
    document.querySelectorAll('#h').forEach(function(a){
        let h = a.dataset.hobbi;
        a.onclick = function(event){
            event.preventDefault();
            fetch('/delete', {
                method: "PUT", 
                body: JSON.stringify({
                    hobbi: h,
                })
            })
            .then(response => response.json())
            .then(result => {
                if (result.status == 201){
                    let l = document.querySelector(`.hobbi${h}`);
                    l.parentElement.remove();
                    
            }
            
            })
            return false;
        }
         
})

}
})
