const express = require("express");
const router = express.Router();
const db = require("../models/db");

// ================= GET ALL STUDENTS =================
router.get("/", (req, res) => {
  db.query("SELECT * FROM students", (err, result) => {
    if (err) {
      return res.status(500).json({
        success: false,
        message: "Database Error",
        error: err.message,
      });
    }

    res.json({
      success: true,
      data: result,
    });
  });
});

// ================= ADD STUDENT =================
router.post("/", (req, res) => {
  const { name, department, phone } = req.body;

  if (!name || !department || !phone) {
    return res.status(400).json({
      success: false,
      message: "All fields are required.",
    });
  }

  db.query(
    "INSERT INTO students (name, department, phone) VALUES (?, ?, ?)",
    [name, department, phone],
    (err, result) => {
      if (err) {
        return res.status(500).json({
          success: false,
          message: "Database Error",
          error: err.message,
        });
      }

      res.status(201).json({
        success: true,
        message: "Student Added Successfully",
        studentId: result.insertId,
      });
    }
  );
});

// ================= UPDATE STUDENT =================
router.put("/:id", (req, res) => {
  const { id } = req.params;
  const { name, department, phone } = req.body;

  if (!name || !department || !phone) {
    return res.status(400).json({
      success: false,
      message: "All fields are required.",
    });
  }

  db.query(
    "UPDATE students SET name = ?, department = ?, phone = ? WHERE id = ?",
    [name, department, phone, id],
    (err, result) => {
      if (err) {
        return res.status(500).json({
          success: false,
          message: "Database Error",
          error: err.message,
        });
      }

      if (result.affectedRows === 0) {
        return res.status(404).json({
          success: false,
          message: "Student Not Found",
        });
      }

      res.json({
        success: true,
        message: "Student Updated Successfully",
      });
    }
  );
});

// ================= DELETE STUDENT =================
router.delete("/:id", (req, res) => {
  const { id } = req.params;

  db.query("DELETE FROM students WHERE id = ?", [id], (err, result) => {
    if (err) {
      return res.status(500).json({
        success: false,
        message: "Database Error",
        error: err.message,
      });
    }

    if (result.affectedRows === 0) {
      return res.status(404).json({
        success: false,
        message: "Student Not Found",
      });
    }

    res.json({
      success: true,
      message: "Student Deleted Successfully",
    });
  });
});

module.exports = router;