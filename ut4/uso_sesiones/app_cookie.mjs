import express from "express"
import cookieParser from "cookie-parser"

const app = express()

app.get("/set-cookie", (req, res)=> {
    res.cookie("tarjeta", {num: "2374852793649", CVV: 564}, {maxAge: 1000 * 60 * 60 * 24})
    .send("Cookie establecida")
})


app.listen(5000)