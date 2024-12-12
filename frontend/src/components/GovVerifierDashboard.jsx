import React, { useState, useEffect } from 'react';

const GovVerifierDashboard = () => {
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
      <h1 className="text-2xl font-bold mb-4">Government Verifier Dashboard</h1>

      {submissions.length === 0 ? (
        <p>No submissions available for verification.</p>
      ) : (
        submissions.map((submission) => (
          <div key={submission.keyId} className="p-4 mb-4 border rounded-md shadow-sm bg-white">
            <h2 className="text-xl font-semibold">{submission.institutionName}</h2>
            <p><strong>Location:</strong> {submission.location}</p>
            <p><strong>Facilities:</strong> {submission.facilities}</p>
            <p><strong>Admission Fees:</strong> {submission.admissionFees}</p>

            <h3 className="mt-4 font-semibold">Courses:</h3>
            <ul>
              {submission.courses.map((course, index) => (
                <li key={index}>{course.name} - Cutoff: {course.cutoff}, Placement: {course.placementStats}</li>
              ))}
            </ul>

            <div className="mt-4">
              <textarea
                className="w-full p-2 border rounded mb-4"
                placeholder="Provide rejection comment"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
              ></textarea>
              <button
                className="px-4 py-2 bg-green-500 text-white rounded mr-2"
                onClick={() => handleApprove(submission)}
              >
                Approve
              </button>
              <button
                className="px-4 py-2 bg-blue-500 text-white rounded"
                onClick={() => handleReject(submission)}
              >
                Reject
              </button>
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default GovVerifierDashboard;
