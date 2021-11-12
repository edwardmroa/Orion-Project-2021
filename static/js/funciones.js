function listarProd(){
    document.getElementById("formulario").action="/gestion_productos/consulta";
}
function eliminarProd(){
    document.getElementById("formulario").action="/gestion_productos/eliminar";
}
function actualizarProd(){
    document.getElementById("formulario").action="/gestion_productos/actualizar";
}
function crearProd(){
    document.getElementById("formulario").action="/gestion_productos/crear";
}