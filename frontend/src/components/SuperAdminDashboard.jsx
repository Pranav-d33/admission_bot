import React, { useState, useEffect } from 'react';

const SuperAdminDashboard = () => {
  const [submissions, setSubmissions] = useState([]);
  const [comment, setComment] = useState("");


  useEffect(() => {
    // Fetch the approved submissions from localStorage
    const storedData = JSON.parse(localStorage.getItem("approvedData")) || [];
    setSubmissions(storedData);
  }, []);

  const handleApprove = async (submission) => {
    alert(`Approved Submission: ${submission.institutionName}`);
    /*
    
    try {
      // Send the approved data to the backend
      const response = await fetch('https://your-backend-url.com/api/approvals', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(submission),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await response.json();
      console.log('Success:', result);

      // Optionally handle the response from the server
    } catch (error) {
      console.error('Error sending approval:', error);
    }
       */

    // Retrieve existing data from localStorage (institution data)
    let storedData = await JSON.parse(localStorage.getItem("approvedData")) || [];
    const updatedSubmissions = storedData.filter((sub) => sub.keyId !== submission.keyId);
    // Save the updated list back to localStorage
    localStorage.setItem("approvedData", JSON.stringify(updatedSubmissions));

    // Optionally update the state with the new data
    setSubmissions(updatedSubmissions);
  };

  const handleReject = (submission) => {
    if (!comment.trim()) {
      alert("Please provide a comment for rejection.");
      return;
    }

    const updatedSubmission = {
      ...submission,
      rejectionComment: comment,
    };

    alert(`Rejected Submission: ${submission.institutionName}, Comment: ${comment}`);

    // Store rejected data back to localStorage or backend
    const rejectedList = JSON.parse(localStorage.getItem("rejectedData")) || [];
    rejectedList.push(updatedSubmission);
    localStorage.setItem("rejectedData", JSON.stringify(rejectedList));

    // Optionally, remove from approved list
    const updatedSubmissions = submissions.filter((sub) => sub.keyId !== submission.keyId);
    setSubmissions(updatedSubmissions);

    // Clear the comment input after rejection
    setComment("");
  };

  return (
    <div className="p-6 bg-gray-100">
      <h1 className="text-2xl font-bold mb-4">Super Admin Dashboard</h1>

      {submissions.length === 0 ? (
        <p>No Approved Data Available.</p>
      ) : (
        submissions.map((submission) => (
          <div key={submission.keyId} className="p-4 mb-4 border rounded-md shadow-sm bg-white">
            <h3 className="font-semibold text-lg mb-2">
              Institution: {submission.institutionName || "N/A"}
            </h3>
            <p>Key: {submission.keyId || "N/A"}</p>
            <p>Location: {submission.location || "N/A"}</p>
            <p>Facilities: {submission.type || "N/A"}</p>
            <p>Admission Fees: {submission.websiteLink || "N/A"}</p>
            <p>Admission Fees: {submission.Established || "N/A"}</p>

            <h4 className="mt-4 font-semibold">Courses:</h4>
            <ul>
              {submission.courses && submission.courses.length > 0 ? (
                submission.courses.map((course, i) => (
                  <li key={i}>
                    {course.name || "Unnamed Course"} - Placement: {course.placementStats || "N/A"}, Cutoff: {course.cutoff || "N/A"}
                  </li>
                ))
              ) : (
                <p>No courses available.</p>
              )}
            </ul>
            <p>Affiliation: {submission.Affiliation || "N/A"}</p>
            <p>hostel_facilities: {submission.hostel_facilities || "N/A"}</p>
            <p>admissionFees: {submission.admissionFees || "N/A"}</p>
            <p>mess_facilities: {submission.mess_facilities || "N/A"}</p>
            <p>reap_percentile_required: {submission.reap_percentile_required || "N/A"}</p>
            <p>placement_records: {submission.placement_records || "N/A"}</p>
            <p>average_package: {submission.average_package || "N/A"}</p>
            <p>highest_package: {submission.highest_package || "N/A"}</p>
          </div>
        ))
      )}
    </div>
  );

};

export default SuperAdminDashboard;
