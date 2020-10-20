document.addEventListener("DOMContentLoaded", function(){
    const submit = document.querySelector('#submit');
    const message = document.querySelector("#message");
    submit.disabled = true;
    message.onkeyup = () => {
        if (message.value.length > 0) {
            submit.disabled = false;
        }
        else {
            submit.disabled = true;
        }
    }
    let form = document.querySelector("#formmsg");
    form.onsubmit = function(event){
        event.preventDefault();
        let user = document.querySelector("h1").innerHTML;
        let msg = document.querySelector("#message").value;
        fetch('/message', {
            method: "POST", 
            body: JSON.stringify({
                msg: msg,
                user: user
            })
        })
        .then(response => response.json())
        .then(result => {
            let l = document.createElement("li");
            l.innerHTML = `${result[0].message}
            <a href=""><img id="icon" src="/static/hobbibi/icon-delete-16.png" alt=""></a><br><small>${result[0].timestamp}</small>`;
            let a = l.children[0];
            a.className = `msg${result[0].id} m`;
            a.setAttribute("id", "m");
            a.dataset.msg = `${result[0].id}`;
            document.querySelector("#msg").appendChild(l);
            l.className = "c";
            console.log(l)
            let m = document.querySelector("#message");
            m.value = '';
            submit.disabled = true;
            var messageBody = document.querySelector('#meg');
            meg.scrollTop = meg.scrollHeight - meg.clientHeight;
            a.addEventListener("click", delete_message());
        })
    }

    document.querySelectorAll('a').forEach((a) => {
        a.addEventListener("click", delete_message());
    })
function delete_message(){
    document.querySelectorAll('#m').forEach(function(a){
        let m = a.dataset.msg;
        a.onclick = function(event){
            var sure = confirm("Are you sure you want to delete this message?");
            if(sure){
            event.preventDefault();
            fetch('/delete_msg', {
                method: "PUT", 
                body: JSON.stringify({
                    msg: m,
                })
            })
            .then(response => response.json())
            .then(result => {
                if (result.status == 201){
                    let l = document.querySelector(`.msg${m}`);
                    l.parentElement.innerHTML = "<div style='background-color: white; color: #007bff; font-size: 12px;'><i>This message was deleted</i></div>";
                                       
            }
            })
            return false;
        }
    }
        
})

}
})