const contenedor = document.querySelector(".container-product");
const productList = [["Arroz-5000g.jpg", "A001", "Arroz 1lb", "2500"],
                    ["Leche-1lt.jpg", "A002", "Leche 1lt", "2800"],
                    ["Huevo-Docena.jpg", "A003", "Docena de Huevos", "12000"],
                    ["Colcafe.jpg", "A004", "Cafe Colcafe", "12000"],
                    ["papelDeCocina.jpg", "A005", "Papel de Cocina", "12000"],
                    ["Azucar.jpg", "A006", "Azucar", "12000"],
                    ["Azucar.jpg", "A006", "Azucar", "12000"],
                    ["Azucar.jpg", "A006", "Azucar", "12000"],
                    ["Azucar.jpg", "A006", "Azucar", "12000"]];

function crearProducto(img, codigo,nombre,precio){    
    img = `<img class= "productoimg" src="static/img/Producto/${img}">`;
    nombre = `<h2>${nombre}</h2>`;
    precio = `<h3>Precio: $${precio}</h3>`;
    codigo = `<p>Codigo: ${codigo}</p>`; 
    return [img, codigo, nombre, precio] 
}

let documentFragment = document.createDocumentFragment();

for(var i=0; i<productList.length; i++){
    const Producto = crearProducto(productList[i][0], productList[i][1], productList[i][2], productList[i][3]);    
    let div = document.createElement("DIV");
    div.classList.add(`item${i}`, 'flex-item');
    div.innerHTML += Producto[0] + Producto[2] + Producto[3] + Producto[1];
    documentFragment.appendChild(div);
}

contenedor.appendChild(documentFragment);





