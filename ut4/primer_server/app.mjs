import express from "express"
import path from "path"

const port = 5000
const app = express()
const rutaActual = path.resolve(".")

//decodificado de json en body
app.use(express.json())
app.use(express.urlencoded({extended:true}))


//envio de json
app.get("/coches/:id", (req, res) => {
    const coche = {
        marca: "Audi",
        modelo: "Q6",
        año_fab: 2024,
        kms: 35000,
        precio: 36000
    }
    res.json(coche)
})

// variables de query
app.get("/nuevo-usuario", (req, res) => {
    const {email, password} = req.query
    console.log(email, password)
    if(!email || !password || email.trim() == "" || password.trim() == ""){ // no existe alguna de las variables
        res.status = 400
        res.send("ERROR: La petición necesita el email y la contraseña")
    }else{
        res.send(`<h1>Usuario creado</h1>
                <h2>Email: ${email}</h2>
                <h2>Contraseña: ${password}</h2>
            `)
    }
})

app.get("/archivo", (req, res) => {
    const rutaCompleta = path.join(rutaActual, "primer_server/form_fichero.html")
    res.sendFile(rutaCompleta)
})
// enviar archivo
app.post("/archivo", (req, res) => {
    console.table(req.body)
    const fichero = req.body.fichero
    if(!fichero || fichero.trim() == ""){
        res.sendStatus(400)
    }
    const rutaCompleta = path.join(rutaActual, fichero)
    res.sendFile(rutaCompleta)
})


app.post("/usuarios/ingreso", (req, res) => {
    //simulamos el ingreso en una base de datos de un usuario
    setTimeout(() => res.sendStatus(200), 2000)
})

//parámetros de ruta
app.get("/usuarios/:id", (req, res) => {
    const paramId = req.params.id
    const number = parseInt(paramId)
    if(number > 15){
        res.send("Eres admin")
    }
    res.send("Eres un visitante")
})

// ruta con comodín
app.get("/usuarios{*splat}", (req, res) =>{
    res.send("Usuarios")
})

app.get("/", (req, res) => {
    console.log("adios mundo")
    res.send("<h1>adios mundo</h1>")
})
//ruta no válida
app.get("/{*splat}", (req, res) => {
    res.status = 404
    res.send("ERROR 404: RECURSO NO ENCONTRADO")
}) // 404

app.listen(port, () => {
    console.log(`Servidor iniciado en ${port}`)
})