import express from "express"

import rutas from "./routes.mjs"

const PORT = 5000
const app = express()

app.use("/api",rutas)

app.listen(PORT, ()=> {
    console.log("SERVIDOR INICIADO")
})