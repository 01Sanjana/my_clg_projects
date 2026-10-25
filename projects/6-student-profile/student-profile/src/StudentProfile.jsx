
import React from "react";
import "./StudentProfile.css";

function StudentProfile({ student }) {
  return (
    <div className="student-card">
      <header className="college-header">
        <h2>ST. VINCENT PALLOTTI</h2>
        <h3>COLLEGE OF ENGINEERING AND TECHNOLOGY</h3>
        <p>Nagpur, Maharashtra</p>
      </header>

      <div className="profile-content">
        <img
          src={student.photo}
          alt={student.name}
          className="student-photo"
        />

        <p className="profile-label">STUDENT PROFILE</p>
        <h2 className="student-name">{student.name}</h2>

        <div className="student-details">
          <p><strong>UID:</strong> {student.uid}</p>
          <p><strong>Department:</strong> {student.department}</p>
          <p><strong>Year / Semester:</strong> {student.year}</p>
          <p><strong>Email:</strong> {student.email}</p>
          <p><strong>Contact:</strong> {student.contact}</p>
        </div>

        <div className="bio-section">
          <h3>About Me</h3>
          <p>{student.bio}</p>
        </div>
      </div>

      <footer className="college-footer">
        SVPCET Nagpur | Student Portal
      </footer>
    </div>
  );
}

export default StudentProfile;
