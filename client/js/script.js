//elements
var submitButton = document.getElementById('submitForm');
var modal = document.getElementById('modal');
var close = document.getElementById('close');
var currentPetId = 1;
var currentAnimal = {};
var currentUser = false;
//data
var myPets = []


//inputs
var petName = document.getElementById('name').value;
var petAge = document.getElementById('age').value;
var petType = document.getElementById('petType').value;
var petGender = document.getElementById('petGender').value;
var animalName = document.getElementById('animalName');
var animalAge = document.getElementById('animalAge');
var animalOwner = document.getElementById('animalOwner')
var closeReq = document.getElementById('closeReq');
var reqModal = document.getElementById('reqModal');
var editPet = document.getElementById('editPet');
var deletePet = document.getElementById('deletePet');
var deleteModal = document.getElementById('deleteModal');
var deleteButtonYes = document.getElementById('yesDelete');
var deleteButtonNo = document.getElementById('noDelete');
var animalGender = document.getElementById('animalGender');
var petOwner = document.getElementById('owner');
var petUl = document.getElementById('petUl');
var animalType = document.getElementById('animalType');

var submitEdit = document.getElementById('submitEdit');
var loginButton = document.getElementById('loginButton');
var loginForm = document.getElementById('loginForm');
var closeLog = document.getElementById('closeLog');
var firstNameCreate = document.getElementById('firstNameCreate');
var lastNameCreate = document.getElementById('lastNameCreate');
var emailCreate = document.getElementById('emailCreate');
var passwordCreate = document.getElementById('passwordCreate');

var loginError = document.getElementById('loginError');

var createError = document.getElementById('createError');


var noAuth = document.getElementById('noAuth');


var emailLogin = document.getElementById('emailLogin');
var passwordLogin = document.getElementById('passwordLogin');
var submitUserLogin = document.getElementById('submitUserLogin');


var authModal = document.getElementById('authModal');
var closeAuthModal = document.getElementById('closeAuthModal');
closeAuthModal.onclick = function () {
    authModal.style.display='none';
}

submitUserLogin.onclick = function() {
    userLoginRequest();

}



loginButton.onclick = function() {
    loginForm.style.display = "inline-block";
    registerForm.style.display = "none";
}

closeLog.onclick = function() {
    loginForm.style.display = "none";
}


var closeReg = document.getElementById('closeReg');
var registerForm = document.getElementById('registerForm');
var registerButton = document.getElementById('registerButton');

closeReg.onclick = function() {
    registerForm.style.display = "none";
}

registerButton.onclick = function() {
    registerForm.style.display = "inline-block";
    loginForm.style.display = "none";
}

var submitUserCreate = document.getElementById('submitUserCreate');
submitUserCreate.onclick = function() {

    userCreateRequest();
    // registerForm.style.display = "none";
    // firstNameCreate.value = "";
    // lastNameCreate.value = "";
    // emailCreate.value = "";
    // passwordCreate.value = "";
    
}






//var genderValue = animalGender.options[animalGender.selectedIndex].text;

submitButton.onclick = function() {
    if (currentUser) {
        
        //have modal show and then disappear after 2 seconds.
        modal.style.display = "inline";
        setTimeout( function() { 
            modal.style.display = "none"; }, 2000);
        //append object to list
        var petName = document.getElementById('name').value;
        var petAge = document.getElementById('age').value;
        var petType = document.getElementById('petType').value;
        var petGender = document.getElementById('petGender').value;
        var petOwner = document.getElementById('owner').value;
        
        
        var petObj = {petName:petName, petAge: petAge, petType: petType, petGender: petGender, petOwner: petOwner};
        myPets.push(petObj);
        
        
        animalName.innerHTML = petName;
        animalAge.innerHTML = petAge;
        animalGender.innerHMTL = petGender;
        animalOwner.innerHTML = petOwner;
        animalType.innerHMTL = petType;
        console.log(petType)
        
        animalGender.innerHTML = petGender.toString();
        animalType.innerHTML = petType.toString();


        var li = document.createElement("li");

        
        li.innerHTML = `Name: ${petName} &nbsp; | &nbsp;  Age: ${petAge} &nbsp;  |  &nbsp; Gender: ${petGender}`;
        li.classList.add('petContainer');
        petUl.appendChild(li);
        


        sendPet();
        clear();
        console.log('after clear');
    } else {
        //do something
        noAuth.innerHTML = "Please Log In First";
        
    }
}




close.onclick = function() {
    modal.style.display = "none";
}

let clear = function() {
    var petName = document.getElementById('name').value = "";
    var petAge = document.getElementById('age').value = "";
    var petType = document.getElementById('petType').value = "";
    var petGender = document.getElementById('petGender').value = "";
    var petOwner = document.getElementById('owner').value = "";

}

closeReq.onclick = function() {
    reqModal.style.display = "none";
}

editPet.onclick = function() {
    
    reqModal.style.display = "inline-block";
    var editAge = document.getElementById('editAge');
    var editName = document.getElementById('editName');
    var editOwner = document.getElementById('editOwner');
    var editType = document.getElementById('editType');
    var editGender = document.getElementById('editGender');
    
    editName.value = animalName.innerHTML;
    editAge.value = animalAge.innerHTML;
    editOwner.value = animalOwner.innerHTML;
    editType.value = animalType.innerHTML;
    editGender.value = animalGender.innerHTML;
    //editPetById(currentPetId)
    
    

}


submitEdit.onclick = function() {
    reqModal.style.display = "none";
    updatePet(currentPetId);
}

deletePet.onclick = function(petId) {
   
    deleteModal.style.display = "inline-block";
    deleteButtonYes.onclick = function() {
        deleteModal.style.display = "none";
        deletePetById(currentPetId);
        animalAge.innerHTML = ""
        animalGender.innerHTML = ""
        animalType.innerHTML = ""
        animalOwner.innerHTML = ""
        animalName.innerHTML = ""
    
    }
    
    deleteButtonNo.onclick = function() {
        deleteModal.style.display = "none";
    }

    //authModal.style.display = "inline-block";
    
    
}



var deletePetById = function(petId) {
    dbDeletePet(petId);
}




var displayData = function(data) {
    petUl.innerHTML = "";
    data.forEach( function (pet) {
        var li = document.createElement("li");
        li.innerHTML = `Name: ${pet['name']} &nbsp; | &nbsp;  Age: ${pet['age']} &nbsp;  |  &nbsp; Gender: ${pet['gender']}`;
        li.classList.add('petContainer');
        petUl.appendChild(li);
        li.onclick = function() {
            currentPetId = pet.id;
            console.log("current id: ", currentPetId);
            currentAnimal = pet;
            setAnimal(currentAnimal.id);
        }
    })
}

var setAnimal = function(id) {
    console.log("current animal: ", currentPetId, "id: ", id);
    myPets.forEach( function (pet) {
        if (pet.id == id) {
            animalName.innerHTML = pet.name;
            animalGender.innerHTML = pet.gender;
            animalAge.innerHTML = pet.age;
            animalOwner.innerHTML = pet.owner;
            animalType.innerHTML = pet.type;
        }
    })
}

// var loadData = function() {
//     displayData(myPets);
// }

var notLoggedIn = document.getElementById('notLoggedIn');
var tabsShow = document.getElementById('tabs-style-shape');

var loadData = function() {
    return fetch('http://localhost:8080/pets', {
        credentials: "include"
    }).then(function (response) {
        if (response.status == 401) {
            notLoggedIn.style = "text-align:center;";
            tabsShow.style.display = "none";
            loginForm.style.display = "inline-block"
            // TODO: hide pet stuff, ask user to login first
        } else {
            notLoggedIn.style.display = "none";
            tabsShow.style.display = "inline-block";
            tabsShow.style = "margin:0 auto;"
            // now logged in
            // TODO: show pet stuff
            response.json().then(function (data) {
                myPets = data;
                displayData(data);
                setAnimal(currentAnimal.id);
            });
        }
    });
}


var encode = function() {
    var name = document.getElementById('name').value
    var owner = document.getElementById('owner').value
    var age = document.getElementById('age').value
    var gender = document.getElementById('petGender').value
    var type = document.getElementById('petType').value
    
    var n = encodeURIComponent(name);
    var o = encodeURIComponent(owner);
    var a = encodeURIComponent(age)
    var g = encodeURIComponent(gender)
    var t = encodeURIComponent(type)
    

    var encodedString = `name=${n}&owner=${o}&age=${a}&gender=${g}&type=${t}`;
    console.log(encodedString);
    return encodedString;
}

var editEncode = function() {


    var editAge = document.getElementById('editAge').value;
    var editName = document.getElementById('editName').value;
    var editOwner = document.getElementById('editOwner').value;
    var editType = document.getElementById('editType').value;
    var editGender = document.getElementById('editGender').value;

    
    var n = encodeURIComponent(editName);
    var o = encodeURIComponent(editOwner);
    var a = encodeURIComponent(editAge);
    var g = encodeURIComponent(editGender);
    var t = encodeURIComponent(editType);
    

    var encodedString = `name=${n}&owner=${o}&age=${a}&gender=${g}&type=${t}`;
    console.log(encodedString);
    return encodedString;
}


var encodeUser = function() {

    var firstNameCreate = document.getElementById('firstNameCreate').value;
    var lastNameCreate = document.getElementById('lastNameCreate').value;
    var emailCreate = document.getElementById('emailCreate').value;
    var passwordCreate = document.getElementById('passwordCreate').value;




    var f = encodeURIComponent(firstNameCreate);
    var l = encodeURIComponent(lastNameCreate);
    var e = encodeURIComponent(emailCreate);
    var p = encodeURIComponent(passwordCreate);

    var encodedString = `first_name=${f}&last_name=${l}&email=${e}&password=${p}`
    console.log("encoded user string", encodedString)
    return encodedString;
}

var encodeLogin = function() {
    var emailLogin = document.getElementById('emailLogin').value;
    var passwordLogin = document.getElementById('passwordLogin').value;
    

    var e = encodeURIComponent(emailLogin);
    var p = encodeURIComponent(passwordLogin);
    var encodedString = `email=${e}&password=${p}`
    console.log('user login string ', encodedString);
    return encodedString; 
    
    
}


var sendPet = function() {
    var encodedString = encode()
    fetch('http://localhost:8080/pets', {
        credentials: "include",
        body: encodedString,
        method: "POST",
        headers:{
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then( function () {
        loadData();
    });
}

var userCreateRequest = function() {
    var encodedString = encodeUser()
    fetch('http://localhost:8080/users', {
        credentials: "include",
        body:encodedString,
        method: "POST",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then( function (response) {
        if (response.status == 201) {
            createError.innerHTML = "";
            registerForm.style.display = "none";
            loadData();
        } else if (response.status == 422) {
            createError.innerHTML = "user already exists. log in instead.";
            //registerForm.style.display = "inline-block";
            //createError.innerHTML = "user already exists. log in instead.";
            // alert('the last thing ran');

        }
        
    })
}

var userLoginRequest = function() {

    var encodedString = encodeLogin();
    fetch('http://localhost:8080/sessions', {
        body: encodedString,
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    }).then( function (response) {
        if (response.status == 201) {
            currentUser = true;
            loginError.innerHTML = "";
            loginForm.style.display = "none";
            emailLogin.value = "";
            passwordLogin.value = "";
            noAuth.style.display = "none";
            noAuth.innerHTML = "";
            loadData();

        } else {
            loginError.innerHTML = "wrong username or password";
            loginForm.style.display = "inline-block";
        }
    })
}


var dbDeletePet  = function(petId) {
    fetch(`http://localhost:8080/pets/${petId}`, {
        credentials: "include",
        method: "DELETE"
    }).then( function () {
        loadData();
    })
}


var updatePet = function(petId) {
    var encodedString = editEncode()
    fetch(`http://localhost:8080/pets/${petId}`, {
        credentials: "include",
        body: encodedString,
        method:"PUT",
        headers: {
            'Content-Type':'x-www-form-urlencoded'
        }
    }).then(function () {
        loadData();
        // setAnimal(petId);
    })
}



loadData();
