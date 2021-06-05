const formulario = document.getElementById('form');
const inputs = document.querySelectorAll('#form input');

const expresiones = {
	usuario: /^[a-zA-Z0-9\_\-]{4,16}$/,
	nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/,
	apellido: /^[a-zA-ZÀ-ÿ\s]{1,40}$/,
	password: /^.{4,12}$/,
	correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
}

const campos = {
    usuario: false,
    correo: false,
    password: false,
    nombre: false,
    apellido: false,
}


const validarForm = (e) =>{
    switch(e.target.name){
        case "username":
            validarCampo(expresiones.usuario, e.target, 'usuario');
        break;
        case "email":
            validarCampo(expresiones.correo, e.target, 'email');
        break;
        case "password":
            validarCampo(expresiones.password, e.target, 'password');
        break;
        case "name":
            validarCampo(expresiones.nombre, e.target, 'nombre');
        break;
        case "lastname":
            validarCampo(expresiones.apellido, e.target, 'apellido');
        break;
    }
};


const validarCampo = (expresion, input, campo) => {
    if(expresion.test(input.value)){
        document.getElementById(`grupo_${campo}`).classList.add('form_grupo_correcto');
        document.getElementById(`grupo_${campo}`).classList.remove('form_grupo_incorrecto');

        document.querySelector(`#grupo_${campo} i`).classList.add('fa-check-circle');
        document.querySelector(`#grupo_${campo} i`).classList.remove('fa-times-circle');

        campos[campo] = true;

    }else{
        document.getElementById(`grupo_${campo}`).classList.add('form_grupo_incorrecto');
        document.getElementById(`grupo_${campo}`).classList.remove('form_grupo_correcto');

        document.querySelector(`#grupo_${campo} i`).classList.add('fa-times-circle');
        document.querySelector(`#grupo_${campo} i`).classList.remove('fa-check-circle');

        document.querySelector(`#grupo_${campo} .form_input_error`).classList.add('form_input_error_activo');

        campos[campo] = false;
    }
};

inputs.forEach((input) => {
    input.addEventListener('keyup', validarForm);
    input.addEventListener('blur', validarForm);
});
