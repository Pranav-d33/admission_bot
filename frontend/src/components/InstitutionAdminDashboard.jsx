import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const InstitutionAdminDashboard = () => {
    const navigate = useNavigate();

    const [submissions, setSubmissions] = useState([]);
    const [comment, setComment] = useState("");

    useEffect(() => {
        // Fetch data from localStorage
        const storedData = JSON.parse(localStorage.getItem("institutionData")) || [];
        setSubmissions(storedData);
    }, []);

    const handleApprove = (submission) => {
        // Handle approval logic
        const updatedSubmission = { ...submission, status: "approved" };

        // Retrieve current institution data from localStorage
        const institutionData = JSON.parse(localStorage.getItem("institutionData")) || [];

        // Remove the approved submission from institutionData
        const updatedInstitutionData = institutionData.filter(item => item.keyId !== submission.keyId);

        // Update localStorage with the modified institutionData
        localStorage.setItem("institutionData", JSON.stringify(updatedInstitutionData));

        // Retrieve current approved data from localStorage
        const storedData = JSON.parse(localStorage.getItem("approvedData")) || [];

        // Check if the submission is already in the approved data
        const isAlreadyApproved = storedData.some(item => item.keyId === updatedSubmission.keyId);

        if (!isAlreadyApproved) {
            // Add the new approved submission to the approved data if it's not already present
            const updatedSubmissions = [...storedData, updatedSubmission];

            // Update localStorage with the new approved list
            localStorage.setItem("approvedData", JSON.stringify(updatedSubmissions));
        } else {
            alert("This submission has already been approved!");
        }

        // Optionally update the state with the new data
        setSubmissions(updatedInstitutionData);  // Updating the UI with the new data

        alert("Submission Approved!");
    };



    const handleReject = (submission) => {
        if (!comment.trim()) {
            alert("Please provide a comment for rejection.");
            return;
        }
        console.log("Rejected Submission:", submission, "Comment:", comment);
        alert("Submission Rejected!");

        // Store rejected data in localStorage
        const rejectedList = JSON.parse(localStorage.getItem("rejectedData")) || [];
        rejectedList.push({ ...submission, rejectionComment: comment });
        localStorage.setItem("rejectedData", JSON.stringify(rejectedList));

        // Remove submission from the current submissions list
        const updatedSubmissions = submissions.filter((sub) => sub.keyId !== submission.keyId);

        // Update localStorage with the new submissions list
        // localStorage.setItem("institutionData", JSON.stringify(updatedSubmissions));

        setSubmissions(updatedSubmissions);
    };

    const logout = () => {
        navigate('/'); // Redirect to the login page
    };

    return (
        <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">Institution Admin Dashboard</h2>
            {submissions.length === 0 ? (
                <p>No submissions to review.</p>
            ) : (
                submissions.map((submission, index) => (
                    <div key={index} className="mb-6 border rounded p-4">
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
                    
                        <div className="mt-4">
                            <textarea
                                className="w-full p-2 border rounded mb-2"
                                placeholder="Add a comment (required for rejection)"
                                value={comment}
                                onChange={(e) => setComment(e.target.value)}
                            ></textarea>
                            <button
                                onClick={() => handleApprove(submission)}
                                className="bg-green-500 text-white py-1 px-3 rounded mr-2"
                            >
                                Approve
                            </button>
                            <button
                                onClick={() => handleReject(submission)}
                                className="bg-red-500 text-white py-1 px-3 rounded"
                            >
                                Reject
                            </button>
                        </div>
                    </div>
                ))
            )}

            <button
                onClick={logout}
                className="bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-800 m-2"
            >
                Logout
            </button>
        </div>
    );
};

export default InstitutionAdminDashboard;
