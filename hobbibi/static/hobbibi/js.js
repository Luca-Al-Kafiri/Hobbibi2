document.addEventListener("DOMContentLoaded", function(){
    document.querySelector('#search').style.display='none';
    document.querySelector('#main').style.display = "block";
    let form = document.querySelector("#form")
    form.onsubmit = function(event){
        event.preventDefault();
        let hobbi = document.querySelector("#hobbi").value;
        fetch('/search', {
            method: "POST",
            body: JSON.stringify({
                hobbi: hobbi,
            })
        })
        .then(response => response.json())
        .then(results => {
            document.querySelector('#main').style.display = "none";
            document.querySelector('#search').style.display = "block";
            document.querySelector('#mytable').innerHTML= '';
            results.forEach((element) => {
                let a = document.createElement('tr');
                a.className = `${element.user}`;
                a.innerHTML = `<td><a href="profile/${element.user}">${element.user}</a></td>
                <td>${element.age}</td>
                <td>${element.hobbi}</td>`;
                document.querySelector('#mytable').append(a);
            })
        })
    }
})