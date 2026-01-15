import {createClient} from "redis"

const client = await createClient({
    url:"redis://localhost:6379"
}).on("error", (err) => {
    console.error(err)
}).connect()

await client.set("dato2", "valor")
const valor = await client.get("dato2")
if(valor){
    console.log(valor)
}else{
    console.log("Valor no encontrado")
}
// uso para JSON
const objeto = {
    nombre: "Francisco",
    email: "ff@gmail.com",
    edad: 100
}
await client.set("objeto", JSON.stringify(objeto))

const objetoLeido = await client.get("objeto")
const jsonObjeto = JSON.parse(objetoLeido)
jsonObjeto.edad = 56
console.log(jsonObjeto)

// cada segundo, imprime el tiempo de vida restante de la clave
setInterval(async () => {
    const ttl = await client.ttl("objeto")
    console.log(`A la clave "objeto" le quedan [${ttl}] segundos de vida`)
}, 1000)

// establece la caducidad de la clave después de 1050ms, por lo que inicia siendo indefinida
setTimeout(async () => {
    await client.expire("objeto", 10)
}, 1050)

// intenta encontrar la clave después de su caducidad
setTimeout(async () => {
    const valor = await client.get("objeto")
    console.log(valor)
}, 11000)