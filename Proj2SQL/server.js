const express=require("express");
const cors=require("cors");
require("./models/db");
const studentRoutes=require("./routes/studentRoutes");
const app=express();
app.use(cors());
app.use(express.json());
app.use("/students",studentRoutes);
app.get("/",(req,res)=>{
  res.send("Student Management SQL API Running...");
});
const PORT=5000;
app.listen(PORT,()=>{
  console.log(`Server running on http://localhost:${PORT}`);
});