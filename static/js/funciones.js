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

function listarLote(){
    document.getElementById("formulario").action="/gestion_lote/consulta";
}
function eliminarLote(){
    document.getElementById("formulario").action="/gestion_lote/eliminar";
}
function actualizarLote(){
    document.getElementById("formulario").action="/gestion_lote/actualizar";
}
function crearLote(){
    document.getElementById("formulario").action="/gestion_lote/crear";
}