import {Router} from "express"

const router = new Router()

router.get("/hola", (req, res) =>{
    res.send("Hola")
})

export default router

