const mysql = require("mysql2");
const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "Sajib+230122",
  database: "student_management",
});
db.connect((err) => {
  if (err) {
    console.error("Database Connection Failed:", err);
  } else {
    console.log("MySQL Connected Successfully");
  }
});
module.exports = db;