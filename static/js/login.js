const inputs = document.querySelectorAll(".input");
const login_btn = document.getElementById("Login");
const LOCAL_HOST = "http://127.0.0.1:5000";
const headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json'
};

function addcl(){
	let parent = this.parentNode.parentNode;
	parent.classList.add("focus");
}

function remcl(){
	let parent = this.parentNode.parentNode;
	if(this.value == ""){
		parent.classList.remove("focus");
	}
}


inputs.forEach(input => {
	input.addEventListener("focus", addcl);
	input.addEventListener("blur", remcl);
});

// async function login() {
// 	const mongo_cb = document.getElementById("flexSwitchCheckChecked");
// 	const data = {
// 		"user":inputs[0].value,
// 		"pass":inputs[1].value,
// 		"db":inputs[2].value,
// 		"use_mongo":mongo_cb.checked
// 	}

// 	console.log(data)
// 	const res = await fetch(`${LOCAL_HOST}/login`, {
//         method: "POST",
//         body: JSON.stringify(data),  // Send the use_mongo flag to the backend
// 		headers: headers
//     });

// 	const results = await res.json();
// 	console.log(results)


// }
// const login = (e) = >
// {
// 	const mongo_cb = document.getElementById("flexSwitchCheckChecked");
// 	e.preventDefault();
// 	localStorage.setItem("use_mongo", mongo_cb.checked);
// 	document.getElementById("login_form").submit();
// }
// login_btn.addEventListener("click",login)