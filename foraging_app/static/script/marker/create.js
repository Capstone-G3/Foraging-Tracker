const selectContainer = document.getElementById('id_marker-species');

const formContainer = document.getElementById('species_form');
const formState = {
    'active' : formContainer.innerHTML,
    'inactive' : '' 
} 
selectContainer.addEventListener('change', hideshow)

function hideshow(){
    if(selectContainer.selectedIndex == 0){
        formContainer.innerHTML = formState['active'];
    }else{
        formContainer.innerHTML= formState['inactive'];
    }
}