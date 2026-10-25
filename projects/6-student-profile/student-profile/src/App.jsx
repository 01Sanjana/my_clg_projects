
import React from "react";
import StudentProfile from "./StudentProfile";
import "./App.css";

const student = {
  name: "SANJANA ADMANE",
  uid: "24010030",
  department: "Information Technology",
  year: "3rd Year - Vth Semester",
  email: "sanjanaadmane.24@stvincentngp.edu.in",
  contact: "8459751018",
  photo: "/sanjana.jpg",
  bio: "Creative and curious IT student interested in software development, data analytics, artificial intelligence, and learning new technologies."
};

function App() {
  return (
    <div className="app">
      <h1 className="page-title">Student Portal</h1>

      <div className="profile-container">
        <StudentProfile student={student} />
      </div>
    </div>
  );
}

export default App;
